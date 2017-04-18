
import sys
import localconfig
from neo4j.v1 import GraphDatabase, basic_auth

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=basic_auth(localconfig.DBUSERNAME, localconfig.DBPASSWORD))

propagation_terminator = [] # a list of claim/argument ids that have been updated in this propagation - so we don't update them twice / repeatedly


def propagate_from_a_claim(id):
    """Beginning with a claim, propagate state updates upwards in the graph"""
     # save a reference to this claim
    propagation_terminator.append(id)
    
    # get all the arguments this claim is used in 
    argsUsingThisClaim = get_arguments_using_claim(id)

    # calculate the new states for each argument
    for arg in argsUsingThisClaim:
        newArgState = calculate_argument_state([50,50])
        print(newArgState)
    
    # select the argument with the smallest id that's not in the propagation_terminator then pass it to propagate_from_an_argument


def get_arguments_using_claim(claimId):
    """Takes a claim ID and returns a list of argument tuples (argumentId, argumentState, [(premisState,)]) that use that claim"""
    returnArgs = []
    session = driver.session()
    neoArgs = session.run("MATCH (claim:Claim)-[:USED_IN]->(argument:ArgGroup) "
                          "WHERE ID(claim) = {claimId} "
                          "OPTIONAL MATCH (premis:Claim)-->(argument) "
                          "WITH argument, {id: ID(premis), state: premis.state} AS premises "
                          "RETURN {id: ID(argument), state: argument.state, premises: COLLECT(premises)} AS arguments ", 
                          claimId = int(claimId))
    for arg in neoArgs:
        print(arg.items())
        returnArgs.append(('argumentId',25,[50,50]))
    
    session.close()
    return returnArgs

def calculate_argument_state(premisStates):
    """Takes a list of states and calculates the argument state, which it then returns"""
    return 50


# below are probably going to go, they're just placeholders anyway
def next_claim_to_propagate():
    print("get next claim to propagate")

def next_argument_to_propagate():
    print("get next argument to propagate")


def calculate_claim_state_from_arguments():
    print("calculate claim state from arguments")

def calculate_argument_state_from_claims():
    print("calculate state from argument")


#basic command line arguments
def main():
    if len(sys.argv) != 3:
        print('usage: ./propagator.py { --claim | --arg } nodeID')
        sys.exit(1)
    
    nodeType = sys.argv[1]
    nodeId = sys.argv[2]

    if nodeType == '--claim':
        propagate_from_a_claim(nodeId)
    elif nodeType == '--arg':
        print('TODO: start from argument')
    else:
        print('unknown option: ' + nodeType)
        sys.exit(1)

if __name__ == "__main__":
    main()