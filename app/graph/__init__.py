from flask import Blueprint

graph = Blueprint('graph', __name__)

from . import routes
# from ..models import Permission


@graph.app_context_processor
def inject_permissions():
    return dict(Permission="Permission")