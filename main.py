import connexion
from flask import Response, request, jsonify
from Src.DTO.filter import filter
from Src.DTO.domain_prototype import domain_prototype
from Src.Core.format_reporting import format_reporting
from Src.Reports.report_factory import report_factory
from Src.data_reposity import data_reposity
from Src.Managers.settings_manager import settings_manager
from Src.Services.start_service import start_service
from Src.Models.warehouse import warehouse_model
from Src.Models.warehouse_transaction import warehouse_transaction
from Src.Core.format_transaction import format_transaction
from Src.Processors.turnover_process import turnover_process
from Src.Core.validator import validator
from datetime import datetime
from Src.Processors.blocking_process import blocking_process

from Src.Services.observe_service import observe_service
from Src.Services.nomenclature_service import nomenclature_service
from Src.Core.event_type import event_type
from Src.Processors.turnover_balanse_sheet import turnover_balanse_sheet
from Src.Managers.reposity_manager import reposity_manager
import json


app = connexion.FlaskApp(__name__)
manager = settings_manager()
manager.open("settings.json")
reposity = data_reposity()
_nomenclature_service = nomenclature_service(reposity)
_reposity_manager = reposity_manager(reposity, manager)
_balanse_sheet = turnover_balanse_sheet(manager)
start = start_service(reposity, manager)
start.create()



@app.route("/api/nomenclature", methods=["GET"])
def get_nomenclature(unique_code: str):
    try:
        data = reposity.data[data_reposity.nomenclature_key()]
    except:
        return Response("Нет данных!", 400)
        
    nomenclature = _nomenclature_service.get_nomenclature(data, unique_code)
    if len(nomenclature) == 0:
        return Response("Номенклатура с таким кодом не найдена!", 400)
        
    
    report = report_factory(manager).create_default()
    report.create(nomenclature)
    return report.result
    
    
@app.route("/api/nomenclature", methods=["PUT"])
def put_nomenclature():
    
    request_data = request.get_json()
    name = request_data.get("name") 
    group_id = request_data.get("group_id")
    range_id = request_data.get("range_id")
    
    result = _nomenclature_service.put_nomenclature(name, group_id, range_id)
    
    return Response(result)


@app.route("/api/nomenclature", methods=["PATCH"])
def patch_nomenclature():
    request_data = request.get_json()
    result = observe_service.raise_event(event_type.CHANGE_NOMENCLATURE, request_data)
    result = result[type(_nomenclature_service).__name__]
    
    return Response(result)


@app.route("/api/nomenclature", methods=["DELETE"])
def delete_nomenclature(unique_code: str):
    
    result = observe_service.raise_event(event_type.DELETE_NOMENCLATURE, unique_code)
    result = result[type(_nomenclature_service).__name__]
    return Response(result)


@app.route("/reports/balanse_sheet/<date_start>/<date_end>/<warehouse_name>", methods=["GET"])
def reports_balanse_sheet(date_start:str, date_end:str, warehouse_name:str ):
    
    try:
        date_start = datetime.strptime(date_start, "%Y-%m-%d")
        date_end = datetime.strptime(date_end, "%Y-%m-%d")
    except:
        return Response(f"Неверно введены даты!", 400)
    
    transactions = reposity.data[reposity.transaction_key()]
    if not transactions:
        return Response("Нет транзакций для расчета.", 400)
    
    balanse_sheet = _balanse_sheet.processing(transactions, date_start, date_end, warehouse_name)
    report = report_factory(manager).create_default()
    report.create([balanse_sheet])
    data = report.result
    with open("tbs_report.json", 'w', encoding='utf-8') as f:
            f.write(data)
    return data
    


@app.route("/api/reposity/save", methods=["POST"])
def save_reposity():
    result = observe_service.raise_event(event_type.SAVE_DATA_REPOSITY, {})
    
    result = result[type(_reposity_manager).__name__]
    if manager.settings.first_start:
        manager.settings.first_start = False
        manager.save()
    return Response(result)
        

@app.route("/api/reposity/restore", methods=["POST"])
def restore_reposity():
    result = observe_service.raise_event(event_type.RESTORE_DATA_REPOSITY, {})
    result = result[type(_reposity_manager).__name__]
    return Response(result)


@app.route("/api/filter/<domain>", methods=["POST"])
def filter_data(domain: str):
    if domain not in reposity.keys():
        return Response(f"Домен '{domain}'не найден!", 400)
    
    request_data = request.get_json()
    item_filter = filter.create(request_data)
    
    try:
        data = reposity.data[domain]
    except Exception as e:
        return Response(f"Нет данных!", 400)
    
    prototype = domain_prototype(data)
    prototype.create(item_filter)
    if not prototype.data:
        return {}
    
    report = report_factory(manager).create_default()
    report.create(prototype.data)
    return report.result


@app.route("/api/filter/transactions", methods=["POST"])
def filter_transactions():
    try:
        # получение списка транзакций
        transactions = reposity.data[reposity.transaction_key()]
    except Exception as e:
        return Response(f"Нет данных!", 400)
    
    request_data = request.get_json()
    
    try:
        warehouse = request_data.get("warehouse")
        nomenclature = request_data.get("nomenclature")
    except Exception as e:
        return Response(f"Ключи warehouse или nomenclature не найдены!", 400)
    print(warehouse)
    
    warehouse_filter = filter.create(warehouse)
    nomenclature_filter = filter.create(nomenclature)
    
    # prototype = domain_prototype(transactions)
    # prototype.create(warehouse_filter)
    # prototype.create(nomenclature_filter)
    
    # if not prototype.data:
    #     return {}
    
    # report = report_factory(manager).create_default()
    # report.create(prototype.data)
    # return report.result


@app.route("/api/block_period/set", methods=["POST"])
def set_block_period():
    request_data = request.get_json()
    new_block_period = request_data.get("block_period")
    if new_block_period is None:
        return Response("Дата блокировки не указана!", 400)
        
    manager.settings.block_period = new_block_period
    manager.save()
    
    blocked_turnover_process = blocking_process(manager)
    
    transactions = reposity.data[reposity.transaction_key()]
    if not transactions:
        return Response("Нет транзакций для пересчета.", 400)
    blocked_turnovers = blocked_turnover_process.processing(transactions)

    reposity.data[data_reposity.blocked_turnover_key()] = blocked_turnovers

    return Response(f"new_block_period: {new_block_period}."
                    f"count_of_blocked_turnovers: {len(blocked_turnovers)}",
                    200)


@app.route("/api/block_period/get", methods=["GET"])
def get_block_period():
    return str(manager.settings.block_period)


@app.route("/api/reports/transactions", methods=["GET"])
def reports_transaction(format: str):
    inner_format = format_reporting(format)
    report = report_factory(manager).create(inner_format)
    report.create( reposity.data[ data_reposity.transaction_key()] )
    return report.result


@app.route("/api/reports/turnovers", methods=["GET"])
def reports_turnover(format: str):
    process_turnover = turnover_process.create()
    turnovers = process_turnover.processing(reposity.data[data_reposity.transaction_key()])
    
    format = format.upper()
    inner_format = format_reporting(format)
    report = report_factory(manager).create(inner_format)
    report.create(turnovers)

    return report.result


@app.route("/api/reports/formats", methods=["GET"])
def formats():
    return [{"name":item.name, "value":item.value} for item in format_reporting]


@app.route("/api/reports/range/<format>", methods=["GET"])
def reports_range(format: str):
    inner_format = format_reporting(format)
    report = report_factory(manager).create(inner_format)
    report.create( reposity.data[ data_reposity.range_key()  ] )
    return report.result


@app.route("/api/reports/group/<format>", methods=["GET"])
def reports_group(format: str):
    inner_format = format_reporting(format)
    report = report_factory(manager).create(inner_format)
    report.create( reposity.data[ data_reposity.group_key()  ] )
    return report.result


@app.route("/api/reports/nomenclature/<format>", methods=["GET"])
def reports_nomenclature(format: str):
    inner_format = format_reporting(format)
    report = report_factory(manager).create(inner_format)
    report.create( reposity.data[ data_reposity.nomenclature_key()  ] )
    return report.result


@app.route("/api/reports/recipe/<format>", methods=["GET"])
def reports_recipe(format: str):
    inner_format = format_reporting(format)
    report = report_factory(manager).create(inner_format)
    report.create( reposity.data[ data_reposity.receipt_key()  ] )
    return report.result


if __name__ == "__main__":
    app.add_api("swagger.yaml")
    app.run(port = 8080)