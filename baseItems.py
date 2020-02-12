import sys
from collections import OrderedDict
from functools import wraps

# Get access to the running scripts variables
module_globals = sys.modules['__main__'].__dict__

log_enabled=False

def logged(class_name):
    def actual_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if log_enabled:
                print(f'\n<< Calling: {class_name}.{func.__name__} >>')
            return func(*args, **kwargs)
        return wrapper
    return actual_decorator

class BaseItem(object):
    """ Defines a base item, eg: a Component in a Component Diagram """
    def __init__(self,  label, **attrs):
        self.owner = None
        self.label = label
        self.attrs = attrs
        self.id = None

    def __repr__(self):
        return 'BaseItem.label = "{}"'.format(self.label)

    @property
    def Diagram(self):
        if self.owner:
            return self.owner.diagram
        else:
            raise ValueError('%s has no owner' % (self.__repr__()))

    @property
    def Helper(self):
        return self.Diagram.helper

    @property 
    def Collections(self):
        """ Returns the set of collections the item belongs to """
        c = []
        o = self.owner.diagram
        while o.level > 0:
            c.append(o)
            if hasattr(o, 'owner'):
                o = getattr(o.owner, 'diagram', None)
            else:
                o = None                

        return c

class BaseItemCollection(object):
    cls = 'baseItems.BaseItemCollection'

    """ Represents an Object that owns base items, eg: a Diagram """
    @logged(cls)
    def __init__(self, diagram):
        self.collection = OrderedDict()
        self.diagram = diagram

    @logged(cls)
    def add_item(self, i):
        """ Add BaseItem i to the collection """
        i.owner = self
        self.collection[hash(i)] = i
        return i

    def add_new_item(self, itemType, label, **attrs):
        i = itemType(self, label, **attrs)
        return self.add_item(i)

    def items(self):
        return [(k,v) for (k,v) in list(module_globals.items()) if (isinstance(v, BaseItem))]
        
    def values(self):
        for v in list(self.collection.values()):
            yield v

    def values_by_type(self, t):
        for v in self.values():
            if isinstance(v, t):
                yield v

    def set_ids(self):
        for (k,v) in list(self.items()):
            #print k,v.label
            v.id = k

    def get_first_item(self):
        return list(self.collection.values())[0]

    def len(self):
        return len(self.collection.values())        