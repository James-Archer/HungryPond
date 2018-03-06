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
        
        self.setGeometry(50, 50, 0, 0)
        self.mainWidget = QWidget(self)
        self.setCentralWidget(self.mainWidget)
        self.setWindowTitle('PondSim')
        self.pondThread = PondThread(self)
        self.world = WorldWidget(self)
        #self.orgsList = OrgsList(self)
        
        mainLayout = QHBoxLayout()
        subWidget = QWidget(self.mainWidget)
        subLayout1 = QVBoxLayout()
        subLayout1.stretch(1)
        self.timeText = QLabel(f"Time:\n{self.pond.t}", self.mainWidget)
        self.numOrgsText = QLabel(f"Population:\n{len(self.pond.orgs)} (+{len(self.pond.eggs)})", self.mainWidget)
        self.foodFreeText = QLabel(f"Food:\n{sum([i.food for i in self.pond.food])}", self.mainWidget)
        self.totalFreeFoodText = QLabel(f"Total food:\n{round(self.pond.countNetFood(), 2)}", self.mainWidget)
        
        subLayout1.addWidget(self.timeText)
        subLayout1.addWidget(self.numOrgsText)
        subLayout1.addWidget(self.foodFreeText)
        subLayout1.addWidget(self.totalFreeFoodText)
        subWidget.setLayout(subLayout1)
        subWidget.setFixedWidth(100)
        mainLayout.addWidget(subWidget)
        mainLayout.addWidget(self.world)
        #mainLayout.addWidget(self.orgsList)
        
        self.mainWidget.setLayout(mainLayout)
        self.show()
    
    def closeEvent(self, event):
        
        self.running = False
        time.sleep(0.2)
        event.accept()
        
    def updateText(self):
        
        self.timeText.setText(f"Time:\n{self.pond.t}")
        self.numOrgsText.setText(f"Population:\n{len(self.pond.orgs)} (+{len(self.pond.eggs)})")
        self.foodFreeText.setText(f"Food:\n{sum([i.food for i in self.pond.food])}")
        self.totalFreeFoodText.setText(f"Total food:\n{round(self.pond.countNetFood(), 2)}")
        #self.orgsList.updateText()
        
    def checkFinished(self):
        
        if len(self.pond.orgs) + len(self.pond.eggs) == 0:
            self.running = False
            self.updateText()
            
class WorldWidget(QWidget):
    
    def __init__(self, parent):
        
        super().__init__()
        self.parent = parent
        self.setFixedSize(int(self.parent.pond.dimensions['x']*0.5),
                          int(self.parent.pond.dimensions['y']*0.5))

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
        for i in self.parent.pond.food:
            x = i.pos['x']/self.parent.pond.dimensions['x']*size.width()
            y = i.pos['y']/self.parent.pond.dimensions['y']*size.height()
            #qp.drawPoint(x, y)
            qp.drawEllipse(QRectF(x-3, y-3, 6, 6))
            
        qp.setPen(Qt.blue)   
        brush.setColor(Qt.blue)
        qp.setBrush(brush)
        # Draw the eggs
        for i in self.parent.pond.eggs:
            x = i.pos['x']/self.parent.pond.dimensions['x']*size.width()
            y = i.pos['y']/self.parent.pond.dimensions['y']*size.height()
            qp.drawRect(QRectF(x-3, y-3, 6, 6))
            
        qp.setPen(Qt.green)   
        brush.setColor(Qt.green)
        qp.setBrush(brush)
        # Draw the organisms
        for i in self.parent.pond.orgs:
            x = i.pos['x']/self.parent.pond.dimensions['x']*size.width()
            y = i.pos['y']/self.parent.pond.dimensions['y']*size.height()
            qp.drawEllipse(QRectF(x-5, y-5, 10, 10))
            
class OrgsList(QWidget):
    
    def __init__(self, parent):
        
        super().__init__()
        self.parent = parent
        self.pond = self.parent.pond
        self.initUI()
        
    def initUI(self):
        
        self.layout = QVBoxLayout()
        self.layout.stretch(1)
        self.orgsDisplays = []
        for org in self.pond.orgs:
            self.orgsDisplays.append(OrgsDisplay(self, org))
            self.layout.addWidget(self.orgsDisplays[-1])
        self.setLayout(self.layout)
        
    def updateText(self):
        
        self.checkAlive()
        #self.checkNewOrgs()
        for i in self.orgsDisplays:
            i.updateText()
            
    def checkAlive(self):
        for i in self.orgsDisplays:
            if i.org.food <= 0:
                #self.layout.removeWidget(i)
                i.setParent(None)
                #i.deleteLater()
                i = None
        self.orgsDisplays = [i for i in self.orgsDisplays if i != None]
    
    def checkNewOrgs(self):
        
        for org in self.pond.orgs:
            if not any(i.org == org for i in self.orgsDisplays):
                self.orgsDisplays.append(OrgsDisplay(self, org))
                self.layout.addWidget(self.orgsDisplays[-1])
        
class OrgsDisplay(QWidget):
    
    def __init__(self, parent, org):
        
        super().__init__()
        self.parent = parent
        self.org = org
        self.initUI()
        
    def initUI(self):
        
        self.nameText = QLabel(f"<b>{self.org.name}</b>")
        self.foodText = QLabel(f"Food: {round(self.org.food, 2)}")
        
        layout = QVBoxLayout()
        layout.stretch(1)
        layout.addWidget(self.nameText)
        layout.addWidget(self.foodText)
        self.setLayout(layout)
        self.setFixedWidth(150)
        
    def updateText(self):
        
        self.nameText.setText(f"<b>{self.org.name}</b>")
        self.foodText.setText(f"Food: {round(self.org.food, 2)}")
        
class PondThread(QThread):
    
    def __init__(self, master, fps = 100, cps = 100):
        
        super().__init__()
        self.master = master
        self.fps = fps
        self.cps = cps
        self.lastUpdate = 0
        self.updateTime = self.cps/self.fps

    def run(self):
        while self.master.running:
            self.lastUpdate += 1
            self.updatePond()
            if self.lastUpdate >= self.updateTime:
                self.lastUpdate = 0
                self.updateGUI()
            self.master.checkFinished()
            time.sleep(0.01)
        self.updateGUI()
        print('Thread finished')
    
    def updatePond(self):
        
        self.master.pond.step()
        
    def updateGUI(self):
        
        self.master.world.update()
        self.master.updateText()
        
if __name__=='__main__':
    
    app = QApplication(sys.argv)
    ex = MainWindow(pond.Pond(1))
    for i in ex.pond.orgs:
        i.loadBrain('brain4', mutate = False)
    ex.pondThread.start()
    sys.exit(app.exec_())