from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


def to_dict(row):
    """
    Covert a row into dict
    :param row: sqlalchemy row
    :return: dict
    """
    result = {}
    for col in row.__table__.columns:
        result[col.name] = getattr(row, col.name)
        if type(result[col.name]) == datetime:
            result[col.name] = result[col.name].strftime("%Y-%m-%d %H:%M:%S")
    return result
