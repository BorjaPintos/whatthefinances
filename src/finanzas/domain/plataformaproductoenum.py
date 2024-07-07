from enum import Enum


class PlataformaProductoEnum(Enum):
    Investing = 1
    Yahoo_Finances = 2

    @staticmethod
    def get_enum_from_value(id_plataforma: int):
        try:
            return PlataformaProductoEnum(id_plataforma)
        except:
            return None

    def get_dto(self):
        return {"id": self.value,
                "nombre": self.name}

    @classmethod
    def get_all(cls):
        return [e for e in cls]

    @classmethod
    def get_all_dto(cls):
        return [e.get_dto() for e in cls]
