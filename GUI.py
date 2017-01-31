import subprocess
import sys
from appJar import gui

def press(btn):
    if btn=='Generate and compute the TSP':
        nodes = app.getEntry('nodes')
        min_xy = app.getEntry('min')
        max_xy = app.getEntry('max')
        subprocess.Popen([sys.executable, 'main.py', str(nodes), str(min_xy), str(max_xy)])
        
app = gui()

#setup 'intro'
app.showSplash('TSP-Heuristics' '\n' 'by Yanick Dickbauer, Manuel Perner, Philipp Prei\u00df', fill='LightSeaGreen', stripe='DarkSeaGreen', fg='black', font=24)

#setup gui
app.setFont(14, 'Calibri')
app.setButtonFont(12, 'Calibri')
app.setTitle('TSP-Heuristics')
app.setBg('LightSeaGreen')
app.setResizable(canResize=True)

#create a paged window
app.startPagedWindow('Welcome to TSP-Heuristcs')

#create 1st page
app.startPage()
app.setBg('DarkSeaGreen')
app.addMessage('mess', 'This program generates a random TSP and solves it using different heuristics. The results of the heuristics are compared with an optimal solver solution.\nYou will be asked to define the number of nodes that should be generated and for the range of the coordinates in which the nodes are created.\n\nIncluded heuristics are:\n- MST Heuristic\n- Multi-Fragment\n- Nearest Neighbour\n- Nearest Insertion\n- Cheapest Insertion\n\nPlease proceed to the next page to enter the desired values.', None, 0, 2)
app.stopPage()

#create 2nd page
app.startPage()
app.setBg('DarkSeaGreen')
app.addLabel('nodes', 'Please enter the number of points to be generated:', None, 0)           
app.addNumericEntry('nodes', None, 0) 
app.addLabel('min', 'Define the minimum value for x and y coordinates:', None, 0)
app.addNumericEntry('min', None, 0)
app.addLabel('max', 'Define the maximum value for x and y coordinates:', None, 0)
app.addNumericEntry('max', None, 0)
app.addButton('Generate and compute the TSP', press, None, 0, 2)
app.stopPage()

app.stopPagedWindow()

#set focus on 1st input box
app.setEntryFocus('nodes')

#start the gui
app.go()
