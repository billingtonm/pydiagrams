#! python3

# Example of using the "Together" grouping

from pydiagrams.Component import ComponentContext as Context

# Select from one of these Helpers (PUML recommended)
# from pydiagrams.helpers.Graphviz import Helper
from pydiagrams.helpers.PUML     import Helper

# Setup a Component diagram called c
with Context(Helper) as x:
    C=x.Component

    a=C('A')

    # Two items that should occur together
    with x.Together():
        b=C('B')
        c=C('C')

    with x.Together():
        d=C('D')
        e=C('E')
    
    f=C('F')
    g=C('G')

    a >> b >> c >> d >> f

    c >> f >> g

    a >> f 