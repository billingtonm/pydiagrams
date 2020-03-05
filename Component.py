# Component diagram

# Standard python libraries
from contextlib import contextmanager #required for the cond function

# Local python libraries
#from Diagram import DiagramBase, Item, Context
import pydiagrams.Diagram as Diagram
from pydiagrams.helpers.PUML import Helper

from .helpers.constants import *
from pydiagrams.baseItems import logged

##########################################################################
# Constants

# component shape keys
Component = 'Component'
Interface = 'Interface'


# group shapes
Cloud = 'Cloud'
Database = 'Database'
Folder = 'Folder'
Frame = 'Frame'
Node = 'Node'
Package = 'Package'
Rectangle = 'Rectangle'

##########################################################################
# Item Classes

class ComponentDiagramItem(Diagram.Item):
    """ Base class for all Items in a component Diagram """
    def __init__(self, label, shape, **attrs):
        Diagram.Item.__init__(self, label, **attrs)
        self.attrs['shape'] = shape

    def __hash__(self):
        return abs(hash(self.label))

    def __str__(self):
        attrs = self.attrs.copy()
        attrs['groups'] = [g.id for g in self.Collections]
        attrs['links'] = [g.id for g in self.Links]
        # Call the helper's node render function
        return self.Helper.node(self.Id, self.Label, **attrs)

    # Override operators

    # >>  ==  vertical link
    def __rshift__(self, i2):
        """ Override the >> operator to mean to add an edge between this item and the i2 """
        return self.link_edge(i2, 'vertical')

    def __lshift__(self, i2):
        """ Override the << operator to mean to add an edge between i2 this item """
        def link(source, dest):
            return source.link_edge(dest, 'up')

        # if type(i2) == list:
        # Attempt to iterate through i2
        try:
            l=[link(i, self) for i in i2]
            return l[0]
        except TypeError:
            return link(i2, self)

    # ^  == up link
    def __xor__(self, i2):
        """ Override the ^ operator to mean to add an 'up' edge """
        return self.link_edge(i2, 'up')

    # | == down link
    def __or__(self, i2):
        """ Override the ^ operator to mean to add an 'up' edge """
        return self.link_edge(i2, 'down')

    # >= == right link
    def __ge__(self, i2):
        """ Override the >= operator to mean to add an 'right' edge """
        return self.link_edge(i2, 'right')

    # <= == left link
    def __le__(self, i2):
        """ Override the <= operator to mean to add an 'left' edge """
        return self.link_edge(i2, 'left')

    # -  == horizontal line
    def __sub__(self, i2):
        """ Override the - operator to add a horizontal line """
        return self.link_edge(i2, 'hline')

    # =  == vertical line
    #def __eq__(self, i2):
    #    return self.link_edge(i2, 'vline')

    # >>=  == vertical dotted arrow
    def __irshift__(self, i2):
        return self.link_edge(i2,'vdotted')



# _groups = Stack()

##########################################################################
# Diagram Classes
class ComponentDiagram(Diagram.DiagramBase):
    def __init__(self, helper, filename=None, context=None, **attrs):
        Diagram.DiagramBase.__init__(self, helper, filename, **attrs)
        self._context = context
        if self._context._groups.count() == 0:
            # print('Component.ComponentDiagram.__init__: Initial push:')
            self._context._groups.push(self)

    def inherit(self, attrs):
        a = self.attrs.copy()

        for k in ['shape', 'fillcolor']:
            if k in a:
                a.pop(k)

        a.update(attrs)
        return a

    def Group(self, shape, label, **attrs):
        g=ComponentSubDiagram(parent=self, id=None, shape=shape, label=label, **self.inherit(attrs))
        #self.collection.add_item(g)
        self._context._groups.current().collection.add_item(g)
        return g
    
    def add_new_item(self, shape, label, **kwargs):
        #kwargs.update({'shape':shape})
        #return self.collection.add_new_item(Item, label, **kwargs)
        i = ComponentDiagramItem(label, shape, **self.inherit(kwargs))
        #print('Adding <{}> to <{}>'.format(label,  self._context._groups.current().label))
        return self._context._groups.current().collection.add_item(i)
        #return self.collection.add_item(i)

    # Item functions: Component, Interface, Actor
    def Component(self, label, **attrs):
        return self.add_new_item(Component, label, **attrs)

    def Interface(self, label, **attrs):
        return self.add_new_item(Interface, label, **attrs)

    def Actor(self, label, **attrs):
        return self.add_new_item('Actor', label, **attrs)

    # Group functions: Cloud, Database, Folder, Frame, Node, Package
    def Cloud(self, label=None, **attrs):
        return self.Group(Cloud, label, **attrs)

    def Database(self, label=None, **attrs):
        return self.Group(Database, label, **attrs)

    def Folder(self, label=None, **attrs):
        return self.Group(Folder, label, **attrs)

    def Frame(self, label=None, **attrs):
        return self.Group(Frame, label, **attrs)

    def Node(self, label=None, **attrs):
        return self.Group(Node, label, **attrs)

    def Package(self, label=None, **attrs):
        return self.Group(Package, label, **attrs)

    def Rectangle(self, label=None, **attrs):
        return self.Group(Rectangle, label, **attrs)

    def Together(self):
        g=TogetherGroup(parent=self)
        self._context._groups.current().collection.add_item(g)
        return g

#-------------------------------------------------------------------------
class ComponentSubDiagram(ComponentDiagram, ComponentDiagramItem):
    def __init__(self, parent, id, shape, label, **attrs):
        ComponentDiagram.__init__(self, helper=parent.helper, context=parent._context, **attrs)
        ComponentDiagramItem.__init__(self, label, shape, **attrs)
        self.attrs['shape'] = shape

        self.parent = parent
        self.id = id
        self.level = self.parent.level + 1

        self.node_attrs = parent.node_attrs.copy()
        self.edge_attrs = parent.edge_attrs.copy()

        # Denotes that this is to be treated as a group
        self.is_group = False

    # Renders this diagram
    def __str__(self):
        if self.is_group:
            a = self.helper.startSubdiagram(self.id, self.label, **self.attrs)
            a += '\n'.join([str(v) for v in list(self.collection.values())])
            a += self.helper.endSubdiagram(self.id, self.label, **self.attrs)
            return a
        else:
            return ComponentDiagramItem.__str__(self)

    def __enter__(self):
        self.is_group = True
        #print(f'Entering <{self.id}>, <{self.label}>')
        self._context._groups.push(self)
        #print('push done')
        return self

    def __exit__(self, *args):
        if self.is_group:
            g= self._context._groups.pop()
            #print(f'Exiting <{g.id}>, <{g.label}>')

    def all_except(self, *args, **kwargs):
        """ Use: 
                all_except(shape=TypeName)  to exclude by type 
                all_except(a,b,c) to exclude items a,b,c
        """
        ret = []
        k_shape = 'shape'
        shape = kwargs.get(k_shape)
        for v in self.all():
            if not v in args:
                argcheck=True
            else:
                argcheck=False

            typecheck=True
            if shape:
                if v.attrs[k_shape] == shape:
                    typecheck=False

            if argcheck and typecheck:
                ret.append(v)

        return Diagram.Items(*ret)

class TogetherGroup(ComponentDiagram):
    def __init__(self, parent):
        ComponentDiagram.__init__(self, helper=parent.helper, context=parent._context)
        self.parent = parent
        self.level = self.parent.level + 1

    # Renders this diagram
    def __str__(self):
        a = self.helper.startTogether()
        a += '\n'.join([str(v) for v in list(self.collection.values())])
        a += self.helper.endTogether()
        return a

    def __enter__(self):
        self._context._groups.push(self)
        return self
    
    def __exit__(self, *args):
        g= self._context._groups.pop()

##########################################################################
# Context Classes
class ComponentContextPUML(Diagram.Context):
    def __init__(self, filename=None):
        print('Generating!:',filename)
        self.diagram = ComponentDiagram(Helper, filename)

class ComponentContext(Diagram.Context):
    def __init__(self, helper, filename=None):
        super().__init__()
        print (f'\tGenerating Component Diagram ...: {filename}')
        self.diagram=ComponentDiagram(helper, filename, context=self)
