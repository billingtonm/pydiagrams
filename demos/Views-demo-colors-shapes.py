from pydiagrams.Views  import ViewContext

from pydiagrams.helpers.Graphviz import Helper
#from pydiagrams.helpers.PUML import Helper
from pydiagrams.helpers.constants import *

with ViewContext(Helper, label="Colours and Shapes") as d:
    # setting 'node_attrs' specifies default properties for all new Nodes
    # Graphviz supports fixed widths
    d.node_attrs = {'width':"2.0"}

    # View diagrams support different shapes
    t = d.Table('Table')
    v = d.View('View')
    i = d.Integration('Integration')
    p = d.Package('Package')
    f = d.File('File')
    s = d.System('System')
    k = d.Task('Task')

    # Colours can be set with 'fillcolor' attribute
    # For conveinance, pydiagrams supports the paired12 colour scheme
    # which can be specified by 'colorN' where 1 < N < 12
    tc = d.Table('color1',      fillcolor=color1)
    vc = d.View('color2',       fillcolor=color2)
    ic = d.Integration('color3', fillcolor=color3)
    pc = d.Package('color4', fillcolor=color4)
    fc = d.File('color5', fillcolor=color5)
    sc = d.System('color6', fillcolor=color6)
    kc = d.Task('color7', fillcolor=color7)

    tc2 = d.Table('color8',      fillcolor=color8)
    vc2 = d.View('color9',       fillcolor=color9)
    ic2 = d.Integration('color10', fillcolor=color10)
    pc2 = d.Package('color11', fillcolor=color11)
    fc2 = d.File('color12', fillcolor=color12)

    # pydiagrams also supports the grey6 colorscheme
    # which can be specified by 'greyN' where 1 <= N <- 6
    sg = d.System('grey1', fillcolor=grey1)
    kg = d.Task('grey2', fillcolor=grey2)
    tg = d.Table('grey3',      fillcolor=grey3)
    vg = d.View('grey4',       fillcolor=grey4)
    ig = d.Integration('grey5', fillcolor=grey5)
    pg = d.Package('grey6', fillcolor=grey6, fontcolor=white) #Also set fontcolor


    # setting the global attributes allows new edges to share common properties
    d.edge_attrs = {label:'With fillcolor'}
    # edges can be 'chained together'
    t >> tc >> tc2 >> tg 
    v >> vc >> vc2 >> vg
    i >> ic >> ic2 >> ig
    p >> pc >> pc2 >> pg
    f >> fc >> fc2
    s >> sc >> sg
    k >> kc >> kg

    
    