from . import helper

import json

helper.shape = {
        # Components
        'Cloud':'generic.cloud',
        'Database':'generic.database',
        'Folder':'generic.generic-physical-data-transfer-device',
        'Frame':'generic.bucket',
        'Node':'generic.block',
        'Package':'generic.generic-container',
        'Rectangle':'generic.generic-cube',    
        'Component':'generic.processor',
        'Interface':'generic.gateway',
        'Diamond':'diamond',
        'Server':'generic.server',
        'Actor':'generic.pc',

        # Below here are TODO
        # Views
        'Table'         :   'rect',
        'View'          :   'parallelogram',
        'Package'       :   'invhouse',
        'File'          :   'folder',
        'Integration'   :   'invtrapezium',
        'System'        :   'ellipse',
        'Task'          :   'cds',

        #Architecture
        'Entity'        :   'ellipse',
        'Module'        :   'component',
        'SystemIntegration' : 'rect'
    }

helper.comment_format = "# {text}\n"

class Helper(helper.helper):

    extension   = 'arcentry.json'
    name = 'arcentry'

    node_count = 0

    json_encoder = json.JSONEncoder()

    @staticmethod
    def render_attrs(label, attrs, enclosed=True):
        attrs.update({'label':label or ""})
        return Helper.json_encoder.encode(attrs)
        #return attrs

    @staticmethod
    def node(id, label, **kwargs):
        s= 'shape'
        Helper.remove(kwargs, 'width')

        kwargs.setdefault('type', 'component')
        if s in kwargs:
            kwargs.setdefault('componentType', Helper.shape(kwargs.pop(s)))

        if 'groups' in kwargs:
            kwargs['groups'].reverse()

        if 'links' in kwargs:
            links = kwargs.pop('links')
            if len(links) > 0:
                kwargs.setdefault('connections', links)

        ret = '"{}":{}'.format( id, Helper.render_attrs(label, kwargs) )

        if Helper.node_count > 0:
            ret = ',' + ret
        
        Helper.node_count += 1
        return ret


    @staticmethod    
    def edge(fromId, toId, label=None, **kwargs):
        #return '{} -> {}'.format(fromId, toId) + ' ' + Helper.render_attrs(label, kwargs)
        return ''

    comment_format = "' {text}\n"

    @staticmethod
    def startDiagram(*args, **attrs):
        return "{"

    @staticmethod
    def endDiagram(*args):
        return '}'

    @staticmethod
    def startSubdiagram(id, label, **kwargs):
        # arcentry doesn't have subdiagrams, instead the nodes report their parent groups
        return ''


    @staticmethod
    def endSubdiagram(id, label, **kwargs):
        return ''

    @staticmethod
    def comment(text):
        # comments are not supported in json
        return ''    