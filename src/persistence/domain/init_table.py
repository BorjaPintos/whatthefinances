from src.persistence.infrastructure.orm.baseentity import BaseEntity


class InitTable:
    ENTITIES_TO_INIT = []

    @staticmethod
    def get_entities_to_init():
        return InitTable.ENTITIES_TO_INIT

    def __call__(self, entity: BaseEntity):
        InitTable.ENTITIES_TO_INIT.append(entity)
        return entity
