# The Python Analyzer

Will run propagation updates through the db & create analytics data. (these may be split, we'll see!)  

P.S. I have no idea what I'm doing.

---

 - install python 
 - install the [python neo4j bolt driver](http://neo4j.com/docs/api/python-driver/current/) `pip install neo4j-driver` 

 ---

Full propagation can come later if at all.  (it'd just be looping through axioms / roots however we defined those)

Some ideas for propagation:

 - Marking propagation with propagation IDs: Generate an ID for each propagation run which is added to each claim/argument (they'll have a propagation ID array). Run the propagation but terminate a path whenever the current propagation ID is found.
 - Create a propagation node: for each claim/argument that is processed, create a link between it and the propagation node. Use to terminate propagation paths. This has the advantage of not bloating claim/argument nodes with a propagation array and also makes it easy to find out how much impact a claim / argument update had.
 - Hold an array of claim/argument IDs that have been processed in memory, check against it for propagation path termination. This should probably be the path to start with, when we get to a scale at which this becomes a problem, we'll hopefully have thought up something better.

Going with the last idea:

Now walk the tree. Do the smallest ids first
While doing so, hold a few things in memory:
`propagation-termination`: a list of claim/argument ids that have been updated in this propagation.
`path-pointer`: an id of the  

Whenever something is added / updated, this gets passed those things that changed then runs the propagation from there.

### Propagate from a claim
1. Add this claim to `propagation-termination`.
2. **Get** all the arguments this claim is used in.
3. For each argument: *calculate the new probability/state*.
4. Select the argument with the smallest ID value that isn't already in `propagation-termination`

### Propagate from an argument
1. Add the ID of this argument to `propagation-termination`. 
2. **Get** all the claims that use this argument.
3. For each claim  *calculate the new probability/state*.
4. Select the claim with the smallest ID value that isn't already in `propagation-termination`

### Step over from a claim (we're on a claim which is used in no arguments)
1. **Get** all the arguments used by this claim
2. Filter out the arguments that are not in `propagation-termination` - assuming we end up with only one.
3. **Get** all the claims that use this argument.
4. Select the claim with the smallest ID value (that isn't already in `propagation-termination`), it should already have been updated (now go up again unless there are no claims left in which case, step over from an argument)

### Step over from an argument (we're on an argument and have updated all the claims that use it)
1. **Get** all the claims used in this argument.
2. Filter out the claims that are not in `propagation termination` - assuming we end up with only one.
3. **Get** all the arguments this claim is used in.
4. Select the argument with the smallest ID value (that isn't already in `propagation-termination`), it should already have been updated. Now go up from here.

Had a think through: if there's a cycle we should be ok going up. But stepping over might become an infinitie issue. So how do we detect a cycle?