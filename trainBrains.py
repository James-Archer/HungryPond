# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 15:06:08 2018

@author: James

Gets some basic brains going

"""

import pond
import numpy as np
import matplotlib.pyplot as plt

def getLifetime(org, t):
    
    if org.deathday:
        return org.deathday - org.birthday
    else:
        return t - org.birthday
    
def getLongestLifetime(orgs, t):
    
    longestLiving = orgs[0]
    lifetime = 0
    for i in orgs[1:]:
        if getLifetime(i, t) > lifetime:
            lifetime = getLifetime(i, t)
            longestLiving = i
    return longestLiving
    
if __name__=='__main__':
    

    lifetime = []
    stdevLT = []
    maxLT = []
    
    for i in range(10):
        print(i)
        p = pond.Pond(10)
        if i != 0:
            for org in p.orgs:
                org.loadBrain(f'brain{i-1}')
        else:
            for org in p.orgs:
                org.loadBrain('first_run/brain9')
        p.runForN(10000)
        getLongestLifetime(p.orgs + p.deadOrgs, p.t).saveBrain(f"brain{i}")
            
        lifetimes = [getLifetime(i, p.t) for i in p.orgs]
        lifetimes += [getLifetime(i, p.t) for i in p.deadOrgs]
        lifetime.append(np.average(lifetimes))
        stdevLT.append(np.std(lifetimes))
        maxLT.append(max(lifetimes))

    
    plt.errorbar(list(range(10)), lifetime, stdevLT)
    plt.plot(list(range(10)), maxLT)
    plt.show()