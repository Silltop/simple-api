import logging
from sqlite3 import OperationalError, DatabaseError
from typing import Optional

from flask import abort
from models import GeolocationModel
from api import db, app


def handle_db_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except OperationalError as e:
            logging.error(f"OperationalError: Could not connect to the database. Is the database down? Error: {e}")
            abort(500, "Internal server error.")

        except DatabaseError as e:
            logging.error(f"DatabaseError occurred: {e}")
            abort(500, "Internal server error.")

        except Exception as e:
            logging.error(f"Unexpected error occurred: {e}")
            abort(500, "Internal server error.")

    return wrapper


def add_result_to_db(result: dict) -> None:
    existing_entry = GeolocationModel.query.filter_by(
        ip=result["ip"],
        hostname=result["hostname"],
        country_code=result["country_code"],
        city=result["city"],  # potentially can be problematic if city name is written differently
    ).first()
    if existing_entry:
        return

    entry = GeolocationModel(
        ip=result["ip"],  # type: ignore
        hostname=result["hostname"],  # type: ignore
        country_code=result["country_code"],  # type: ignore
        city=result["city"],  # type: ignore
    )
    db.session.add(entry)


@handle_db_errors
def add_results_to_db(results: list) -> None:
    with app.app_context():
        for result in results:
            add_result_to_db(result)
            db.session.commit()


@handle_db_errors
def delete_result_from_db(ips: list) -> None:
    #  assuming that if user wants to delete, they want to delete all entries for that IP
    with app.app_context():
        for ip in ips:
            entries = GeolocationModel.query.filter_by(ip=ip).all()
            for entry in entries:
                db.session.delete(entry)
            db.session.commit()


@handle_db_errors
def get_results_from_db(ips: list) -> Optional[list]:
    with app.app_context():
        for ip in ips:
            entries = GeolocationModel.query.filter_by(ip=ip).all()
            return entries
