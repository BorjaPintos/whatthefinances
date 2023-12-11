from sqlalchemy import Column, Text, Integer
from src.login.domain.user import User
from src.persistence.domain.init_table import InitTable
from src.persistence.infrastructure.orm.baseentity import BaseEntity


@InitTable()
class UserEntity(BaseEntity):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    password = Column(Text, nullable=False)

    @staticmethod
    def get_order_column(str_property: str):
        switcher = {
            "id": UserEntity.id,
            "name": UserEntity.name,
            "password": UserEntity.password
        }
        return switcher.get(str_property, UserEntity.id)

    @staticmethod
    def get_filter_column(str_property: str):
        switcher = {
            "id": UserEntity.id,
            "name": UserEntity.name,
        }
        return switcher.get(str_property)

    @staticmethod
    def cast_to_column_type(column: Column, value: str):
        caster = {
            UserEntity.id: int,
            UserEntity.name: str,
            UserEntity.password: str,
        }
        return caster.get(column)(value)

    def convert_to_object_domain(self) -> User:
        return User(id=self.id,
                    name=self.name,
                    encrypted_password=self.password)
