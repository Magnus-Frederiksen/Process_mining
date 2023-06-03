import sys
import unittest
from pybeamline.sources import xes_log_source_from_file
import Process_Discovery
import Conformance_Checking

class process_mining_test(unittest.TestCase):

    def test_Lossy_Counting_1(self):
        source = xes_log_source_from_file("XES-files\ABCD.xes") #source
        test_LC = Process_Discovery.Lossy_count(0.001) #conditions, dependendecy, and 'and' Threshold will not be needed
        test_LC.setPrintRefreshRate(sys.maxsize)  #dont need to print model
        test_LC.subscribe(source)
        eventList = test_LC.getEvents()

        expected_events = dict()
        expected_events['A'] = (1, 0)
        expected_events['B'] = (1, 0)
        expected_events['C'] = (1, 0)
        expected_events['D'] = (1, 0)

        for event, (frequency,bucket) in eventList.items():
            if event in expected_events:
                self.assertEqual(expected_events[event][0], frequency)  # check if its eventName is correct
                self.assertEqual(expected_events[event][1], bucket)  # check if its frequency is correct
                del expected_events[event]  # removed the expected element in case the caseID is repeated in some way
            else:
                print("case ID: {0}, was not expected".format(caseID))
                self.assertTrue(False)  #the caseID was not expected

        if len(expected_events) > 0:#unobserved expected events
            for event in expected_events: #print unobserved event
                print("event {0} is missing".format(event))
            self.assertTrue(False)  # the caseID was not expected

    def test_Lossy_Counting_2(self):
        source = xes_log_source_from_file("XES-files\LC-test.xes") #source
        test_LC = Process_Discovery.Lossy_count(0.01) #conditions, dependendecy, and 'and' Threshold will not be needed
        test_LC.setPrintRefreshRate(sys.maxsize)  #dont need to print model
        test_LC.subscribe(source)
        eventList = test_LC.getEvents()

        expected_events = dict()
        expected_events['A'] = (6, 0)
        expected_events['B1'] = (2, 0)
        expected_events['B2'] = (3, 0)
        expected_events['C'] = (6, 0)
        expected_events['D'] = (5, 0)
        expected_events['E'] = (6, 0)
        expected_events['F'] = (4, 0)

        for event, (frequency,bucket) in eventList.items():
            if event in expected_events: # check if its eventName is correct
                self.assertEqual(expected_events[event][0], frequency) # check if its frequency is correct
                self.assertEqual(expected_events[event][1], bucket)  # check if its bucket is correct
                del expected_events[event]  # removed the expected element in case the caseID is repeated in some way
            else:
                print("case ID: {0}, was not expected".format(caseID))
                self.assertTrue(False)  #the caseID was not expected

        if len(expected_events) > 0:#unobserved expected events
            for event in expected_events: #print unobserved event
                print("event {0} is missing".format(event))
            self.assertTrue(False)  # the caseID was not expected

    def test_Lossy_Counting_3(self):
        source = xes_log_source_from_file("XES-files\LC-test.xes") #source
        test_LC = Process_Discovery.Lossy_count(0.2) #conditions, dependendecy, and 'and' Threshold will not be needed
        test_LC.setPrintRefreshRate(sys.maxsize)  #dont need to print model
        test_LC.subscribe(source)
        eventList = test_LC.getEvents()

        expected_events = dict()
        expected_events['C'] = (5, 2)
        expected_events['D'] = (4, 3)
        expected_events['E'] = (5, 4)
        expected_events['F'] = (2, 6)

        for event, (frequency,bucket) in eventList.items():
            if event in expected_events: # check if its eventName is correct
                self.assertEqual(expected_events[event][0], frequency) # check if its frequency is correct
                self.assertEqual(expected_events[event][1], bucket)  # check if its bucket is correct
                del expected_events[event]  # removed the expected element in case the caseID is repeated in some way
            else:
                print("case ID: {0}, was not expected".format(caseID))
                self.assertTrue(False)  #the caseID was not expected

        if len(expected_events) > 0:#unobserved expected events
            for event in expected_events: #print unobserved event
                print("event {0} is missing".format(event))
            self.assertTrue(False)  # the caseID was not expected

    def test_Lossy_Counting_4(self):
        source = xes_log_source_from_file("XES-files\LC-test.xes") #source
        test_LC = Process_Discovery.Lossy_count(0.125) #conditions, dependendecy, and 'and' Threshold will not be needed
        test_LC.setPrintRefreshRate(sys.maxsize)  #dont need to print model
        test_LC.subscribe(source)
        eventList = test_LC.getEvents()

        expected_events = dict()
        expected_events['A'] = (6, 0)
        expected_events['C'] = (6, 1)
        expected_events['D'] = (5, 1)
        expected_events['E'] = (6, 2)
        expected_events['F'] = (4, 3)

        for event, (frequency,bucket) in eventList.items():
            if event in expected_events: # check if its eventName is correct
                self.assertEqual(expected_events[event][0], frequency) # check if its frequency is correct
                self.assertEqual(expected_events[event][1], bucket)  # check if its bucket is correct
                del expected_events[event]  # removed the expected element in case the caseID is repeated in some way
            else:
                print("case ID: {0}, was not expected".format(caseID))
                self.assertTrue(False)  #the caseID was not expected

        if len(expected_events) > 0:#unobserved expected events
            for event in expected_events: #print unobserved event
                print("event {0} is missing".format(event))
            self.assertTrue(False)  # the caseID was not expected

    def test_HM_LC_1(self):
        source = xes_log_source_from_file("XES-files\ABCD.xes") #source
        test_HM_LC = Process_Discovery.HM_LC(0.01, 0, 0) #conditions, dependendecy, and 'and' Threshold will not be needed
        test_HM_LC.setModelRefreshRate(sys.maxsize)  #dont need to print model
        test_HM_LC.subscribe(source)
        D_C = test_HM_LC.getD_C()

        expected_DC = dict() #the expected dictionary of stored events
        expected_DC['100'] = ('D', 4, 0)

        for caseID, (eventName, frequency, bucket, date) in D_C.items(): #for all currently saved caseID's
            if caseID in expected_DC: #if the caseID is expected to be present
                self.assertEqual(expected_DC[caseID][0], eventName) #check if its eventName is correct
                self.assertEqual(expected_DC[caseID][1], frequency) #check if its frequency is correct
                self.assertEqual(expected_DC[caseID][2], bucket) #check if its bucket of discovery is correct
                del expected_DC[caseID] #removed the expected element in case the caseID is repeated in some way
            else:
                print("case ID: {0}, was not expected".format(caseID))
                self.assertTrue(False)  #the caseID was not expected

        if len(expected_DC) > 0: #unobserved expected caseIDs
            for caseID in expected_DC: #print unobserved caseIDs
                print("event {0} is missing".format(caseID))
            self.assertTrue(False)


        D_R = test_HM_LC.getD_R()

        expected_DR = dict() #the expected dictionary of stored events
        expected_DR[('A', 'B')] = (1, 0)
        expected_DR[('B', 'C')] = (1, 0)
        expected_DR[('C', 'D')] = (1, 0)

        for relation, (frequency, bucket, time) in D_R.items(): #for all currently saved relation's
            if relation in expected_DR: #if the relation is expected to be present
                self.assertEqual(expected_DR[relation][0], frequency) #check if its frequency is correct
                self.assertEqual(expected_DR[relation][1], bucket) #check if its bucket of discovery is correct
                del expected_DR[relation] #removed the expected element in case the relation is repeated in some way
            else:
                print("case ID: {0}, was not expected".format(relation))
                self.assertTrue(False)  #the relation was not expected

        if len(expected_DR) > 0: #unobserved expected relations
            for relation in expected_DR: #print unobserved relations
                print("event {0} is missing".format(relation))
            self.assertTrue(False)  # the relation was not expecte

    def test_HM_LC_2(self):
        source = xes_log_source_from_file("XES-files\LC-test.xes") #source
        test_HM_LC = Process_Discovery.HM_LC(0.01, 0, 0) #conditions, dependendecy, and 'and' Threshold will not be needed
        test_HM_LC.setModelRefreshRate(sys.maxsize)  #dont need to print model
        test_HM_LC.subscribe(source)
        D_C = test_HM_LC.getD_C()

        expected_DC = dict() #the expected dictionary of stored events
        expected_DC['100'] = ('F', 5, 0)
        expected_DC['101'] = ('E', 5, 0)
        expected_DC['102'] = ('F', 6, 0)
        expected_DC['103'] = ('E', 5, 0)
        expected_DC['104'] = ('F', 5, 0)
        expected_DC['105'] = ('F', 6, 0)

        for caseID, (eventName, frequency, bucket, date) in D_C.items(): #for all currently saved caseID's
            if caseID in expected_DC: #if the caseID is expected to be present
                self.assertEqual(expected_DC[caseID][0], eventName) #check if its eventName is correct
                self.assertEqual(expected_DC[caseID][1], frequency) #check if its frequency is correct
                self.assertEqual(expected_DC[caseID][2], bucket) #check if its bucket of discovery is correct
                del expected_DC[caseID] #removed the expected element in case the caseID is repeated in some way
            else:
                print("case ID: {0}, was not expected".format(caseID))
                self.assertTrue(False)  #the caseID was not expected

        if len(expected_DC) > 0: #unobserved expected caseIDs
            for caseID in expected_DC: #print unobserved caseIDs
                print("event {0} is missing".format(caseID))
            self.assertTrue(False)


        D_R = test_HM_LC.getD_R()

        expected_DR = dict() #the expected dictionary of stored events
        expected_DR[('A', 'B2')] = (3, 0)
        expected_DR[('A', 'B1')] = (2, 0)
        expected_DR[('B1', 'C')] = (2, 0)
        expected_DR[('B2', 'C')] = (3, 0)
        expected_DR[('C', 'D')] = (5, 0)
        expected_DR[('C', 'E')] = (1, 0)
        expected_DR[('D', 'E')] = (5, 0)
        expected_DR[('A', 'C')] = (1, 0)
        expected_DR[('E', 'F')] = (4, 0)

        for relation, (frequency, bucket, time) in D_R.items(): #for all currently saved relation's
            if relation in expected_DR: #if the relation is expected to be present
                self.assertEqual(expected_DR[relation][0], frequency) #check if its frequency is correct
                self.assertEqual(expected_DR[relation][1], bucket) #check if its bucket of discovery is correct
                del expected_DR[relation] #removed the expected element in case the relation is repeated in some way
            else:
                print("case ID: {0}, was not expected".format(relation))
                self.assertTrue(False)  #the relation was not expected

        if len(expected_DR) > 0: #unobserved expected relations
            for relation in expected_DR: #print unobserved relations
                print("event {0} is missing".format(relation))
            self.assertTrue(False)  # the relation was not expecte

    def test_HM_LC_3(self):
        source = xes_log_source_from_file("XES-files\LC-test.xes") #source
        test_HM_LC = Process_Discovery.HM_LC(0.125, 0, 0) #conditions, dependendecy, and 'and' Threshold will not be needed
        test_HM_LC.setModelRefreshRate(sys.maxsize)  #dont need to print model
        test_HM_LC.subscribe(source)
        D_C = test_HM_LC.getD_C()

        expected_DC = dict() #the expected dictionary of stored events
        expected_DC['100'] = ('F', 5, 0)
        expected_DC['101'] = ('E', 5, 0)
        expected_DC['102'] = ('F', 5, 2)
        expected_DC['103'] = ('E', 4, 1)
        expected_DC['104'] = ('F', 4, 2)
        expected_DC['105'] = ('F', 6, 0)

        for caseID, (eventName, frequency, bucket, date) in D_C.items(): #for all currently saved caseID's
            if caseID in expected_DC: #if the caseID is expected to be present
                self.assertEqual(expected_DC[caseID][0], eventName) #check if its eventName is correct
                self.assertEqual(expected_DC[caseID][1], frequency) #check if its frequency is correct
                self.assertEqual(expected_DC[caseID][2], bucket) #check if its bucket of discovery is correct
                del expected_DC[caseID] #removed the expected element in case the caseID is repeated in some way
            else:
                print("case ID: {0}, was not expected".format(caseID))
                self.assertTrue(False)  #the caseID was not expected

        if len(expected_DC) > 0: #unobserved expected caseIDs
            for caseID in expected_DC: #print unobserved caseIDs
                print("event {0} is missing".format(caseID))
            self.assertTrue(False)


        D_R = test_HM_LC.getD_R()

        expected_DR = dict() #the expected dictionary of stored events
        # expected_DR[('A', 'B2')] = (3, 0)
        # expected_DR[('A', 'B1')] = (2, 0)
        # expected_DR[('B1', 'C')] = (2, 0)
        # expected_DR[('B2', 'C')] = (3, 1)
        expected_DR[('C', 'D')] = (5, 1)
        # expected_DR[('C', 'E')] = (1, 0)
        expected_DR[('D', 'E')] = (5, 2)
        # expected_DR[('A', 'C')] = (1, 0)
        expected_DR[('E', 'F')] = (4, 3)

        for relation, (frequency, bucket, time) in D_R.items(): #for all currently saved relation's
            if relation in expected_DR: #if the relation is expected to be present
                self.assertEqual(expected_DR[relation][0], frequency) #check if its frequency is correct
                self.assertEqual(expected_DR[relation][1], bucket) #check if its bucket of discovery is correct
                del expected_DR[relation] #removed the expected element in case the relation is repeated in some way
            else:
                print("case ID: {0}, was not expected".format(relation))
                self.assertTrue(False)  #the relation was not expected

        if len(expected_DR) > 0: #unobserved expected relations
            for relation in expected_DR: #print unobserved relations
                print("event {0} is missing".format(relation))
            self.assertTrue(False)  # the relation was not expecte

    def test_HM_LC_4(self):
        source = xes_log_source_from_file("XES-files\LC-test.xes") #source
        test_HM_LC = Process_Discovery.HM_LC(0.1, 0, 0) #conditions, dependendecy, and 'and' Threshold will not be needed
        test_HM_LC.setModelRefreshRate(sys.maxsize)  #dont need to print model
        test_HM_LC.subscribe(source)
        D_C = test_HM_LC.getD_C()

        expected_DC = dict() #the expected dictionary of stored events
        expected_DC['100'] = ('F', 5, 0)
        expected_DC['101'] = ('E', 5, 0)
        expected_DC['102'] = ('F', 6, 1)
        expected_DC['103'] = ('E', 5, 0)
        expected_DC['104'] = ('F', 4, 2)
        expected_DC['105'] = ('F', 6, 0)

        for caseID, (eventName, frequency, bucket, date) in D_C.items(): #for all currently saved caseID's
            if caseID in expected_DC: #if the caseID is expected to be present
                self.assertEqual(expected_DC[caseID][0], eventName) #check if its eventName is correct
                self.assertEqual(expected_DC[caseID][1], frequency) #check if its frequency is correct
                self.assertEqual(expected_DC[caseID][2], bucket) #check if its bucket of discovery is correct
                del expected_DC[caseID] #removed the expected element in case the caseID is repeated in some way
            else:
                print("case ID: {0}, was not expected".format(caseID))
                self.assertTrue(False)  #the caseID was not expected

        if len(expected_DC) > 0: #unobserved expected caseIDs
            for caseID in expected_DC: #print unobserved caseIDs
                print("event {0} is missing".format(caseID))
            self.assertTrue(False)


        D_R = test_HM_LC.getD_R()

        expected_DR = dict() #the expected dictionary of stored events
        # expected_DR[('A', 'B2')] = (3, 0)
        # expected_DR[('A', 'B1')] = (2, 0)
        # expected_DR[('B1', 'C')] = (2, 0)
        expected_DR[('B2', 'C')] = (3, 1)
        expected_DR[('C', 'D')] = (5, 1)
        # expected_DR[('C', 'E')] = (1, 0)
        expected_DR[('D', 'E')] = (5, 2)
        # expected_DR[('A', 'C')] = (1, 0)
        expected_DR[('E', 'F')] = (4, 2)

        for relation, (frequency, bucket, time) in D_R.items(): #for all currently saved relation's
            if relation in expected_DR: #if the relation is expected to be present
                self.assertEqual(expected_DR[relation][0], frequency) #check if its frequency is correct
                self.assertEqual(expected_DR[relation][1], bucket) #check if its bucket of discovery is correct
                del expected_DR[relation] #removed the expected element in case the relation is repeated in some way
            else:
                print("case ID: {0}, was not expected".format(relation))
                self.assertTrue(False)  #the relation was not expected

        if len(expected_DR) > 0: #unobserved expected relations
            for relation in expected_DR: #print unobserved relations
                print("event {0} is missing".format(relation))
            self.assertTrue(False)  # the relation was not expecte


    def test_HM_LCB_1(self):
        source = xes_log_source_from_file("XES-files\ABCD.xes") #source
        test_HM_LCB = Process_Discovery.HM_LCB(100, 0, 0) #conditions, dependendecy, and 'and' Threshold will not be needed
        test_HM_LCB.setModelRefreshRate(sys.maxsize)  #dont need to print model
        test_HM_LCB.subscribe(source)
        D_C = test_HM_LCB.getD_C()

        expected_DC = dict() #the expected dictionary of stored events
        expected_DC['100'] = ('D', 4, 0)

        for caseID, (eventName, frequency, bucket, date) in D_C.items(): #for all currently saved caseID's
            if caseID in expected_DC: #if the caseID is expected to be present
                self.assertEqual(expected_DC[caseID][0], eventName) #check if its eventName is correct
                self.assertEqual(expected_DC[caseID][1], frequency) #check if its frequency is correct
                self.assertEqual(expected_DC[caseID][2], bucket) #check if its bucket of discovery is correct
                del expected_DC[caseID] #removed the expected element in case the caseID is repeated in some way
            else:
                print("case ID: {0}, was not expected".format(caseID))
                self.assertTrue(False)  #the caseID was not expected

        if len(expected_DC) > 0: #unobserved expected caseIDs
            for caseID in expected_DC: #print unobserved caseIDs
                print("event {0} is missing".format(caseID))
            self.assertTrue(False)


        D_R = test_HM_LCB.getD_R()

        expected_DR = dict() #the expected dictionary of stored events
        expected_DR[('A', 'B')] = (1, 0)
        expected_DR[('B', 'C')] = (1, 0)
        expected_DR[('C', 'D')] = (1, 0)

        for relation, (frequency, bucket, time) in D_R.items(): #for all currently saved relation's
            if relation in expected_DR: #if the relation is expected to be present
                self.assertEqual(expected_DR[relation][0], frequency) #check if its frequency is correct
                self.assertEqual(expected_DR[relation][1], bucket) #check if its bucket of discovery is correct
                del expected_DR[relation] #removed the expected element in case the relation is repeated in some way
            else:
                print("case ID: {0}, was not expected".format(relation))
                self.assertTrue(False)  #the relation was not expected

        if len(expected_DR) > 0: #unobserved expected relations
            for relation in expected_DR: #print unobserved relations
                print("event {0} is missing".format(relation))
            self.assertTrue(False)  # the relation was not expecte

    def test_HM_LCB_2(self):
        source = xes_log_source_from_file("XES-files\LC-test.xes") #source
        test_HM_LCB = Process_Discovery.HM_LCB(100, 0, 0) #conditions, dependendecy, and 'and' Threshold will not be needed
        test_HM_LCB.setModelRefreshRate(sys.maxsize)  #dont need to print model
        test_HM_LCB.subscribe(source)
        D_C = test_HM_LCB.getD_C()

        expected_DC = dict() #the expected dictionary of stored events
        expected_DC['100'] = ('F', 5, 0)
        expected_DC['101'] = ('E', 5, 0)
        expected_DC['102'] = ('F', 6, 0)
        expected_DC['103'] = ('E', 5, 0)
        expected_DC['104'] = ('F', 5, 0)
        expected_DC['105'] = ('F', 6, 0)

        for caseID, (eventName, frequency, bucket, date) in D_C.items(): #for all currently saved caseID's
            if caseID in expected_DC: #if the caseID is expected to be present
                self.assertEqual(expected_DC[caseID][0], eventName) #check if its eventName is correct
                self.assertEqual(expected_DC[caseID][1], frequency) #check if its frequency is correct
                self.assertEqual(expected_DC[caseID][2], bucket) #check if its bucket of discovery is correct
                del expected_DC[caseID] #removed the expected element in case the caseID is repeated in some way
            else:
                print("case ID: {0}, was not expected".format(caseID))
                self.assertTrue(False)  #the caseID was not expected

        if len(expected_DC) > 0: #unobserved expected caseIDs
            for caseID in expected_DC: #print unobserved caseIDs
                print("event {0} is missing".format(caseID))
            self.assertTrue(False)


        D_R = test_HM_LCB.getD_R()

        expected_DR = dict() #the expected dictionary of stored events
        expected_DR[('A', 'B2')] = (3, 0)
        expected_DR[('A', 'B1')] = (2, 0)
        expected_DR[('B1', 'C')] = (2, 0)
        expected_DR[('B2', 'C')] = (3, 0)
        expected_DR[('C', 'D')] = (5, 0)
        expected_DR[('C', 'E')] = (1, 0)
        expected_DR[('D', 'E')] = (5, 0)
        expected_DR[('A', 'C')] = (1, 0)
        expected_DR[('E', 'F')] = (4, 0)

        for relation, (frequency, bucket, time) in D_R.items(): #for all currently saved relation's
            if relation in expected_DR: #if the relation is expected to be present
                self.assertEqual(expected_DR[relation][0], frequency) #check if its frequency is correct
                self.assertEqual(expected_DR[relation][1], bucket) #check if its bucket of discovery is correct
                del expected_DR[relation] #removed the expected element in case the relation is repeated in some way
            else:
                print("case ID: {0}, was not expected".format(relation))
                self.assertTrue(False)  #the relation was not expected

        if len(expected_DR) > 0: #unobserved expected relations
            for relation in expected_DR: #print unobserved relations
                print("event {0} is missing".format(relation))
            self.assertTrue(False)  # the relation was not expecte

    def test_HM_LCB_3(self):
        source = xes_log_source_from_file("XES-files\LC-test.xes") #source
        test_HM_LCB = Process_Discovery.HM_LCB(budget=10, and_threshold=0, dependency_threshold=0) #conditions, dependendecy, and 'and' Threshold will not be needed
        test_HM_LCB.setModelRefreshRate(sys.maxsize)  #dont need to print model
        test_HM_LCB.subscribe(source)
        D_C = test_HM_LCB.getD_C()

        expected_DC = dict() #the expected dictionary of stored events
        expected_DC['100'] = ('F', 5, 0)
        expected_DC['101'] = ('E', 5, 0)
        expected_DC['102'] = ('F', 6, 1)
        expected_DC['103'] = ('E', 5, 0)
        expected_DC['104'] = ('F', 4, 3)
        expected_DC['105'] = ('F', 6, 0)

        for caseID, (eventName, frequency, bucket, date) in D_C.items(): #for all currently saved caseID's
            if caseID in expected_DC: #if the caseID is expected to be present
                self.assertEqual(expected_DC[caseID][0], eventName) #check if its eventName is correct
                self.assertEqual(expected_DC[caseID][1], frequency) #check if its frequency is correct
                self.assertEqual(expected_DC[caseID][2], bucket) #check if its bucket of discovery is correct
                del expected_DC[caseID] #removed the expected element in case the caseID is repeated in some way
            else:
                print("case ID: {0}, with event: {1}, frequency: {2} and, bucket: {3} was not expected".format(caseID,eventName,frequency,bucket))
                self.assertTrue(False)  #the caseID was not expected

        if len(expected_DC) > 0: #unobserved expected caseIDs
            for caseID in expected_DC: #print unobserved caseIDs
                print("event {0} is missing".format(caseID))
            self.assertTrue(False)


        D_R = test_HM_LCB.getD_R()

        expected_DR = dict() #the expected dictionary of stored events
        # expected_DR[('A', 'B2')] = (3, 0)
        # expected_DR[('A', 'B1')] = (1, 1)
        # expected_DR[('B1', 'C')] = (1, 1)
        # expected_DR[('B2', 'C')] = (3, 0)
        expected_DR[('C', 'D')] = (2, 3)
        # expected_DR[('C', 'E')] = (1, 2)
        expected_DR[('D', 'E')] = (4, 3)
        # expected_DR[('A', 'C')] = (1, 7)
        expected_DR[('E', 'F')] = (4, 3)

        for relation, (frequency, bucket, time) in D_R.items(): #for all currently saved relation's
            if relation in expected_DR: #if the relation is expected to be present
                self.assertEqual(expected_DR[relation][0], frequency) #check if its frequency is correct
                self.assertEqual(expected_DR[relation][1], bucket) #check if its bucket of discovery is correct
                del expected_DR[relation] #removed the expected element in case the relation is repeated in some way
            else:
                print("case ID: {0}, was not expected".format(relation))
                self.assertTrue(False)  #the relation was not expected

        if len(expected_DR) > 0: #unobserved expected relations
            for relation in expected_DR: #print unobserved relations
                print("event {0} is missing".format(relation))
            self.assertTrue(False)  # the relation was not expecte

    def test_HM_LCB_4(self):
        source = xes_log_source_from_file("XES-files\LC-test-2.xes") #source
        test_HM_LCB = Process_Discovery.HM_LCB(budget=8, and_threshold=0, dependency_threshold=0) #conditions, dependendecy, and 'and' Threshold will not be needed
        test_HM_LCB.setModelRefreshRate(sys.maxsize)  #dont need to print model
        test_HM_LCB.subscribe(source)
        D_C = test_HM_LCB.getD_C()

        expected_DC = dict() #the expected dictionary of stored events
        expected_DC['100'] = ('F', 5, 0)
        expected_DC['101'] = ('E', 5, 0)
        expected_DC['102'] = ('F', 5, 1)
        expected_DC['103'] = ('E', 5, 0)

        for caseID, (eventName, frequency, bucket, date) in D_C.items(): #for all currently saved caseID's
            if caseID in expected_DC: #if the caseID is expected to be present
                self.assertEqual(expected_DC[caseID][0], eventName) #check if its eventName is correct
                self.assertEqual(expected_DC[caseID][1], frequency) #check if its frequency is correct
                self.assertEqual(expected_DC[caseID][2], bucket) #check if its bucket of discovery is correct
                del expected_DC[caseID] #removed the expected element in case the caseID is repeated in some way
            else:
                print("case ID: {0}, with event: {1}, frequency: {2} and, bucket: {3} was not expected".format(caseID,eventName,frequency,bucket))
                self.assertTrue(False)  #the caseID was not expected

        if len(expected_DC) > 0: #unobserved expected caseIDs
            for caseID in expected_DC: #print unobserved caseIDs
                print("event {0} is missing".format(caseID))
            self.assertTrue(False)


        D_R = test_HM_LCB.getD_R()

        expected_DR = dict() #the expected dictionary of stored events
        # expected_DR[('A', 'B2')] = (2, 0)
        # expected_DR[('A', 'B1')] = (1, 0)
        # expected_DR[('B1', 'C')] = (1, 1)
        # expected_DR[('B2', 'C')] = (2, 0)
        expected_DR[('C', 'D')] = (3, 1)
        expected_DR[('C', 'E')] = (1, 2)
        expected_DR[('D', 'E')] = (3, 2)
        # expected_DR[('A', 'C')] = (1, 7)
        expected_DR[('E', 'F')] = (2, 2)

        for relation, (frequency, bucket, time) in D_R.items(): #for all currently saved relation's
            if relation in expected_DR: #if the relation is expected to be present
                self.assertEqual(expected_DR[relation][0], frequency) #check if its frequency is correct
                self.assertEqual(expected_DR[relation][1], bucket) #check if its bucket of discovery is correct
                del expected_DR[relation] #removed the expected element in case the relation is repeated in some way
            else:
                print("case ID: {0}, was not expected".format(relation))
                self.assertTrue(False)  #the relation was not expected

        if len(expected_DR) > 0: #unobserved expected relations
            for relation in expected_DR: #print unobserved relations
                print("event {0} is missing".format(relation))
            self.assertTrue(False)  # the relation was not expecte

    def test_CC_BP_1(self):
        B = []
        B.append(('A','B'))
        B.append(('B','C'))
        B.append(('C','D'))

        P = dict()
        P[('A','B')] = (0, 0)
        P[('B','C')] = (1, 1)
        P[('C','D')] = (2, 2)

        F = dict()
        F[('A','B')] = 2
        F[('B','C')] = 1
        F[('C','D')] = 0

        M = (B,P,F)

        source = xes_log_source_from_file("XES-files\CC_BP_test1.xes")  # source
        test_CC_BP = Conformance_Checking.CC_BH(M)
        test_CC_BP.subscribe(source)

        conformance = test_CC_BP.getConformance()
        completeness = test_CC_BP.getCompleteness()
        confidence = test_CC_BP.getConfidence()

        expectedConformance = dict()
        expectedCompleteness = dict()
        expectedConfidence = dict()

        expectedConformance['100'] = 0.5
        expectedCompleteness['100'] = 1
        expectedConfidence['100'] = 0.5

        for caseID in expectedConformance:
            self.assertEqual(expectedConformance[caseID], conformance[caseID])
            self.assertEqual(expectedCompleteness[caseID], completeness[caseID])
            self.assertEqual(expectedConfidence[caseID], confidence[caseID])

    def test_CC_BP_2(self):
        B = []
        B.append(('A','B'))
        B.append(('B','C'))
        B.append(('B','D'))
        B.append(('C','D'))
        B.append(('C','E'))
        B.append(('D','E'))
        B.append(('D','F'))
        B.append(('E','F'))

        P = dict()
        P[('A','B')] = (0,0)
        P[('B','C')] = (1,1)
        P[('B','D')] = (1,1)
        P[('C','D')] = (2,2)
        P[('C','E')] = (2,2)
        P[('D','E')] = (2,3)
        P[('D','F')] = (2,3)
        P[('E','F')] = (3,4)

        F = dict()
        F[('A','B')] = 2
        F[('B','C')] = 2
        F[('B','D')] = 1
        F[('C','D')] = 1
        F[('C','E')] = 1
        F[('D','E')] = 1
        F[('D','F')] = 0
        F[('E','F')] = 0

        M = (B,P,F)

        source = xes_log_source_from_file("XES-files\CC_BP_test2.xes")  # source
        test_CC_BP = Conformance_Checking.CC_BH(M)
        test_CC_BP.subscribe(source)

        conformance = test_CC_BP.getConformance() #the extracted results
        completeness = test_CC_BP.getCompleteness()
        confidence = test_CC_BP.getConfidence()


        expectedConformance = dict() #the expected results
        expectedCompleteness = dict()
        expectedConfidence = dict()

        expectedConformance['100'] = 2/3
        expectedCompleteness['100'] = 1
        expectedConfidence['100'] = 1 - (1/2)

        expectedConformance['101'] = 4/7
        expectedCompleteness['101'] = 1
        expectedConfidence['101'] = 1

        expectedConformance['102'] = 1
        expectedCompleteness['102'] = 1
        expectedConfidence['102'] = 0

        expectedConformance['103'] = 0
        expectedCompleteness['103'] = -1
        expectedConfidence['103'] = -1

        expectedConformance['104'] = 0
        expectedCompleteness['104'] = -1
        expectedConfidence['104'] = -1

        expectedConformance['105'] = 0.5
        expectedCompleteness['105'] = 1
        expectedConfidence['105'] = 1

        for caseID in expectedConformance: #comparing by caseID
            self.assertEqual(expectedConformance[caseID], conformance[caseID])
            self.assertEqual(expectedCompleteness[caseID], completeness[caseID])
            self.assertEqual(expectedConfidence[caseID], confidence[caseID])

    def test_CC_BP_3(self):
        B = []
        B.append(('A','B1'))
        B.append(('B1','C'))
        B.append(('B1','B2'))
        B.append(('B2','B3'))
        B.append(('B3','B1'))
        B.append(('B2','E'))
        B.append(('C','D'))
        B.append(('D','C'))
        B.append(('D','E'))
        B.append(('E','F'))

        P = dict()
        P[('A','B1')] = (0,0)
        P[('B1','C')] = (1,4)
        P[('B1','B2')] = (1,4)
        P[('B2','B3')] = (2,4)
        P[('B3','B1')] = (3,4)
        P[('B2','E')] = (2,4)
        P[('C','D')] = (2,7)
        P[('D','C')] = (3,7)
        P[('D','E')] = (3,7)
        P[('E','F')] = (3,8)

        F = dict()
        F[('A','B1')] = 3
        F[('B1','C')] = 3
        F[('B1','B2')] = 2
        F[('B2','B3')] = 4
        F[('B3','B1')] = 3
        F[('B2','E')] = 1
        F[('C','D')] = 2
        F[('D','C')] = 3
        F[('D','E')] = 1
        F[('E','F')] = 0

        M = (B,P,F)

        source = xes_log_source_from_file("XES-files\CC_BP_test2.xes")  # source
        test_CC_BP = Conformance_Checking.CC_BH()
        test_CC_BP.setM(M)
        test_CC_BP.subscribe(source)

        conformance = test_CC_BP.getConformance() #the extracted results
        completeness = test_CC_BP.getCompleteness()
        confidence = test_CC_BP.getConfidence()

        expectedConformance = dict() #the expected results
        expectedCompleteness = dict()
        expectedConfidence = dict()

        expectedConformance['100'] = 1
        expectedCompleteness['100'] = 1
        expectedConfidence['100'] = 1 - (1/4)

        expectedConformance['101'] = 2/7
        expectedCompleteness['101'] = 0.5
        expectedConfidence['101'] = 1

        expectedConformance['102'] = 0
        expectedCompleteness['102'] = -1
        expectedConfidence['102'] = -1

        expectedConformance['103'] = 5/7
        expectedCompleteness['103'] = 1
        expectedConfidence['103'] = 1 - (1/4)

        expectedConformance['104'] = 1
        expectedCompleteness['104'] = 1/3
        expectedConfidence['104'] = 0

        expectedConformance['105'] = 5/6
        expectedCompleteness['105'] = 1
        expectedConfidence['105'] = 1

        for caseID in expectedConformance: #compare by caseID
            self.assertEqual(expectedConformance[caseID], conformance[caseID])
            self.assertEqual(expectedCompleteness[caseID], completeness[caseID])
            self.assertEqual(expectedConfidence[caseID], confidence[caseID])



    def test_XES_to_model_1(self):

        expectedB = [] #the expected relations in B
        expectedB.append(('A','B'))
        expectedB.append(('B','C'))
        expectedB.append(('B','D'))
        expectedB.append(('C','D'))
        expectedB.append(('C','E'))
        expectedB.append(('D','E'))
        expectedB.append(('D','F'))
        expectedB.append(('E','F'))

        expectedP = dict()#the expected P_min and P_max for each relation
        expectedP[('A','B')] = (0,0)
        expectedP[('B','C')] = (1,1)
        expectedP[('B','D')] = (1,1)
        expectedP[('C','D')] = (2,2)
        expectedP[('C','E')] = (2,2)
        expectedP[('D','E')] = (2,3)
        expectedP[('D','F')] = (2,3)
        expectedP[('E','F')] = (3,4)

        expectedF = dict()#the expected F for each relation
        expectedF[('A','B')] = 2
        expectedF[('B','C')] = 2
        expectedF[('B','D')] = 1
        expectedF[('C','D')] = 1
        expectedF[('C','E')] = 1
        expectedF[('D','E')] = 1
        expectedF[('D','F')] = 0
        expectedF[('E','F')] = 0


        test_CC_BP = Conformance_Checking.CC_BH() #process XES file
        test_CC_BP.setM_FromXES('XES-files/XES_to_ref_model1.xes')
        M = test_CC_BP.getM()
        (B,P,F) = M #extract the 3 model elements

        for relation in expectedB:#for all expected relations
            if relation in B: #see if it exist
                B.remove(relation) #remove in case repeats
            else:
                print("Expected relation: {0}, doesnt exist".format(relation))
                self.assertTrue(False)
            self.assertEqual(expectedP[relation], P[relation]) #test the relation key gives same value on P and F as expected
            self.assertEqual(expectedF[relation], F[relation])

        self.assertEqual(0,len(B)) #make sure we dont have any relations to spare

        maxF = test_CC_BP.getMaxOfF() #test the max of F of model
        self.assertEqual(2,maxF)

    def test_XES_to_model_2(self):

        expectedB = [] #the expected relations in B
        expectedB.append(('A','B1'))
        expectedB.append(('B1','C'))
        expectedB.append(('B1','B2'))
        expectedB.append(('B2','B3'))
        expectedB.append(('B3','B1'))
        expectedB.append(('B2','E'))
        expectedB.append(('C','D'))
        expectedB.append(('D','C'))
        expectedB.append(('D','E'))
        expectedB.append(('E','F'))

        expectedP = dict()#the expected P_min and P_max for each relation
        expectedP[('A','B1')] = (0,0)
        expectedP[('B1','C')] = (1,4)
        expectedP[('B1','B2')] = (1,4)
        expectedP[('B2','B3')] = (2,4)
        expectedP[('B3','B1')] = (3,4)
        expectedP[('B2','E')] = (2,4)
        expectedP[('C','D')] = (2,7)
        expectedP[('D','C')] = (3,7)
        expectedP[('D','E')] = (3,7)
        expectedP[('E','F')] = (3,8)

        expectedF = dict()#the expected F for each relation
        expectedF[('A','B1')] = 3
        expectedF[('B1','C')] = 3
        expectedF[('B1','B2')] = 2
        expectedF[('B2','B3')] = 4
        expectedF[('B3','B1')] = 3
        expectedF[('B2','E')] = 1
        expectedF[('C','D')] = 2
        expectedF[('D','C')] = 3
        expectedF[('D','E')] = 1
        expectedF[('E','F')] = 0


        test_CC_BP = Conformance_Checking.CC_BH() #process XES file
        test_CC_BP.setM_FromXES('XES-files/XES_to_ref_model2.xes')
        M = test_CC_BP.getM()
        (B,P,F) = M #extract the 3 model elements

        for relation in expectedB:#for all expected relations
            if relation in B: #see if it exist
                B.remove(relation) #remove in case repeats
            else:
                print("Expected relation: {0}, doesnt exist".format(relation))
                self.assertTrue(False)
            self.assertEqual(expectedP[relation], P[relation]) #test the relation key gives same value on P and F as expected
            self.assertEqual(expectedF[relation], F[relation])

        self.assertEqual(0,len(B)) #make sure we dont have any relations to spare

        maxF = test_CC_BP.getMaxOfF() #test the max of F of model
        self.assertEqual(4,maxF)

if __name__=='__main__':
	unittest.main()