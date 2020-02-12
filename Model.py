import pydiagrams.baseItems as bi

class Item(bi.BaseItem):
    @property 
    def Id(self):
        if self.id:
            return self.id
        else:
            return self.label.replace(' ', '_')

    @Id.setter
    def Id(self, value):
        self.id = value

# Model
class Model(bi.BaseItemCollection):
    pass

class Context():
    """ Represents a general data model. Implements as a context """
    def __init__(self, model):
        self.model = model

    def __enter__(self):
        return self.model

    def __exit__(self, *args):
        self.model.set_ids()

# A class for mantaining many-many relationships between two objects
# the classes are A and B
class ManyToMany(dict):
    class Index(dict):
        def __setitem__(self, key, value):
            if key in self:
                self[key].append(value)
            else:
                super().__setitem__(key, [value])

    def __init__(self):
        super().__init__({})
        self._A = ManyToMany.Index()
        self._B = ManyToMany.Index()

    def get(self, a, b):
        return self.__getitem__((a,b))

    def set(self, a, b, value=None):
        super().__setitem__( (a,b), value)
        self._A[a] = b
        self._B[b] = a

    def get_by_A(self, a):
        """ Returns the set of B objects for an A """
        return self._A.__getitem__(a)

    def get_by_B(self, b):
        """ Returns the set of A objects for a B """
        return self._B.__getitem__(b)

    def set_by_A(self, a, b_list):
        for b in b_list:
            self.set(a, b)

    def set_by_B(self, b, a_list):
        for a in a_list:
            self.set(a, b)            