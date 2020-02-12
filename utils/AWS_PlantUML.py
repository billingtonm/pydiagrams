import AWS_Icons

import re
import subprocess
import os 
import os.path
import configparser

PUML_JAR=r'D:\Software\plantuml\plantuml.jar'

PUML_TEMPLATE = '''
!startsub {macro}
{sprite}
{macros}
!endsub
'''

STEREOTYPE_SKINPARAM_TEMPLATE = '''
skinparam {entity_type}<<{stereotype}>> {{
    {skinparam}
}}
'''.lstrip()

MACROS_TEMPLATE = '''
!define {macro}(alias) PUML_ENTITY({entity_type},{color},{unique_name},alias,{stereotype})
!definelong {macro}(alias,label,e_type="{entity_type}",e_color="{color}",e_stereo="{stereotype}",e_sprite="{unique_name}")
PUML_ENTITY(e_type,e_color,e_sprite,label,alias,e_stereo)
!enddefinelong
'''

LOG=True

class PUML_Item:
    def __init__(self, aws_icon, category):
        self.aws_icon = aws_icon
        self.category = category

    @property
    def name(self):
        n=self.aws_icon.name.replace('-', '').replace(' ', '_')
        n=n.replace('.', '')
        return n

    @property
    def include(self):
        # Uses the 'subpart' feature of plantuml to include just the macro required
        c = self.category.include
        return '{}!{}'.format(c.replace('!include ', ''), self.name)

    def __repr__(self):
        return '{}("{}")'.format(self.__class__.__name__, self.name)

    def generate_sprite(self):
        size='16z'

        sprite_filename = self.aws_icon.filename.replace('.png','.sprite.puml')

        if os.path.isfile(sprite_filename):
            sprite_file = open(sprite_filename, "r")
            sprite = ''.join(sprite_file.readlines())
            if LOG:
                print('Using sprite file: {}'.format(sprite_filename))

            return sprite
        else:
            if LOG:
                print('Generating sprite for: {}'.format(self.aws_icon.filename))

        cmd = ['java', '-Djava.awt.headless=true', '-jar', PUML_JAR,
               '-encodesprite',
               size,
               self.aws_icon.filename]
        output = subprocess.check_output(cmd, universal_newlines=True)

        lines = output.split('\n')

        # replace the filename with the name of the item
        lines[0] = re.sub(r'^(\s*sprite\s+\$)\w+(\s+\[\d+x\d+/\d+z?\]\s*\{\s*)$',
                          r'\g<1>{}\g<2>'.format(self.name),
                          lines[0],
                          re.I)
        sprite_file = open(sprite_filename, "w")



        sprite = '\n'.join(lines)

        sprite_file.write(sprite)

        return sprite 

    def sprite_reference(self):
        fname = self.aws_icon.filename.replace(self.category.puml.aws_icons.IconBasePath, '')
        args = fname.split(self.category.puml.aws_icons.IconSet_Suffix)
        # if len(args) == 1:
        #     args.append('')
        return f'sprite ${self.name} $filename("{args[0]}", "{args[1]}")'

    @property
    def scale(self):
        size = self.aws_icon.size
        return 100/max(size)

    @property
    def sprite(self):
        # return self.generate_sprite()
        return self.sprite_reference()

    @property
    def macro(self):
        return self.name

    def __str__(self):
        macros = MACROS_TEMPLATE.format(
             macro=self.macro
            ,entity_type = 'rectangle'
            ,color = self.category.color
            ,unique_name = self.name + '{{scale={scale}}}'.format(scale=self.scale)
            ,stereotype = self.name
        )
        return PUML_TEMPLATE.format(sprite=self.sprite, macros=macros, macro=self.macro)

class PUML_Category:
    def __init__(self, puml, aws_category, color):
        self.puml = puml # reference to parent class
        self.aws_category = aws_category
        self.color = color 

    def items(self):
        for icon in self.aws_category.iter_files():
            i = PUML_Item(icon, self)
            self.puml.add_item(i)
            yield i

    @property
    def name(self):
        return self.aws_category.name

    @property
    def clean_name(self):
        n = self.name.title()
        for repchar in '& ,_':
            n = n.replace(repchar, '')
        return n

    @property 
    def relative_filename(self):
        return f'$AWS_PLANTUML\\{self.puml.LIB_DIR}\\{self.name}.puml'

    @property
    def include(self):
        return f'!include {self.relative_filename}'

    def filename(self, sub):
        return os.path.join(self.puml.OUT_PATH, sub, self.name + '.puml')

    def write(self):
        print(f'Generating PUML for category: {self.name}')

        with open(self.puml.lib_file(self.name), 'w') as cat:
            for i in self.items():
                output = str(i)
                cat.write(output)

        with open(self.puml.test_file(self.name), 'w') as f:
            def w(text):
                f.write(text + '\n')

            w('@startuml\n')
            w('!$AWS_PLANTUML={} + "\{}"'.format((self.puml.OutputBasePath), self.puml.SOURCE_DIR)) 
            w('!include $AWS_PLANTUML\\common.puml')
            w(self.include)
            w('\ntitle {}'.format(self.name))
            for (n,i) in enumerate(self.items()):
                w('{}({}, "{}")'.format(i.macro, i.name.lower(), i.name))

            w('\n@enduml')

class PlantUML:
    
    def __init__(self, OUT_PATH=None, AWS_ICON_PATH=None):

        self.env_var_set = False

        if OUT_PATH:
            self.OUT_PATH = OUT_PATH
        else:
            self.OUT_PATH = os.getenv('PLANTUML_AWS')
            self.env_var_set = True

        if self.OUT_PATH:
            print(f'Writing output to %PLANTUML_AWS% = "{self.OUT_PATH}"')
        else:
            raise Exception('No output path specified. Set environment variable PLANTUML_AWS to the directory that the PlantUML code should be written to')

        self.aws_icons = AWS_Icons.AWS_Icons(AWS_ICON_PATH)

        self.configfile = os.path.join(self.OUT_PATH, 'puml.ini')
        self.config = configparser.ConfigParser()

        self.config.read(self.configfile)

        self.category_colors = self.config['Category.Colors']

        self.item_aliases = self.config['Item.Aliases']

        self.items = {}

        self.SOURCE_DIR = 'dist'
        self.TEST_DIR = 'test'
        self.LIB_DIR = 'lib'

    @property
    def OutputBasePath(self):
        """ For PlantUML scripts: the base path for PLANTUML_AWS """
        if self.env_var_set:
            return '%getenv("PLANTUML_AWS")'
        else:
            return '"{}"'.format(self.OUT_PATH)

    def write_ini(self):
        colors = {}
        for cat in self.aws_icons.iter_categories():
            colors[cat.name] = '#777777'

        self.category_colors = colors

        with open(self.configfile, 'w') as f:
            self.config.write(f)

    def filename(self, sub, name):
        """ returns a filename in a sub directory for PUML code """
        return os.path.join(self.OUT_PATH, sub, name+'.puml')

    def source_file(self, name):
        """ returns a filename for a file containing source code """
        return self.filename(self.SOURCE_DIR, name)

    def test_file(self, name):
        """ returns a filename for a file containing source code """
        return self.filename(self.TEST_DIR, name)

    def lib_file(self, name):
        """ returns a filename for a file containing source code """
        return self.filename(os.path.join(self.SOURCE_DIR, self.LIB_DIR), name)


    def iter_categories(self):
        for cat in self.aws_icons.iter_categories():
            yield PUML_Category(self, cat, self.category_colors[cat.name])

    def process_categories(self):
        with open(self.source_file('all'), 'w') as all:
            for pu_cat in self.iter_categories():
                pu_cat.write()
                all.write(pu_cat.include + '\n')

    def add_item(self, item):
        self.items[item.name] = item

    def process_aliases(self):
        with open(self.source_file('aliases'), 'w') as aliases:

            print ('\nProcessing aliases:')

            for ia in sorted(self.item_aliases.items()):                   
                aliases.write(
                    """
!includesub {macro_include}
!function {alias}($id, $label="")
{function}($id, $label)
!endfunction\n\n""".format(
                        alias = ia[0].upper(),
                        function = ia[1],
                        macro_include = self.items[ia[1]].include 
                    )
                )

    def make_includes(self):
        """ Generates a file containing the include statements for the items """
        with open(self.source_file('includes') ,'w') as f:
            for cat in self.iter_categories():
                f.write('!define Category__{name} {filename}\n'.format(name=cat.clean_name, filename=cat.relative_filename))
            for (k,item) in sorted(self.items.items()):
                f.write(f'!define Item__{item.name} {item.include}\n')



if __name__ == '__main__':
    # Commented out, this value comes from env var PLANTUML_AWS
    # AWS_PLANTUML=r'D:\Software\plantuml\AWS-PlantUML-new'
    AWS_PLANTUML = None

    aws_icons = AWS_Icons.AWS_Icons()

    PU = PlantUML(AWS_PLANTUML)

    if False:
        cat = AWS_Icons.AWS_Category(aws_icons, 'Game Tech')
        pu_cat = PUML_Category(PU, cat, '#693CC5')

        for f in cat.get_files():
            print(f)

        print('\nItems:')
        for i in pu_cat.items():
            print(i.name)


        pu_cat.write()

    PU.process_categories()        
    PU.process_aliases()
    PU.make_includes()