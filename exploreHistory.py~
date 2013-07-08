'''
Created on 8 Jul 2013

@author: James McInerney
'''

import json
import pickle
from matplotlib.pyplot import *

ROOT = '[path to directory where data is stored]'


def printWholeHistory(history):
    for item in history:
        print 'time',item['timestampMs'],'lat',item['latitude'],'lng',item['longitude'],'accuracy','%i meters'%item['accuracy']
        
h = pickle.load(open(ROOT + 'loc_history.p','r'))
print 'len h',len(h)

#find out how many are high accuracy readings (defined as being <40 m accuracy)
accThres = 40
ha = [h0 for h0 in h if 'accuracy' in h0 and int(h0['accuracy'])<accThres]
print '# readings with < %i acc'%accThres, len(ha)

