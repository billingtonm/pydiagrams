from contextlib import contextmanager # contextmanager decorator (for IntegrationSet)
import copy # required to create integration copies for middleware functionality

import pydiagrams.Model as Model

# constants for properties
url = 'url'
direction= 'direction'

class Namespace:
    pass

class IntegrationFragment():
    """ Temporary class used during the creation of a integration when used with operations,
        eg: SimpleItem1 >> SimpleItem2 % 'Label'
        This class stores the result of the intermediate operation: SimpleItem2 % 'label'
    """
    def __init__(self, simpleItem, description):
        self.simpleItem = simpleItem
        self.description = description

##########################################################################
# Item Classes
class Item(Model.Item):
    def __init__(self, label, **attrs):
        super().__init__(label, **attrs)

    def get_attributes_by_type(self, t):
        """ return local attributes that are instances of type t """
        #return [(k,v) for (k,v) in self.__dict__.items() if isinstance(v, t)]
        return [v for v in list(self.__dict__.values()) if isinstance(v, t)]

    @property 
    def Description(self):
        return self.label        

class SimpleItem(Item):
    """ Items that can be owned by Systems """
    @property
    def isEntity(self):
        return isinstance(self, EntityItem)

    @property
    def isModule(self):
        return isinstance(self, ModuleItem)

    # >> 
    # This creates an internal integration from a ModuleItem to an EntityItem
    # can be called on a list of items or a single item
    def __rshift__(self, itemSet):
        def link(item, description=None):
            if isinstance(item, SimpleItem):
                # Determine integration type, Internal or External
                if self.owner == item.owner:
                    # The owner of the items match, therefore Internal Integration
                    assert isinstance(self.owner, SystemItem), 'Item does not belong to a System'
                    newOwner = self.owner

                    # switch around any erroroneous Entity >> Module defintions
                    if self.isEntity and item.isModule:
                        sourceItem = item
                        destItem = self
                    else:
                        sourceItem = self
                        destItem = item

                else:
                    newOwner = self.owner.get_root_owner().current_context_item
                    assert newOwner is not None, 'Can only add integrations from within a IntegrationSet context'
                    sourceItem = self
                    destItem = item

                # Create the IntegrationItem
                integration = IntegrationItem(
                        sourceSystem = self.owner, sourceItem = sourceItem, 
                        destSystem = item.owner, destItem = destItem, 
                        description=description)
                newOwner.add_integration(integration)
                return integration

            else:
                raise ValueError('>> operator only supported for Modules & Entities')

        if type(itemSet) == list:
            for item in itemSet:
                link(item)
            return None
        elif isinstance(itemSet, IntegrationFragment):
            return link(itemSet.simpleItem, itemSet.description)
        else:
            return link(itemSet)

    # %
    # This operator enables an integration to be constructed with a label/description
    # eg: SimpleItem1 >> SimpleItem2 % 'Description'
    # means: create an integration from SimpleItem1 to SimpleItem2 with description 'Description'
    def __mod__(self, description):
        return IntegrationFragment(self, description)

class ModuleItem(SimpleItem):
    pass

class EntityItem(SimpleItem):
    pass        

class ArchItem(Item):
    """ Item with Integrations (eg: System, IntegrationSet) """
    def __init__(self, label, **attrs):
        super().__init__(label, **attrs)
        self.integrations = []

    def add_integration(self, integration):
        integration.owner = self
        self.integrations.append(integration)

    @property
    def Ints(self):
        return self.integrations

    def get_root_owner(self):
        return self.owner

class SystemItem(ArchItem):
    def __init__(self, label, entities, modules, **attrs):
        super().__init__(label, **attrs)
        self.create_attributes(EntityItem, entities)
        self.create_attributes(ModuleItem, modules)

    @property
    def Entities(self):
        """ Return a dict of the entities in this class """
        return self.get_attributes_by_type(EntityItem)

    @property
    def Modules(self):
        """ Return a dict of the entities in this class """
        return self.get_attributes_by_type(ModuleItem)

    def create_attributes(self, itemType, itemList):
        """ Create an attribute for this each item in itemList.
            This is used to create Modules and Entity references
         """
        if not itemList:
            return
        for item in itemList:
            # Create an instance of the item
            if type(item) == str:
                i = itemType(item)
            elif type(item) == tuple:
                i = itemType(item[1])
                i.Id = item[0]     
            
            i.owner = self
            setattr(self, i.Id, i)            
            #print ('Created {itemType}: "{system}".{item}'.format(itemType=itemType, system=self.label, item=i.Id))

class IntegrationSetItem(ArchItem):
    def __init__(self, label, isMiddleware=False, **attrs):
        super().__init__(label, **attrs)
        self.isMiddleware = isMiddleware
        self.mw_system = None # System that is the middleware

    def set_middleware(self, system):
        print('Enabled middlewares')
        self.isMiddleware = True
        self.mw_system = system

    def add_integration(self, integration):
        if not self.isMiddleware:
            super().add_integration(integration)
        else:
            i1 = copy.copy(integration)
            i2 = copy.copy(integration)

            i1.destSystem   = self.mw_system
            i2.sourceSystem = self.mw_system

            # Add the sourceItem to the middleware system
            if not hasattr(self.mw_system, i1.sourceItem.Id):
                new_item = copy.copy(i1.sourceItem)
                new_item.owner = self.mw_system
                setattr(self.mw_system, new_item.Id, new_item)

            for i in [i1, i2]:
                super().add_integration(i)

class IntegrationItem(Item):
    def __init__(self, 
                 sourceSystem, sourceItem, 
                 destSystem, destItem,
                 description = None,
                 url = None,
                 direction = None):
        super().__init__(label = None)                 
        self.sourceSystem = sourceSystem
        self.sourceItem = sourceItem
        self.destSystem = destSystem
        self.destItem = destItem

        self.description = description
        self.direction = direction
        self.url = url

    # & operator
    # This operator enables an integration to have properties appended to it
    # eg: SimpleItem1 >> SimpleItem2 % 'Description' & {url: 'http://example.com/my-integration', direction='right'}
    def __and__(self, attrs):
        assert type(attrs) == dict, "% must be used with a dictionary. eg: % {url: 'http://example.com/my-integration'}"
        self.__dict__.update(attrs)
        return self

    def __repr__(self):
        return 'owner={owner} {sourceSystem.Id}.{sourceItem.Id} >> {destSystem.Id}.{destItem.Id}'.format(**self.__dict__)

    def goVia(self, system):
        """ Makes an integration go via a certain system.
            If an integrations is A >> B, then this makes the integration A >> system >> B
            It returns the pair: [A >> system, system >> B]
        """            
        i0 = IntegrationItem(self.sourceSystem, self.sourceItem,
                             system)
        #TODO


class UserGroupItem(Item):
    pass

##########################################################################

class ArchitectureModel(Model.Model):
    def __init__(self):
        super().__init__(diagram=None)

        self.integrationSets = []        
        self.current_context_item = None
        self.app_user_groups = Model.ManyToMany()

    def System(self, label, entities=None, modules=None, **attrs):
        """ Return the System type """
        new_item = SystemItem(label, entities, modules, **attrs)
        return self.add_item(new_item)

    def Application(self, *args, **kwargs):
        """ Same as System, provided for compatibility with ARK model """
        return self.System(*args, **kwargs)

    def UserGroup(self, label, **kwargs):
        return self.add_item(UserGroupItem(label))

    @contextmanager
    def IntegrationSet(self, label, isMiddleware=False, **attrs):
        intSet = self.add_item(IntegrationSetItem(label, isMiddleware, **attrs))

        if isMiddleware:
            intSet.set_middleware(self.System(label, **attrs))

        self.current_context_item = intSet
        self.integrationSets.append( intSet )
        yield self.current_context_item
        self.current_context_item = None

    @property
    def Systems(self):
        return [v for v in self.values_by_type(SystemItem)]

    @property
    def IntegrationSets(self):
        return [v for v in self.values_by_type(IntegrationSetItem)]

    @property
    def Integrations(self):
        ints = []
        for IS in self.IntegrationSets:
            ints += IS.Ints
        return sorted(ints, key=lambda x:(x.sourceSystem.Id, x.destSystem.Id))

class ArchitectureContext(Model.Context):
    def __init__(self):
        super().__init__(ArchitectureModel())

    def __exit__(self, *args):
        print ('About to exit')
        super().__exit__(*args)
        print ('Done exit')