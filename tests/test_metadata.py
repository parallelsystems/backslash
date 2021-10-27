import requests

from .utils import raises_not_found


def test_add_metadata(metadata_holder, metadata_key, metadata_value):
    metadata_holder.set_metadata(metadata_key, metadata_value)
    another_key = 'another_key'
    another_value = {'another': 31337}
    metadata_holder.set_metadata(another_key, another_value)
    assert metadata_holder.get_metadata() == {
        metadata_key: metadata_value,
        another_key: another_value
    }


def test_add_metadata_dict(metadata_holder, metadata_key, metadata_value):
    another_key = 'another_key'
    another_value = {'another': 31337}

    metadata_holder.set_metadata_dict({metadata_key: metadata_value, another_key: another_value})
    assert metadata_holder.get_metadata() == {
        metadata_key: metadata_value,
        another_key: another_value
    }



def test_get_metadata_by_logical_id(metadata_holder, metadata_key, metadata_value, client):
    assert metadata_holder.logical_id
    metadata_holder.set_metadata(metadata_key, metadata_value)
    result = client.api.call_function(
        'get_metadata', {
            'entity_type': metadata_holder.type,
            'entity_id': metadata_holder.logical_id,
            })
    assert result == {metadata_key: metadata_value}



def test_create_session_with_metadata(client, metadata):
    session = client.report_session_start(metadata=metadata)
    assert session.get_metadata() == metadata


def test_add_metadata_nonexistent_session(nonexistent_session):
    with raises_not_found():
        nonexistent_session.set_metadata('foo', 'bar')


def test_add_test_metadata(started_test):
    """Add test metadata to a started test"""
    new_metadata = {"foo": "bar", "baz": 1}
    params = {"id": started_test.id, "metadata": new_metadata}
    started_test.client.api.call_function("add_test_metadata", params)
    updated_metadata = started_test.get_metadata()
    for key, value in new_metadata.items():
        assert updated_metadata[key] == value

    

def test_add_session_metadata(started_session):
    """Add session metadata to a started session"""
    new_metadata = {"foo": "bar", "baz": 1}
    params = {"id": started_session.id, "metadata": new_metadata}
    started_session.client.api.call_function("add_session_metadata", params)
    updated_metadata = started_session.get_metadata()
    for key, value in new_metadata.items():
        assert updated_metadata[key] == value
    