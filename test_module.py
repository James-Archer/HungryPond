# -*- coding: utf-8 -*-
"""
Created on Fri Mar  9 14:33:02 2018

@author: jia335
"""

import pond as p
from math import tan

simple_pond = p.Pond(0)
simple_pond.food = []

coords = [[750, 750], [250, 250], [250, 750], [750, 250]]
for coord in coords:
    simple_pond.food.append(p.Food(pos = {'x': coord[0], 'y': coord[1]}))
    
o = p.Organism(simple_pond)
o.brain = p.brains['Naive Brain']
o.pos = {'x': 600, 'y': 600}
simple_pond.orgs.append(o)

def test_naivebrain():
    
    initial = dict(simple_pond.orgs[0].pos)
    simple_pond.step()
    final = simple_pond.orgs[0].pos
    print(initial, final)
    
    delta = [final['x'] - initial['x'], final['y'] - initial['y']]
    assert tan((750 - initial['y'])/(750 - initial['x'])) == tan(delta[1]/delta[0])