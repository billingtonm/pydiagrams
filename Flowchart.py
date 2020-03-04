# Flowchart diagram

# Standard python libraries
from contextlib import contextmanager #required for the cond function

# Local python libraries
#from py import DiagramBase, Context, Item, PassthroughItem
import pydiagrams.Diagram as diagram
from pydiagrams.helpers.constants import *

def label_format(s):
    """ Converts an id into a label """
    return s.replace('_', ' ').title()

##########################################################################
# Item Classes

class FlowchartDiagramItem(diagram.Item):
    """ Base class for all Items in a Flowchart Diagram """
    def __init__(self, label, shape, **attrs):
        attrs.update({'shape':shape})
        diagram.Item.__init__(self, label, **attrs)
        self.nodeBranches = None

    def Branch(self, **branches):
        self.nodeBranches = branches
        for (label, target) in list(branches.items()):
            self.link(target, label=label_format(label))

class ActivityItem(FlowchartDiagramItem):
    def __init__(self, label, **attrs):
        attrs.setdefault(fillcolor, color1)
        FlowchartDiagramItem.__init__(self, label, shape='Rectangle', **attrs)

class ConditionItem(FlowchartDiagramItem):
    def __init__(self, label, **attrs):
        FlowchartDiagramItem.__init__(self, label, shape='Diamond', **attrs)

class FlowchartDiagram(diagram.DiagramBase):
    def __init__(self, helper, filename=None, **attrs):
        diagram.DiagramBase.__init__(self, helper, filename, **attrs)
        for s in ['Start', 'End', 'Terminal', 'Process', 'Decision', 'IO', 'PredefinedProcess', 'OnPageConnector', 'OffPageConnector', 'Database', 'Document', 'ManualOperation', 'ManualInput', 'Preparation']:
            setattr(self, s, self.__item__('FC_' + s))            

    def __item__(self, shape):
        """ Returns a function to add a new item """
        def add(label="", **attrs):
            return self.add_item(FlowchartDiagramItem(label, shape, **attrs))
        return add

    def Activity(self, label=None, **attrs):
        """ Returns an Activity Item """
        return self.add_item(ActivityItem(label, **attrs)) 

    def Condition(self, label, **attrs):
        return self.add_item(ConditionItem(label, **attrs))


class FlowchartContext(diagram.Context):
    def __init__(self, helper, filename=None):
        self.diagram = FlowchartDiagram(helper, filename)