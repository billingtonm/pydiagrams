import pydiagrams.baseItems as baseItems
from pydiagrams.helpers.constants import *

import datetime
import sys
import os.path
from contextlib import contextmanager #required for the DiagramBase.subgraph

from pydiagrams.baseItems import logged

class Item(baseItems.BaseItem):
    cls = "Diagram.Item"
    def __init__(self, label, **attrs):
        baseItems.BaseItem.__init__(self, label, **attrs)
        self._links = []
        self.is_group = False

    @property
    def Id(self):
        return self.id or 'n' + str(hash(self))

    @Id.setter
    def Id(self, value):
        self.id = value        

    @property
    def Label(self):
        return self.label or self.Id.replace('_', ' ').title()

    @Label.setter
    def Label(self, value):
        self.label = value        

    @property
    def Note(self):
        return self.attrs.get('note')

    @Note.setter
    def Note(self, value):
        self.attrs['note'] = value

    @property
    def Links(self):
        """ Return the set of items this item is linked to """
        return self._links

    @logged(cls)
    def __str__(self):
        # Call the helper's node render function
        return self.Helper.node(self.Id, self.Label, **self.attrs)

    def link(self, i2, label=None, **attrs):
        #print ('link: {} -> {}'.format(self.Id, i2.Id))
        """ Create a link between this Item and i2 """
        edge_attrs = attrs
        fromItem = self

        #if isinstance(self, DiagramBase):
        if self.is_group:
            edge_attrs.update(ltail='cluster_'+self.id )
            fromItem = self.get_first_item()

        # If the node is required to go to a subgraph, then
        # need to direct to the first item and set the special Graphviz attributes
        # TODO: Use the helper instead        
        if i2.is_group:
            i2 = i2.get_first_item()
            edge_attrs.update(lhead='cluster_' + i2.Diagram.id) # set the target for the cluster

        d = self.Diagram
        assert d,"Uhoh no diagram for {}".format(self.__repr__())

        #print(f'{d=} ')
        #print(f'{d.level=}')
        #print(f'{i2.Diagram=}')
        while (d != i2.Diagram) and (d.level > 0):
            d = d.parent

        e=Edge(fromItem, i2, label, **attrs)
        d.add_item(e)

        # record the object being linked to
        self._links.append(i2)

        return i2

    def link_edge(self, i2, dir=None):
        def do_link(i2):
            if isinstance(i2, baseItems.BaseItem):
                return self.link(i2, dir=dir)
            elif isinstance(i2, ItemEdge):
                return self.link(i2.item, dir=dir, **i2.attrs)        
            else:
                raise ValueError('type(i2)=' + str(type(i2)))
        if type(i2) == list or isinstance(i2, Items):
            #print(f'Do link {self=} {i2=}')
            #a= list(map(do_link, i2))
            a = [do_link(i) for i in i2]
            return a[0]
        else:
            return do_link(i2)


    def __rshift__(self, i2):
        """ Override the >> operator to mean to add an edge between this item and the i2 """
        return self.link_edge(i2)

    def __mod__(self, s):
        """ Override the % operator to add attributes to an edge. Used with the >> operator
            eg: Add a label to an edge:
                n1 >> n2 % "my label"
            eg: Add a label and color to an edge:
                n1 >> n2 % {label:'my label', color:'blue'}
        """
        if type(s) == str:
            return ItemEdge(item=self, label=s)
        elif type(s) == dict:
            return ItemEdge(item=self, attrs=s) 
        else:
            raise ValueError                                    

class DiagramBase(Item):
    cls = 'Diagram.DiagramBase'
    @logged(cls)
    def __init__(self, helper, filename=None, label=None, **attrs):
        Item.__init__(self, label=label, **attrs)
        self.id = 'g'
        self.collection = baseItems.BaseItemCollection(self)

        self.parent = None
        self.helper = helper

        # The full filename of the user's script
        self._user_module_file = os.path.realpath(sys.modules['__main__'].__file__ )

        self._filename = filename
        self._pathname = None

        self.level = 0

        self.edge_attrs = {}
        self.node_attrs = {}

        self.passthrough_index = 0
        self.is_group = True

    # Property functions to deal with the file naming
    @property 
    def FileName(self):
        if self._filename:
            fn = self._filename 
        else:
            fn = os.path.basename(self._user_module_file).replace('.py', '') 
        return fn + '.' + self.helper.extension

    @FileName.setter
    def FileName(self, value):
        self._filename = value

    @property
    def PathName(self):
        if self._pathname:
            return self._pathname
        else:
            return os.path.dirname(self._user_module_file)

    @PathName.setter
    def PathName(self, value):
        self._pathname = value

    # Full file name (path + file + extension) of the file to be written
    @property 
    def OutputFileName(self):
        return os.path.join(self.PathName, self.FileName)

    def add_item(self, item):
        # Determine base attributes of this item
        if isinstance(item, Edge):
            base_attrs = item.fromItem.Diagram.edge_attrs.copy()
            # Remove the label key
            #if base_attrs.has_key(label):
            #    base_attrs.pop(label)
        elif isinstance(item, Item):
            base_attrs = self.node_attrs.copy()
        else:
            base_attrs = {}


        ia = item.attrs.copy()
        item.attrs = base_attrs
        item.attrs.update(ia)

        if 'label' in item.__dict__:
            if not item.label:
                item.label = base_attrs.get(label)

        return self.collection.add_item(item)

    @logged(cls)
    def __str__(self):
        if self.parent:
            return \
                self.helper.startSubdiagram(self.id, self.label, **self.attrs) + '\n' \
                + '\n'.join([ str(v) for v in list(self.collection.values()) ]) \
                + self.helper.endSubdiagram(self.id, self.label, **self.attrs) + '\n' 
        else:
            return 'ViewDiagram({id}, "{label}")'.format(**self.__dict__)

    @logged(cls)
    def render(self):
        # This is the main diagram
        yield self.helper.comment('Generated by pydiagrams @ {}').format(datetime.datetime.now())
        yield self.helper.startDiagram(self.FileName, self.label, **self.attrs) + '\n'

        for v in list(self.collection.values()):
            # print( 'Rendering',v.id , 'label=',v.label or '')
            yield str(v) + '\n'

        yield self.helper.endDiagram() + '\n'

    @logged(cls)
    def dump(self):
        if self._filename =='stdout': # Special mode for writing output to stdout
            for l in self.render():
                print(l)
        else:
            output_filename = self.OutputFileName
            print('Creating...: {}'.format(output_filename))
            with open(output_filename, 'w') as f:
                f.writelines(self.render())
                
    def __getitem__(self, label):
        """ Returns an Item with a label """
        for v in list(self.collection.values()):
            if v.label == label:
                return v
        raise ValueError # notfound

    def get_first_item(self):
        for i in list(self.collection.values()):
            if not isinstance(i, DiagramBase):
                return i

    def passthrough(self, line):
        """ Adds a line of native code to the output """
        return self.add_item(PassthroughItem(line))

    @contextmanager
    def Cluster(self, label, **attrs):
        #attrs.update({'label':label})
        sub = self.__class__(helper=self.helper, label=label, **attrs)

        # Set the attributes for the sub diagram
        sub.parent = self
        sub.level = self.level + 1
        sub.node_attrs = self.node_attrs.copy()
        sub.edge_attrs = self.edge_attrs.copy()
        sub.id = hash(self)

        self.add_item(sub)

        yield sub

        # on exit, set the ids
        sub.collection.set_ids()

    # Return all the items in the diagram. recurses into subdiagrams
    def all(self, name_contains=None):
        items = []
        self.collection.set_ids()
        for v in self.collection.values():
            if isinstance(v, DiagramBase) and v.is_group:
                for v2 in v.all(name_contains):
                    items.append(v2)
            elif isinstance(v, Item):
                if name_contains:
                    if name_contains in v.Id:
                        items.append(v)    
                else:
                    items.append(v)
        return Items(*items)

class Edge(baseItems.BaseItem):
    def __init__(self, fromItem, toItem, label, **attrs):
        baseItems.BaseItem.__init__(self, label, **attrs)
        (self.fromItem, self.toItem) = (fromItem, toItem)

    def __str__(self):
        a=self.attrs.copy()
        if label in a:
            a.pop(label)

        # Call the helper's edge render function
        return self.Helper.edge(self.fromItem.Id, self.toItem.Id, label=self.label, **a)

class PassthroughItem(baseItems.BaseItem):
    def __init__(self, line):
        baseItems.BaseItem.__init__(self, label=None)
        self.line = line

    def __str__(self):
        # Call the helper's node render function
        return self.line


class ItemEdge(object):
    """ Class that is returned as a result of: 
        - Item() % str
        - Item() % dict
    """
    def __init__(self, item, label="", attrs={}):
        self.item = item
        self.attrs = attrs
        if label != "":
            self.attrs.update(label=label)

class Items(object):
    """ Container class for Item. Enables operations on a set of Items
    """
    def __init__(self, *items):
        self.itemList = []
        for i in items:
            assert isinstance(i, Item), '<{}> is not an instance of a Item'.format(i)
            self.itemList.append(i)


    def __getitem__(self, index):
        return self.itemList[index]

    def __iter__(self):
        return iter(self.itemList) 

    # Allow a set of Items to be linked to another item
    def __rshift__(self, i2):
        if isinstance(i2, Item) or isinstance(i2, ItemEdge):
            for i in self.itemList:
                i.link_edge(i2)
        else:
            raise ValueError('type of i2 is {}'.format(type(i2)))

class Stack:
    def __init__(self):
        self._stack = []

    def __iter__(self):
        return iter(self._stack)

    @logged('Diagram.Stack')
    def push(self, e):
        # print(f'\tIn push: {self._stack=}')
        self._stack.append(e)

    def pop(self):
        return self._stack.pop()

    def count(self):
        return len(self._stack)

    def current(self):
        return self._stack[-1]

class Context(object):
    """ Class to manage the context of a Diagram.
        Allows the use of the 'with' syntax to automatically Start and End the flowchart """
    def __init__(self, diagram=None):
        self._groups = Stack()
        self.diagram = diagram



    def __enter__(self):
        return self.diagram

    def __exit__(self, *args):
        self.diagram.collection.set_ids()
        # print( 'About to call render()')
        self.diagram.render()
        self.diagram.dump()         

        self.diagram.helper.generate_diagram(self.diagram.OutputFileName)
        