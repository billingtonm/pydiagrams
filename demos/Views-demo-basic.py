from pydiagrams.Views  import ViewContext

from pydiagrams.helpers.Graphviz import Helper
#from pydiagrams.helpers.PUML import Helper
from pydiagrams.helpers.constants import *

with ViewContext(Helper, label="Basic Example") as d:

    # Create some Nodes
    t = d.Table('Table')
    v = d.View('View')
    i = d.Integration('Integration')

    # Create an 'edge' from Table to View
    v >> t

    # Use "%" to specify a label for the edge
    i >> t % "Writes to"
    