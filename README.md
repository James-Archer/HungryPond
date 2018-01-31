# HungryPond
Simulation of mini-organism evolution using a home-made neural network. The neural net (https://github.com/James-Archer/NeuralNetwork) sorta works, in that it seems to do what I want for this purpose. The network is quite simple, and the "learning" is done by survivability and reproduction in the environment.

Running *guiPlayer.py* should give a very simple visualisation of what's going on.

Currently the features of the simulation are moving and eating. The organisms die, bounce off walls, "think" and eat. The food is consumed and currently not replensished.

To do:
* Add reproduction.
* Add regrowth of food.
* Add carnivorous features.
* Expand the inputs to the network (perhaps they can evolve to include more inputs, such as nearest organism info).
* Player - show world and organism info.
