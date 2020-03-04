from pydiagrams.Flowchart import FlowchartContext

#from pydiagrams.helpers.Blockdiag import Helper
#from pydiagrams.helpers.PUML import Helper
from pydiagrams.helpers.Graphviz import Helper

# include constants
#from pydiagrams.helpers.constants import *

# Start the diagram, define the output file
with FlowchartContext(Helper) as f:
    # Define styles

    # Define the nodes
    start = f.Start()
    decision = f.Decision()
    process  = f.Process()
    end = f.End()

    # Define the flows
    start >> decision

    # Decisions
    decision.Branch(true = process, false=end)

    process >> decision