#! python3

from pydiagrams.Component import ComponentContext, _groups

# Select from one of these Helpers (PUML recommended)
#from pydiagrams.helpers.Graphviz import Helper
#from pydiagrams.helpers.Blockdiag     import Helper
from pydiagrams.helpers.arcentry     import Helper

# Setup a Component diagram called c
# Demonstrates use of Components, Interface and Notes
with ComponentContext(Helper, 'Component-demo-basic') as c:
    fc = c.Component('First Component', note='A note can also\nbe on several lines')
    c.Interface('Data Access') - fc
    fc >>= c.Interface('HTTP', note='Web Service only') % 'Use'

""" 
@startuml

package "Some Group" {
  HTTP - [First Component]
  [Another Component]
}
 
node "Other Groups" {
  FTP - [Second Component]
  [First Component] --> FTP
} 

cloud {
  [Example 1]
}


database "MySql" {
  folder "This is my folder" {
	[Folder 3]
  }
  frame "Foo" {
	[Frame 4]
  }
}


[Another Component] --> [Example 1]
[Example 1] --> [Folder 3]
[Folder 3] --> [Frame 4]

@enduml
"""

with ComponentContext(Helper, 'Component-demo-grouping') as g:
    with g.Package("Some Group") as g1:
        g.Interface('HTTP') - g.Component('First Component')
        ac = g.Component('Another Component')

    with g.Node('Other Groups') as g2:
        g.Interface('FTP') - g.Component('Second Component')
        # Access components by looking for their label
        # rather than accessing via a  variable
        g1['First Component'] >> g2['FTP']

    with g.Cloud() as g3:
        ex1 = g.Component('Example 1')

    with g.Database('MySql') as db:
        with g.Folder('This is my folder') as fg1:
            f3 = g.Component('Folder 3')
        with g.Frame('Foo') as fg2:
            f4 = g.Component('Frame 4')

    ac >> g3['Example 1']
    ex1 >> f3 >> f4 #Can chain links together

# ---------------------------------------------------------
# It is also possible to change arrow direction by adding 
# left, right, up or down keywords inside the arrow
""" 
@startuml
[Component] -left-> left 
[Component] -right-> right 
[Component] -up-> up
[Component] -down-> down
@enduml
"""

with ComponentContext(Helper, 'Component-demo-arrowdir') as a:
    comp = a.Component('Component')
    i=a.Interface # define a shortcut for defining interfaces
    comp <= i('left')
    comp >= i('right')
    comp ^ i('up')
    comp | i('down')


# Test that an item can be either a group or a node

with ComponentContext(Helper, 'Component-demo-groupnode') as b:
    n1 = b.Node('Node')

    # Use a node as a Group
    with b.Node('Group Node') as n2:
        c1 = b.Component('component')
    
    n1 >> c1
    
    with b.Database('RMS') as db:
        rs = b.Rectangle('rag_skus')

    c1 >> rs

