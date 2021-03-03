from django.http import HttpResponse

# Neo4j
from neo4j import GraphDatabase, WRITE_ACCESS

# json
import json

# restframework
from rest_framework.response import Response
from rest_framework.decorators import api_view


NEO4J_HOST = "ec2-18-204-8-11.compute-1.amazonaws.com"
NEO4J_PORT = 7677
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "guai"
NEO4J_URI = "bolt://{NEO4J_HOST}:{NEO4J_PORT}".format(NEO4J_HOST=NEO4J_HOST,NEO4J_PORT=NEO4J_PORT)
print(NEO4J_URI)


def create_driver(uri, user, password):
    driver = GraphDatabase.driver(uri, auth=(user, password), encrypted = False)
    return driver

def get_driver_and_session():
    driver = create_driver(NEO4J_URI, user=NEO4J_USERNAME, password=NEO4J_PASSWORD)   
    session = driver.session(default_access_mode=WRITE_ACCESS)
    return driver, session

@api_view()
def CollaborativeFilter(request, pk):
    driver, session = get_driver_and_session()
    query = """MATCH (c:Cliente {customerid: "%s" }) MATCH (c)-[:REALIZO]->(:Transaccion)-[:CONTIENE]->(p:Producto) MATCH (p)<-[:CONTIENE]-(:Transaccion)<-[:REALIZO]-(u:Cliente) MATCH (u)-[:REALIZO]->(:Transaccion)-[:CONTIENE]->(rec:Producto) RETURN rec.sku AS sku, rec.nombre AS nombre, rec.precio AS precio, COUNT(*) AS puntaje ORDER BY puntaje DESC LIMIT 5""" % pk
    result = session.run(query).data()
    session.close()
    driver.close()
    return Response(result)


