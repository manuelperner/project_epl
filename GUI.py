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
        nodes = int(app.getEntry('nodes'))
        min_xy = int(app.getEntry('min'))
        max_xy = int(app.getEntry('max'))
        print(nodes,min_xy,max_xy)
        
        

app = gui()
#app.showSplash('TSP-Heuristics' '\n' 'by Yanick Dickbauer, Manuel Perner, Philipp Prei\u00df', fill='LightSeaGreen', stripe='DarkSeaGreen', fg='white', font=30)
app.setFont(18, 'Calibri')
app.setButtonFont(16, 'Calibri')
app.setTitle('TSP-Heuristics')
app.setBg('DarkSeaGreen')
#app.setGeometry(800,600)
app.setResizable(canResize=True)
app.addLabel('title', 'Welcome to TSP-Heuristcs', None, 0, 2)
app.addHorizontalSeparator(None, 0, 3, colour = 'DarkSeaGreen')
app.addMessage('mess', 'Long explanation for TSP-Heuristics. Instructions on how to use the app in detail. Centered.', None, 0, 2)
app.setMessageBg('mess', 'red')
app.addHorizontalSeparator(None, 0, 3, colour = 'DarkSeaGreen')
app.addLabel('nodes', 'Please enter the number of points to be generated:', None, 0)           
app.addNumericEntry('nodes', None, 1) 
app.addLabel('min', 'Define the minimum value for x and y coordinates:', None, 0)
app.addNumericEntry('min', None, 1)
app.addLabel('max', 'Define the maximum value for x and y coordinates:', None, 0)
app.addNumericEntry('max', None, 1)
app.addButtons(['Compute the TSP', 'Cancel'], press, None, 0, 2)

app.setEntryFocus('nodes')

app.go()
