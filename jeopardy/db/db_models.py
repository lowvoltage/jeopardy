from typing import Any

from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# TODO: Can we avoid declaring the models twice, once at the `pydantic`, once at the DB side?
# TODO: `mypy` is not happy. Fix it later
class Jeopardy(Base):  # type: ignore [valid-type, misc]
    __tablename__ = 'jeopardy'

    question_id = Column(Integer, primary_key=True)
    show_no = Column(Integer)
    air_date = Column(Date)
    round = Column(String)
    category = Column(String)
    value = Column(Integer)
    question = Column(String)
    answer = Column(String)

    # TODO: Is there an OOTB way to do this?
    def to_dict(self) -> dict[str, Any]:
        result = {field.name: getattr(self, field.name) for field in self.__table__.c}
        result['value'] = f'${self.value}'  # TODO: Settle on an int/str policy for "value" field
        return result
