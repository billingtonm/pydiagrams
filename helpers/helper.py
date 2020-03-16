shape = {}
# Format for comments. Use {text} to denote where the comment text should go
comment_format = "/* {text} */\n"

class helper(object):
    """ 
    The Helper class stores the methods specific to a diagram language.
    It's passed to the FlowchartBase object to be used when rendering code
    """

    # File extension
    extension = ""

    # Name of helper
    name = ""

    # Dictionary that tracks the number of edges between 2 nodes
    # This dictionary has the key that is a tuple of (source,target)
    edge_counter = {}

    @staticmethod
    def remove(d, k):
        """ Remove a key from dict d """
        if k in d:
            d.pop(k) 

    output_format = 'png'

    @staticmethod
    def shape(in_shape, **kwargs):
        """ Translate a shape to this one recognized by the helper """
        return shape.get(in_shape, in_shape) 

    @staticmethod
    def node(id, label=None, **kwargs):
        pass

    @staticmethod
    def edge(fromId, toId, label=None, **kwargs):
        pass

    @staticmethod
    def startDiagram(*args):
        """ Called first during the render to initialise a diagram """
        pass

    @staticmethod
    def endDiagram(*args):
        """ Called last uring the render to finalise a diagram """
        pass


    @staticmethod
    def startSubdiagram(id, **kwargs):
        pass

    @staticmethod
    def endSubdiagram(id, **kwargs):
        pass

    @staticmethod
    def comment(text):
        return comment_format.format(text=text)

    @staticmethod
    def generate_diagram(source_file):
        print(f'Diagram generation not implemented.')

    @staticmethod
    def startTogether():
        return ''

    @staticmethod
    def endTogether():
        return ''

    @staticmethod
    def add_edge(source, target):
        """ Counts a new edge between a source and target and returns the next sequence """
        key = (source,target)
        count = helper.edge_counter.get(key, 0)
        helper.edge_counter[key] = count + 1

        return count
