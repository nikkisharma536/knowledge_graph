import pandas as pd
from py2neo import Graph


#####################################################################
# Graph database config
#####################################################################

# Set up a link to the local graph database.
# Ideally get password from ENV variable
# graph = Graph(getenv("NEO4J_URL"), auth=(getenv("NEO4J_UID"), getenv("NEO4J_PASSWORD")))
graph = Graph("bolt://127.0.0.1:7687", auth=('neo4j', 'test'))

# Add uniqueness constraints.
graph.run("CREATE CONSTRAINT ON (p:Person) ASSERT p.uid IS UNIQUE;")
graph.run("CREATE CONSTRAINT ON (c:Country) ASSERT c.name IS UNIQUE;")
graph.run("CREATE CONSTRAINT ON (m:MajorStream) ASSERT m.name IS UNIQUE;")
graph.run("CREATE CONSTRAINT ON (w:WorkType) ASSERT w.name IS UNIQUE;")



def read_data():
    data = pd.read_csv(

        "./data/survey_results_public.csv",
        low_memory=False)
    print("Column name of data : ", data.columns)
    return data


def process_user_data(data):
    user_data = data[['Respondent','Hobby', 'OpenSource', 'Student', 'Employment', 'CompanySize', 'YearsCoding']]
    user_data =  user_data.dropna()

    # Convert data frame to list of dictionaries
    # Neo4j UNWIND query expects a list of dictionaries
    # for bulk insertion
    user_data = list(user_data.T.to_dict().values())
    print(user_data)

    query = """
            UNWIND {rows} AS row

            MERGE (person:Person {uid:row.Respondent})
            ON CREATE SET 
                person.codes_as_hobby = row.Hobby,
                person.contributes_to_open_source = row.OpenSource,
                person.is_student = row.Student,
                person.employment_status = row.Employment,
                person.company_size = row.CompanySize,
                person.total_years_of_coding_experience = row.YearsCoding
        """

    run_neo_query(user_data,query)


def process_country_data(data):
    country_data = data[['Respondent', 'Country']]
    country_data = country_data.dropna()
    country_data = list(country_data.T.to_dict().values())

    query = """
           UNWIND {rows} AS row
           MERGE (person:Person {uid:row.Respondent})
           MERGE (country:Country {name:row.Country})
           MERGE (person)-[:LIVES_IN]->(country)
       """
    run_neo_query(country_data,query)


def process_major_data(data):
    major_data = data[['Respondent', 'UndergradMajor']]
    major_data = major_data.dropna()
    major_data = list(major_data.T.to_dict().values())

    query = """
            UNWIND {rows} AS row
            MERGE (person:Person {uid:row.Respondent})
            MERGE (major:MajorStream {name:row.UndergradMajor})
            MERGE (person)-[:MAJORED_IN]->(major)
        """
    run_neo_query(major_data,query)


def process_dev_data(data):
    dev_data = data[['Respondent', 'DevType']]
    dev_data = dev_data.dropna()

    s = dev_data['DevType'].str.split(';').apply(pd.Series, 1).stack()
    s.name = "DevType"
    del dev_data["DevType"]
    s = s.to_frame().reset_index()
    dev_data = pd.merge(dev_data, s, right_on='level_0', left_index = True)

    del dev_data["level_0"]
    del dev_data["level_1"]
    dev_data = list(dev_data.T.to_dict().values())

    query = """
           UNWIND {rows} AS row
           MERGE (person:Person {uid:row.Respondent})
           MERGE (work:WorkType {name:row.DevType})
           MERGE (person)-[:WORKS_IN_INDUSTRY]->(work)
           
       """
    run_neo_query(dev_data,query)


def run_neo_query(data, query):
    batches = get_batches(data)

    for index, batch in batches:
        print('[Batch: %s] Will add %s node to Graph' % (index, len(batch)))
        graph.run(query, rows=batch)


def get_batches(lst, batch_size=100):
    return [(i, lst[i:i + batch_size]) for i in range(0, len(lst), batch_size)]


if __name__== "__main__":
    data = read_data()
    process_user_data(data)
    process_country_data(data)
    process_major_data(data)
    process_dev_data(data)
