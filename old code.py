from datetime import datetime
import xml.etree.ElementTree as ET
import graphviz as pgv
from collections import defaultdict
import reactivex as rx
from reactivex import operators as op
import json
from library import extract_xes



F = dict()

program_running = True
noFilesYet = True

source = rx.empty()

print("type 1 to add a file, type 2 to trivial mine them, type 3 to end program")
while program_running:
    choice = input()
    if choice == '1':
        newSource = rx.create(extract_xes)
        source = rx.concat(source,newSource)

    elif choice == '2':
        listofActivties = []
        source.subscribe(
            on_next=lambda i:
            listofActivties.append(i),
            on_error=lambda e, l: print("Error Occurred: {0} to {1}".format(e, l)),
            on_completed=lambda: print("Done!"),
        )


        def sort(listofActivities):
            dictofActivites = dict()
            for activity in listofActivities:
                if activity[0] not in dictofActivites:
                    dictofActivites[activity[0]] = []
                dictofActivites[activity[0]].append((activity[1], activity[2]))
            return dictofActivites


        def sortbyDate(dictofActivities):
            for case in dictofActivities:
                dictofActivities[case] = sorted(dictofActivities[case],
                key=lambda t: t[1])
            return dictofActivities


        sorteddictofActivities = sortbyDate(sort(listofActivties))

        F = dict()
        for case, activitiesofCase in sorteddictofActivities.items():
            for activity in range(0, len(activitiesofCase) - 1):
                ai = activitiesofCase[activity][0]
                aj = activitiesofCase[activity + 1][0]
                if ai not in F:
                    F[ai] = dict()
                if aj not in F[ai]:
                    F[ai][aj] = 0
                F[ai][aj] += 1
        for ai in sorted(F.keys()):
            for aj in sorted(F[ai].keys()):
                print(ai, '->', aj, ':', F[ai][aj])
                l = 2+2

        G = pgv.Graph(comment='Mønti Pythøn ik den Hølie Grailen')


        G.graph_attr['rankdir'] = 'LR'
        G.node_attr['shape'] = 'box'
        G.edge_attr['arrowType'] = 'normal'



        for ai in F:
            for aj in F[ai]:
                G.edge(ai, aj, label=str(F[ai][aj]), dir='forward')

        G.render('doctest-output/m00se.gv').replace('\\', '/')

    else:
        program_running = False

