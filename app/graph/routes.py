from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from ariadne import graphql_sync, make_executable_schema, gql, load_schema_from_path
from ariadne.constants import PLAYGROUND_HTML
import os
from . import graph
from .model import query, mutation

type_defs = gql(load_schema_from_path("app/graph/schema.graphql"))
schema = make_executable_schema(type_defs, query, mutation)

static_dir = os.path.join('client', 'build')

app = Flask(__name__,
    root_path=os.path.abspath(".."),
    static_folder=static_dir,
    static_url_path='')

cors = CORS(app, resources={r"/graphql": {"origins": "*"}})

@graph.route('/')
def root():
    return send_from_directory(static_dir, "index.html")


@graph.route("/graphql", methods=["GET"])
def graphql_playgroud():
    """Serve GraphiQL playground"""
    return PLAYGROUND_HTML, 200


@graph.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()

    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug)

    status_code = 200 if success else 400
    return jsonify(result), status_code

