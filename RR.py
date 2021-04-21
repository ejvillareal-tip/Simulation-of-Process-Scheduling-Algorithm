import sys 
from PyQt5.QtWidgets import (QMainWindow, QWidget, QDesktopWidget, QApplication, QPushButton, QLabel, QTableWidget)
from PyQt5 import *

from PyQt5 import QtGui, QtCore, Qt
from PyQt5.QtGui import *
from PyQt5.Qt import *
from PyQt5.QtCore import *

import numpy as np

#Other Win
import main

RR_values = []
RR_qt = 0

class RR_Win(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "Round Robin"
        self.width = 1200
        self.height = 950

        self.initWindow()

    def initWindow(self):
        self.resize(self.width, self.height)
        self.setWindowTitle(self.title)

        self.Labels()
        self.Buttons()
        self.center()
        self.Table()
        
        self.show()

    #move window to center
    def center(self):
        # geometry of the main window
        qr = self.frameGeometry()

        # center point of screen
        cp = QDesktopWidget().availableGeometry().center()

        # move rectangle's center point to screen's center point
        qr.moveCenter(cp)

        # top left of rectangle becomes top left of window centering it
        self.move(qr.topLeft())

    def Labels(self):
        titleLabel = QLabel("Round Robin", self)
        titleLabel.setGeometry(QRect(30+150+250,50, 900, 100))
        titleLabel.setStyleSheet("QWidget { color: Black}")
        titleLabel.setFont(QtGui.QFont('Sanserif', 30, QtGui.QFont.Bold))

        quantumTimeLbl = QLabel("Quantum Time: ", self)
        quantumTimeLbl.setGeometry(QRect(100,800, 500, 50))
        quantumTimeLbl.setStyleSheet("QWidget { color: Black}")
        quantumTimeLbl.setFont(QtGui.QFont('Sanserif', 15, QtGui.QFont.Bold))

        self.onlyInt = QIntValidator()
        self.quantumTimeLE = QLineEdit("",self)
        self.quantumTimeLE.setFont(QtGui.QFont('Times New Roman',14))
        self.quantumTimeLE.setGeometry(QRect(100+200,800+10, 100, 35))
        self.quantumTimeLE.setValidator(self.onlyInt)
        
    def Buttons(self):
        backButton = QPushButton('Back', self)
        backButton.setGeometry(QRect(150,850, 150, 50))
        #backButton.setStyleSheet("QWidget {background-color: Blue}")
        backButton.setFont(QtGui.QFont('Times New Roman',14))
        backButton.clicked.connect(self.clickedBack)

        self.addBtnHeight = 0

        self.addButton = QPushButton('', self)
        self.addButton.setIcon(QtGui.QIcon('Icons/plus.png'))
        self.addButton.setGeometry(QRect(45,220, 37, 37))
        self.addButton.clicked.connect(self.clickedAdd)

        self.deleteBtnHeight = 0

        self.deleteButton = QPushButton('', self)
        self.deleteButton.setIcon(QtGui.QIcon('Icons/remove.png'))
        self.deleteButton.setGeometry(QRect(1080,220, 37, 37))
        self.deleteButton.clicked.connect(self.clickedDelete)
        self.deleteButton.hide()

        calButton = QPushButton('Simulate', self)
        calButton.setGeometry(QRect(1200-150-165,850, 150, 50))
        calButton.setFont(QtGui.QFont('Times New Roman',14))
        calButton.clicked.connect(self._clickedCal)
    
    def Table(self):
        self.row = 1
        self.column = 3
        self.RRTable = QTableWidget(self.row,self.column,self)
        self.RRTable.setGeometry(QRect(100,50+100, 975, 650))
        
        self.RRTable.setHorizontalHeaderLabels(("Process ID", "Arrival Time", "Burst Time"))
        self.RRTable.setColumnWidth(0,316)
        self.RRTable.setColumnWidth(1,316)
        self.RRTable.setColumnWidth(2,316)

        self.updateAddRow()

    def clickedBack(self):
        self._processSchedWin = main.processSchedWin()
        self._processSchedWin.show()
        self.hide()

    def clickedAdd(self):
        self.addBtnHeight += 37
        self.animAddBtn = QPropertyAnimation(self.addButton, b"geometry")
        self.animAddBtn.setDuration(1)
        self.animAddBtn.start()
        self.animAddBtn.setEndValue(QRect(45,220 + self.addBtnHeight, 37, 37))

        
        self.RRTable.insertRow(self.rowCount)

        self.deleteBtnHeight += 37
        self.animdelBtn = QPropertyAnimation(self.deleteButton, b"geometry")
        self.animdelBtn.setDuration(1)
        self.animdelBtn.start()
        self.animdelBtn.setEndValue(QRect(1080,220 - 37 + self.deleteBtnHeight, 37, 37))
        self.deleteButton.show()

        self.updateAddRow()

    def clickedDelete(self):
        if self.RRTable.rowCount() > 0:
            self.RRTable.removeRow(self.RRTable.rowCount()-1)
            
            self.addBtnHeight -= 37
            self.animAddBtn.start()
            self.animAddBtn.setEndValue(QRect(45,220 + self.addBtnHeight, 37, 37))

            self.deleteBtnHeight -= 37
            self.animdelBtn.start()
            self.animdelBtn.setEndValue(QRect(1080,220 - 37 + self.deleteBtnHeight, 37, 37))

            #self.updateTableLineEdit()

        if self.RRTable.rowCount() == 1:
            self.deleteButton.hide()

        self.updateDelRow()

    def updateAddRow(self):
        self.rowCount = self.RRTable.rowCount()
        self.onlyInt = QIntValidator()
        for i in range(1,3): 
            self.tableLE = QLineEdit()
            self.tableLE.setFont(QtGui.QFont('Times New Roman',14))
            self.tableLE.setValidator(self.onlyInt)
            self.RRTable.setCellWidget(self.RRTable.rowCount()-1, i, self.tableLE)
        
        if self.RRTable.rowCount() > 0:
            for x in range(0,self.RRTable.rowCount()):
                self.tableLable = QLineEdit()
                self.tableLable.setFont(QtGui.QFont('Times New Roman',14))
                self.RRTable.setCellWidget(self.RRTable.rowCount()-1, 0, self.tableLable)

    def updateDelRow(self):
        self.rowCount = self.RRTable.rowCount()
        self.onlyInt = QIntValidator()
        for i in range(1,3): 
            self.tableLE = QLineEdit()
            self.tableLE.setFont(QtGui.QFont('Times New Roman',14))
            self.tableLE.setValidator(self.onlyInt)
            self.RRTable.setCellWidget(self.RRTable.rowCount(), i, self.tableLE)
        
        if self.RRTable.rowCount() > 0:
            for x in range(0,self.RRTable.rowCount()):
                self.tableLable = QLineEdit()
                self.tableLable.setFont(QtGui.QFont('Times New Roman',14))
                self.RRTable.setCellWidget(self.RRTable.rowCount(), 0, self.tableLable)

    def _clickedCal(self):
        self.valTables = []
        
        for row in range(0,self.rowCount):
            col_index = 0
            for col in range(0,3):
                item = self.RRTable.cellWidget(row, col)
                item_text = item.text()
                if col_index > 0:
                    if item_text == '':
                        self.valTables.append(item_text)
                    else:
                        self.valTables.append(int(item_text))
                else:
                    self.valTables.append(item_text)
                    
                col_index += 1

        self.lengthVal = len(self.valTables)

        #getting all process ID
        processID = []
        i = 0 # PID starts with 0 index
        while i < self.lengthVal:
            processID.append(self.valTables[i])
            i += 3

        emptyCount = 0
        for i in range(self.lengthVal):
            if self.valTables[i] == '':
                emptyCount+=1
        
        if emptyCount > 0:
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Information)
                msg.setText("Error: empty value")
                msg.setInformativeText("There is/are empty value, Please fill it before to proceed.")
                msg.setWindowTitle("Error")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.show()

        elif str(self.quantumTimeLE.text()) == '':
            QTmsg = QMessageBox(self)
            QTmsg.setIcon(QMessageBox.Information)
            QTmsg.setText("Error: Quantum time is empty")
            QTmsg.setInformativeText("Please enter the quantum time before to proceed.")
            QTmsg.setWindowTitle("Error")
            QTmsg.setStandardButtons(QMessageBox.Ok)
            QTmsg.show()

        # check if there is/are the same process ID
        elif len(processID) != len(set(processID)):
            msgPID = QMessageBox(self)
            msgPID.setIcon(QMessageBox.Information)
            msgPID.setText("Error: Same process ID")
            msgPID.setInformativeText("There are the same process ID, Please check it.")
            msgPID.setWindowTitle("Error")
            msgPID.setStandardButtons(QMessageBox.Ok)
            msgPID.show()

        else:
            global RR_values
            global RR_qt
            RR_qt = int(self.quantumTimeLE.text())
            RR_values = self.valTables
            self._RR_ResultWin = RR_ResultWin()
            self._RR_ResultWin.show()
            self.hide()

class RR_ResultWin(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = "First Come First Serve Result"
        self.width = 1200
        self.height = 950

        self.initWindow()

    def initWindow(self):
        self.resize(self.width, self.height)
        self.setWindowTitle(self.title)
        self.center()

        self.variables()
        self.resultLabels()
        self.resultTable()
        self.resultButtons()

        self.show()

    #move window to center
    def center(self):
        # geometry of the main window
        qr = self.frameGeometry()

        # center point of screen
        cp = QDesktopWidget().availableGeometry().center()

        # move rectangle's center point to screen's center point
        qr.moveCenter(cp)

        # top left of rectangle becomes top left of window centering it
        self.move(qr.topLeft())

    def resultLabels(self):
        titleResultLabel = QLabel("Result", self)
        titleResultLabel.setGeometry(QRect(30+125+350,50, 900, 100))
        titleResultLabel.setStyleSheet("QWidget { color: Black}")
        titleResultLabel.setFont(QtGui.QFont('Sanserif', 30, QtGui.QFont.Bold))

    def variables(self):
        global RR_values
        global RR_qt
        self.RR_valTables = RR_values
        lengthRR_valTables = len(self.RR_valTables)

        values = self.RR_valTables

        allProcess = int(lengthRR_valTables/3)

        listedVal = []

        for i in range(allProcess): # adding 2d array
            listedVal.append([])

        indexVal = 0
        for row in range(allProcess): # Converting the values to 2d array
            for col in range(3):
                listedVal[row].append(values[indexVal])
                indexVal += 1

        quantumTime = RR_qt
        qtProcess = 0

        totalEndTime = 0
        queue = []
        oldindex = []

        numTerminate = 0

        time = 0
        loop = True
        while loop != False: 
            # if is there process arrive in current time then add it into queue
            for row in range(allProcess):
                if time == int(listedVal[row][1]): ## if there equal to time
                    queue.append([]) ## adding to queue
                    queue[int(len(queue))-1].append(listedVal[row][0])
                    queue[int(len(queue))-1].append(int(listedVal[row][1]))
                    queue[int(len(queue))-1].append(int(listedVal[row][2]))

            if qtProcess == quantumTime: # if the quantum time reach the max then switch the index to top
                #saving the last queue that have been executed
                oldindex.append([])
                oldindex[0].append(queue[0][0])
                oldindex[0].append(int(queue[0][1]))
                oldindex[0].append(int(queue[0][2]))

                queue.pop(0) # remove that process
                
                queue.append([]) ## add again the process
                queue[int(len(queue)) - 1].append(oldindex[0][0])
                queue[int(len(queue)) - 1].append(int(oldindex[0][1]))
                queue[int(len(queue)) - 1].append(int(oldindex[0][2]))

                oldindex.pop(0) # then remove the old process to make new variable

                qtProcess = 0 # reset after processing

            # executing the first in queue
            if int(len(queue)) > 0:
                queue[0][2] = int(queue[0][2]) - 1 # subtract 1 burst time
                qtProcess += 1
                if int(queue[0][2]) == 0:
                    qtProcess = 0

            qRow = 0
            while qRow < int(len(queue)):
                if int(queue[qRow][2]) <= 0: # if the process has 0 burst time, delete that process in queue
                    for x in range (allProcess): # inputing the end time process
                        if listedVal[x][0] == queue[qRow][0]: # if process id is same as in queue, then input it in specific process
                            listedVal[x].append(time+1)
                            numTerminate +=1
                    queue.pop(qRow)
                qRow += 1

            if numTerminate == allProcess:
                totalEndTime = time+1
                loop = False
            
            time += 1

        for i in range(allProcess): #inputing the turn around time and waiting time
            listedVal[i].append(int(listedVal[i][3]) - int(listedVal[i][1])) # End Time - Arrival Time
            listedVal[i].append(int(listedVal[i][4]) - int(listedVal[i][2])) # Turn Around Time - Burst Time

        #print(listedVal)
        self.cpuUtil = 0
        totalBurstTime = 0
        self.aveTT = 0
        self.aveWT = 0

        for i in range(allProcess): #computing the Cpu Utilization
            totalBurstTime += int(listedVal[i][2])

        self.cpuUtil = (totalBurstTime/totalEndTime)*100 # formula for Cpu Utilization

        for i in range(allProcess): #computing the average turn around time
            self.aveWT += int(listedVal[i][5])/allProcess
            self.aveTT += int(listedVal[i][4])/allProcess

        #print("CPU Utilization: ", "%.2f" %self.cpuUtil)
        #print("Average Waiting Time: ", "%.2f" %self.aveWT)
        #print("Average Turn Around Time: ", "%.2f" %self.aveTT)


        self.allProcessNew = allProcess
        self.listedValNew = listedVal

    def resultTable(self):
        self.rowResultTable = self.allProcessNew
        self.columnResultTable = 6
        self.RRResultTable = QTableWidget(self.rowResultTable,self.columnResultTable,self)
        self.RRResultTable.setGeometry(QRect(100,50+100, 975, 350))
        self.RRResultTable.setFont(QtGui.QFont('Sanserif', 12))

        self.RRResultTable.setHorizontalHeaderLabels(("Process ID", "Arrival Time", "Burst Time","End Time","Turn Around Time","Wating Time"))
        self.RRResultTable.setColumnWidth(0,158)
        self.RRResultTable.setColumnWidth(1,158)
        self.RRResultTable.setColumnWidth(2,158)
        self.RRResultTable.setColumnWidth(3,158)
        self.RRResultTable.setColumnWidth(4,158)
        self.RRResultTable.setColumnWidth(5,158)

        for i in range(self.rowResultTable): # inputting the End time into table
            self.RRResultTable.setItem(i,0,QTableWidgetItem(str(self.listedValNew[i][0])))
            self.RRResultTable.setItem(i,1,QTableWidgetItem(str(self.listedValNew[i][1])))
            self.RRResultTable.setItem(i,2,QTableWidgetItem(str(self.listedValNew[i][2]))) 
            self.RRResultTable.setItem(i,3,QTableWidgetItem(str(self.listedValNew[i][3])))
            self.RRResultTable.setItem(i,4,QTableWidgetItem(str(self.listedValNew[i][4])))
            self.RRResultTable.setItem(i,5,QTableWidgetItem(str(self.listedValNew[i][5])))
            
        self.aveWTLabel = QLabel(self)
        self.aveWTLabel.setGeometry(QRect(100,500, 900, 50))
        self.aveWTLabel.setStyleSheet("QWidget { color: Black}")
        self.aveWTLabel.setFont(QtGui.QFont('Sanserif', 13, QtGui.QFont.Bold))
        self.aveWTLabel.setText("Average Waiting Time: " + "%.2f" %(self.aveWT))

        self.aveTTLabel = QLabel(self)
        self.aveTTLabel.setGeometry(QRect(100,500 + 25, 900, 50))
        self.aveTTLabel.setStyleSheet("QWidget { color: Black}")
        self.aveTTLabel.setFont(QtGui.QFont('Sanserif', 13, QtGui.QFont.Bold))
        self.aveTTLabel.setText("Average Turn Around Time: " + "%.2f" %(self.aveTT))

        self.CPUUtilLabel = QLabel(self)
        self.CPUUtilLabel.setGeometry(QRect(100,500 + 25 + 25, 900, 50))
        self.CPUUtilLabel.setStyleSheet("QWidget { color: Black}")
        self.CPUUtilLabel.setFont(QtGui.QFont('Sanserif', 13, QtGui.QFont.Bold))
        self.CPUUtilLabel.setText("CPU Utilization: " + "%.0f" %(self.cpuUtil) + "%")

    def resultButtons(self):
        backButton = QPushButton('Back to RR', self)
        backButton.setGeometry(QRect(150,850, 150, 50))
        #backButton.setStyleSheet("QWidget {background-color: Blue}")
        backButton.setFont(QtGui.QFont('Times New Roman',14))
        backButton.clicked.connect(self.clickedBackFCFS)

        calButton = QPushButton('Main Menu', self)
        calButton.setGeometry(QRect(1200-150-165,850, 150, 50))
        calButton.setFont(QtGui.QFont('Times New Roman',14))
        calButton.clicked.connect(self.clickedMainMenu)

    def clickedBackFCFS(self):
        self._RR_Win = RR_Win()
        self._RR_Win.show()
        self.hide()

    def clickedMainMenu(self):
        self._processSchedWin = main.processSchedWin()
        self._processSchedWin.show()
        self.hide()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = RR_Win()
    sys.exit(app.exec_())