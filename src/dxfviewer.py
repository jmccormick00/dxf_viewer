# -*- coding: utf-8 *-*
import sys
import dxfImporter

from vector3D import vector3D
from camera3D import camera3D
from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt4.Qt import Qt
from PyQt4 import QtGui
from PyQt4 import QtOpenGL


class ViewerWidget(QtOpenGL.QGLWidget):
    '''
    Reads in a DXF file and shows it
    '''

    def __init__(self, parent):
        QtOpenGL.QGLWidget.__init__(self, parent)
        self.setMinimumSize(500, 500)
        self.d_vArray = []
        self.camera = camera3D(vector3D(0.0, 0.0, 10.0),
                                vector3D(0.0, 0.0, 0.0),
                                vector3D(0.0, 1.0, 0.0),
                                vector3D(0.0, 1.0, 0.0))

    def paintGL(self):
        '''
        Drawing routine
        '''

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glEnableClientState(GL_VERTEX_ARRAY)
        glColor(1.0, 0.0, 0.0)
        glPushMatrix()
        self.camera.updateCamera()
        glVertexPointer(3, GL_FLOAT, 0, self.d_vArray)
        glDrawArrays(GL_LINES, 0, len(self.d_vArray))
        glPopMatrix()
        glFlush()

    def mousePressEvent(self, event):
        '''
        Called when the mouse button is pressed
        '''
        self.mouseLastPos = event.pos()

    def mouseMoveEvent(self, event):
        '''
        Called when the mouse moves
        '''
        mouseDeltaX = event.x() - self.mouseLastPos.x()
        mouseDeltaY = event.y() - self.mouseLastPos.y()
        if(event.buttons() & Qt.LeftButton):
            self.camera.orbitX(mouseDeltaX * (-0.005))
            self.camera.orbitY(mouseDeltaY * 0.005)
        if(event.buttons() & Qt.RightButton):
            self.camera.panHorizontal(mouseDeltaX * -0.01)
            self.camera.panVertical(mouseDeltaY * 0.01)
        if(event.buttons() & Qt.MiddleButton):
            self.camera.zoomCamera(mouseDeltaY * (-0.01))

        self.mouseLastPos = event.pos()
        self.glDraw()

    def resizeGL(self, w, h):
        '''
        Resize the GL window
        '''

        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60.0, float(w) / float(h), 0.0, 1000.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def initializeGL(self):
        '''
        Initialize GL
        '''

        # set viewing projection
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

    def buildVertexArray(self, vList):
        self.d_vArray = []
        for l in vList:
            self.d_vArray.append(l[0])
            self.d_vArray.append(l[1])


class ViewerMainWindow(QtGui.QMainWindow):
    '''The main window'''

    d_widget = 0

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("DXF Viewer")

        openFile = QtGui.QAction(QtGui.QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.loadFile)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)

        self.d_widget = ViewerWidget(self)
        self.setCentralWidget(self.d_widget)

    def loadFile(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '/home')
        self.d_widget.buildVertexArray(dxfImporter.read(filename))
        self.d_widget.glDraw()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = ViewerMainWindow()
    window.show()
    app.exec_()
