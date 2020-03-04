# Demonstration of using the my python library 
# for doing flowcharts from python
from pydiagrams.Flowchart import FlowchartContext

#from pydiagrams.helpers.Blockdiag import Helper
# from pydiagrams.helpers.PUML import Helper
from pydiagrams.helpers.Graphviz import Helper

# include constants
from pydiagrams.helpers.constants import *

# Start the diagram, define the output file
with FlowchartContext(Helper) as f:

    # Define some styles
    start_style = {fillcolor:color5}
    end_style = {fillcolor:color3}
    decision_style = {fillcolor:color11}

    # Define the nodes
    problem = f.Start("Lamp doesn't work", **start_style)

    if_plugged_in      = f.Decision('Lamp plugged in?', **decision_style)
    if_bulb_burned_out = f.Decision('Bulb burned out?', **decision_style)

    plug_in_lamp = f.End(**end_style)
    replace_bulb = f.End(**end_style)
    repair_lamp = f.End(**end_style)

    # Flows
    problem >> if_plugged_in

    # setup branches for the Decisions
    if_plugged_in.Branch(Yes = if_bulb_burned_out, No = plug_in_lamp)
    if_bulb_burned_out.Branch(Yes = replace_bulb, No = repair_lamp)
