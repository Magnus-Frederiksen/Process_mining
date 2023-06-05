#from datetime import datetime
#import xml.etree.ElementTree as ET
import graphviz as pgv
#from collections import defaultdict
import reactivex as rx
from reactivex import create
from reactivex import operators as op
#import json
#from pybeamline import bevent
import sys

from pybeamline.sources import xes_log_source_from_file
#from pybeamline.mappers import sliding_window_to_log
import Process_Discovery
import Conformance_Checking

import time

#source of events
source = xes_log_source_from_file("XES-files\display.xes")

#Lossy Count
# new_LC = Process_Discovery.Lossy_count()
# new_LC.setMax_approx_error(0.01)
# new_LC.setPrintRefreshRate(32)
# new_LC.subscribe(source)
#HM_LC
new_HM_LC = Process_Discovery.HM_LC(max_approx_error=0.01, dependency_threshold=0.7, and_threshold=0.6)
new_HM_LC.setModelRefreshRate(5) #by default is 1/max_approx_error
new_HM_LC.setLabel('Time') #by default is Frequency
new_HM_LC.setFileName('test')
new_HM_LC.setlabelRounder(2)
new_HM_LC.subscribe(source)

# start_time = time.time()
# print("--- %s seconds ---" % (time.time() - start_time))
# 26220
#


# #HM_LCB
# new_HM_LCB = Process_Discovery.HM_LCB(20, 0.4, 0.4)
# new_HM_LCB.setModelRefreshRate(3) #by default is 1
# new_HM_LCB.setLabel('Dependency') #by default is Frequency
# new_HM_LCB.setlabelRounder(2) #by default is 2
# new_HM_LCB.setFileName('test_miner_for_HM_LCB') #by default is HM_LC
# new_HM_LCB.subscribe(source)
#
# #own model for conformance checking
# Model one
# B = []
# B.append(('A','B'))
# B.append(('B','C'))
# B.append(('B','D'))
# B.append(('C','D'))
# B.append(('C','E'))
# B.append(('D','E'))
# B.append(('D','F'))
# B.append(('E','F'))
#
# P = dict()
# P[('A','B')] = (0,0)
# P[('B','C')] = (1,1)
# P[('B','D')] = (1,1)
# P[('C','D')] = (2,2)
# P[('C','E')] = (2,2)
# P[('D','E')] = (2,3)
# P[('D','F')] = (2,3)
# P[('E','F')] = (3,4)
#
# F = dict()
# F[('A','B')] = 2
# F[('B','C')] = 2
# F[('B','D')] = 1
# F[('C','D')] = 1
# F[('C','E')] = 1
# F[('D','E')] = 1
# F[('D','F')] = 0
# F[('E','F')] = 0
#
# M = (B,P,F)

# Model 2
# B = []
# B.append(('A','B1'))
# B.append(('B1','C'))
# B.append(('B1','B2'))
# B.append(('B2','B3'))
# B.append(('B3','B1'))
# B.append(('B2','E'))
# B.append(('C','D'))
# B.append(('D','C'))
# B.append(('D','E'))
# B.append(('E','F'))
# #
# P = dict()
# P[('A','B1')] = (0,0)
# P[('B1','C')] = (1,4)
# P[('B1','B2')] = (1,4)
# P[('B2','B3')] = (2,4)
# P[('B3','B1')] = (3,4)
# P[('B2','E')] = (2,4)
# P[('C','D')] = (2,7)
# P[('D','C')] = (3,7)
# P[('D','E')] = (3,7)
# P[('E','F')] = (3,8)
# #
# F = dict()
# F[('A','B1')] = 3
# F[('B1','C')] = 3
# F[('B1','B2')] = 2
# F[('B2','B3')] = 4
# F[('B3','B1')] = 3
# F[('B2','E')] = 1
# F[('C','D')] = 2
# F[('D','C')] = 3
# F[('D','E')] = 1
# F[('E','F')] = 0
# #
# M = (B,P,F)

# conformance_checking = Conformance_Checking.CC_BH()
# conformance_checking.setM_FromXES('XES-files/example.xes')

# start_time = time.time()
# print("--- %s seconds ---" % (time.time() - start_time))

# conformance_checking.subscribe(source)
#
# conformance_checking.printRefModel()


# conformance_checking.subscribe(source)

# Print Stream
# source.subscribe(
#     on_next=lambda i: {
#         print(i)
#     },
#     on_error=lambda e, l: print("Error Occurred: {0} to {1}".format(e, l)),
#     on_completed=lambda: print("done"),
# )