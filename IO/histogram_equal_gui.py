import numpy as np
import sys
from PyQt4 import QtCore
from PyQt4 import QtGui
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from matplotlib.backends.backend_qt4 import NavigationToolbar2QT as NavigationToolbar
from skimage import img_as_float, io


# import the MainWindow widget from the converted .ui files
from ArchaeoPY.GUI.mpl import Ui_MainWindow

#import ArchaeoPY modules
from adaptive_equal import intensity_rescale

class ArchaeoPYMainWindow(QtGui.QMainWindow, Ui_MainWindow):

        
        """Customization for Qt Designer created window"""
    
        def ClearPlot(self):
            self.mpl.canvas.ax.clear()
            self.mpl.canvas.draw()
            
        def copy_to_clipboard(self):
            pixmap = QtGui.QPixmap.grabWidget(self.mpl.canvas)
            QtGui.QApplication.clipboard().setPixmap(pixmap)
            
        def Open_File(self):
            self.fname = QtGui.QFileDialog.getOpenFileName()
            
        def Image2Float(self):
            image = io.imread(self.fname)
            self.array = img_as_float(image)
            
        def Plot_Function(self):
            self.output = intensity_rescale(self.array)            
            self.mpl.canvas.ax.clear()
            print np.shape(self.output)
            self.mpl.canvas.ax.imshow(self.output)                        
            self.mpl.canvas.draw()
                        
        def Button_Definitions(self):
            self.firstrun=True
            
            self.Open_button = QtGui.QPushButton('Open', self)
            self.fname = self.Open_button.clicked.connect(self.Open_File)
            self.Button_Layout.addWidget(self.Open_button)
            
            self.pushButton_plot.clicked.connect(self.Plot_Function)
            self.pushButton_clear.clicked.connect(self.ClearPlot)
            QtGui.QShortcut(QtGui.QKeySequence("Ctrl+P"),self, self.Plot_Function)
            
            QtGui.QShortcut(QtGui.QKeySequence("Ctrl+C"),self, self.copy_to_clipboard)
        
        def __init__(self, parent = None):
            # initialization of the superclass
            super(ArchaeoPYMainWindow, self).__init__(parent)
            # setup the GUI --> function generated by pyuic4
            self.setupUi(self)
            #Adds a Matplotlib Toolbar to the display, clears the display and adds only the required buttons
            self.navi_toolbar = NavigationToolbar(self.mpl.canvas, self)
            self.navi_toolbar.clear()
    
        #Adds Buttons
            a = self.navi_toolbar.addAction(self.navi_toolbar._icon('home.png'), 'Home',
                                            self.navi_toolbar.home)
            #a.setToolTip('returns axes to original position')
            a = self.navi_toolbar.addAction(self.navi_toolbar._icon('move.png'), 'Pan',
                                            self.navi_toolbar.pan)
            a.setToolTip('Pan axes with left mouse, zoom with right')
            a = self.navi_toolbar.addAction(self.navi_toolbar._icon('zoom_to_rect.png'), 'Zoom',
                                            self.navi_toolbar.zoom)
            a.setToolTip('Zoom to Rectangle')
            a = self.navi_toolbar.addAction(self.navi_toolbar._icon('filesave.png'), 'Save',
                               self.navi_toolbar.save_figure)
            a.setToolTip('Save the figure')
    
            #Button_layout is a QT desginer Grid Layout.
            self.toolbar_grid.addWidget(self.navi_toolbar)
            self.Button_Definitions()
            self.plot_options()
            
if __name__=='__main__':
    #Creates Main UI window
    app = QtGui.QApplication(sys.argv)
    
    app.processEvents()
    
    #Creates Window Form     
    form = ArchaeoPYMainWindow()
    
    #display form and focus
    form.show()
    #if sys.platform == "darwin":
    form.raise_()
    
    #Something to do with the App & Cleanup?
    app.exec_()
    atexit.register(form.cleanup)