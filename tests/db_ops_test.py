from sqlite3 import DatabaseError, OperationalError
from unittest.mock import MagicMock, patch

import pytest
import werkzeug.exceptions

from db_ops import (
    add_result_to_db,
    add_results_to_db,
    delete_result_from_db,
    get_results_from_db,
    handle_db_errors,
)


@patch("db_ops.db")
@patch("db_ops.GeolocationModel")
def test_add_result_to_db_existing_entry(mock_geolocation_model, mock_db):
    mock_geolocation_model.query.filter_by.return_value.first.return_value = True
    mock_db = MagicMock()
    db_session_add = mock_db.session.add
    result = {"ip": "127.0.0.1", "hostname": "localhost", "country_code": "US", "city": "New York"}
    add_result_to_db(result)
    db_session_add.assert_not_called()


@patch("db_ops.db.session")
@patch("db_ops.GeolocationModel")
def test_add_result_to_db_new_entry(mock_geolocation_model, mock_db_session):
    mock_geolocation_model.query.filter_by.return_value.first.return_value = None
    result = {"ip": "127.0.0.1", "hostname": "localhost", "country_code": "US", "city": "New York"}
    mock_db_session.add = MagicMock()
    add_result_to_db(result)
    mock_db_session.add.assert_called_once()


@patch("db_ops.db.session")
@patch("db_ops.GeolocationModel")
def test_add_results_to_db(mock_geolocation_model, mock_db_session):
    mock_geolocation_model.query.filter_by.return_value.first.return_value = None
    results = [
        {"ip": "127.0.0.1", "hostname": "localhost", "country_code": "US", "city": "New York"},
        {"ip": "192.168.1.1", "hostname": "testhost", "country_code": "US", "city": "Los Angeles"},
    ]
    mock_db_session.add = MagicMock()
    add_results_to_db(results)
    assert mock_db_session.add.call_count == 2


@patch("db_ops.db.session")
@patch("db_ops.GeolocationModel")
def test_delete_result_from_db(mock_query, mock_db_session):
    mock_entry = MagicMock()
    mock_query.query.filter_by.return_value.all.return_value = [mock_entry]
    ips = ["127.0.0.1"]
    mock_db_session.delete = MagicMock()
    delete_result_from_db(ips)
    mock_db_session.delete.assert_called_once()


@patch("db_ops.db.session")
@patch("db_ops.GeolocationModel")
def test_get_results_from_db(mock_query, mock_db_session):
    mock_entry = MagicMock()
    mock_query.query.filter_by.return_value.all.return_value = [mock_entry]
    ips = ["127.0.0.1"]
    results = get_results_from_db(ips)
    assert results == [mock_entry.to_dict()]


@patch("db_ops.GeolocationModel")
def test_get_results_from_db_no_entries(mock_query):
    mock_query.query.filter_by.return_value.all.return_value = []
    ips = ["127.0.0.1"]
    results = get_results_from_db(ips)
    assert results == []


def test_handle_db_errors_operational_error():
    @handle_db_errors
    def mock_func():
        raise OperationalError("Operational error message")

    with pytest.raises(werkzeug.exceptions.InternalServerError, match="Internal server error"):
        mock_func()


def test_handle_db_errors_database_error():
    @handle_db_errors
    def mock_func():
        raise DatabaseError("Database error message")

    with pytest.raises(werkzeug.exceptions.InternalServerError):
        mock_func()


def test_handle_db_errors_generic_error():
    @handle_db_errors
    def mock_func():
        raise ValueError("A generic error occurred")

    with pytest.raises(werkzeug.exceptions.InternalServerError):
        mock_func()
