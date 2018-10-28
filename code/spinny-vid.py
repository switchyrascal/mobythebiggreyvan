# Install by adding a button using the macro dialog
# Currently hard-coded file and group ordering
# Use by starting a screencast then pressing the button
# To clean up:
# ffmpeg -y -i screencast.webm -r 10 -vf scale=640:360 -ss 00:00:04 -t 00:00:27 screencast.gif
# ffmpeg -y -i screencast.webm -ss 00:00:04 -t 00:00:27 screencast.mp4
import FreeCAD
import FreeCADGui
from PySide import QtCore

class Input:
    def __init__(self):
        self.wait = 50
        self.next = 0
        self.objs = []

class StartState:
    def process(self, input):
        state = self
        if input.next < input.wait:
            input.next += 1
        if input.next == input.wait:
            input.next = 0
            state = ShowState()
        return state

class ShowState:
    def process(self, input):
        state = self
        if input.next < len(input.objs):
            input.objs[input.next].Visibility = True
            input.next += 1
        if input.next == len(input.objs):
            input.next = 0
            state = WaitState()
        return state

class WaitState:
    def process(self, input):
        state = self
        if input.next < input.wait:
            input.next += 1
        if input.next == input.wait:
            input.next = 0
            input.objs.reverse()
            state = HideState()
        return state

class HideState:
    def process(self, input):
        state = self
        if input.next < len(input.objs):
            input.objs[input.next].Visibility = False
            input.next += 1
        if input.next == len(input.objs):
            input.next = 0
            state = FinishState()
        return state

class FinishState:
    def process(self, input):
        return None

class SpinParts():
    def __init__(self, app, gui, order, doc):
        self.input = Input()
        self.state = StartState()
        self.app = app.getDocument(doc)
        self.gui = gui.getDocument(doc)
        self.timer = QtCore.QTimer()
        self.load_objects(order)
        self.reset_view()
        self.start_animation()

    def handle_next_object(self):
        self.state = self.state.process(self.input)
        if None == self.state:
            self.finish_animation()
        else:
            self.update_animation()

    def load_objects(self, order):
        for j in order:
            for i in self.app.Objects:
                o = self.gui.getObject(i.Name)
                if None != o.Object:
                    parent = self.get_parent(o.Object.getParentGroup())
                    if (0 < len(i.OutList) and j == parent) or (0 == len(i.OutList) and 1 == len(i.InList) and j == parent):
                        print(o.Object.Label, i.Name)
                        self.input.objs.append(o)

    def reset_view(self):
        v = self.gui.activeView()
        v.setAnimationEnabled(False)
        for o in self.input.objs:
            o.Visibility = True
        v.viewRight()
        v.fitAll()
        for o in self.input.objs:
            o.Visibility = False
        v.redraw()
        v.setAnimationEnabled(True)
        v.startAnimating(0, 1, 0, 0.1)

    def start_animation(self):
        QtCore.QObject.connect(self.timer, QtCore.SIGNAL('timeout()'), self.handle_next_object)
        self.timer.start(25)

    def update_animation(self):
        FreeCADGui.updateGui()

    def finish_animation(self):
        self.timer.stop()
        self.gui.activeView().stopAnimating()

    def get_parent(self, parent):
        l = ''
        while True:
            if None == parent:
                break
            l = parent.Label
            parent = parent.getParentGroup()
        return l

order = [
    'Floor',
    'Electrical',
    'Plumbing',
    'Garage',
    'Bathroom',
    'Bedroom',
    'Galley',
    'Living Area',
    'Roof',
    'Walls',
]
spinner = SpinParts(FreeCAD, FreeCADGui, order, 'moby')
