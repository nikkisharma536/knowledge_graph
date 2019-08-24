from flask_api import FlaskAPI
import api.query_graph as graphapi
import traceback
from flask import request

#####################################################################
# Configs
#####################################################################
app = FlaskAPI("KnowledgeGraphAPI")


#####################################################################
# API Endpoints
#####################################################################

@app.route('/', methods=["GET"])
def hello():
    try:
        return {
            'status': 'successful',
            'message': 'Welcome to the knowledge graph api.',
            'supported_endpoints': ['%s' % rule for rule in app.url_map.iter_rules()]
        }
    except Exception as ex:
        traceback.print_exc()
        return {'status': 'failed', 'error': str(ex)}


# Passing p_id via Url. Parameter p_id
# will be passed to the function
@app.route('/person_details_with_relationships/<int:p_id>', methods=["GET"])
def person_relation_by_id(p_id):
    try:
        return graphapi.relation_of_person_by_id(p_id)
    except Exception as ex:
        traceback.print_exc()
        return {'status': 'failed', 'error': str(ex)}


# Same as last endpoint,
# but serving data via POST this time
@app.route('/person_details', methods=["GET", "POST"])
def call_get_person_by_id():
    try :
        # Use request.data for fetching
        # json passed to request
        p_id = request.data.get('p_id')
        return graphapi.get_person_by_id(p_id)
    except Exception as ex:
        traceback.print_exc()
        return {'status': 'failed', 'error': str(ex)}



@app.route('/graph_size', methods=["GET"])
def count_all_node():
    try :
        return graphapi.get_all_count()
    except Exception as ex:
        traceback.print_exc()
        return {'status': 'failed', 'error': str(ex)}


#####################################################################
# Entry point
#####################################################################

if __name__ == "__main__":
    app.run()
