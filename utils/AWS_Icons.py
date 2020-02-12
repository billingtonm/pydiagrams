import os
import os.path

import glob
import fnmatch
from PIL import Image

ICON_SET_LIGHT = {'path':'PNG Light', 'file_suffix':'light-bg', 'suffix':True}
ICON_SET_NORMAL = {'path':'PNG Light', 'file_suffix':'light-bg', 'suffix':False}
ICON_SET_DARK  = {'path':'PNG Dark', 'file_suffix':'dark-bg', 'suffix':True}


class AWS_Icon:
    def __init__(self, filename, category):
        self.filename = filename
        self.category = category
        self.icon_set = category.aws_icons.icon_set

    @property 
    def basename(self):
        return os.path.splitext(os.path.basename(self.filename))[0]

    @property
    def dirname(self):
        return os.path.dirname(self.filename)

    @property
    def ext(self):
        """ The extension of the filename """
        return os.path.splitext(self.filename)[-1]

    @property
    def size(self):
        """ Returns the size of the image """
        return  Image.open(self.filename).size

    @property
    def name(self):
        # remove any scale information from the basename
        n = self.basename.split('@')[0] 

        if self.icon_set['suffix']:
            n = n.rstrip(self.icon_set['file_suffix'])
        
        n = n.rstrip('_')

        return n

    @property
    def scale(self):
        """ 
        The scale of the image as reported in the filename. This comes from looking for @[digit]x at the end of the filename
        eg: '@4x.png' would return 4
        """
        parts = self.basename.split('@')

        # if the name doesn't have a '@' then there's no scale, return 1 as the scale
        if len(parts) == 1:
            return 1

        # if the (last) part after the '@' doesn't have an 'x' then we don't have a scale
        if not parts[-1].endswith('x'):
            return 1

        # Attempt to return the scale as a number
        try:
            return int(parts[-1].rstrip('x'))
        except ValueError:
            return 1

    def __repr__(self):
        return self.filename

class AWS_Category:
    def __init__(self, aws_icons, category_path):
        self.aws_icons = aws_icons
        self.category_path = category_path

    def __repr__(self):
        return '{}("{}")'.format(self.__class__.__name__, self.category_path)

    @property
    def name(self):
        return self.category_path

    @property
    def path(self):
        return os.path.join(self.aws_icons.IconBasePath, self.category_path)

    def iter_files(self):
        glob_pattern = os.path.join(self.path, '**/*.png')
        name_filter = self.aws_icons.IconSet_Suffix
        suffix_filter = self.aws_icons.icon_set['suffix']

        I = lambda fn: AWS_Icon(fn, self)

        for fn in glob.iglob(glob_pattern, recursive=True):
            if name_filter in fn:
                if suffix_filter:
                    yield I(fn)
            else:
                if not suffix_filter or self.name == '__Custom':
                    yield I(fn)

    def get_files(self):
        return list(self.iter_files())

class NoIconPathError(Exception):
    def __init__(self):
        super().__init__('No Icon Path specified. Set Environment variable AWS_ICONS the path that contains the AWS Icons')

class AWS_Icons:
    def __init__(self, basepath=None, icon_set=ICON_SET_LIGHT):
        """ 
        basepath : The filepath that stores the AWS Icon set
        icon_set : The icons come in two options: 'PNG_Dark', PNG_Light. This is the set to use
        """        
        self.basepath = basepath or os.getenv('AWS_ICONS')
        if not self.basepath:
            raise NoIconPathError()
        self.icon_set = icon_set

    @property
    def IconBasePath(self):
        return os.path.join(self.basepath, self.icon_set['path']) 

    @property 
    def IconSet_Suffix(self):
        return '_' + self.icon_set['file_suffix']

    def iter_categories(self):
        print(self.IconBasePath)
        """ The catagories are the subdirectories """
        for dn in os.listdir(self.IconBasePath):
            d = os.path.join(self.IconBasePath, dn)
            if os.path.isdir(d):
                yield AWS_Category(self, dn)

    def get_categories(self):
        return list(self.iter_categories())


if __name__ == '__main__':
    icons = AWS_Icons()

    for c in icons.iter_categories():
        print(c.path)