## Description

Northern Arizona University Department of Mathematics & Statistics Research Showcase is dedicated to developing a web-based platform for Northern Arizona University's Department of Mathematics & Statistics. This platform aims to organize, archive, and showcase student research, particularly senior capstone projects, with potential expansions for additional research and other departments.

## Architecture

Present a diagram of the high-level architecture

Links to an external site. of your system. Use a UML package diagram to describe the main modules and how they interrelate. See some examples at:

https://www.uml-diagrams.org/package-diagrams-examples.html

Links to an external site.

Make clear the layers of your architecture (if they exist) as described in:

https://www.uml-diagrams.org/multi-layered-application-uml-model-diagram-example.html

Links to an external site.

Links to an external site.Provide a brief rationale of your architecture explaining why you designed it that way. 

### UML Package Diagram

![UML Package Diagram](./images/UML-package-diagram.svg)

Grading criteria (5 points): Adequate use of UML; Adequate design of an architecture for the system; Adequate description of the rationale.


## Class Diagrams

Present a refined class diagram of your system, including implementation details such as visibilities, attributes to represent associations, attribute types, return types, parameters, etc. The class diagram should match the code you have produced so far, but not be limited to it (e.g., it can contain classes not implemented yet). 

The difference between this class diagram and the one that you presented in D.3 is that the last focuses on the conceptual model of the domain while the former reflects the implementation. Therefore, the implementation details are relevant in this case. 

### Refined Class Diagram

![UML Class Diagram](./images/Design-UML.drawio.svg) 

Grading criteria (6 points): Adequate use of UML; Adequate choice of classes and relationships; Completeness of the diagram; Adequate presentation of implementation details. 

## Sequence Diagrams

Present a sequence diagram

Links to an external site. that represents how the objects in your system interact for a specific use case. Also include the use case's description in this section. The sequence diagram should be consistent with the class diagram and architecture. 

Grading criteria (5 points): Adequate use of UML; Adequate design of the sequence diagram; Consistency with the class diagram; Consistency with the use case description; Not including the use case description; Over simplistic diagram.


## Design Patterns

Split this section into 2 subsections. For each subsection, present a UML class diagram showing the application of a design pattern

Links to an external site. to your system (a different pattern for each section). Each class diagram should contain only the classes involved in the specific pattern (you don’t need to represent the whole system). Choose patterns from two different categories: Behavioral, Structural, and Creational. You are not limited to design patterns studied in class. 

Your system may not be appropriate for any design pattern. In this case, for didactic purposes, be creative and extend a little bit the scope of your system to make the design patterns appropriate. 

Implement each design pattern in your system and provide GitHub links to the corresponding classes. Example (the links are just illustrative):

    Car: https://github.com/user/repo/blob/master/src/com/proj/main/Car.java 

Links to an external site.
IBreakBehavior: https://github.com/user/repo/blob/master/src/com/proj/main/IBreakBehavior.java
Links to an external site.
BrakeWithABS: https://github.com/user/repo/blob/master/src/com/proj/main/BrakeWithABS.java
Links to an external site.
Brake: https://github.com/user/repo/blob/master/src/com/proj/main/Brake.java

    Links to an external site.

Grading criteria (6 points, 3 for each pattern): Correct use of the design pattern as described in the literature; Adequate choice of the design pattern; Adequate implementation of the design pattern.


## Design Principles

How does your design observe the SOLID principles? Provide a short description of followed principles giving concrete examples from your classes. 

Grading criteria (6 points): Show correct understanding of SOLID principles; Provide enough details to justify how the principles were observed.