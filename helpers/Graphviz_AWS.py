import os
import os.path

import pydiagrams.helpers.Graphviz as Graphviz
import pydiagrams.AWS as AWS

class Helper(Graphviz.Helper):
    AWS_ICONS_PATH = os.getenv('AWS_ICONS')

    extension   = 'gv'    
    name = 'Graphviz_AWS'

    @staticmethod
    def node(id, label, **kwargs):
        shape = 'shape'
        if shape in kwargs:
            s=kwargs.pop(shape)

            if isinstance(s, AWS.AWS_Item):
                kwargs['image'] = s.icon.filename.replace(Helper.AWS_ICONS_PATH, '').lstrip(os.path.sep)
            else:
                # Reset properties to defaults for the node
                kwargs[shape] = s
                kwargs['color'] = 'black'
                kwargs['fixedsize'] = 'false'
                kwargs['labelloc'] = 'c'
                kwargs['width'] = ''
                kwargs['height'] = ''
                kwargs['fillcolor'] = '#fefece'
                return Graphviz.Helper.node(id, label, **kwargs)

        #return '\n' + id + ' ' + Helper.render_attrs(label, kwargs)
        return str(Graphviz.GV_Item(id, label=label, **kwargs))

    @staticmethod
    def startDiagram(*args, **attrs):        
        # Add extra attributes to help an AWS diagram look neater
        Graphviz.Helper.graph_defaults.update(
            nodesep=0.8 # Increase spacing between nodes
            ,imagepath = Helper.AWS_ICONS_PATH
        )
        
        Graphviz.Helper.node_defaults.update(
            fillcolor='white',
            color='white',  # Disables the border
            shape='rect',
            fixedsize='true',
            width=1.38,
            height=1.9,     # Lengthen the shape so that label appears underneath
            imagescale='true',
            labelloc='b'    # Label at bottom of shape
        )

        return Graphviz.Helper.startDiagram(*args, **attrs)

