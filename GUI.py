from appJar import gui
#import main as m

# function called by pressing the buttons
def press(btn):
    if btn=='Cancel':
        app.stop()
    else:
        print('Number of nodes:', app.getEntry('nodes'))
        print('Minimum value for x and y coordinates:', app.getEntry('min'))
        print('Maximum value for x and y coordinates:', app.getEntry('max'))
        nodes = app.getEntry('nodes')
        min_xy = app.getEntry('min')
        max_xy = app.getEntry('max')
        
        

app = gui()
app.showSplash('TSP-Heuristics' '\n' 'by Yanick Dickbauer, Manuel Perner, Philipp Prei\u00df', fill='LightSeaGreen', stripe='DarkSeaGreen', fg='white', font=30)

app.setBg('DarkSeaGreen')
app.addLabel('title', 'Welcome to TSP-Heuristcs', 0, 0, 2)
app.addLabel('nodes', 'Please enter the number of points to be generated:', 1, 0)           
app.addEntry('nodes', 1, 1)
app.addLabel('min', 'Define the minimum value for x and y coordinates:', 2, 0)
app.addEntry('min', 2, 1)
app.addLabel('max', 'Define the maximum value for x and y coordinates:', 3, 0)
app.addEntry('max', 3, 1)
app.addButtons(['Submit', 'Cancel'], press, 4, 0, 2)

app.setEntryFocus('nodes')

app.go()
