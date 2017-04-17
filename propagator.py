
import localconfig
from neo4j.v1 import GraphDatabase, basic_auth

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=(localconfig.DBUSERNAME, localconfig.DBPASSWORD))

propagation_terminator = [] # a list of claim/argument ids that have been updated in this propagation - so we don't update them twice / repeatedly


def print_claim_by_id(id):
    with driver.session() as session:
        with session.begin_transaction() as tx:
            for record in tx.run("MATCH (arg)-[]->(claim:Claim) "
                                 "WHERE ID(claim) = {id} "
                                 "RETURN claim.body", id=id):
                print(record["claim.body"])

print_claim_by_id(25)

def propagate_from_a_claim(id):
    """Beginning with a claim, propagate state updates upwards in the graph"""
    propagation_terminator.append(id) # save a reference to this claim
    # get all the arguments this claim is used in 
    argsUsingThisClaim = get_arguments_using_claim(id)
    print(argsUsingThisClaim)


def get_arguments_using_claim(claimId):
    """Takes a claim ID and returns a list of argument tuples (id, state, [(premisState,)]) that use that claim"""
    with driver.session() as session:
        with session.begin_transaction() as db_transaction:
            for record in db_transaction.run("MATCH (claim:Claim)-[:USED_IN]->(argument:ArgGroup) "
                                 "WHERE ID(claim) = {claimId} "
                                 "RETURN argument", claimId=claimId):
    return 1

def next_claim_to_propagate():
    print("get next claim to propagate")

def next_argument_to_propagate():
    print("get next argument to propagate")


def calculate_claim_state_from_arguments():
    print("calculate claim state from arguments")

def calculate_argument_state_from_claims():
    print("calculate state from argument")