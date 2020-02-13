# Demonstration of using the my python library 
# for doing flowcharts from python
from pydiagrams.Flowchart import FlowchartContext

#from pydiagrams.helpers.Blockdiag import Helper
from pydiagrams.helpers.PUML import Helper
# from pydiagrams.helpers.Graphviz import Helper


# Start the diagram, define the output file
with FlowchartContext(Helper) as f:
    # Define some Activity Nodes. 
    # These don't reqire labels, they are generated from the Id 
    application     = f.Activity()
    refactor        = f.Activity()
    container       = f.Activity()
    serverless      = f.Activity()
    virtual_machine = f.Activity('Custom label for VM')

    # Define the Condition Nodes, with labels
    if_serverless       = f.Condition('Can it be a Serverless function?')
    if_long_running     = f.Condition( "Is it a long running function")
    if_run_occasionally = f.Condition( "Does it run occasionally?")
    if_time_sensitive   = f.Condition( "Is it time sensitive?")
    if_10m              = f.Condition( ">10 million requests?")
    if_containers       = f.Condition( "Are Containers supported?")

    # Draw the links between Nodes 
    application >> if_serverless
    refactor >> application

    # Simpler syntax for branching
    # Syntax Option 1: 
    if_serverless.Branch(Yes = if_long_running, No =  if_containers)

    # Syntax Option 2 
    if_long_running.Branch(Yes = refactor, No = if_run_occasionally)


    if_run_occasionally.Branch(
        Yes = if_10m,
        No  = if_time_sensitive)

    if_10m.Branch(
        Yes =  if_containers,
        No =   serverless)

    if_time_sensitive.Branch(
        Yes = if_10m,
        No  = serverless)

    if_containers.Branch(
        Yes = container,
        No  = virtual_machine
    )

    # Pass graphviz code to align the serverless, vm and container nodes
    if Helper.name == 'Graphviz':
        f.passthrough('{rank=max; serverless container virtual_machine};')

