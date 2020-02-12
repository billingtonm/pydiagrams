# Local python libraries


# import pydiagrams.Diagram as Diagram
import pydiagrams.Diagram as Diagram
import pydiagrams.Component as Component
from pydiagrams.baseItems import logged
import pydiagrams.utils.AWS_Icons as AWS_Icons


# Maps an AWS Icon to a value that we can use here
class AWS_Item:
    def __init__(self, icon):
        self.icon = icon

    @property
    def name(self):
        n=self.icon.name #.title()
        for repchar in '-.':
            n=n.replace(repchar, '')
        n=n.replace(' ', '_')
        
        return n

    def __str__(self):
        return self.name
        
    def __repr__(self):
        return f'{self.__class__.__name__}({self.name=})'

    @staticmethod
    def from_icons(aws_icons):
        for cat in aws_icons.iter_categories():
            for icon in cat.iter_files():
                if icon.name not in ( 'Database', 'Cloud'):
                    yield AWS_Item(icon)


##########################################################################
# Item Classes
class AWSDiagramItem(Component.ComponentDiagramItem):
    def __init__(self, label, aws_item, **attrs):
        # super().__init__(label, 'rectangle', **attrs)
        try:
            print(f'{aws_item.name=}')
            super().__init__(label, aws_item.name, **attrs)
            self.aws_item = aws_item
        except:
            print(f'{aws_item=}')
            raise

##########################################################################
# Diagram Classes

class AWSDiagram(Component.ComponentDiagram):
    cls = 'AWS.AWSDiagram'

    @logged(cls)
    def __init__(self, helper, filename=None, context=None, aws_icons=None, **attrs):
        super().__init__(helper, filename, context, **attrs)

        # Add each AWS Icon as a method to this package
        for i in AWS_Item.from_icons(aws_icons):
            #print(f'{i.name=}, {i.icon.category.name=}')
            setattr(self, i.name, self.__item__(i))

    @logged(cls)
    def add_new_item(self, aws_item, label, **kwargs):
        if isinstance(aws_item, AWSDiagramItem):
            """ Override the base add_new_item method """
            i = AWSDiagramItem(aws_item=aws_item, label=label, **kwargs)
            collection = self._context._groups.current().collection 
            r= collection.add_item(i)
            return r
        else:
            return super().add_new_item(aws_item, label, **kwargs)

    def __item__(self, item):
        """ Called when a AWS Item is invoked """
        @logged(AWSDiagram.cls)
        def add(label="", **attrs):
            # print(f'{AWSDiagram.cls}.__item__: Calling add for: {item} {label=}')
            return self.add_new_item(item, label, **attrs)
        return add


##########################################################################
# Context Classes
class AWSContext(Diagram.Context):
    def __init__(self, helper, filename=None, **attrs):
        super().__init__()

        # AWS_ICON_PATH=r'D:\Software\plantuml\AWS-Architecture-Icons_PNG\AWS-Architecture-Icons_PNG_20191031'
        # aws_icons = AWS_Icons.AWS_Icons(AWS_ICON_PATH)
        aws_icons = AWS_Icons.AWS_Icons()
        self.diagram=AWSDiagram(helper, filename, context=self,aws_icons=aws_icons, **attrs)


if __name__ == '__main__':
    from pydiagrams.helpers.PUML import Helper
    with AWSContext(Helper) as a:
        pass
