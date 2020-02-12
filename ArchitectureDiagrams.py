from pydiagrams.Architecture import Item
from pydiagrams.helpers.GraphML import Helper
from pydiagrams.helpers import constants as C

import itertools
import colour # from pip install colour. Doco @ https://pypi.org/project/colour/

class Renderer():
    def __init__(self, filename=None):
        self.lines = []
        self.filename= filename

    def write(self, line):
        self.lines.append(line)

    def dump(self):
        if self.filename:
            fn = self.filename + '.' + Helper.extension
            with open(fn, 'w') as f:
                for line in self.lines:
                    f.write(line + '\n')
            print(f'Done writing to: {fn}')

        else:
            print('\n'.join(self.lines))

    def __enter__(self):
        self.write(Helper.startDiagram('', ''))
        return self

    def __exit__(self, *args):
        self.write(Helper.endDiagram())
        self.dump()

class ItemRenderer():
    def __init__(self, mainRenderer, item, **attrs):
        self.mainRenderer = mainRenderer
        self.item = item
        self.lines = []
        self.attrs = attrs

    def __str__(self):
        return str(self.item.id)       

    def write(self, line):
        self.mainRenderer.lines.append(line)

    def __enter__(self):
        #print('{t}.{id}.begin'.format(t=type(self.item), id=self.item.Id))
        return self

    def __exit__(self, *args):
        #print('{t}.{id}.end'.format(t=type(self.item), id=self.item.Id))
        pass

class SystemRenderer(ItemRenderer):
    def __enter__(self):
        self.write(Helper.startSubdiagram(self.item.Id, self.item.label, **self.item.attrs))
        return super().__enter__()

    def __exit__(self, *args):
        self.write(Helper.endSubdiagram(self.item.Id, self.item.label, **self.item.attrs))
        super().__exit__(*args)

class ShapeRenderer(ItemRenderer):
    """ Renders an item as a basic shape """
    def __init__(self, shape, *args, **attrs):
        super().__init__(*args, **attrs)
        self.shape = shape

    def __str__(self):
        node_id =''
        if hasattr(self.item.owner, 'Id'):
            node_id = self.item.owner.Id

        attrs = self.attrs.copy()
        attrs.update(self.item.attrs)

        node_id += self.item.Id if hasattr(self.item, 'Id') else self.item.id 
        return Helper.node(node_id, self.item.label, shape=self.shape, **attrs)


class EntityRenderer(ShapeRenderer):
    def __init__(self, *args):
        super().__init__('Entity', *args, fillcolor=C.color1)

class ModuleRenderer(ShapeRenderer):
    def __init__(self, *args):
        super().__init__('Component', *args, fillcolor=C.color3)

class SystemShapeRenderer(ShapeRenderer):
    def __init__(self, *args, **kwargs):
        super().__init__('SystemIntegration', *args, **kwargs)


class IntegrationRender(ItemRenderer):
    """ Integration between Items """
    def __str__(self):
        e=self.item
        return Helper.edge(
            fromId = e.sourceSystem.Id + '_' + e.sourceItem.Id
            ,toId = e.destSystem.Id + '_' + e.destItem.Id
            ,label=e.description
            ,url=e.url
            ,direction=e.direction
        )

class IntegrationSystemRender(ItemRenderer):
    """ Integration between Systems """
    def __str__(self):
        e=self.item
        return Helper.edge(
            fromId = e.sourceSystem.Id
            ,toId = e.destSystem.Id
            ,label=e.description
            ,url=e.url
            ,direction=e.direction
        )


class ArchitectureDiagram():
    """ General diagram.
    This class will represent the standard properties and methods for a diagram,
    eg:
    - Filename and File handling
    - Standard properties, etc...
    """
    def __init__(self, model, filename=None, **attrs):
        self.model = model
        self.filename = filename
        self.attrs = attrs

    def generate(self):
        pass


class Entity(ArchitectureDiagram):

    def generate(self):
        m = self.model

        with Renderer(self.filename) as r:
            for system in m.Systems:
                with SystemRenderer(r, system):

                    r.write(Helper.startSubdiagram(system.Id + '_group', '', shape='EntityGroup'))                        
                    for entity in system.Entities:
                        r_ent =  EntityRenderer(r, entity)
                        r.lines += [str(r_ent)]

                    r.write(Helper.endSubdiagram(system.Id + '_group', '', shape='EntityGroup'))                        

                    for module in system.Modules:
                        r.write(str(ModuleRenderer(r, module)))

                    for int in system.Ints:
                        r.write(str(IntegrationRender(r, int)))

            intset_id = 0
            for intsets in m.IntegrationSets:

                for int in intsets.Ints:
                    r.write(str(IntegrationRender(r, int)))

                intset_id += 1


class Integration(ArchitectureDiagram):
    def generate(self):
        m=self.model

        with Renderer(self.filename) as r:
            
            # Go through the integrations and count the number of times a system
            # is the source or destination of the integration.
            # This can be used to determine the width/height of the system node
            int_from = {}
            int_to = {}
            for int in m.Integrations:
                int_from[int.sourceSystem]   = int_from.get(int.sourceSystem, 0) + 1
                int_to[int.destSystem]     = int_to.get(int.destSystem, 0) + 1


            for system in m.Systems:
                size=max(system.int_from, system.int_to)
                r.write(str(SystemShapeRenderer(r, system, 
                    width=60, 
                    height=90+(size*30),
                    rotationAngle=270,
                    fontsize=20
                    )))

            for intsets in m.IntegrationSets:
                for int in intsets.Ints:
                    r.write(str(IntegrationSystemRender(r, int)))

def get_fillcolor(item):
    """ Gets the fillcolor for an item """
    assert isinstance(item, Item), 'item must be of instance Architecture.Item'
    return item.attrs['fillcolor']   

def set_fillcolor(item, color):
    """ Gets the fillcolor for an item """
    assert isinstance(item, Item), 'item must be of instance Architecture.Item'
    item.attrs['fillcolor'] = color   

class System(ArchitectureDiagram):
    def generate(self):
        m=self.model

        with Renderer(self.filename) as r:
            int_count = {}
            for int in m.Integrations:
                int_count[int.sourceSystem]   = int_count.get(int.sourceSystem, 0) + 1
                int_count[int.destSystem]     = int_count.get(int.destSystem, 0) + 1


            for (n,system) in enumerate(m.Systems):
                r.write(str(ShapeRenderer('circle', r, system, width=int_count.get(system) / 5 , fillcolor=get_fillcolor(system))))

            for ((sourceSystem, destSystem), g) in itertools.groupby(m.Integrations, key=lambda x:(x.sourceSystem, x.destSystem)):
                label = ',\n'.join([i.description or i.sourceItem.Id for i in g])
                
                line_color = list(get_fillcolor(sourceSystem).range_to(get_fillcolor(destSystem), 3))[1]
                font_color = list(get_fillcolor(sourceSystem).range_to(get_fillcolor(destSystem), 3))[1]

                line_color.luminance = 0.3
                font_color.luminance = 0.25


                r.write(Helper.edge(fromId = sourceSystem.Id, toId=destSystem.Id, label=label, color=line_color, fontcolor=font_color))   

def assign_system_colors(model, saturation=0.9, lightness=0.8):
    sysCount = len(model.Systems)
    print('Assigning system colors:')
    for (n,system) in enumerate(model.Systems):
        set_fillcolor( system, colour.Color(hsl=( (n/sysCount)*1, saturation, lightness )))
        print('\t{}\tSystem {}, \tfillcolor={}'.format(n,system.id, get_fillcolor(system)))

def count_integrations(model):
    for s in model.Systems:
        s.int_from = 0
        s.int_to = 0

    for int in model.Integrations:
        int.sourceSystem.int_from += 1
        int.destSystem.int_to += 1


def generate_all(model, basefilename=None):    
    assign_system_colors(model)
    count_integrations(model)

    for Diagram in ArchitectureDiagram.__subclasses__():
        print('Generating Diagram type: ', Diagram.__name__)
        Diagram(model, basefilename + '-' + Diagram.__name__).generate()