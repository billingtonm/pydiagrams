# pydiagrams

pydiagrams is a tool to generate software diagrams by using Python as a DSL.
pydiagrams providers a framework for describing a software diagram as python code, and translating into it source code specific to a rendering program.

It can generate the following types of diagrams:
* Flowcharts
* Database "View" diagrams / Data flow diagrams
* UML Component diagrams
* Integration Architecture diagrams

These diagrams are can be generated via a choice of rendering programs:
* [PlantUML](https://plantuml.com/)
* [Graphviz](https://graphviz.org/)
* [yEd (as GraphML)](https://www.yworks.com/products/yed)
* [Blockdiag](http://blockdiag.com/en/)

## Motivation
Diagram generation languages (such as PlantUML, Graphviz, Blockdiag) provide general-purpose diagrams, but require the user to learn a specific syntax. 
They each have certain strengths and weaknesses that sometimes require switching from one format to another.
pydiagrams instead provides a simple python-DSL that allows the user to write a single diagram that is can then be translated into the rendering program of choice.
