from . import helper

from pydiagrams.utils.Renderers import Graphviz as Renderer

helper.shape = {
        # Components
        'Cloud':'cloud',
        'Database':'database',
        'Folder':'folder',
        'Frame':'tab',
        'Node':'box3d',
        'Rectangle':'rect',    
        'Component':'component',
        'Interface':'circle',
        'Diamond':'diamond',

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
        'SystemIntegration' : 'rect',

        #Flowchart
        'FC_Start'      :   'ellipse',
        'FC_End'        :   'rect:rounded',
        'FC_Terminal'   :   'rect',
        'FC_Process'    :   'rect',
        'FC_Decision'   :   'diamond',
        'FC_IO'         :   'parallelogram',
        'FC_PredefinedProcess'  : 'record', 
        'FC_OnPageConnector'    :  'point',
        'FC_OffPageConnector'   :  'invhouse',
        'FC_Database' : 'cylinder',
        'FC_Document' : 'component',
        'FC_ManualOperation' : 'invtrapezium',
        'FC_ManualInput' : 'trapezium',
        'FC_Preparation' : 'hexagon'
    }

helper.comment_format = "# {text}\n"

def render_attr(attr, value):
    v=value
    if attr == 'label' and Helper.html_labels:
        format = '{}=<{}>'
        v=v.replace('&', '&amp;')
    else:
        format = '{}="{}"'

    return format.format(attr, v)

class GV_Attributes(dict):
    def __init__(self, d, permitted):
        super().__init__(d)
        self.permitted = permitted


    def __str__(self):
        return '; '.join([render_attr(k,v) for (k,v) in list(self.items()) if v is not None and k in self.permitted]) \

class GV_Item:
    permitted_attributes = "_background area bb bgcolor center charset clusterrank color colorscheme comment compound concentrate Damping defaultdist dim dimen diredgeconstraints distortion dpi epsilon esep fillcolor fixedsize fontcolor fontname fontnames fontpath fontsize forcelabels gradientangle group height href id image imagepath imagepos imagescale inputscale K label label_scheme labeljust labelloc landscape layer layerlistsep layers layerselect layersep layout levels levelsgap lheight lp lwidth margin maxiter mclimit mindist mode model mosek newrank nodesep nojustify normalize notranslate nslimit  ordering orientation orientation outputorder overlap overlap_scaling overlap_shrink pack packmode pad page pagedir pencolor penwidth peripheries pin pos quadtree quantum rankdir ranksep ratio rects regular remincross repulsiveforce resolution root rotate rotation samplepoints scale searchsize sep shape shapefile showboxes sides size skew smoothing sortv splines start style stylesheet target tooltip truecolor URL vertices viewport voro_margin width xdotversion xlabel xlp z".split()
    def __init__(self, id=None, **attrs):
        self.id = id
        self.attrs = GV_Attributes(attrs, GV_Item.permitted_attributes)

    @property
    def Id(self):
        return self.id

    @property
    def Note(self):
        return self.attrs.get('note')

    @Id.setter
    def Id(self, value):
        self.id = value
   
    def __str__(self):
        output = f'\n{self.Id} [{self.attrs}];'
        if 'note' in self.attrs:
            output += \
                f"""\n{self.Id}_NOTE [shape="note"; color="lightgoldenrod4"; fillcolor="lightgoldenrod1" label="{self.Note}"];
{self.Id}_NOTE -> {self.Id} [constraint=false; style=dashed; color=lightgoldenrod4; arrowhead="empty"]
{{rank=same; {self.Id} {self.Id}_NOTE }}
                """

        return output

class GV_Edge:
    # Attributes that are allowed for an Edge (from https://graphviz.gitlab.io/_pages/doc/info/attrs.html)
    permitted_attributes='arrowhead arrowsize arrowtail color colorscheme comment constraint decorate dir edgehref edgetarget edgetooltip edgeURL fillcolor fontcolor fontname fontsize head_lp headclip headhref headlabel headport headtarget headtooltip headURL href id label labelangle labeldistance labelfloat labelfontcolor labelfontname labelfontsize labelhref labeltarget labeltooltip labelURL layer len lhead lp ltail minlen nojustify penwidth pos samehead sametail showboxes style tail_lp tailclip tailhref taillabel tailport tailtarget tailtooltip tailURL target tooltip URL weight xlabel xlp'.split()
    def __init__(self, fromId, toId, **attrs):
        self.fromId = fromId
        self.toId = toId
        self.attrs = GV_Attributes(attrs, GV_Edge.permitted_attributes)

    def __str__(self):
        return '{} -> {} [{}];'.format(self.fromId, self.toId, self.attrs)

class Helper(helper.helper):

    extension   = 'gv'    
    name = 'Graphviz'

    html_labels = False # Set to true for HTML labels

    @staticmethod
    def render_attrs(label, attrs, enclosed=True):
        attrs.update({'label':label or ""})
        return \
            ('[' if enclosed else '') \
            + '; '.join([render_attr(k,v) for (k,v) in list(attrs.items())]) \
            + (']' if enclosed else '') \
            + ';' 

    @staticmethod
    def node(id, label, **kwargs):
        shape = 'shape'
        if shape in kwargs:
            # print(f'shape={kwargs[shape]}')
            if kwargs[shape] == 'Interface':
                kwargs['xlabel'] = label
                label = ""
                kwargs['width']=0.3
            
            mapped_shape = Helper.shape(kwargs[shape])

            # Support style attributes in the shape name. they occur after the ':' character 
            shape_type = mapped_shape.split(':')             

            kwargs[shape] = shape_type[0]

            if 'fillcolor' in kwargs:
                kwargs.setdefault('style', 'filled') 

            if len(shape_type) > 1:
                s='style'
                r=shape_type[1]
                if s in kwargs:
                    kwargs[s] += (',' + r)
                else:
                    kwargs[s] = r

        return str(GV_Item(id, label=label, **kwargs))

    @staticmethod    
    def edge(fromId, toId, label=None, **kwargs):
        # return '{} -> {}'.format(fromId, toId) + ' ' + Helper.render_attrs(label, kwargs)
        return str(GV_Edge(fromId, toId, label=label, **kwargs))

    note_node_attrs = {
            'shape':'note',
            'fillcolor':'lightyellow',
            'color':'darkred',
            'fontname':'Cambria',
            'fontcolor':'darkred' 
            }

    note_edge_attrs = {
            'color':'darkred',
            'style':'dashed',
            'constraint':'false',
            'arrowhead':'open'
    }

    comment_format = "' {text}\n"

    FONTNAME='Calibri'

    # Graphviz defaults for each type
    graph_defaults = {
        'fontname':FONTNAME,
        'fontsize':20,
        'labelloc':'t'
    }

    node_defaults = {
        'style':'filled',
        'colorscheme':'paired12',
        'fontname':FONTNAME,
        'fontsize':14
        }

    edge_defaults = {
        'fontname':FONTNAME,
        'fontsize':14
    }

    @staticmethod
    def startDiagram(*args, **attrs):
        return """
digraph g {{
#######################################
# base formatting

fontname="{fontname}";
compound=true; #enables edges between clusters

{graph_defaults}

{node_defaults}

{edge_defaults}

#######################################
{attrs}
        """.format(
            fontname='Calibri', 
            graph_defaults = GV_Item('graph', **Helper.graph_defaults),
            node_defaults  = GV_Item('node', **Helper.node_defaults),
            edge_defaults  = GV_Item('edge', **Helper.edge_defaults),
            attrs=Helper.render_attrs(args[1], attrs, False))

    @staticmethod
    def endDiagram(*args):
        return '}'

    cluster_counter = 0

    @staticmethod
    def startSubdiagram(id, label, **kwargs):
        if 'fillcolor' in kwargs:
            kwargs.setdefault('bgcolor', kwargs['fillcolor'])

        cluster_id = id or Helper.cluster_counter

        kwargs.setdefault('label',label)
        attrs = "; ".join(['{}="{}"'.format(k,v) for (k,v) in list(kwargs.items())]) +";"



        Helper.cluster_counter += 1        

        return """
subgraph cluster_{id} {{
    fontsize=18;
{attrs}""".format(id=cluster_id, attrs=attrs)


    @staticmethod
    def endSubdiagram(id, label, **kwargs):
        return "\n}} \n".format(id=id)

    @staticmethod
    def generate_diagram(source_file):
        print(f'Calling graphviz to render the file as {Helper.output_format}')
        Renderer(r'c:\Program Files (x86)\Graphviz2.38\bin\dot').generate(source_file, Helper.output_format)

    @staticmethod
    def startTogether():
        return '\n{rank=same;\n'

    @staticmethod
    def endTogether():
        return '\n};\n'
