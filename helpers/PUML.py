from pydiagrams.helpers.constants import *
from pydiagrams.helpers import helper 

from pydiagrams.utils.Renderers import PlantUML as Renderer


# Map of shapes
helper.shape = {
        'Cloud':'cloud',
        'Database':'database',
        'Folder':'folder',
        'Frame':'frame',
        'Node':'node',
        'Package':'package',
        'Rectangle':'rectangle',    
        'Component':'component',
        'Interface':'interface',
        'Diamond':'interface',

        # Views
        'Table'         :   'rectangle',
        'View'          :   'rectangle',
        'Package'       :   'package',
        'File'          :   'folder',
        'Integration'   :   'interface',
        'System'        :   'cloud',
        'Task'          :   'component',

        #Architecture
        'Entity'        :   'rectangle',
        'Module'        :   'component',
        'EntityGroup'   :   'database',

        #Flowchart : Need to use 'Component' shapes
        'FC_Start'      :   'rectangle',
        'FC_End'        :   'rectangle',
        'FC_Terminal'   :   'rectangle',
        'FC_Process'    :   'rectangle',
        'FC_Decision'   :   'interface',
        'FC_IO'         :   'rectangle',
        'FC_PredefinedProcess'  : 'component', 
        'FC_OnPageConnector'    :  'rectangle',
        'FC_OffPageConnector'   :  'rectangle',
        'FC_Database' : 'database',
        'FC_Document' : 'rectangle',
        'FC_ManualOperation' : 'rectangle',
        'FC_ManualInput' : 'rectangle',
        'FC_Preparation' : 'rectangle'        
    }

helper.comment_format = "' {text}\n"


class Helper(helper.helper):
    """ 
    The Helper class stores the methods specific to a diagram language.
    It's passed to the FlowchartBase object to be used when rendering code
    """

    extension   = "puml"
    name = "PUML"

    arrows = {
         'vertical'   : '-->',
         'horizontal' : '->',
         'right'    : '-right->',
         'left'     : '-left->',
         'up'       : '-up->',
         'down'     : '-down->',
         'hline'    : '-',
         'vline'    : '--',
         'vdotted'  : '..>'
        }

    # For plantuml, the theme to include
    #theme = 'w:\\plantuml\\theme-blue.iuml'
    theme = 'https://raw.githubusercontent.com/billingtonm/plantuml-themes/master/theme-blue.iuml'

    @staticmethod
    def node(id, label, **kwargs):
        #eg: interface "[DR3] Customer Review Authorisation" as rms_cra
        n = str(Helper.shape(kwargs.get('shape', 'rectangle')))
        if label or label != '':            
            n += ' "{}"'.format(label)
        n += ' as {} '.format(id)

        if fillcolor in kwargs:
            FILLCOLOR=kwargs[fillcolor]
            if not FILLCOLOR.startswith('#'):
                n += '#'
            n += FILLCOLOR

        if 'note' in kwargs:
            n += '\nnote right of {id}\n{note}\nend note'.format(id=id, note=kwargs['note'])
        return n

    @staticmethod
    def edge(fromId, toId, label=None, **kwargs):
        dir = kwargs.get('dir', None)

        if not dir:
            dir = 'vertical'

        edge = '{} {} {}'.format(fromId, Helper.arrows[dir], toId)

        if label:
            edge += ' : ' + label

        return edge

    @staticmethod
    def startDiagram(*args, **attrs):
        """ Called first during the render to initialise a diagram """

        ret= """@startuml {filename}""".format(filename=args[0])

        if Helper.theme:
            ret += "\n!includeurl {theme}".format(theme=Helper.theme)

        return ret


    @staticmethod
    def endDiagram(*args):
        """ Called last uring the render to finalise a diagram """
        return "@enduml"


    @staticmethod
    def startSubdiagram(id, label, **kwargs):
        shape=Helper.shape(kwargs.get('shape', 'rectangle'))
        #label=kwargs.get('label')
        
        
        t = shape
        if label and label != '':
            t += ' "{}" '.format(label)

        color=str(kwargs.get('fillcolor', ""))
        if color:
            if not color.startswith('#'):
                t += '#' 
            t += str(color)

        #return '{shape} "{label}" {color} {{\n'.format(shape=shape, label=label, color=color)
        return t + ' {\n'

    @staticmethod
    def endSubdiagram(id, label, **kwargs):
        return "\n}} \n".format(id=id)

    @staticmethod
    def generate_diagram(source_file):
        print(f'Calling plantuml to render the file as {Helper.output_format}')
        Renderer().generate(source_file, Helper.output_format)
