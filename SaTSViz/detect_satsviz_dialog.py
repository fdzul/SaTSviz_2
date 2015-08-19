# -*- coding: utf-8 -*-
"""
/***************************************************************************
 satsvizDialog
                                 A QGIS plugin
 SaTSViz aims to provide QGIS an additional feature of analysis by utilising SaTScan. All input files needed for SaTScan are created by the plugin and the output files from it are read by the plugin and fed in to QGIS to visualise the analysis results. The plugin provides benefit to both the software's
                             -------------------
        begin                : 2015-06-24
        git sha              : $Format:%H$
        copyright            : (C) 2015 by by Vasuda Trehan under guidance of Shiva Reddy Koti
        email                : vasudatrehan@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os
from qgis.core import *
import qgis.utils


from PyQt4 import uic,QtCore ,QtGui

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'detect_satsviz_dialog_base.ui'))


class satsvizDialog(QtGui.QDialog, FORM_CLASS): 
    def __init__(self, parent=None):                      #calling toolButton2
        """Constructor."""
        super(satsvizDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
    # calling all the things here initially
        self.setupUi(self)
        self.toolButton
        self.comboBox_5
        self.comboBox
        self.comboBox_2
        self.comboBox_3
        self.comboBox_4
        
        self.radioButton
        self.comboBox_7
        self.radioButton_2
        self.comboBox_13
        self.radioButton_3
        self.comboBox_8
        self.radioButton_4
        self.comboBox_10
        self.radioButton_5
        self.comboBox_9
        self.radioButton_6
        self.comboBox_11
        
              #connecting ToolButton2 and function
        QtCore.QObject.connect(self.comboBox_5, QtCore.SIGNAL("currentIndexChanged(QString)"),self.fields)  #connecting combo_box 5 to ramaining combo box usiing .fields function
        QtCore.QObject.connect(self.toolButton, QtCore.SIGNAL("clicked()"), self.open2)
        QtCore.QObject.connect(self.radioButton, QtCore.SIGNAL("clicked()"), self.open3)
        QtCore.QObject.connect(self.radioButton_2, QtCore.SIGNAL("clicked()"), self.open3)
        QtCore.QObject.connect(self.radioButton_3, QtCore.SIGNAL("clicked()"), self.open3)
        QtCore.QObject.connect(self.radioButton_4, QtCore.SIGNAL("clicked()"), self.open3)
        QtCore.QObject.connect(self.radioButton_5, QtCore.SIGNAL("clicked()"), self.open3)
        QtCore.QObject.connect(self.radioButton_6, QtCore.SIGNAL("clicked()"), self.open3)



# calling the toolButton2 and getting the input in the text 4 line code
    def open2(self):                                                    #defining the function
        self.fname2=QtGui.QFileDialog.getSaveFileName(self,"Save Data File",".","Text files(*.txt);;All Files(*.*)")   # for opening and closing the folder if we will use *.shp file then shape file will open
        print ('path file:',self.fname2)
        self.lineEdit.setText(self.fname2)    # it is the text where our inout is shown            
    def fields(self):        # that function fields is defined here
        layers=qgis.utils.iface.legendInterface().layers()
        i= self.comboBox_5.currentIndex()
        layer= layers[i]
        fields=layer.pendingFields()
        self.comboBox.clear()
        self.comboBox_2.clear()
        self.comboBox_3.clear()
        self.comboBox_4.clear()
        self.comboBox.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_4.addItem("") 
        
        for field in fields:
            
            self.comboBox.addItem(field.name())     # by .name we will get the fields name
            self.comboBox_2.addItem(field.name())
            self.comboBox_3.addItem(field.name())
            self.comboBox_4.addItem(field.name())
            

    def open3(self):
             if self.radioButton.isChecked():
                self.comboBox_7.setEnabled(True)
                self.comboBox_10.setDisabled(True)
                self.comboBox_13.setDisabled(True)
                self.comboBox_8.setDisabled(True)
                self.comboBox_9.setDisabled(True)
                self.comboBox_11.setDisabled(True)
             if self.radioButton_2.isChecked():
                self.comboBox_13.setEnabled(True)
                self.comboBox_7.setDisabled(True)
                self.comboBox_10.setDisabled(True)
                self.comboBox_8.setDisabled(True)
                self.comboBox_9.setDisabled(True)
                self.comboBox_11.setDisabled(True)
             if self.radioButton_3.isChecked():
                self.comboBox_8.setEnabled(True)
                self.comboBox_7.setDisabled(True)
                self.comboBox_13.setDisabled(True)
                self.comboBox_10.setDisabled(True)
                self.comboBox_9.setDisabled(True)
                self.comboBox_11.setDisabled(True)
             if self.radioButton_4.isChecked():
                self.comboBox_10.setEnabled(True)
                self.comboBox_7.setDisabled(True)
                self.comboBox_13.setDisabled(True)
                self.comboBox_8.setDisabled(True)
                self.comboBox_9.setDisabled(True)
                self.comboBox_11.setDisabled(True)
             if self.radioButton_5.isChecked():
                self.comboBox_9.setEnabled(True)
                self.comboBox_7.setDisabled(True)
                self.comboBox_13.setDisabled(True)
                self.comboBox_10.setDisabled(True)
                self.comboBox_8.setDisabled(True)
                self.comboBox_11.setDisabled(True)
             if self.radioButton_6.isChecked():
                self.comboBox_11.setEnabled(True)
                self.comboBox_7.setDisabled(True)
                self.comboBox_13.setDisabled(True)
                self.comboBox_10.setDisabled(True)
                self.comboBox_9.setDisabled(True)
                self.comboBox_8.setDisabled(True)
    
               
            





            
                
