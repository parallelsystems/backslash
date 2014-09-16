from flask import Blueprint

from .models import Session, Test
from weber_utils import paginated_view
from .api_utils import auto_render, render_api_object

blueprint = Blueprint('rest', __name__)


def _register_rest_getters(objtype):
    typename = objtype.__name__.lower()
    @blueprint.route('/{0}s/<int:object_id>'.format(typename), endpoint='get_single_{0}'.format(typename))
    @auto_render
    def get_single_object(object_id):
        return objtype.query.get(object_id)

    @blueprint.route('/{0}s'.format(typename), endpoint='query_{0}s'.format(typename))
    @paginated_view(renderer=render_api_object)
    def query_objects():
        return objtype.query



################################################################################

_register_rest_getters(Session)
_register_rest_getters(Test)
