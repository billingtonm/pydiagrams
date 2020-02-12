from pydiagrams.helpers.constants import *
#from pydiagrams.helpers.PUML import Helper
import pydiagrams.helpers.PUML as PUML

class Helper(PUML.Helper):
    """ 
    This Helper extends the PUML helper form using the AWS_PlantUML library
    """

    # extension   = "puml"
    name = "PUML_AWS"

    # arrows = {
    #      'vertical'   : '-->',
    #      'horizontal' : '->',
    #      'right'    : '-right->',
    #      'left'     : '-left->',
    #      'up'       : '-up->',
    #      'down'     : '-down->',
    #      'hline'    : '-',
    #      'vline'    : '--',
    #      'vdotted'  : '..>'
    #     }

    # # For plantuml, the theme to include
    theme = ''

    includes = set()

    @staticmethod
    def node(id, label, **kwargs):
        #eg: interface "[DR3] Customer Review Authorisation" as rms_cra
        shape = Helper.shape(kwargs.get('shape', 'rectangle'))

        # if the shape is text, its a normal component, otherwise it's an AWSDiagramItem
        if type(shape) == str:
            return PUML.Helper.node(id, label, **kwargs)

        n = ''
        if shape.name not in Helper.includes:
            Helper.includes.add(shape.name)
            n = f'!includesub Item__{shape.name}\n'

        # print(f'{shape.name=} {type(shape)=} {label=}')

        n += f'{shape.name}({id},"{label}")' 

        if 'note' in kwargs:
            n += '\nnote right of {id}\n{note}\nend note'.format(id=id, note=kwargs['note'])
        return n

    @staticmethod
    def startDiagram(*args, **attrs):
        """ Called first during the render to initialise a diagram """

        ret= """@startuml {filename}
!$AWS_PLANTUML=%getenv("PLANTUML_AWS") + "\dist"
!include $AWS_PLANTUML\common.puml
""".format(filename=args[0])

        if Helper.theme:
            ret += "\n!include {theme}".format(theme=Helper.theme)

        return ret