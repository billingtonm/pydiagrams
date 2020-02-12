import os
import os.path
import subprocess

class GenerationException(Exception):
    pass

class RendererProgram:
    """ Base class for a program that can be called to render a diagram """
    def __init__(self, execute_args, commands=None, subprocess_params={}, help=None, version=None):
        """ subprocess_params = extra parameters passed to subprocess.run, eg: shell=True"""
        self.execute_args = execute_args
        self.subprocess_params = subprocess_params
        self.last_execute_process = None

        self.__commands__ = commands
        self.__command_cache__ = {}

        # Create functions for commands
        for command in commands:
            setattr(self, command, self.__command__(command))

        for (name, command) in [('help', help), ('version', version)]:
            if command:
                setattr(self, name, self.__command__(command))


    def execute(self, args):
        cmd = self.execute_args + args
        self.last_execute_process = subprocess.run(args=cmd, capture_output=True, universal_newlines=True, **self.subprocess_params)
        return self.last_execute_process


    def __command__(self, command):
        def execute_command():
            if not command in self.__command_cache__:
                self.__command_cache__[command] = self.do_command(command)
            return self.__command_cache__[command]
        return execute_command

    @staticmethod
    def build_args(*args, **kwargs):
        pass

    @staticmethod
    def output_format(format):
        pass

    def output_file(self, source, format):
        """ Return the option to specify the output filename and path """
        pass

    def do_command(self, *args, **kwargs):
        """ Executes a simple command, eg: help or version """
        args = self.build_args(*args, **kwargs)
        return self.execute(args)

    def file_command(self, file, *args, **kwargs):
        """ Executes a command that requires a source file """
        args =  self.build_args(*args, **kwargs) + [file]
        return self.execute(args)

    def generate(self, source, format, **kwargs):
        """ Generates a rendered version of the PUML source in the image format specified """
        result = self.file_command(source, self.output_format(format), *self.output_file(source, format), **kwargs)

        if result.returncode != 0:
            raise GenerationException(result.stderr)


class PlantUML(RendererProgram):
    COMMANDS = 'language printfonts testdot'.split()

    def __init__(self, plantuml_jar=None):
        self.plantuml_jar = plantuml_jar or os.getenv('PLANTUML_JAR')

        if not self.plantuml_jar:
            raise Exception('No PLANTUML_JAR specified. Set environment variable PLANTUML_JAR to the location of the PlantUML jar file')

        # '-Djava.awt.headless=true'
        execute_args = ['java', '-jar', self.plantuml_jar]

        super().__init__(
            execute_args,
            PlantUML.COMMANDS,
            subprocess_params=dict(shell=True),
            help='help',
            version='version'
            )

        self.ext= 'puml'

    @staticmethod
    def build_args(*args, **kwargs):
        a= ['-{}'.format(a) for a in args]
        for k,v in kwargs.items():
            a.append('-' + k)
            a.append(v)

        return a

    @staticmethod
    def output_format(format):
        return 't' + format


    def output_file(self, source, format):
        return {'output':'"{}"'.format(os.path.dirname(source))}

    def generate(self, source, format, **kwargs):
        """ Generates a rendered version of the PUML source in the image format specified """
        result = self.file_command(source, self.output_format(format), **self.output_file(source, format))

        if result.returncode != 0:
            raise GenerationException(result.stderr)
        
class Graphviz(RendererProgram):
    def __init__(self, gv_executable=None):
        self.gv_executable = gv_executable

        execute_args = [gv_executable]

        super().__init__(
            execute_args,
            [],
            subprocess_params=dict(shell=True),
            help='?',
            version='V'
            )

        self.ext = 'gv'

    @staticmethod
    def build_args(*args, **kwargs):
        return ['-{}'.format(a) for a in args] + ['-{}={}'.format(k,v) for k,v in list(kwargs.items())]

    @staticmethod
    def output_format(format):
        return 'T' + format

    def output_file(self, source, format):
        return ['o' + os.path.splitext(source)[0] + "." + format]


if __name__ == '__main__':
    R = PlantUML(r'D:\Software\plantuml\plantuml.jar')

    R = Graphviz(r'c:\Program Files (x86)\Graphviz2.38\bin\dot')
    
    try:
        gen=R.generate(r'C:\Users\billingtonm\Dropbox\Code\pydiagrams\pydiagrams\demos\AWS-demo.' + R.ext, 'png')
        print('Done!')
    except:
        print(R.last_execute_process.args)
        print(R.last_execute_process.stderr)
    