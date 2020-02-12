from pydiagrams.Views  import ViewContext

from pydiagrams.helpers.Graphviz import Helper
#from pydiagrams.helpers.PUML import Helper
from pydiagrams.helpers.constants import *

with ViewContext(Helper, label="Sources") as d:

    # Create some Nodes
    d.node_attrs = {fillcolor:color4} # Specify a color for all Tables
    t1 = d.Table('Table 1')
    t2 = d.Table('Table 2')
    t4 = d.Table('Table 4')
    t3 = d.Table('Table 3')
    t5 = d.Table('Table 5')
 
    d.node_attrs = {fillcolor:color3} # Specify a color for all Views
    v1 = d.View('View 1')
    v2 = d.View('View 2')
    v3 = d.View('View 3')

    # A << B indicates that item A is sourced from B
    # it's useful for items like Views that get data from numerous Tables
    v1 << t1

    # Can specify that a view comes from multiple Tables by using []
    # v2 gets data from t2, t3, t4
    v2 << [t2, t3, t4]

    v3 << [t3, t4, t5]

    # "View 4" is created 'anonymously'. 
    # This is useful for when you don't need to refer to the Node again...
    d.View('View 4', fillcolor=color1) << [v1, v2, v3]

    # ... but if you must refer to it again, you can via it's label
    # As "View 4" was created under item 'd', we can do d[label] to find it
    d.Task('Integration Task', fillcolor=grey1) << d['View 4']
