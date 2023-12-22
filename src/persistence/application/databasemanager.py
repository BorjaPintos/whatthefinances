import traceback
from contextlib import contextmanager
from typing import List
from unittest.mock import Mock

from loguru import logger

from src.persistence.domain.database import Database
from src.persistence.domain.init_table import InitTable
from src.persistence.infrastructure.mockdatabase import MockDatabase
from src.persistence.infrastructure.orm.baseentity import BaseEntity
from src.persistence.infrastructure.postgresql.postgresdatabase import PostgresDatabase
from src.persistence.infrastructure.sqlite.sqlitedatabase import SQLiteDatabase


class DatabaseManager:
    _DATABASE = None

    @staticmethod
    def init(config: dict):
        DatabaseManager._DATABASE = DatabaseManager.__init_database(config)
        return DatabaseManager

    @staticmethod
    def __init_database(config: dict) -> Database:
        switch_database = {
            'mock': MockDatabase,
            'sqlite': SQLiteDatabase,
            'postgres': PostgresDatabase
        }
        return switch_database.get(config["type"])(config[config["type"]])

    @staticmethod
    def get_database() -> Database:
        return DatabaseManager._DATABASE

    @staticmethod
    def list_tables() -> List[str]:
        return DatabaseManager._DATABASE.list_tables()

    @staticmethod
    def delete_table(entity: BaseEntity):
        return DatabaseManager._DATABASE.delete_table(entity)

    @staticmethod
    def clear_table(table_name: str):
        return DatabaseManager._DATABASE.clear_table(table_name)

    @staticmethod
    def describe_table(table_name: str) -> List[tuple]:
        """devuelve (nombre,tipo)"""
        return DatabaseManager._DATABASE.describe_table(table_name)

    @staticmethod
    def check_if_table_exist(table_name: str):
        return DatabaseManager._DATABASE.check_if_table_exist(table_name)

    @staticmethod
    def check_if_table_has_data(table_name: str):
        return DatabaseManager._DATABASE.check_if_table_has_data(table_name)

    @staticmethod
    def create_table(entity: BaseEntity) -> bool:
        return DatabaseManager._DATABASE.create_table(entity)

    @staticmethod
    def exec_sql(query: str, commit: bool = True):
        return DatabaseManager._DATABASE.exec_sql(query, commit)

    @staticmethod
    def commit():
        return DatabaseManager._DATABASE.commit()

    @staticmethod
    def rollback():
        return DatabaseManager._DATABASE.rollback()

    @staticmethod
    def new_session():
        return DatabaseManager._DATABASE.new_session()

    @staticmethod
    @contextmanager
    def get_session_scope():
        """Provide a transactional scope around a series of operations."""
        session = DatabaseManager._DATABASE.new_session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    @contextmanager
    def get_readonly_session_scope():
        """Provide a readonly transactional scope around a series of operations."""
        session = DatabaseManager._DATABASE.new_session()
        try:
            yield session
            session.rollback()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    def init_tables(config_init):
        entities_to_init = InitTable.get_entities_to_init()
        for entity in entities_to_init:
            if config_init["delete_data_on_init"]:
                DatabaseManager.delete_table(entity)
                DatabaseManager.commit()
            try:
                if not DatabaseManager.check_if_table_exist(entity.__tablename__):
                    DatabaseManager.create_table(entity)
                    DatabaseManager.commit()
                    logger.info("Tabla '{}', creada correctamente", entity.__tablename__)
                else:
                    logger.info("Ya existe la tabla '{}'", entity.__tablename__)
            except Exception as e:
                DatabaseManager.rollback()
                traceback.print_exc()
                logger.info("No se pudo crear la tabla '{}'", entity.__tablename__)
                logger.error(e)

    @staticmethod
    def init_data(config_init):
        for table, sql_path in config_init["sql_path_files"].items():
            if not DatabaseManager.check_if_table_has_data(table):
                with open(sql_path, encoding="utf-8") as file:
                    seguir = True
                    while seguir:
                        query = file.readline()
                        if query is not None and query not in ["", "\n", "\r\n"]:
                            DatabaseManager.exec_sql(query, commit=False)
                        else:
                            seguir = False
        DatabaseManager.commit()
