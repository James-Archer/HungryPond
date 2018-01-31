# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 13:53:59 2018

@author: James Archer

The visual player for the simulation.

"""

import pond

import sys
import time
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QMessageBox, QFileDialog, QLabel,
                             QWidget, QHBoxLayout, QVBoxLayout, QLineEdit)
from PyQt5.QtCore import Qt, QThread, QRectF
from PyQt5.QtGui import QDoubleValidator, QPainter, QBrush

class MainWindow(QMainWindow):
    
    def __init__(self, p):
        
        super().__init__()
        self.pond = p
        self.foods = []
        self.organisms = []
        self.running = True
        self.initUI()

    def initUI(self):
        
        self.setGeometry(50, 50, int(0.5*self.pond.dimensions['x']), int(0.5*self.pond.dimensions['y']))
        self.mainWidget = QWidget(self)
        self.setCentralWidget(self.mainWidget)
        self.setWindowTitle('PondSim')
        self.pondThread = PondThread(self)
        self.world = QWidget(self.mainWidget)
        self.show()
    
    def closeEvent(self, event):
        
        self.running = False
        time.sleep(0.1)
        event.accept()
        
    def paintEvent(self, e):

        qp = QPainter()
        qp.begin(self)
        self.drawPoints(qp)
        qp.end()
        
    def drawPoints(self, qp):
      
        qp.setPen(Qt.red)
        brush = QBrush(Qt.SolidPattern)
        brush.setColor(Qt.red)
        qp.setBrush(brush)
        size = self.size()
        
        # Draw the food
        for i in self.pond.food:
            x = i.pos['x']/self.pond.dimensions['x']*size.width()
            y = i.pos['y']/self.pond.dimensions['y']*size.height()
            #qp.drawPoint(x, y)
            qp.drawEllipse(QRectF(x, y, 5, 5))
            
        qp.setPen(Qt.green)   
        brush.setColor(Qt.green)
        qp.setBrush(brush)
        # Draw the organisms
        for i in self.pond.orgs:
            x = i.pos['x']/self.pond.dimensions['x']*size.width()
            y = i.pos['y']/self.pond.dimensions['y']*size.height()
            qp.drawEllipse(QRectF(x, y, 10, 10))
        
class PondThread(QThread):
    
    def __init__(self, master):
        
        super().__init__()
        self.master = master

    def run(self):
        while self.master.running:
            self.master.pond.step()
            self.master.update()
            time.sleep(0.01)
        
if __name__=='__main__':
    
    app = QApplication(sys.argv)
    ex = MainWindow(pond.Pond(10))
    ex.pondThread.start()
    sys.exit(app.exec_())