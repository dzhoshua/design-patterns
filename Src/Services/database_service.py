from Src.Core.abstract_logic import abstract_logic
from Src.Core.event_type import event_type
from Src.Services.observe_service import observe_service
import psycopg2
import os
import json
from datetime import datetime


class database_service(abstract_logic):
    
    def __init__(self):
        self.file_name = "dump.sql"
        self.db_name = os.getenv("DB_NAME", None)
        self.db_user = os.getenv("POSTGRESQL_USER", None)
        self.db_password = os.getenv("POSTGRESQL_PASS", None)
        self.db_port = os.getenv("POSTGRESQL_PORT", None)
        observe_service.append(self)
        
        
    def __connect(self):
        try: 
            connection = psycopg2.connect(database = self.db_name,
                                    user = self.db_user,
                                    password = self.db_password,
                                    port = self.db_port) 
            cursor = connection.cursor() 
        
        except Exception as ex:
            observe_service.raise_event(event_type.ERROR, ex)
        observe_service.raise_event(event_type.INFO, f"Подключение к базе данных прошло успешно.")
        return connection, cursor 
    
    
    def init_database(self):
        try:
            with open(self.file_name, 'r') as file:
                query = file.read()
        except Exception as ex:
            observe_service.raise_event(event_type.ERROR, f"Ошибка при открытии файла {self.file_name}!")
        
        connection, cursor = self.__connect()
        try:
            cursor.execute(query)
            connection.commit()
        except Exception:
            observe_service.raise_event(event_type.ERROR, f"Ошибка при создании таблиц базы данных!")
        observe_service.raise_event(event_type.INFO, f"Схема таблиц базы данных установленна.")
    
    
    def write(self, table_name, id, name, document):
        query = f"""
               INSERT INTO {table_name} (id, name, document, timestamp)
               VALUES (%s, %s, %s, %d);
            """
            
        connection, cursor = self.__connect()
        
        try:
            cursor.execute(query, (id, name, document, datetime.timestamp(datetime.now())))
            connection.commit()
        except Exception as ex:
            connection.rollback()
            observe_service.raise_event(event_type.ERROR, f"Ошибка при загрузке данных в базу данных!")
        observe_service.raise_event(event_type.INFO, f"Данные успешно загружены в базу данных.")
        
    
    
    def read(self, table_name):
        query = f"SELECT data FROM {table_name};"
        connection, cursor = self.__connect()
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
        except Exception:
            observe_service.raise_event(event_type.ERROR, f"Ошибка при выгрузке данных из базы данных!")
        return rows

