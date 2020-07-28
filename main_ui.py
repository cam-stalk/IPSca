# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'scanner.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_IPSca(object):
    def setupUi(self, IPSca):
        IPSca.setObjectName("IPSca")
        IPSca.resize(405, 666)
        IPSca.setStyleSheet("selection-color: rgb(0, 0, 255);\n"
"selection-background-color: rgb(255, 255, 255);\n"
"alternate-background-color: rgb(255, 255, 255);\n"
"background-color: rgb(48, 48, 48);")
        IPSca.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.centralwidget = QtWidgets.QWidget(IPSca)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Export = QtWidgets.QTabWidget(self.centralwidget)
        self.Export.setStyleSheet("selection-color: rgb(0, 0, 255);\n"
"selection-background-color: rgb(255, 255, 255);\n"
"alternate-background-color: rgb(255, 255, 255);\n"
"background-color: rgb(48, 48, 48);")
        self.Export.setObjectName("Export")
        self.scan = QtWidgets.QWidget()
        self.scan.setObjectName("scan")
        self.label_6 = QtWidgets.QLabel(self.scan)
        self.label_6.setGeometry(QtCore.QRect(210, 150, 38, 17))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("color: rgb(170, 0, 0);")
        self.label_6.setObjectName("label_6")
        self.dead_label = QtWidgets.QLabel(self.scan)
        self.dead_label.setGeometry(QtCore.QRect(300, 170, 41, 17))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.dead_label.setFont(font)
        self.dead_label.setObjectName("dead_label")
        self.label = QtWidgets.QLabel(self.scan)
        self.label.setGeometry(QtCore.QRect(10, 10, 61, 23))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(170, 0, 0);")
        self.label.setObjectName("label")
        self.successful_label = QtWidgets.QLabel(self.scan)
        self.successful_label.setGeometry(QtCore.QRect(300, 190, 41, 17))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.successful_label.setFont(font)
        self.successful_label.setObjectName("successful_label")
        self.targetsList = QtWidgets.QTextEdit(self.scan)
        self.targetsList.setGeometry(QtCore.QRect(10, 40, 151, 192))
        font = QtGui.QFont()
        font.setItalic(False)
        font.setUnderline(False)
        self.targetsList.setFont(font)
        self.targetsList.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.targetsList.setStyleSheet("color: rgb(115, 115, 115);\n"
"background-color: rgb(43, 43, 43);")
        self.targetsList.setObjectName("targetsList")
        self.dead = QtWidgets.QLabel(self.scan)
        self.dead.setGeometry(QtCore.QRect(210, 170, 37, 17))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.dead.setFont(font)
        self.dead.setStyleSheet("color: rgb(170, 0, 0);")
        self.dead.setObjectName("dead")
        self.import_btn = QtWidgets.QToolButton(self.scan)
        self.import_btn.setGeometry(QtCore.QRect(78, 10, 61, 26))
        self.import_btn.setStyleSheet("color: rgb(190, 0, 0);\n"
"font: 75 8pt \"MS Shell Dlg 2\";\n"
"border: none;\n"
"font: 75 14pt \"MS Shell Dlg 2\";\n"
"font-weight: bold;\n"
"background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"stop: 0 #a6a6a6, stop: 0.08 #7f7f7f,\n"
"stop: 0.39999 #717171, stop: 0.4 #626262,\n"
"stop: 0.9 #4c4c4c, stop: 1 #333333);\n"
"}\n"
"\n"
"#bottomFrame {\n"
"border: none;\n"
"background: white;\n"
"")
        self.import_btn.setObjectName("import_btn")
        self.shuffle_btn = QtWidgets.QPushButton(self.scan)
        self.shuffle_btn.setGeometry(QtCore.QRect(10, 230, 151, 23))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.shuffle_btn.setFont(font)
        self.shuffle_btn.setStyleSheet("color: rgb(190, 0, 0);\n"
"font: 75 8pt \"MS Shell Dlg 2\";\n"
"border: none;\n"
"font: 75 14pt \"MS Shell Dlg 2\";\n"
"font-weight: bold;\n"
"background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"stop: 0 #a6a6a6, stop: 0.08 #7f7f7f,\n"
"stop: 0.39999 #717171, stop: 0.4 #626262,\n"
"stop: 0.9 #4c4c4c, stop: 1 #333333);\n"
"}\n"
"\n"
"#bottomFrame {\n"
"border: none;\n"
"background: white;\n"
"")
        self.shuffle_btn.setObjectName("shuffle_btn")
        self.terminal = QtWidgets.QTextBrowser(self.scan)
        self.terminal.setGeometry(QtCore.QRect(9, 308, 351, 192))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.terminal.setFont(font)
        self.terminal.setStyleSheet("color: rgb(115, 115, 115);\n"
"background-color: rgb(43, 43, 43);\n"
"\n"
"")
        self.terminal.setObjectName("terminal")
        self.progress_2 = QtWidgets.QLabel(self.scan)
        self.progress_2.setGeometry(QtCore.QRect(10, 550, 256, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.progress_2.setFont(font)
        self.progress_2.setStyleSheet("color: rgb(122, 255, 60);\n"
"font-weight: bold;")
        self.progress_2.setText("")
        self.progress_2.setObjectName("progress_2")
        self.alive_label = QtWidgets.QLabel(self.scan)
        self.alive_label.setGeometry(QtCore.QRect(300, 150, 41, 17))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.alive_label.setFont(font)
        self.alive_label.setStyleSheet("color: rgb(255, 255, 255);\n"
"color: rgb(170, 170, 170);")
        self.alive_label.setObjectName("alive_label")
        self.label_8 = QtWidgets.QLabel(self.scan)
        self.label_8.setGeometry(QtCore.QRect(210, 190, 77, 17))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("color: rgb(170, 0, 0);")
        self.label_8.setObjectName("label_8")
        self.label_5 = QtWidgets.QLabel(self.scan)
        self.label_5.setGeometry(QtCore.QRect(9, 268, 44, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color: rgb(170, 0, 0);")
        self.label_5.setObjectName("label_5")
        self.filter_line = QtWidgets.QLineEdit(self.scan)
        self.filter_line.setGeometry(QtCore.QRect(63, 268, 301, 34))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.filter_line.setFont(font)
        self.filter_line.setStyleSheet("color: rgb(115, 115, 115);\n"
"border-color: rgb(170, 170, 255);\n"
"background-color: rgb(43, 43, 43);")
        self.filter_line.setText("")
        self.filter_line.setObjectName("filter_line")
        self.stop_btn = QtWidgets.QPushButton(self.scan)
        self.stop_btn.setGeometry(QtCore.QRect(288, 230, 71, 23))
        self.stop_btn.setStyleSheet("color: rgb(190, 0, 0);\n"
"font: 75 8pt \"MS Shell Dlg 2\";\n"
"border: none;\n"
"font: 75 14pt \"MS Shell Dlg 2\";\n"
"font-weight: bold;\n"
"background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"stop: 0 #a6a6a6, stop: 0.08 #7f7f7f,\n"
"stop: 0.39999 #717171, stop: 0.4 #626262,\n"
"stop: 0.9 #4c4c4c, stop: 1 #333333);\n"
"}\n"
"\n"
"#bottomFrame {\n"
"border: none;\n"
"background: white;\n"
"")
        self.stop_btn.setObjectName("stop_btn")
        self.load_status = QtWidgets.QLabel(self.scan)
        self.load_status.setGeometry(QtCore.QRect(210, 70, 141, 51))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.load_status.setFont(font)
        self.load_status.setStyleSheet("font-weight: bold;")
        self.load_status.setText("")
        self.load_status.setObjectName("load_status")
        self.scan_btn = QtWidgets.QPushButton(self.scan)
        self.scan_btn.setGeometry(QtCore.QRect(210, 230, 71, 23))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.scan_btn.setFont(font)
        self.scan_btn.setStyleSheet("color: rgb(190, 0, 0);\n"
"font: 75 8pt \"MS Shell Dlg 2\";\n"
"border: none;\n"
"font: 75 14pt \"MS Shell Dlg 2\";\n"
"font-weight: bold;\n"
"background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"stop: 0 #a6a6a6, stop: 0.08 #7f7f7f,\n"
"stop: 0.39999 #717171, stop: 0.4 #626262,\n"
"stop: 0.9 #4c4c4c, stop: 1 #333333);\n"
"}\n"
"\n"
"#bottomFrame {\n"
"border: none;\n"
"background: white;\n"
"")
        self.scan_btn.setObjectName("scan_btn")
        self.export_path = QtWidgets.QLabel(self.scan)
        self.export_path.setGeometry(QtCore.QRect(226, 598, 16, 16))
        self.export_path.setStyleSheet("color: rgb(170, 0, 0);")
        self.export_path.setText("")
        self.export_path.setObjectName("export_path")
        self.progressBar = QtWidgets.QProgressBar(self.scan)
        self.progressBar.setGeometry(QtCore.QRect(10, 500, 351, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.progressBar.setFont(font)
        self.progressBar.setStyleSheet("QProgressBar {\n"
"border: 1px solid black;\n"
"text-align: top;\n"
"padding: 1px;\n"
"border-top-left-radius: 7px;\n"
"border-bottom-left-radius: 7px;\n"
"border-top-right-radius: 7px;\n"
"border-bottom-right-radius: 7px;\n"
"background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1,\n"
"stop: 0 #fff,\n"
"stop: 0.4999 #eee,\n"
"stop: 0.5 #ddd,\n"
"stop: 1 #eee ),\n"
"rgba(255, 255, 255, .10);  \n"
"width: 15px;\n"
"}\n"
"QProgressBar::chunk {\n"
"background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0,\n"
"stop: 0 #0000ff,\n"
"stop: 1 #ff0000 );\n"
"border-top-left-radius: 7px;\n"
"border-bottom-left-radius: 7px;\n"
"border-top-right-radius: 7px;\n"
"border-bottom-right-radius: 7px;\n"
"border: 1px solid black;\n"
"}")
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName("progressBar")
        self.action_label = QtWidgets.QLabel(self.scan)
        self.action_label.setGeometry(QtCore.QRect(-10, 500, 371, 20))
        font = QtGui.QFont()
        font.setPointSize(6)
        font.setBold(True)
        font.setWeight(75)
        self.action_label.setFont(font)
        self.action_label.setAutoFillBackground(False)
        self.action_label.setStyleSheet("margin-left: auto;\n"
"margin-right: auto;\n"
"font-weight: bold;\n"
"background-color: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(255, 235, 235, 206), stop:0.35 rgba(255, 188, 188, 80), stop:0.4 rgba(255, 162, 162, 80), stop:0.425 rgba(255, 132, 132, 156), stop:0.44 rgba(252, 128, 128, 80), stop:1 rgba(255, 255, 255, 0));\n"
"color: yellow;")
        self.action_label.setText("")
        self.action_label.setAlignment(QtCore.Qt.AlignCenter)
        self.action_label.setObjectName("action_label")
        self.progress = QtWidgets.QLabel(self.scan)
        self.progress.setGeometry(QtCore.QRect(10, 530, 256, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.progress.setFont(font)
        self.progress.setStyleSheet("color: rgb(122, 255, 60);\n"
"font-weight: bold;")
        self.progress.setText("")
        self.progress.setObjectName("progress")
        self.Export.addTab(self.scan, "")
        self.settings = QtWidgets.QWidget()
        self.settings.setObjectName("settings")
        self.threads_edit = QtWidgets.QLineEdit(self.settings)
        self.threads_edit.setGeometry(QtCore.QRect(40, 200, 81, 29))
        self.threads_edit.setStyleSheet("background-color: rgb(43, 43, 43);\n"
"selection-color: rgb(0, 0, 255);\n"
"alternate-background-color: rgb(0, 170, 0);\n"
"color: rgb(170, 0, 0);")
        self.threads_edit.setObjectName("threads_edit")
        self.analysisThreadLabel = QtWidgets.QLabel(self.settings)
        self.analysisThreadLabel.setGeometry(QtCore.QRect(40, 180, 152, 18))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.analysisThreadLabel.setFont(font)
        self.analysisThreadLabel.setStyleSheet("color: rgb(170, 0, 0);")
        self.analysisThreadLabel.setObjectName("analysisThreadLabel")
        self.timeout_edit = QtWidgets.QLineEdit(self.settings)
        self.timeout_edit.setGeometry(QtCore.QRect(40, 260, 91, 29))
        self.timeout_edit.setStyleSheet("selection-color: rgb(0, 0, 255);\n"
"background-color: rgb(43, 43, 43);\n"
"color: rgb(170, 0, 0);")
        self.timeout_edit.setObjectName("timeout_edit")
        self.socketTimeoutLabel = QtWidgets.QLabel(self.settings)
        self.socketTimeoutLabel.setGeometry(QtCore.QRect(40, 240, 101, 18))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.socketTimeoutLabel.setFont(font)
        self.socketTimeoutLabel.setStyleSheet("color: rgb(170, 0, 0);")
        self.socketTimeoutLabel.setObjectName("socketTimeoutLabel")
        self.brute_chbx = QtWidgets.QCheckBox(self.settings)
        self.brute_chbx.setEnabled(True)
        self.brute_chbx.setGeometry(QtCore.QRect(140, 260, 94, 23))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.brute_chbx.setFont(font)
        self.brute_chbx.setStyleSheet("color: rgb(170, 0, 0);")
        self.brute_chbx.setObjectName("brute_chbx")
        self.threads_portscan_edit = QtWidgets.QLineEdit(self.settings)
        self.threads_portscan_edit.setGeometry(QtCore.QRect(40, 60, 81, 31))
        self.threads_portscan_edit.setStyleSheet("background-color: rgb(43, 43, 43);\n"
"selection-color: rgb(0, 0, 255);\n"
"alternate-background-color: rgb(0, 170, 0);\n"
"color: rgb(170, 0, 0);")
        self.threads_portscan_edit.setObjectName("threads_portscan_edit")
        self.portThreadsLabel = QtWidgets.QLabel(self.settings)
        self.portThreadsLabel.setGeometry(QtCore.QRect(40, 37, 121, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.portThreadsLabel.setFont(font)
        self.portThreadsLabel.setStyleSheet("color: rgb(170, 0, 0);")
        self.portThreadsLabel.setObjectName("portThreadsLabel")
        self.iot_chbx = QtWidgets.QCheckBox(self.settings)
        self.iot_chbx.setGeometry(QtCore.QRect(140, 200, 78, 23))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.iot_chbx.setFont(font)
        self.iot_chbx.setStyleSheet("color: rgb(170, 0, 0);")
        self.iot_chbx.setObjectName("iot_chbx")
        self.portScanLabel = QtWidgets.QLabel(self.settings)
        self.portScanLabel.setGeometry(QtCore.QRect(10, 10, 121, 18))
        font = QtGui.QFont()
        font.setFamily("Noto Sans")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(9)
        self.portScanLabel.setFont(font)
        self.portScanLabel.setStyleSheet("color: rgb(170, 0, 0);\n"
"font: 75 italic 11pt \"Noto Sans\";")
        self.portScanLabel.setObjectName("portScanLabel")
        self.analysisLabel = QtWidgets.QLabel(self.settings)
        self.analysisLabel.setGeometry(QtCore.QRect(10, 150, 121, 18))
        font = QtGui.QFont()
        font.setFamily("Noto Sans")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(9)
        self.analysisLabel.setFont(font)
        self.analysisLabel.setStyleSheet("color: rgb(170, 0, 0);\n"
"font: 75 italic 11pt \"Noto Sans\";")
        self.analysisLabel.setObjectName("analysisLabel")
        self.addMassParTextbox = QtWidgets.QLineEdit(self.settings)
        self.addMassParTextbox.setGeometry(QtCore.QRect(140, 60, 231, 31))
        self.addMassParTextbox.setStyleSheet("background-color: rgb(43, 43, 43);\n"
"selection-color: rgb(0, 0, 255);\n"
"alternate-background-color: rgb(0, 170, 0);\n"
"color: rgb(170, 0, 0);")
        self.addMassParTextbox.setObjectName("addMassParTextbox")
        self.additionalMasParLabel = QtWidgets.QLabel(self.settings)
        self.additionalMasParLabel.setGeometry(QtCore.QRect(140, 40, 211, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.additionalMasParLabel.setFont(font)
        self.additionalMasParLabel.setStyleSheet("color: rgb(170, 0, 0);")
        self.additionalMasParLabel.setObjectName("additionalMasParLabel")
        self.portsList = QtWidgets.QLineEdit(self.settings)
        self.portsList.setGeometry(QtCore.QRect(140, 120, 231, 31))
        self.portsList.setStyleSheet("background-color: rgb(43, 43, 43);\n"
"selection-color: rgb(0, 0, 255);\n"
"alternate-background-color: rgb(0, 170, 0);\n"
"color: rgb(170, 0, 0);")
        self.portsList.setObjectName("portsList")
        self.portsLabel = QtWidgets.QLabel(self.settings)
        self.portsLabel.setGeometry(QtCore.QRect(140, 97, 121, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.portsLabel.setFont(font)
        self.portsLabel.setStyleSheet("color: rgb(170, 0, 0);")
        self.portsLabel.setObjectName("portsLabel")
        self.Export.addTab(self.settings, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.format_combo = QtWidgets.QComboBox(self.tab)
        self.format_combo.setGeometry(QtCore.QRect(90, 20, 111, 31))
        self.format_combo.setStyleSheet("color: rgb(190, 0, 0);\n"
"font: 75 8pt \"MS Shell Dlg 2\";\n"
"border: none;\n"
"font: 75 14pt \"MS Shell Dlg 2\";\n"
"font-weight: bold;\n"
"background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"stop: 0 #a6a6a6, stop: 0.08 #7f7f7f,\n"
"stop: 0.39999 #717171, stop: 0.4 #626262,\n"
"stop: 0.9 #4c4c4c, stop: 1 #333333);\n"
"\n"
"}\n"
"\n"
"#bottomFrame {\n"
"border: none;\n"
"background: white;\n"
"")
        self.format_combo.setObjectName("format_combo")
        self.format_combo.addItem("")
        self.format_combo.addItem("")
        self.format_combo.addItem("")
        self.submit_export = QtWidgets.QPushButton(self.tab)
        self.submit_export.setGeometry(QtCore.QRect(220, 20, 71, 31))
        self.submit_export.setStyleSheet("color: rgb(190, 0, 0);\n"
"font: 75 8pt \"MS Shell Dlg 2\";\n"
"border: none;\n"
"font: 75 14pt \"MS Shell Dlg 2\";\n"
"font-weight: bold;\n"
"background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"stop: 0 #a6a6a6, stop: 0.08 #7f7f7f,\n"
"stop: 0.39999 #717171, stop: 0.4 #626262,\n"
"stop: 0.9 #4c4c4c, stop: 1 #333333);\n"
"}\n"
"\n"
"#bottomFrame {\n"
"border: none;\n"
"background: white;\n"
"")
        self.submit_export.setObjectName("submit_export")
        self.label_4 = QtWidgets.QLabel(self.tab)
        self.label_4.setGeometry(QtCore.QRect(10, 20, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: rgb(170, 0, 0);")
        self.label_4.setObjectName("label_4")
        self.export_path_2 = QtWidgets.QLabel(self.tab)
        self.export_path_2.setGeometry(QtCore.QRect(10, 90, 441, 20))
        self.export_path_2.setStyleSheet("color: rgb(170, 0, 0);")
        self.export_path_2.setText("")
        self.export_path_2.setObjectName("export_path_2")
        self.Export.addTab(self.tab, "")
        self.horizontalLayout.addWidget(self.Export)
        IPSca.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(IPSca)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 405, 23))
        self.menubar.setObjectName("menubar")
        IPSca.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(IPSca)
        self.statusbar.setObjectName("statusbar")
        IPSca.setStatusBar(self.statusbar)
        self.label.setBuddy(self.import_btn)

        self.retranslateUi(IPSca)
        self.Export.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(IPSca)

    def retranslateUi(self, IPSca):
        _translate = QtCore.QCoreApplication.translate
        IPSca.setWindowTitle(_translate("IPSca", "IPSca"))
        self.label_6.setText(_translate("IPSca", "ALIVE:"))
        self.dead_label.setText(_translate("IPSca", "<span style=\"color:#FF0000;\">0</span>"))
        self.label.setText(_translate("IPSca", "Targets"))
        self.successful_label.setText(_translate("IPSca", "<span style=\"color:#4cbb17;\">0</span>"))
        self.targetsList.setHtml(_translate("IPSca", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Noto Sans\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt;\">192.168.0.0/24</span></p></body></html>"))
        self.dead.setText(_translate("IPSca", "DEAD:"))
        self.import_btn.setText(_translate("IPSca", "->"))
        self.shuffle_btn.setText(_translate("IPSca", "Shuffle"))
        self.alive_label.setText(_translate("IPSca", "0"))
        self.label_8.setText(_translate("IPSca", "SUCCESSFUL:"))
        self.label_5.setText(_translate("IPSca", "Filter :"))
        self.stop_btn.setText(_translate("IPSca", "STOP"))
        self.scan_btn.setText(_translate("IPSca", "SCAN"))
        self.Export.setTabText(self.Export.indexOf(self.scan), _translate("IPSca", "Scan"))
        self.threads_edit.setText(_translate("IPSca", "20"))
        self.analysisThreadLabel.setText(_translate("IPSca", "Threads"))
        self.timeout_edit.setText(_translate("IPSca", "5"))
        self.socketTimeoutLabel.setText(_translate("IPSca", "SocketTimeout"))
        self.brute_chbx.setText(_translate("IPSca", "Bruteforce"))
        self.threads_portscan_edit.setText(_translate("IPSca", "1000"))
        self.portThreadsLabel.setText(_translate("IPSca", "Threads"))
        self.iot_chbx.setText(_translate("IPSca", "IoT only"))
        self.portScanLabel.setText(_translate("IPSca", "PORT SCAN"))
        self.analysisLabel.setText(_translate("IPSca", "ANALYSING"))
        self.addMassParTextbox.setText(_translate("IPSca", "-e tun0"))
        self.additionalMasParLabel.setText(_translate("IPSca", "Additional masscan parameters"))
        self.portsList.setText(_translate("IPSca", "80,81,8080,8081,1024"))
        self.portsLabel.setText(_translate("IPSca", "Ports"))
        self.Export.setTabText(self.Export.indexOf(self.settings), _translate("IPSca", "Settings"))
        self.format_combo.setItemText(0, _translate("IPSca", "json"))
        self.format_combo.setItemText(1, _translate("IPSca", "csv"))
        self.format_combo.setItemText(2, _translate("IPSca", "html"))
        self.submit_export.setText(_translate("IPSca", "OK"))
        self.label_4.setText(_translate("IPSca", "<html><head/><body><p><span style=\" font-weight:600;\">Format</span></p></body></html>"))
        self.Export.setTabText(self.Export.indexOf(self.tab), _translate("IPSca", "Export"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    IPSca = QtWidgets.QMainWindow()
    ui = Ui_IPSca()
    ui.setupUi(IPSca)
    IPSca.show()
    sys.exit(app.exec_())

