import connexion
from flask import Response, request
from Src.DTO.filter import filter
from Src.DTO.domain_prototype import domain_prototype
from Src.Core.format_reporting import format_reporting
from Src.Reports.report_factory import report_factory
from Src.data_reposity import data_reposity
from Src.settings_manager import settings_manager
from Src.start_service import start_service
from Src.Models.warehouse import warehouse_model
from Src.Models.warehouse_transaction import warehouse_transaction
from Src.Core.format_transaction import format_transaction
from Src.Core.validator import validator

app = connexion.FlaskApp(__name__)
manager = settings_manager()
manager.open("settings.json")
reposity = data_reposity()
start = start_service(reposity)
start.create()




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
    prototype.create(data, item_filter)
    if not prototype.data:
        return {}
    
    report = report_factory(manager).create_default()
    report.create(prototype.data)
    return report.result

# пока не работает
# @app.route("/api/transaction/filter/<domain>", methods=["POST"])
# def filter_transaction(domain: str):
    
#     if domain not in [reposity.warehouse_key(), reposity.nomenclature_key()]:
#         return Response(f"Домен '{domain}'не найден!", 400)
    
#     request_data = request.get_json()
#     item_filter = filter.create(request_data)
    
#     try:
#         # получение списка транзакций
#         transactions = reposity.data[reposity.transaction_key()]
#     except Exception as e:
#         return Response(f"Нет данных!", 400)
    
    
#     prototype = domain_prototype(data)
#     prototype.create(data, item_filter)
#     if not prototype.data:
#         return {}
    
#     report = report_factory(manager).create_default()
#     report.create(prototype.data)
#     return report.result

@app.route("/api/reports/transactions", methods=["GET"])
def reports_transaction(format: str):
    inner_format = format_reporting(format)
    report = report_factory(manager).create(inner_format)
    report.create( reposity.data[ data_reposity.transaction_key()] )
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