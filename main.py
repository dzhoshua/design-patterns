import connexion
from flask import Response, request
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
from Src.Core.logger_level import logger_level
from Src.Logging.logger import logger
from Src.Services.nomenclature_service import nomenclature_service
from Src.Core.event_type import event_type
from Src.Processors.turnover_balanse_sheet import turnover_balanse_sheet
from Src.Managers.reposity_manager import reposity_manager


app = connexion.FlaskApp(__name__)
manager = settings_manager()
manager.open("settings.json")
reposity = data_reposity()
_nomenclature_service = nomenclature_service(reposity)
_reposity_manager = reposity_manager(reposity, manager)
_balanse_sheet = turnover_balanse_sheet(manager)
_logger = logger(manager)
start = start_service(reposity, manager)
start.create()


"""
Форматы отчетов
"""
@app.route("/api/reports/formats", methods=["GET"])
def formats():
    observe_service.raise_event(event_type.INFO, "GET /api/reports/formats")
    result = [{"name":item.name, "value":item.value} for item in format_reporting]
    observe_service.raise_event(event_type.INFO, "Список доступных форматов отчета получен.")
    observe_service.raise_event(event_type.DEBUG, result)
    return result


"""
Отчеты. Единица измерения
"""
@app.route("/api/reports/range/<format>", methods=["GET"])
def reports_range(format: str):
    observe_service.raise_event(event_type.INFO, f"GET /api/reports/range/{format}")
    
    format = format.upper()
    inner_format = format_reporting(format)
    report = report_factory(manager).create(inner_format)
    report.create( reposity.data[ data_reposity.range_key()  ] )
    
    observe_service.raise_event(event_type.INFO, f"Отчет по единицам измерения в формате {format} создан.")
    return report.result


"""
Отчеты. Группа
"""
@app.route("/api/reports/group/<format>", methods=["GET"])
def reports_group(format: str):
    observe_service.raise_event(event_type.INFO, f"GET /api/reports/group/{format}")
    
    format = format.upper()
    inner_format = format_reporting(format)
    report = report_factory(manager).create(inner_format)
    report.create( reposity.data[ data_reposity.group_key()  ] )
    
    observe_service.raise_event(event_type.INFO, f"Отчет по группам в формате {format} создан.")
    return report.result


"""
Отчеты. Номенклатура
"""
@app.route("/api/reports/nomenclature/<format>", methods=["GET"])
def reports_nomenclature(format: str):
    observe_service.raise_event(event_type.INFO, f"GET /api/reports/nomenclature/{format}")
    
    format = format.upper()
    inner_format = format_reporting(format)
    report = report_factory(manager).create(inner_format)
    report.create( reposity.data[ data_reposity.nomenclature_key()  ] )
    
    observe_service.raise_event(event_type.INFO, f"Отчет по номенклатурам в формате {format} создан.")
    return report.result


"""
Отчеты. Рецепты
"""
@app.route("/api/reports/recipe/<format>", methods=["GET"])
def reports_recipe(format: str):
    observe_service.raise_event(event_type.INFO, f"GET /api/reports/recipe/{format}")
    
    format = format.upper()
    inner_format = format_reporting(format)
    report = report_factory(manager).create(inner_format)
    report.create( reposity.data[ data_reposity.receipt_key()  ] )
    
    observe_service.raise_event(event_type.INFO, f"Отчет по рецептам в формате {format} создан.")
    return report.result


"""
Отчеты. Транзакции
"""
@app.route("/api/reports/transactions/<format>", methods=["GET"])
def reports_transaction(format: str):
    observe_service.raise_event(event_type.INFO, f"GET /api/reports/transactions/{format}")
    
    format = format.upper()
    inner_format = format_reporting(format)
    report = report_factory(manager).create(inner_format)
    report.create( reposity.data[ data_reposity.transaction_key()] )
    
    observe_service.raise_event(event_type.INFO, f"Отчет по транзакциям в формате {format} создан.")
    return report.result


"""
Отчеты. Обороты
"""
@app.route("/api/reports/turnovers/<format>", methods=["GET"])
def reports_turnover(format: str):
    observe_service.raise_event(event_type.INFO, f"GET /api/reports/turnovers/{format}")
    
    process_turnover = turnover_process(manager)
    turnovers = process_turnover.processing(reposity.data[data_reposity.transaction_key()])
    
    format = format.upper()
    inner_format = format_reporting(format)
    report = report_factory(manager).create(inner_format)
    report.create(turnovers)
    
    observe_service.raise_event(event_type.INFO, f"Отчет по оборотам в формате {format} создан.")
    return report.result


"""
Отчеты. ОСВ (оборотно-сальдовая ведомость)
"""
@app.route("/api/reports/balanse_sheet/<date_start>/<date_end>/<warehouse_name>", methods=["GET"])
def reports_balanse_sheet(date_start:str, date_end:str, warehouse_name:str ):
    observe_service.raise_event(event_type.INFO, f"GET /api/reports/balanse_sheet/{date_start}/{date_end}/{warehouse_name}")
    
    try:
        date_start = datetime.strptime(date_start, "%Y-%m-%d")
        date_end = datetime.strptime(date_end, "%Y-%m-%d")
    except:
        observe_service.raise_event(event_type.ERROR, "Неверно введены даты!")
        return Response(f"Неверно введены даты!", 400)
    
    transactions = reposity.data[reposity.transaction_key()]
    if not transactions:
        observe_service.raise_event(event_type.ERROR, "Нет транзакций для расчета!")
        return Response("Нет транзакций для расчета!", 400)
    
    balanse_sheet = _balanse_sheet.processing(transactions, date_start, date_end, warehouse_name)
    report = report_factory(manager).create_default()
    report.create([balanse_sheet])
    data = report.result
    with open("tbs_report.json", 'w', encoding='utf-8') as f:
            f.write(data)
            
    observe_service.raise_event(event_type.INFO, f"Отчет по ОСВ создан и записан в файл 'tbs_report.json'.")
    return data


"""
Блокировка. Получение текущей даты
"""
@app.route("/api/block_period/get", methods=["GET"])
def get_block_period():
    observe_service.raise_event(event_type.INFO, "GET /api/block_period/get")
    observe_service.raise_event(event_type.INFO, "Дата блокировки получена.")
    observe_service.raise_event(event_type.DEBUG, f"Текущая дата блокировки: {manager.settings.block_period}")
    return str(manager.settings.block_period)


"""
Блокировка. Установка даты
"""
@app.route("/api/block_period/set", methods=["POST"])
def set_block_period():
    observe_service.raise_event(event_type.INFO, "POST /api/block_period/set")
    
    request_data = request.get_json()
    new_block_period = request_data.get("block_period")
    if new_block_period is None:
        observe_service.raise_event(event_type.ERROR, "Дата блокировки не указана!")
        return Response("Дата блокировки не указана!", 400)
        
    manager.settings.block_period = new_block_period
    try:
        manager.save()
    except Exception as ex:
        observe_service.raise_event(event_type.ERROR, ex)
    
    blocked_turnover_process = blocking_process(manager)
    
    transactions = reposity.data[reposity.transaction_key()]
    if not transactions:
        observe_service.raise_event(event_type.ERROR, "Нет транзакций для пересчета!")
        return Response("Нет транзакций для пересчета!", 400)
    blocked_turnovers = blocked_turnover_process.processing(transactions)
    reposity.data[data_reposity.blocked_turnover_key()] = blocked_turnovers
    
    observe_service.raise_event(event_type.INFO, f"Установлена новая дата блокировки: {new_block_period}")
    return f"new_block_period: {new_block_period}"
    
    
"""
CRUD операции. Получить номенклатуру
"""
@app.route("/api/nomenclature", methods=["GET"])
def get_nomenclature(unique_code: str):
    observe_service.raise_event(event_type.INFO, "GET /api/nomenclature")
    
    try:
        data = reposity.data[data_reposity.nomenclature_key()]
    except:
        observe_service.raise_event(event_type.ERROR, "Нет данных!")
        return Response("Нет данных!", 400)
        
    nomenclature = _nomenclature_service.get_nomenclature(data, unique_code)
    if len(nomenclature) == 0:
        observe_service.raise_event(event_type.ERROR, f"Номенклатура с кодом '{unique_code}' не найдена!")
        return Response("Номенклатура с таким кодом не найдена!", 400)
    
    report = report_factory(manager).create_default()
    report.create(nomenclature)
    observe_service.raise_event(event_type.INFO, f"Номенклатура с кодом '{unique_code}' получена.")
    observe_service.raise_event(event_type.DEBUG, report.result)
    return report.result
    

"""
CRUD операции. Добавить номенклатуру
"""    
@app.route("/api/nomenclature", methods=["PUT"])
def put_nomenclature():
    observe_service.raise_event(event_type.INFO, "PUT /api/nomenclature")
    
    request_data = request.get_json()
    name = request_data.get("name") 
    group_id = request_data.get("group_id")
    range_id = request_data.get("range_id")
    
    result = _nomenclature_service.put_nomenclature(name, group_id, range_id)
    return Response(result)


"""
CRUD операции. Изменить номенклатуру
"""
@app.route("/api/nomenclature", methods=["PATCH"])
def patch_nomenclature():
    observe_service.raise_event(event_type.INFO, "PATCH /api/nomenclature")
    
    request_data = request.get_json()
    result = observe_service.raise_event(event_type.CHANGE_NOMENCLATURE, request_data)
    result = result[type(_nomenclature_service).__name__]
    
    return Response(result)


"""
CRUD операции. Удалить номенклатуру
"""
@app.route("/api/nomenclature", methods=["DELETE"])
def delete_nomenclature(unique_code: str):
    observe_service.raise_event(event_type.INFO, "DELETE /api/nomenclature")
    
    result = observe_service.raise_event(event_type.DELETE_NOMENCLATURE, unique_code)
    result = result[type(_nomenclature_service).__name__]
    return Response(result)


"""
Репозиторий. Сохранение в файл
"""
@app.route("/api/reposity/save", methods=["POST"])
def save_reposity():
    observe_service.raise_event(event_type.INFO, "POST /api/reposity/save")
    result = observe_service.raise_event(event_type.SAVE_DATA_REPOSITY, {})
    
    result = result[type(_reposity_manager).__name__]
    if manager.settings.first_start:
        manager.settings.first_start = False
        manager.save()
    return Response(result)
        

"""
Репозиторий. Восстановление из файла
"""
@app.route("/api/reposity/restore", methods=["POST"])
def restore_reposity():
    observe_service.raise_event(event_type.INFO, "POST /api/reposity/restore")
    result = observe_service.raise_event(event_type.RESTORE_DATA_REPOSITY, {})
    result = result[type(_reposity_manager).__name__]
    return Response(result)


"""
Фильтрация. По медели
"""
@app.route("/api/filter/<domain>", methods=["POST"])
def filter_data(domain: str):
    observe_service.raise_event(event_type.INFO, f"POST /api/filter/{domain}")
    
    if domain not in reposity.keys():
        observe_service.raise_event(event_type.ERROR, f"Домен '{domain}'не найден!")
        return Response(f"Домен '{domain}'не найден!", 400)
    
    request_data = request.get_json()
    item_filter = filter.create(request_data)
    
    try:
        data = reposity.data[domain]
    except:
        observe_service.raise_event(event_type.ERROR, "Нет данных!")
        return Response(f"Нет данных!", 400)
    
    prototype = domain_prototype(data)
    prototype.create(item_filter)
    if not prototype.data:
        observe_service.raise_event(event_type.INFO, "Нет данных подходящих под фильтр.")
        return {}
    
    report = report_factory(manager).create_default()
    report.create(prototype.data)
    
    observe_service.raise_event(event_type.INFO, "Данные отфильтрованы.")
    return Response(report.result, 200)


"""
Фильтрация. Транзакции
"""
@app.route("/api/filter/transactions", methods=["POST"])
def filter_transactions():
    observe_service.raise_event(event_type.INFO, "POST /api/filter/transactions")
    
    try:
        # получение списка транзакций
        transactions = reposity.data[reposity.transaction_key()]
    except:
        observe_service.raise_event(event_type.ERROR, "Нет данных!")
        return Response(f"Нет данных!", 400)
    
    request_data = request.get_json()
    
    try:
        warehouse = request_data.get("warehouse")
        nomenclature = request_data.get("nomenclature")
    except:
        observe_service.raise_event(event_type.ERROR, f"Ключи warehouse или nomenclature не найдены!")
        return Response(f"Ключи warehouse или nomenclature не найдены!", 400)
    print(warehouse)
    
    warehouse_filter = filter.create(warehouse)
    nomenclature_filter = filter.create(nomenclature)
    return "Не доделано. Не работает"
    
    # prototype = domain_prototype(transactions)
    # prototype.create(warehouse_filter)
    # prototype.create(nomenclature_filter)
    
    # if not prototype.data:
    #     return {}
    
    # report = report_factory(manager).create_default()
    # report.create(prototype.data)
    # return report.result


if __name__ == "__main__":
    app.add_api("swagger.yaml")
    # app.run(port = 8080)
    app.run(host="0.0.0.0", port = 8080)