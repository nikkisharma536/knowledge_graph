from py2neo import Graph

#####################################################################
# Graph database config
#####################################################################

# Set up a link to the local graph database.
# Ideally get password from ENV variable
# graph = Graph(getenv("NEO4J_URL"), auth=(getenv("NEO4J_UID"), getenv("NEO4J_PASSWORD")))
graph = Graph("bolt://127.0.0.1:7687", auth=('neo4j', 'test'))


#####################################################################
# Utility functions to talk to our knowledge graph
#####################################################################

def get_person_by_id(p_id):
    query = '''
        MATCH (n:Person {uid: {id}})
        RETURN n as person
    '''
    # Use evaluate() if a single record is expected &
    # use run()if multiple records are expected
    result = graph.run(query, parameters={'id': p_id}).data()
    if len(result) == 0 :
        return {}
    else :
        return result[0]['person']


def relation_of_person_by_id(p_id):
    query = '''
        MATCH (n:Person {uid: {id}})-[r]->(c)
        RETURN n as person,type(r) as relation_name, c as value
    '''
    result = graph.run(query, parameters={'id': p_id}).data()

    if len(result) == 0 :
        return {}
    else :
        person = result[0]["person"]
        person["work_industry"] = [row["value"]["name"] for row in result if row["relation_name"] == "WORKS_IN_INDUSTRY" ]
        person["majored"] = [row["value"]["name"] for row in result if row["relation_name"] == "MAJORED_IN" ]
        person["country"] = [row["value"]["name"] for row in result if row["relation_name"] == "LIVES_IN" ]
        return person


def get_all_count():
    query = '''
        MATCH (n:Person)
        WITH count(n) as count
        RETURN 'Person' as NodeType, count
        UNION ALL
        MATCH (n:Country)
        WITH count(n) as count
        RETURN 'Country' as NodeType, count
        UNION ALL
        MATCH (n:WorkType)
        WITH count(n) as count
        RETURN 'WorkType' as NodeType, count
        UNION ALL
        MATCH (n:MajorStream)
        WITH count(n) as count
        RETURN 'MajorStream' as NodeType, count
    '''

    return graph.run(query).data()




