from flask import abort
from flask_simple_api import error_abort
import requests
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from ...models import Session, SessionMetadata, Test, TestMetadata, db
from .blueprint import API


@API
def set_metadata(entity_type: str, entity_id: int, key: str, value: object):
    _set_metadata_dict(entity_type=entity_type,
                       entity_id=entity_id, metadata={key: value})


@API
def set_metadata_dict(entity_type: str, entity_id: int, metadata: dict):
    _set_metadata_dict(entity_type=entity_type,
                       entity_id=entity_id, metadata=metadata)


def _set_metadata_dict(*, entity_type, entity_id, metadata, commit=True):
    model = _get_metadata_model(entity_type)
    for key, value in metadata.items():
        db.session.add(model(key=key, metadata_item=value, **
                             {'{}_id'.format(entity_type): entity_id}))

    if commit:
        try:
            db.session.commit()
        except IntegrityError:
            abort(requests.codes.not_found)


@API(require_login=False)
def get_metadata(entity_type: str, entity_id: (int, str)):
    return _get_metadata_query(entity_type=entity_type, entity_id=entity_id).scalar() or {}


def _get_metadata_query(*, entity_type, entity_id):
    model = _get_metadata_model(entity_type)
    query = db.session.query(func.json_object_agg(model.key, model.metadata_item))
    if entity_type == 'session':
        related = Session
    elif entity_type == 'test':
        related = Test
    else:
        error_abort('Invalid entity type', requests.codes.bad_request)
    query = query.join(related)
    if isinstance(entity_id, int):
        query = query.filter(related.id == entity_id)
    else:
        query = query.filter(related.logical_id == entity_id)
    return query


def _get_metadata_model(entity_type):
    if entity_type == 'session':
        return SessionMetadata

    if entity_type == 'test':
        return TestMetadata

    error_abort('Unknown entity type')


@API
def add_test_metadata(id: int, metadata: dict):
    try:
        test = Test.query.filter(Test.id == id).one()
        for key, value in metadata.items():
            test.metadatas.append(TestMetadata(key=key, metadata_item=value))
    except NoResultFound:
        abort(requests.codes.not_found)
    db.session.commit()


@API
def add_session_metadata(id: int, metadata: dict):
    try:
        session = Session.query.filter(Session.id == id).one()
        for key, value in metadata.items():
            session.metadata_items.append(
                SessionMetadata(key=key, metadata_item=value))
    except NoResultFound:
        abort(requests.codes.not_found)
    db.session.commit()
