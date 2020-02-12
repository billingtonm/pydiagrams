from pydiagrams.helpers.constants import *
from pydiagrams.helpers import helper 

# Map of shapes
helper.shape = {

        #Flowchart/Component
        'Rectangle':'box',    
        'Diamond':'flowchart.condition',

        # Component
        'Cloud':'cloud',
        'Database':'flowchart.database',
        'Folder':'roundedbox',
        'Frame':'terminator',
        'Node':'flowchart.database',
        'Package':'flowchart.loopout',
        'Component':'box',
        'Interface':'minidiamond',

        # Views
        'Table'         :   'box',
        'View'          :   'input',
        'Package'       :   'flowchart.loopout',
        'File'          :   'roundedbox',
        'Integration'   :   'flowchart.loopin',
        'System'        :   'cloud',
        'Task'          :   'ellipse',

        #Architecture
        'Entity'        :   'box',
        'Module'        :   'roundedbox',
        'EntityGroup'   :   'database'
    }

helper.comment_format = "// {text}\n"


class Helper(helper.helper):
    """ 
    The Helper class stores the methods specific to a diagram language.
    It's passed to the FlowchartBase object to be used when rendering code
    """

    extension   = "diag"
    name = "Blockdiag"

    # Arrow directions aren't really supported by blockiag
    # http://blockdiag.com/en/blockdiag/examples.html#direction-of-edges
    arrows = {
         'vertical'   : '->',
         'horizontal' : '->',
         'right'    : '->',
         'left'     : '<-',
         'up'       : '->',
         'down'     : '->',
         'hline'    : '--',
         'vline'    : '--',
         'vdotted'  : '->'
        }

    theme = ''

    @staticmethod
    def render_attrs(label, attrs, enclosed=True):
        attrs.update({'label':label or ""})
        return \
            ('[' if enclosed else '') \
            + ', '.join(['{}="{}"'.format(k,v) for (k,v) in list(attrs.items())]) \
            + (']' if enclosed else '') \
            + ';' 

    @staticmethod
    def node(id, label, **kwargs):
        shape = 'shape'
        if shape in kwargs:
            kwargs[shape] = Helper.shape(kwargs[shape])

        if fontcolor in kwargs:
            kwargs['textcolor'] = kwargs.pop(fontcolor)

        if fillcolor in kwargs:
            kwargs['color'] = kwargs.pop(fillcolor)


        if 'note' in kwargs:
            #Not supported
            kwargs.pop('note')

        n = id + ' ' + Helper.render_attrs(label, kwargs)
        return n

    @staticmethod
    def edge(fromId, toId, label=None, **kwargs):
        if 'dir' in kwargs:
            kwargs.pop('dir')
        return '{} -> {}'.format(fromId, toId) + ' ' + Helper.render_attrs(label, kwargs)

    @staticmethod
    def startDiagram(*args, **attrs):
        return "blockdiag {\norientation=portrait;"


    @staticmethod
    def endDiagram(*args):
        """ Called last uring the render to finalise a diagram """
        return "}"


    @staticmethod
    def startSubdiagram(id, label, **kwargs):
        kwargs.setdefault('label',label)
        if 'shape' in kwargs:
            kwargs.pop('shape')
        if fillcolor in kwargs:
            kwargs['color'] = kwargs.pop(fillcolor)

        attrs = "; ".join(['{}="{}"'.format(k,v) for (k,v) in list(kwargs.items())]) +";"
        return """
group {id} {{
{attrs}""".format(id=id, attrs=attrs)

    @staticmethod
    def endSubdiagram(id, label, **kwargs):
        return "\n}} \n".format(id=id)