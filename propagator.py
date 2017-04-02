
import localconfig
from neo4j.v1 import GraphDatabase, basic_auth

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=(localconfig.DBUSERNAME, localconfig.DBPASSWORD))
propagation_terminator = []

def print_claim_by_id(id):
    with driver.session() as session:
        with session.begin_transaction() as tx:
            for record in tx.run("MATCH (arg)-[]->(claim:Claim) "
                                 "WHERE ID(claim) = {id} "
                                 "RETURN claim.body", id=id):
                print(record["claim.body"])

print_claim_by_id(25)

def propagate_from_a_claim(id):
    propagation_terminator.append(id)
    with driver.session() as session:
        with session.begin_transaction() as tx:
            for record in tx.run("MATCH (claim:Claim)-->(argument:ArgGroup)<--(premis) "
                                 "WHERE ID(claim) = {id} "
                                 "RETURN arg", premis=premis):
                print("hi")


def next_claim_to_propagate():
    print("get next claim to propagate")

def next_argument_to_propagate():
    print("get next argument to propagate")


def calculate_claim_state_from_arguments():
    print("calculate claim state from arguments")

def calculate_argument_state_from_claims():
    print("calculate state from argument")