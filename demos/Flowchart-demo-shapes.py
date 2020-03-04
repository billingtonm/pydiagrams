from pydiagrams.Flowchart import FlowchartContext

#from pydiagrams.helpers.Blockdiag import Helper
from pydiagrams.helpers.PUML import Helper
# from pydiagrams.helpers.Graphviz import Helper

# include constants
#from pydiagrams.helpers.constants import *

# Start the diagram
with FlowchartContext(Helper) as f:
    # Define styles

    # Define the nodes
    start = f.Start()
    decision = f.Decision()
    process  = f.Process()
    io = f.IO()
    PredefinedProcess = f.PredefinedProcess()
    OnPageConnector = f.OnPageConnector()
    OffPageConnector = f.OffPageConnector()
    Database = f.Database()
    Document = f.Document()
    Manual_Operation = f.ManualOperation()
    Manual_Input = f.ManualInput()
    Preparation = f.Preparation()
    end = f.End()

    # Define the flows
    start >> OnPageConnector >> decision

    # Decisions
    decision.Branch(true = process, false=io)

    process >> Manual_Operation >> Manual_Input >> Document
    io >> PredefinedProcess >> Preparation >> Database 

    Database >> OffPageConnector
    Document >> OffPageConnector

    OffPageConnector >> end

    OnPageConnector.Note = 'This is an OnPageConnector'
