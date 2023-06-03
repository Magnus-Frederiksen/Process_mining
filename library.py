from datetime import datetime
import datetime
import xml.etree.ElementTree as ET
import graphviz as pgv
from collections import defaultdict
import reactivex as rx
from reactivex import create
from reactivex import operators as op
import json
from pybeamline import bevent
from pybeamline.sources import xes_log_source_from_file
import math



# class sliding_window:
#     def __init__(self, max_M):
#         self.max_memory = max_M
#         self.M = []
#
#     def update_sliding_window(self, newEvent):
#         if len(self.M) >= self.max_memory:
#             self.M.pop(0)
#         self.M.append(newEvent)
#
#     def subscribe(self, source):
#         source.subscribe(
#             on_next=lambda i:
#             self.update_sliding_window(i),
#             on_error=lambda e, l: print("Error Occurred: {0} to {1}".format(e, l)),
#             on_completed=lambda: print("Done!"),
#         )
#
#         for event in self.M:
#             self.on_next(event)
#         self.on_completed()


class Lossy_count:
    def __init__(self, max_approx_error = 0.1):
        self.events = dict()
        self.observed_events = 1
        self.bucket_width = int(math.ceil(1/max_approx_error))

    def update_lossy_count(self, newEvent):
        current_bucket = int(math.ceil(self.observed_events / self.bucket_width))
       # print("current bucket is: {0}".format(current_bucket))
        if newEvent.get_event_name() in self.events: #if event exist
            lastEvent = self.events[newEvent.get_event_name()] #save former event locally
            del self.events[newEvent.get_event_name()] #increment event frequency
            self.events[newEvent.get_event_name()] = (lastEvent[0] + 1, lastEvent[1])

        else:
            self.events[newEvent.get_event_name()] = (1, current_bucket - 1) #add the event

        if self.observed_events % self.bucket_width == 0.0: #cleanup time based on max aproximation error

            tobedel = []

            for event, (frequency, bucket) in self.events.items(): #finds all keys to be removed
                if(frequency+bucket <= current_bucket):
                    tobedel.append(event)
            for eventName in tobedel: #cant be deleted on previous for loop as it moves it around
                del self.events[eventName]


        self.observed_events += 1


    def subscribe(self, source):
        source.subscribe(
            on_next=lambda i:
            self.update_lossy_count(i),
            on_error=lambda e, l: print("Error Occurred: {0} to {1}".format(e, l)),
            on_completed=lambda: print("Done!"),
        )

    def setMax_approx_error(self, max_approx_error):
        self.bucket_width = int(math.ceil(1/max_approx_error))

class HM_LC:
    def __init__(self, max_approx_error = 0.1 , min_dependency_threshold = 0, and_threshold = 0.8):
        self.minimum_dependency_threshold = min_dependency_threshold
       # self.positive_observation_threshold = positive_observation_threshold
        self.and_threshold = and_threshold


        self.D_C = dict() #set of event
        self.D_R = dict() #set of relations
        self.observed_events = 1
        self.bucket_width = int(math.ceil(1 / max_approx_error))

        self.modelRefreshRate = 1
        self.modelNumber = 1
        self.modelName = 'HM_LC'

        self.labelType = 1
        self.rounderforLabel = 2

    def update_HM_LC(self, newEvent):
        current_bucket = int(math.ceil(self.observed_events / self.bucket_width)) #calculated bucket
       # print("new event: {0} from trace: {1}, at date: {2}".format(newEvent.get_event_name(), newEvent.get_trace_name(), newEvent.get_event_time()))
        if newEvent.get_trace_name() in self.D_C: #if caseID already exist
            lastEvent = self.D_C[newEvent.get_trace_name()] #localy save former event

            del self.D_C[newEvent.get_trace_name()] #replace caseID's former event with new event
            self.D_C[newEvent.get_trace_name()] = [newEvent.get_event_name(), lastEvent[1] + 1, lastEvent[2],
                                                   newEvent.get_event_time()]


            r_N = (lastEvent[0], newEvent.get_event_name()) #save relation localy

            if r_N in self.D_R: #if relation exists in set
                lastRelation = self.D_R[r_N]  #localy save former relation
                del self.D_R[r_N] #replace relation
                diff = (newEvent.get_event_time() - lastEvent[3]) - lastRelation[2]
                newTime = lastRelation[2] + (diff/(lastRelation[0] + 1))
                self.D_R[r_N] = [lastRelation[0] + 1, lastRelation[1], newTime]
            else: #the relation doesent exist, create it
                self.D_R[r_N] = (1, current_bucket - 1, newEvent.get_event_time() - lastEvent[3])

           # print("from {0} to {1} ocured {2} times at a time of {3}".format(r_N[0],r_N[1],self.D_R[r_N][0],self.D_R[r_N][2]))

        else: #caseID doesnt exist, create it
            self.D_C[newEvent.get_trace_name()] = (newEvent.get_event_name(), 1, current_bucket - 1, newEvent.get_event_time())

        #clean up
        D_Ctobedel = [] #the 2 lists are needed to avoid messing with the comming loops
        D_Rtobedel = []

        #bucket cleaning time
        if self.observed_events % self.bucket_width == 0.0:

            for caseID, (eventName, frequency, bucket, time) in self.D_C.items():
                if frequency + bucket <= current_bucket: #if not above the error threshold on all events occured
                    D_Ctobedel.append(caseID)

            for caseID in D_Ctobedel: # deleted the event
                del self.D_C[caseID]

            for relation,(frequency, bucket, time) in self.D_R.items():
                if frequency + bucket <= current_bucket: #if not above the error threshold of all relations
                    D_Rtobedel.append(relation)

            for relation in D_Rtobedel: #delete the relations
                del self.D_R[relation]

        self.observed_events += 1

    def update_model(self):
        if (self.observed_events - 1) % self.modelRefreshRate == 0: #model refreshrate user defined
            print("new model") #to be deleted!
            G = pgv.Graph(comment='HM_LC') #setting type of graph
            G.graph_attr['rankdir'] = 'LR'
            G.node_attr['shape'] = 'box'
            G.edge_attr['arrowType'] = 'normal'
            above_dependency_threshold = defaultdict(list)


            for (A,B),(frequency, bucket, time)  in self.D_R.items(): #for all relations and all their attributes
                dependency = 0
                if (B,A) in self.D_R: #calculated dependecency of each relation
                    op_frequency = self.D_R[(B,A)][0]
                    dependency = (frequency - op_frequency) / (frequency + op_frequency + 1)
                else:
                    dependency = frequency / (frequency + 1)
                if dependency >= self.minimum_dependency_threshold: #if within dependency relation
                   # G.edge(A, B, label=str(dependency), dir='forward')
                    #newtime round timer
                    #and depedency list of lists
                    above_dependency_threshold[A].append((B, round(frequency,self.rounderforLabel),round(dependency,self.rounderforLabel), time))

            #for the next line of code, A will be the variable for where the edge is coming from
            #C and B will be the where the edge is going to, and its the and/XOR relation for C and B
            for (A), (listOfB) in above_dependency_threshold.items(): #everything above dependency threshold

                choices = len(listOfB) # all that A goes to
                if choices != 2: # if A goes to only 1 or more than to, have to visual idea to implement for multiple paths
                    G.edge(A, listOfB[0][0], label=str(listOfB[0][self.labelType]), dir='forward')
                else:
                    and_relation = False
                    for i in range(0,choices): # for all B's that A goes to
                        for j in range(i + 1, choices): # for all C's that B can have a relation with
                            #frequency for each that goes to each
                            B_to_C = 0
                            C_to_B = 0
                            A_to_B = listOfB[i][1]
                            A_to_C = listOfB[j][1]

                            B = listOfB[i][0]
                            C = listOfB[j][0]

                            #if B and C mutual goes to each other
                            if (B,C) in self.D_R:
                                B_to_C = self.D_R[(B,C)][0]
                            if (C,B) in self.D_R:
                                C_to_B = self.D_R[(C,B)][0]

                            #and relation formular
                            and_relation_Num = 0
                            and_relation_Num = (B_to_C + C_to_B) / (A_to_B + A_to_C + 1)

                            if(and_relation_Num >= self.and_threshold): #if above threshold
                                and_relation = True

                        if(and_relation): #put and on the label
                            G.edge(A, listOfB[i][0], label=str(listOfB[i][self.labelType]) +" AND", dir='forward')
                        else: # put XOR on the label
                            G.edge(A, listOfB[i][0], label=str(listOfB[i][self.labelType]) + " XOR", dir='forward')


            G.render('doctest-output/' + self.modelName + str(self.modelNumber) + '.gv').replace('\\', '/')
            self.modelNumber += 1

            '''     for (C, D), (freq1, bucket1) in self.D_R.items(): #the and thresholds
                                         if C == A and D != B:
                                             rn_BD = 0
                                             rn_DB = 0
                                             if(B,D) in self.D_R:
                                                 rn_DB = self.D_R[(B,D)][0]
                                             if(D,B) in self.D_R:
                                                 rn_DB = self.D_R[(D,B)][0]

                                         if rn_BD <= self.and_threshold * (
                                                 frequency + freq1 + 1) - rn_DB and rn_DB <= self.and_threshold * (
                                                 frequency + freq1 + 1) - rn_BD and frequency <= (
                                                 rn_DB + rn_BD) / self.and_threshold - freq1 - 1 and freq1 <= (
                                                 rn_DB + rn_BD) / self.and_threshold - frequency - 1:
                                             '''

    def subscribe(self, source): #subscribes source to the miner
        source.subscribe(
            on_next=lambda i: #for each new event i
            {
                self.update_HM_LC(i), #update HM_LC with the new event
                self.update_model() #update the painted model
            },
            on_error=lambda e, l: print("Error Occurred: {0} to {1}".format(e, l)),
            on_completed=lambda: print("Done!"), #print done, to indicate the subscribtion has ended
        )

    def setMax_approx_error(self, max_approx_error):
        self.bucket_width = int(math.ceil(1 / max_approx_error))

    def setMin_dependency_threshold(self, min_dependency_threshold):
        self.minimum_dependency_threshold = min_dependency_threshold

    def setAnd_threshold(self, and_threshold):
        self.and_threshold = and_threshold

    def setModelRefreshRate(self, refreshRate): #set how many events should occur before making a new model
        if refreshRate >= 1:
            self.modelRefreshRate = int(refreshRate)


    def setLabel(self, label): #set the type of information each edge on the model should have
        match label:
            case "Time": #the average time for each relation
                self.labelType = 3
                return
            case "Dependency": #the dependecy for each relation
                self.labelType = 2
                return
            case "Frequency": #the amount of times the relation has occured
                self.labelType = 1
                return

    def setlabelRounder(self, rounder): #set how many decimals behind numbers to occur on labels
        if rounder >= 0:
            self.rounderforLabel = int(rounder)

    def setFileName(self, name): #set the name of the files to be saved
        self.modelName = name


class HM_LCB:
    def __init__(self, budget = 10 , min_dependency_threshold = 0, and_threshold = 0.8):
        self.budget = int(budget) #max length of stored events and relations
        self.minimum_dependency_threshold = min_dependency_threshold
       # self.positive_observation_threshold = positive_observation_threshold
        self.and_threshold = and_threshold


        self.D_C = dict() #set of event
        self.D_R = dict() #set of relations
        self.observed_events = 1
        self.current_bucket = 1

        self.modelRefreshRate = 1
        self.modelNumber = 1
        self.modelName = 'HM_LCB'

        self.labelType = 1
        self.rounderforLabel = 2


    def update_HM_LCB(self, newEvent):
        #print("new event: {0} from trace: {1}, at date: {2}".format(newEvent.get_event_name(), newEvent.get_trace_name(), newEvent.get_event_time()))

        #for budget lossy counting, if relation or caseID already exists, the memory will just be replaced and not expanded
        #so we only clean up when the caseID or relation doesnt exist, which results in creating a new one

        if newEvent.get_trace_name() in self.D_C: #if caseID already exist
            lastEvent = self.D_C[newEvent.get_trace_name()] #localy save former event
            del self.D_C[newEvent.get_trace_name()] #replace caseID's former event with new event
            self.D_C[newEvent.get_trace_name()] = [newEvent.get_event_name(), lastEvent[1] + 1, lastEvent[2],
                                                   newEvent.get_event_time()]


            r_N = (lastEvent[0], newEvent.get_event_name()) #save relation localy

            if r_N in self.D_R: #if relation exists in set
                lastRelation = self.D_R[r_N]  #localy save former relation
                del self.D_R[r_N] #replace relation

                diff = (newEvent.get_event_time() - lastEvent[3]) - lastRelation[2] #incase the user wants the time for each relation
                newTime = lastRelation[2] + (diff/(lastRelation[0] + 1))

                self.D_R[r_N] = [lastRelation[0] + 1, lastRelation[1], newTime]

            else: #the relation doesent exist, create it
                while len(self.D_R) + len(self.D_C) >= self.budget:  # if budget is reached when adding a new key + iten
                    self.bucket_cleaning()  # bucket cleaning time
                self.D_R[r_N] = (1, self.current_bucket - 1, newEvent.get_event_time() - lastEvent[3])

           # print("from {0} to {1} ocured {2} times at a time of {3}".format(r_N[0],r_N[1],self.D_R[r_N][0],self.D_R[r_N][2]))

        else: #caseID doesnt exist, create it
            while ((len(self.D_R) + len(self.D_C)) >= self.budget): #if budget is reached when adding a new key + iten
                self.bucket_cleaning() # bucket cleaning time
            self.D_C[newEvent.get_trace_name()] = (newEvent.get_event_name(), 1, self.current_bucket - 1, newEvent.get_event_time())


        #clean up
        self.observed_events += 1

    def bucket_cleaning(self):
        self.current_bucket += 1 #increment bucket to clean all items not within the new bucket number

        D_Ctobedel = [] #the 2 lists are needed to avoid messing with the comming loops
        D_Rtobedel = []

        for caseID, (eventName, frequency, bucket, time) in self.D_C.items(): #for all caseIDs' occured
            if frequency + bucket <= self.current_bucket:  # if not above the bucket threshold on all events occured
                D_Ctobedel.append(caseID)

        for caseID in D_Ctobedel:  # deleted the event
            del self.D_C[caseID]

        for relation, (frequency, bucket, time) in self.D_R.items(): #for all relations occured
            if frequency + bucket <= self.current_bucket:  # if not above the bucket threshold of all relations
                D_Rtobedel.append(relation)

        for relation in D_Rtobedel:  # delete the relations
            del self.D_R[relation]

    def update_model(self):
        if (self.observed_events - 1) % self.modelRefreshRate == 0: #model refreshrate user defined
            print("new model") #to be deleted!
            G = pgv.Graph(comment='HM_LC') #setting type of graph
            G.graph_attr['rankdir'] = 'LR'
            G.node_attr['shape'] = 'box'
            G.edge_attr['arrowType'] = 'normal'
            above_dependency_threshold = defaultdict(list)


            for (A,B),(frequency, bucket, time)  in self.D_R.items(): #for all relations and all their attributes
                dependency = 0
                if (B,A) in self.D_R: #calculated dependecency of each relation
                    op_frequency = self.D_R[(B,A)][0]
                    dependency = (frequency - op_frequency) / (frequency + op_frequency + 1)
                else:
                    dependency = frequency / (frequency + 1)
                if dependency >= self.minimum_dependency_threshold: #if within dependency relation
                   # G.edge(A, B, label=str(dependency), dir='forward')
                    #newtime round timer
                    #and depedency list of lists
                    above_dependency_threshold[A].append((B, round(frequency,self.rounderforLabel),round(dependency,self.rounderforLabel), time))

            #for the next line of code, A will be the variable for where the edge is coming from
            #C and B will be the where the edge is going to, and its the and/XOR relation for C and B
            for (A), (listOfB) in above_dependency_threshold.items(): #everything above dependency threshold

                choices = len(listOfB) # all that A goes to
                if choices != 2: # if A goes to only 1 or more than to, have to visual idea to implement for multiple paths
                    G.edge(A, listOfB[0][0], label=str(listOfB[0][self.labelType]), dir='forward')
                else:
                    and_relation = False
                    for i in range(0,choices): # for all B's that A goes to
                        for j in range(i + 1, choices): # for all C's that B can have a relation with
                            #frequency for each that goes to each
                            B_to_C = 0
                            C_to_B = 0
                            A_to_B = listOfB[i][1]
                            A_to_C = listOfB[j][1]

                            B = listOfB[i][0]
                            C = listOfB[j][0]

                            #if B and C mutual goes to each other
                            if (B,C) in self.D_R:
                                B_to_C = self.D_R[(B,C)][0]
                            if (C,B) in self.D_R:
                                C_to_B = self.D_R[(C,B)][0]

                            #and relation formular
                            and_relation_Num = 0
                            and_relation_Num = (B_to_C + C_to_B) / (A_to_B + A_to_C + 1)

                            if(and_relation_Num >= self.and_threshold): #if above threshold
                                and_relation = True

                        if(and_relation): #put and on the label
                            G.edge(A, listOfB[i][0], label=str(listOfB[i][self.labelType]) +" AND", dir='forward')
                        else: # put XOR on the label
                            G.edge(A, listOfB[i][0], label=str(listOfB[i][self.labelType]) + " XOR", dir='forward')


            G.render('doctest-output/' + self.modelName + str(self.modelNumber) + '.gv').replace('\\', '/')
            self.modelNumber += 1

    def subscribe(self, source): #subscribes source to the miner
        source.subscribe(
            on_next=lambda i: #for each new event i
            {
                self.update_HM_LCB(i), #update HM_LCB with the new event
                self.update_model() #update the painted model
            },
            on_error=lambda e, l: print("Error Occurred: {0} to {1}".format(e, l)),
            on_completed=lambda: print("Done!"), #print done, to indicate the subscribtion has ended
        )

    def setBudget(self, newBudget):
        self.budget = int(newBudget)

    def setMin_dependency_threshold(self, min_dependency_threshold):
        self.minimum_dependency_threshold = min_dependency_threshold

    def setAnd_threshold(self, and_threshold):
        self.and_threshold = and_threshold

    def setModelRefreshRate(self, refreshRate): #set how many events should occur before making a new model
        if refreshRate >= 1:
            self.modelRefreshRate = int(refreshRate)

    def setLabel(self, label): #set the type of information each edge on the model should have
        match label:
            case "Time": #the average time for each relation
                self.labelType = 3
                return
            case "Dependency": #the dependecy for each relation
                self.labelType = 2
                return
            case "Frequency": #the amount of times the relation has occured
                self.labelType = 1
                return

    def setlabelRounder(self, rounder): #set how many decimals behind numbers to occur on labels
        if rounder >= 0:
            self.rounderforLabel = int(rounder)

    def setFileName(self, name): #set the name of the files to be saved
        self.modelName = name

class CC_BH:
    def __init__(self, M = 0):

        self.M = M #the input is expecting to be the
        self.B = M[0]
        self.P = M[1]
        self.F = M[2]

        self.trace_last_event = dict() #recalls last event for trace to find relation

        self.conformance = dict() #saves a traces' conformance
        self.completeness = dict() #saves a traces' completeness
        self.confidence = dict() #saves a traces' confidence

        self.obs = defaultdict(list) #saves all distinct relations in a trace that has ocurred
        self.inc = dict() #saves amount of incorrect relations acording to the reference model of a trace

        self.trace_log = defaultdict(list)


    def update(self, newEvent):
        caseID = newEvent.get_trace_name() #easier reference to caseID
        eventName = newEvent.get_event_name() #easier trefermce to eventNa,e

        self.trace_log[caseID].append(eventName) #updates the specefic caseIDs log


        if caseID not in self.trace_last_event: #if this is first time caseID appears
            self.trace_last_event[caseID] = eventName #save current event

           # self.obs[caseID] = []
            self.inc[caseID] = 0 #set amount of incorect relations for that CaseId to 0

        else: #if the caseID has been seen before

            newPattern = (self.trace_last_event[caseID], eventName) #locally save the relation
            #Step 1: update internal data structures
            if newPattern in self.B: #if the relation is in the aproved relation list
                if newPattern not in self.obs[caseID]: #and that relation has not occured for that caseID before
                    self.obs[caseID].append(newPattern) #save the relation to that CaseId
            else: #if the relation is "illegal" acording to B
                self.inc[caseID] += 1 #increment incorrect for that caseID

            #Step 2: compute online conformance values

            self.conformance[caseID] = len(self.obs[caseID]) / (len(self.obs[caseID]) + self.inc[caseID]) #calculated conformance

            if newPattern in self.B: #if the relation is legal in B
                if self.P[newPattern][0] <= len(self.obs[caseID]) <= self.P[newPattern][1]: #if the relation occurence is within P_min and P_max
                    self.completeness[caseID] = 1 #set completeness for that caseID
                else: #if not within P_min and P_max
                    self.completeness[caseID] = min(1, len(self.obs[caseID]) / (self.P[newPattern][0] + 1)) #calculate completeness


            #confidence = 1 - (F[caseId] /

               # print("case: {0} now has a conformance of: {1} and a completeness of: {2}".format(caseId, conformance,
           #                                                                                       completeness))

            else:
                2+2
              #  print("case: {0} now has a conformance of: {1}, but last behaviour wasnt expected and therefor completeness and confidence cant be found".format(caseId, conformance))
            #Step 3: cleanup


            self.trace_last_event[caseID] = eventName





        #input from algorithm

    def update_XES_to_model(self, newEvent):



    def set_model_from_XES(self, fileName):
        newSource = xes_log_source_from_file(fileName)
        self.M = ()
        self.B = []
        self.P = dict()
        self.F = dict()

        newSource.subscribe(
            on_next=lambda i:
            {
                self.update_XES_to_model(i)
            },
            on_error=lambda e, l: print("Error Occurred: {0} to {1}".format(e, l)),
            on_completed=lambda: print("hej"),
        )


    def set_model(self, M):
        self.M = M
        self.B = M[0]
        self.P = M[1]
        self.F = M[2]



    def print_trace_log(self):
        for caseID in self.trace_log:
            print("caseID: {0}, had the trace: {1}".format(caseID, self.trace_log[caseID]))
            print("which resulted in a final conformance of {0}".format(self.conformance[caseID]))

    def subscribe(self, source):
        source.subscribe(
            on_next=lambda i:
            {
                self.update(i)
            },
            on_error=lambda e, l: print("Error Occurred: {0} to {1}".format(e, l)),
            on_completed=lambda: {
                self.print_trace_log()
            },
        )




def print_log(source):
    print("hello")
    source.subscribe(
        on_next=lambda i:
        print("Activity {0} occured on {1} under the activity case {2}.".format(i.get_event_name(), i.get_event_time(), i.get_trace_name())),
        on_error=lambda e, l: print("Error Occurred: {0} to {1}".format(e, l)),
        on_completed= lambda: print("Done!"),
    )