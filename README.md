# FabControl 3D Printing Materials Testing Framework
FabControl 3D Printing Materials Testing Framework and Gcode generation software repository.

**List of objects:**

`Project`: Used to describe a test Project. Contains all other objects. Has a name, an ID, a list of `Tests[]`, a list of `Machines[]` and a `Material`. Has `getID()` and `print()` methods.

`Material`: Used to describe a test material. Has a name, and ID, a diameter, and a speed ratio - a material specific extrusion multiplier. Has a `print()` method.

`Machine`: Used to describe a machine configuration on which is used to print the tests. Has an ID, a nozzle diameter, a nozzle type, a maker and a model. Has a `getID()` and a `print()` method.

`Test`: Used to describe a set of test tasks. Has an ID, a name, a list of `Tasks[]` and amount of iterations, used to populate the `Tasks[]` list. Has a `print()` method.

`TestSample`: Used to describe an individual test task. Holds reference to parent `Project`, `Machine`, `Material`, `Test`, has a test context ID, an iteration ID, gcode preperation status, a print status, and a global ID, constructed upon instancing. Has `getID()`, `debugPing()` and `print()` methods.

**List of methods:**

`populate(Project)`: a method to generate the test task population. Called once all the variables (machines, tests, materials) have been declared.

`addTest(Project, name, iterations)`: a method to add a test to a project's `Tests[]` list.

`addMachine(Project, ID, diameter, nozzleType, maker, model)`: a method to add a machine to a project's `Machines[]` list.

See [wiki](https://bitbucket.org/MassPortal/material-test-framework/wiki/Home) for a more detailed description!