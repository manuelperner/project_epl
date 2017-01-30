import subprocess
import sys
from appJar import gui

#subprocess.run(['python3', 'main.py', '3', '3', '5'])

# function called by pressing the buttons
def press(btn):
    if btn=='Generate and compute the TSP':
        #print('Number of nodes:', app.getEntry('nodes'))
        #print('Minimum value for x and y coordinates:', app.getEntry('min'))
        #print('Maximum value for x and y coordinates:', app.getEntry('max'))
        nodes = app.getEntry('nodes')
        min_xy = app.getEntry('min')
        max_xy = app.getEntry('max')
        print(type(nodes))
        subprocess.Popen([sys.executable, 'main.py', str(nodes), str(min_xy), str(max_xy)])
        #main.main(nodes,min_xy,max_xy)
        
        

app = gui()
#app.showSplash('TSP-Heuristics' '\n' 'by Yanick Dickbauer, Manuel Perner, Philipp Prei\u00df', fill='LightSeaGreen', stripe='DarkSeaGreen', fg='white', font=30)
app.setFont(18, 'Calibri')
app.setButtonFont(16, 'Calibri')
app.setTitle('TSP-Heuristics')
app.setBg('DarkSeaGreen')
#app.setGeometry(800,600)
app.setResizable(canResize=True)
app.startPagedWindow('Welcome to TSP-Heuristcs')
app.startPage()
app.addMessage('mess', 'This program generates a random TSP and solves it using different heuristics. The results of the heuristics are compared with an optimal solver solution.\nYou will be asked to define the number of nodes that should be generated and for the range of the coordinates in which the nodes are created.\nIncluded heuristics are:\n- MST Heuristic\n- Multi-Fragment\n- Nearest Neighbour\n- Nearest Insertion\n- Cheapest Insertion\nPlease proceed to the next page to enter the desired values.', None, 0, 2)
app.stopPage()

app.startPage()
app.addLabel('nodes', 'Please enter the number of points to be generated:', None, 0)           
app.addNumericEntry('nodes', None, 0) 
app.addLabel('min', 'Define the minimum value for x and y coordinates:', None, 0)
app.addNumericEntry('min', None, 0)
app.addLabel('max', 'Define the maximum value for x and y coordinates:', None, 0)
app.addNumericEntry('max', None, 0)
app.addButton('Generate and compute the TSP', press, None, 0, 2)
app.stopPage()

app.setEntryFocus('nodes')

app.go()
