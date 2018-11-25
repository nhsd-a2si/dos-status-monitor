import pytest
from pymongo import MongoClient
from dos_status_monitor import config, database


@pytest.fixture
def db():
    client = MongoClient(config.MONGODB_URI)
    base = client.get_database()
    return base

@pytest.fixture
def watched_services(db):
    ws = db['watched_services']
    return ws

def clear_and_verify_empty(watched_services):
    watched_services.delete_many({})
    filter = {}
    assert watched_services.count_documents(filter) == 0

def test_add_service_to_watchlist(watched_services):
    clear_and_verify_empty(watched_services)
    test_id = '12345'
    database.add_watched_service(test_id)
    filter = {'id': test_id}
    assert watched_services.count_documents(filter) == 1
    results = watched_services.find(filter)
    result = results[0]
    assert result['id'] == test_id

def test_remove_service_from_watchlist(watched_services):
    test_id = '123456'
    watched_services.insert_one({'id': test_id})
    filter = {'id': test_id}
    assert watched_services.count_documents(filter) == 1
    results = watched_services.find(filter)
    assert results[0]['id'] == test_id

    database.remove_watched_service(test_id)
    filter = {'id': test_id}
    assert watched_services.count_documents(filter) == 0

