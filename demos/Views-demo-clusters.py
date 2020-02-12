######################################################################
# Standard Imports
from pydiagrams.Views  import ViewContext
from pydiagrams.helpers.Graphviz import Helper
from pydiagrams.helpers.constants import *

#####################################################################
# Start Diagram
with ViewContext(Helper, label="Cluster Demo") as d:

    # Create a cluster containing a Table
    with d.Cluster("Cluster 1", fillcolor=color1) as c1:              
        # Create a Table node in c
        t1 = c1.Table('Table #1')                 

    # Create cluster containing a table
    with d.Cluster("Cluster 2", fillcolor=color2) as c2:              
        # Create a Table node in c2
        t2 = c2.Table('Table #2')                 


    # Clusters can be nested
    with d.Cluster('Cluster 3', fillcolor=color3) as c3:
        with c3.Cluster('Cluster 3.1', fillcolor=color4) as c31:  # created with reference to c3
            t31 = c31.Table('Table #3.1')

        t3 = c3.Table('Table #3')

    # Arrow from Table #2 to Table #1
    t1 >> t2 % "t1 >> t2"

    # Arrow from t3 to t31
    t3 >> t31 % "t3 >> t31"

    # Can link clusters
    c2 >> c31 % "c2 >> c31"

    t4 = d.Table("Table #4")

    # Can link clusters to items
    c1 >> t4 % "c1 >> t4"

    # Can link items to clusers
    t4 >> c3 % "t4 >> c3"