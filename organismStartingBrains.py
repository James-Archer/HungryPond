# -*- coding: utf-8 -*-
"""
Created on Tue Mar  6 14:14:54 2018

@author: jia335

Some default brains to start with

"""

import neuralnetwork as NN

'''
The basic brain I used at the start. Not very clever.
'''
simpleBrain = NN.Network()
simpleBrain.createNetwork([3,2],[2,2])

'''
Moves towards nearest food (hopefully)
'''
naiveBrain = NN.Network()
naiveBrain.addInputs(3)
naiveBrain.addOutputs(2)
naiveBrain.addSynapse(naiveBrain.inputs[1], naiveBrain.outputs[1])
naiveBrain.addSynapse(naiveBrain.inputs[0], naiveBrain.outputs[0])
for syn in naiveBrain.synapses:
    syn.weight = 1
for out in naiveBrain.outputs:
    out.type = 'Sum'


brains = {'Simple Brain': simpleBrain,
          'Naive Brain': naiveBrain
        }