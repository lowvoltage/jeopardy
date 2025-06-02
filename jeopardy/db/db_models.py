from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# TODO: Can we avoid declaring the models twice, once at the `pydantic`, once at the DB side?
# TODO: `mypy` is not happy. Fix it later
class Jeopardy(Base):  # type: ignore [valid-type, misc]
    __tablename__ = 'jeopardy'

    id = Column(Integer, primary_key=True)
    show_no = Column(Integer)
    air_date = Column(Date)
    round = Column(String)
    category = Column(String)
    value = Column(Integer)
    question = Column(String)
    answer = Column(String)
