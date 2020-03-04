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
    start = f.Start('Start')
    input = f.IO('Input N')
    modulo = f.Process('Remainder=N modulo 2')
    remainder_test = f.Decision('Remainder = 0 ?')
    even = f.Process('Answer = EVEN')
    odd = f.Process('Answer = ODD')
    output_answer = f.IO()
    end = f.End()

    # Define the flows
    start >> input >> modulo >> remainder_test

    remainder_test.Branch(
        Yes =  even, 
        No  = odd)

    even >> output_answer
    odd >> output_answer

    output_answer >> end
