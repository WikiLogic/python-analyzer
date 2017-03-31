
import localconfig
from neo4j.v1 import GraphDatabase, basic_auth

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=(localconfig.DBUSERNAME, localconfig.DBPASSWORD))

def print_claim_by_id(id):
    with driver.session() as session:
        with session.begin_transaction() as tx:
            for record in tx.run("MATCH (arg)-[]->(claim:Claim) "
                                 "WHERE ID(claim) = {id} "
                                 "RETURN claim.body", id=id):
                print(record["claim.body"])

print_claim_by_id(25)