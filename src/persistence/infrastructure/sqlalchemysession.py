from sqlalchemy.orm.session import Session


class SQLAlchmeySession(Session):

    def save_or_update(self, domainObject):

        raise Exception("NotImplemented")
