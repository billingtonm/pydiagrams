# View Data Source diagram

# Standard python libraries
from contextlib import contextmanager #required for the cond function

# Local python libraries
import pydiagrams.Diagram as diagram

##########################################################################
# Item Classes
class DatabaseObjectItem(diagram.Item):
    def __init__(self, label, shape, **attrs):
        attrs.update({'shape':shape})
        diagram.Item.__init__(self, label, **attrs)

        # Stores the objects id's that SEND DATA to this instance
        # eg: if this were a view, the sources would be the tables/views th
        self.sources = []
        
    def add_source(self, source_item):
        #print 'add_source "{}" << "{}"'.format(self.Label,source_item.Label)
        assert isinstance(source_item, DatabaseObjectItem), "source_item is not a DatabaseObjectItem"
        self.sources.append(source_item)
        source_item.link(self)  # Create a link from the source_item to this


    # <<  : Set sources for this item
    def __lshift__(self, i2):
        if type(i2) == list:
            for i in i2:
                self.add_source(i)
        elif isinstance(i2, DatabaseObjectItem):
            self.add_source(i2)
        else:
            raise ValueError

# ========================================================
class ViewDiagram(diagram.DiagramBase):
    nodeTypes = {
        'Table'         :   'Table',
        'View'          :   'parallelogram',
        'Package'       :   'invhouse',
        'File'          :   'folder',
        'Integration'   :   'invtrapezium',
        'System'        :   'ellipse',
        'Task'          :   'cds'
    }

    def __init__(self, helper, filename=None, label=None, **attrs):
        diagram.DiagramBase.__init__(self, helper, filename, label, **attrs)
           
def make_method(shape):
    def make_item(self, label, **attrs):
        return self.add_item(DatabaseObjectItem(label, shape, **attrs))
    return make_item

# Dynamically create methods in ViewDiagram that create Item
for (method, shape) in list(ViewDiagram.nodeTypes.items()):
    setattr(ViewDiagram, method, make_method(method))            

# ========================================================
class ViewContext(diagram.Context):
    def __init__(self, helper, filename=None, **attrs):
        self.diagram = ViewDiagram(helper, filename, **attrs)

# ========================================================
class Items(diagram.Items):
    def __init__(self, *items):
        super(Items, self).__init__(*items)