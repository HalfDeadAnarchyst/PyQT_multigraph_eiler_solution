# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1249, 881)
        MainWindow.setToolTipDuration(1)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setEnabled(True)
        self.tabWidget.setGeometry(QtCore.QRect(20, 10, 1221, 831))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        font.setPointSize(11)
        self.tabWidget.setFont(font)
        self.tabWidget.setObjectName("tabWidget")
        self.setup_tab = QtWidgets.QWidget()
        self.setup_tab.setObjectName("setup_tab")
        self.start_button = QtWidgets.QPushButton(self.setup_tab)
        self.start_button.setEnabled(False)
        self.start_button.setGeometry(QtCore.QRect(10, 710, 411, 51))
        self.start_button.setObjectName("start_button")
        self.region_groupBox = QtWidgets.QGroupBox(self.setup_tab)
        self.region_groupBox.setGeometry(QtCore.QRect(0, 10, 421, 151))
        self.region_groupBox.setObjectName("region_groupBox")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.region_groupBox)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 20, 401, 81))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.region_verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.region_verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.region_verticalLayout.setObjectName("region_verticalLayout")
        self.region_comboBox = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.region_comboBox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.region_comboBox.setEditable(True)
        self.region_comboBox.setMaxCount(2147483644)
        self.region_comboBox.setObjectName("region_comboBox")
        self.region_comboBox.addItem("")
        self.region_verticalLayout.addWidget(self.region_comboBox)
        self.district_comboBox = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.district_comboBox.setEnabled(False)
        self.district_comboBox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.district_comboBox.setEditable(True)
        self.district_comboBox.setMaxCount(2147483644)
        self.district_comboBox.setObjectName("district_comboBox")
        self.district_comboBox.addItem("")
        self.region_verticalLayout.addWidget(self.district_comboBox)
        self.region_sel_comboBox = QtWidgets.QComboBox(self.region_groupBox)
        self.region_sel_comboBox.setEnabled(False)
        self.region_sel_comboBox.setGeometry(QtCore.QRect(10, 110, 321, 22))
        self.region_sel_comboBox.setObjectName("region_sel_comboBox")
        self.region_sel_en_checkBox = QtWidgets.QCheckBox(self.region_groupBox)
        self.region_sel_en_checkBox.setEnabled(False)
        self.region_sel_en_checkBox.setGeometry(QtCore.QRect(350, 100, 71, 41))
        self.region_sel_en_checkBox.setObjectName("region_sel_en_checkBox")
        self.tasks_map_groupBox = QtWidgets.QGroupBox(self.setup_tab)
        self.tasks_map_groupBox.setGeometry(QtCore.QRect(440, 10, 771, 351))
        self.tasks_map_groupBox.setObjectName("tasks_map_groupBox")
        self.tasks_table = QtWidgets.QTableWidget(self.tasks_map_groupBox)
        self.tasks_table.setGeometry(QtCore.QRect(10, 20, 751, 321))
        self.tasks_table.setObjectName("tasks_table")
        self.tasks_table.setColumnCount(0)
        self.tasks_table.setRowCount(0)
        self.heli_groupBox = QtWidgets.QGroupBox(self.setup_tab)
        self.heli_groupBox.setGeometry(QtCore.QRect(10, 390, 411, 261))
        self.heli_groupBox.setStatusTip("")
        self.heli_groupBox.setObjectName("heli_groupBox")
        self.heli_comboBox = QtWidgets.QComboBox(self.heli_groupBox)
        self.heli_comboBox.setGeometry(QtCore.QRect(8, 20, 371, 21))
        self.heli_comboBox.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.heli_comboBox.setEditable(True)
        self.heli_comboBox.setMaxCount(2147483644)
        self.heli_comboBox.setObjectName("heli_comboBox")
        self.heli_comboBox.addItem("")
        self.heli_label_chars = QtWidgets.QLabel(self.heli_groupBox)
        self.heli_label_chars.setGeometry(QtCore.QRect(140, 50, 121, 21))
        self.heli_label_chars.setObjectName("heli_label_chars")
        self.heli_speed_label = QtWidgets.QLabel(self.heli_groupBox)
        self.heli_speed_label.setGeometry(QtCore.QRect(10, 110, 121, 21))
        self.heli_speed_label.setObjectName("heli_speed_label")
        self.heli_dist_label = QtWidgets.QLabel(self.heli_groupBox)
        self.heli_dist_label.setGeometry(QtCore.QRect(10, 190, 121, 21))
        self.heli_dist_label.setObjectName("heli_dist_label")
        self.heli_mass_label = QtWidgets.QLabel(self.heli_groupBox)
        self.heli_mass_label.setGeometry(QtCore.QRect(10, 70, 121, 21))
        self.heli_mass_label.setObjectName("heli_mass_label")
        self.heli_mass_label_param = QtWidgets.QLabel(self.heli_groupBox)
        self.heli_mass_label_param.setGeometry(QtCore.QRect(10, 90, 47, 21))
        self.heli_mass_label_param.setObjectName("heli_mass_label_param")
        self.heli_speed_label_param = QtWidgets.QLabel(self.heli_groupBox)
        self.heli_speed_label_param.setGeometry(QtCore.QRect(10, 130, 47, 21))
        self.heli_speed_label_param.setObjectName("heli_speed_label_param")
        self.heli_dist_label_param = QtWidgets.QLabel(self.heli_groupBox)
        self.heli_dist_label_param.setGeometry(QtCore.QRect(10, 210, 47, 21))
        self.heli_dist_label_param.setObjectName("heli_dist_label_param")
        self.heli_picture = QtWidgets.QLabel(self.heli_groupBox)
        self.heli_picture.setGeometry(QtCore.QRect(140, 90, 261, 141))
        self.heli_picture.setText("")
        self.heli_picture.setObjectName("heli_picture")
        self.heli_dist_label_2 = QtWidgets.QLabel(self.heli_groupBox)
        self.heli_dist_label_2.setGeometry(QtCore.QRect(10, 150, 121, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.heli_dist_label_2.setFont(font)
        self.heli_dist_label_2.setObjectName("heli_dist_label_2")
        self.heli_dist_label_param_2 = QtWidgets.QLabel(self.heli_groupBox)
        self.heli_dist_label_param_2.setGeometry(QtCore.QRect(10, 170, 47, 21))
        self.heli_dist_label_param_2.setObjectName("heli_dist_label_param_2")
        self.start_progressBar = QtWidgets.QProgressBar(self.setup_tab)
        self.start_progressBar.setGeometry(QtCore.QRect(10, 670, 421, 31))
        self.start_progressBar.setProperty("value", 0)
        self.start_progressBar.setObjectName("start_progressBar")
        self.tasks_groupBox = QtWidgets.QGroupBox(self.setup_tab)
        self.tasks_groupBox.setEnabled(False)
        self.tasks_groupBox.setGeometry(QtCore.QRect(10, 180, 411, 181))
        self.tasks_groupBox.setObjectName("tasks_groupBox")
        self.add_task_button = QtWidgets.QPushButton(self.tasks_groupBox)
        self.add_task_button.setGeometry(QtCore.QRect(230, 90, 81, 26))
        self.add_task_button.setObjectName("add_task_button")
        self.delete_task_button = QtWidgets.QPushButton(self.tasks_groupBox)
        self.delete_task_button.setGeometry(QtCore.QRect(320, 90, 81, 26))
        self.delete_task_button.setObjectName("delete_task_button")
        self.task_from_comboBox = QtWidgets.QComboBox(self.tasks_groupBox)
        self.task_from_comboBox.setGeometry(QtCore.QRect(230, 30, 171, 21))
        self.task_from_comboBox.setObjectName("task_from_comboBox")
        self.task_to_comboBox = QtWidgets.QComboBox(self.tasks_groupBox)
        self.task_to_comboBox.setGeometry(QtCore.QRect(230, 60, 171, 21))
        self.task_to_comboBox.setObjectName("task_to_comboBox")
        self.task_from_label = QtWidgets.QLabel(self.tasks_groupBox)
        self.task_from_label.setGeometry(QtCore.QRect(200, 30, 47, 21))
        self.task_from_label.setObjectName("task_from_label")
        self.task_to_label = QtWidgets.QLabel(self.tasks_groupBox)
        self.task_to_label.setGeometry(QtCore.QRect(210, 60, 41, 21))
        self.task_to_label.setObjectName("task_to_label")
        self.task_amount_label = QtWidgets.QLabel(self.tasks_groupBox)
        self.task_amount_label.setGeometry(QtCore.QRect(230, 120, 41, 21))
        self.task_amount_label.setObjectName("task_amount_label")
        self.task_amount_num_label = QtWidgets.QLabel(self.tasks_groupBox)
        self.task_amount_num_label.setGeometry(QtCore.QRect(270, 120, 21, 21))
        self.task_amount_num_label.setObjectName("task_amount_num_label")
        self.task_all_amount_label = QtWidgets.QLabel(self.tasks_groupBox)
        self.task_all_amount_label.setGeometry(QtCore.QRect(130, 150, 81, 21))
        self.task_all_amount_label.setAlignment(QtCore.Qt.AlignCenter)
        self.task_all_amount_label.setObjectName("task_all_amount_label")
        self.task_all_amount_num_label = QtWidgets.QLabel(self.tasks_groupBox)
        self.task_all_amount_num_label.setGeometry(QtCore.QRect(220, 150, 21, 21))
        self.task_all_amount_num_label.setObjectName("task_all_amount_num_label")
        self.import_task_button = QtWidgets.QPushButton(self.tasks_groupBox)
        self.import_task_button.setGeometry(QtCore.QRect(10, 30, 161, 26))
        self.import_task_button.setObjectName("import_task_button")
        self.save_task_button = QtWidgets.QPushButton(self.tasks_groupBox)
        self.save_task_button.setGeometry(QtCore.QRect(10, 60, 161, 26))
        self.save_task_button.setObjectName("save_task_button")
        self.generate_task_button = QtWidgets.QPushButton(self.tasks_groupBox)
        self.generate_task_button.setGeometry(QtCore.QRect(10, 90, 161, 25))
        self.generate_task_button.setObjectName("generate_task_button")
        self.len_map_groupBox = QtWidgets.QGroupBox(self.setup_tab)
        self.len_map_groupBox.setGeometry(QtCore.QRect(440, 390, 771, 371))
        self.len_map_groupBox.setObjectName("len_map_groupBox")
        self.len_table = QtWidgets.QTableWidget(self.len_map_groupBox)
        self.len_table.setGeometry(QtCore.QRect(10, 20, 751, 341))
        self.len_table.setObjectName("len_table")
        self.len_table.setColumnCount(0)
        self.len_table.setRowCount(0)
        self.tabWidget.addTab(self.setup_tab, "")
        self.statistics_tab = QtWidgets.QWidget()
        self.statistics_tab.setEnabled(False)
        self.statistics_tab.setObjectName("statistics_tab")
        self.barc_path_groupBox = QtWidgets.QGroupBox(self.statistics_tab)
        self.barc_path_groupBox.setGeometry(QtCore.QRect(10, 10, 591, 411))
        self.barc_path_groupBox.setObjectName("barc_path_groupBox")
        self.barc_path_widget = QtWidgets.QWidget(self.barc_path_groupBox)
        self.barc_path_widget.setGeometry(QtCore.QRect(0, 30, 591, 381))
        self.barc_path_widget.setObjectName("barc_path_widget")
        self.barc_money_groupBox = QtWidgets.QGroupBox(self.statistics_tab)
        self.barc_money_groupBox.setGeometry(QtCore.QRect(610, 10, 591, 411))
        self.barc_money_groupBox.setObjectName("barc_money_groupBox")
        self.barc_money_widget = QtWidgets.QWidget(self.barc_money_groupBox)
        self.barc_money_widget.setGeometry(QtCore.QRect(10, 30, 581, 381))
        self.barc_money_widget.setObjectName("barc_money_widget")
        self.results_groupBox = QtWidgets.QGroupBox(self.statistics_tab)
        self.results_groupBox.setGeometry(QtCore.QRect(610, 440, 601, 361))
        self.results_groupBox.setObjectName("results_groupBox")
        self.result_stats_tableview = QtWidgets.QTableWidget(self.results_groupBox)
        self.result_stats_tableview.setGeometry(QtCore.QRect(10, 20, 581, 331))
        self.result_stats_tableview.setObjectName("result_stats_tableview")
        self.result_stats_tableview.setColumnCount(0)
        self.result_stats_tableview.setRowCount(0)
        self.results_groupBox_2 = QtWidgets.QGroupBox(self.statistics_tab)
        self.results_groupBox_2.setGeometry(QtCore.QRect(10, 620, 471, 181))
        self.results_groupBox_2.setObjectName("results_groupBox_2")
        self.result_path_tableview = QtWidgets.QTableWidget(self.results_groupBox_2)
        self.result_path_tableview.setGeometry(QtCore.QRect(10, 20, 451, 151))
        self.result_path_tableview.setObjectName("result_path_tableview")
        self.result_path_tableview.setColumnCount(0)
        self.result_path_tableview.setRowCount(0)
        self.results_groupBox_3 = QtWidgets.QGroupBox(self.statistics_tab)
        self.results_groupBox_3.setGeometry(QtCore.QRect(10, 440, 471, 181))
        self.results_groupBox_3.setObjectName("results_groupBox_3")
        self.result_base_label = QtWidgets.QLabel(self.results_groupBox_3)
        self.result_base_label.setGeometry(QtCore.QRect(10, 30, 181, 16))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        font.setPointSize(11)
        self.result_base_label.setFont(font)
        self.result_base_label.setObjectName("result_base_label")
        self.result_length_label = QtWidgets.QLabel(self.results_groupBox_3)
        self.result_length_label.setGeometry(QtCore.QRect(10, 60, 181, 16))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        font.setPointSize(11)
        self.result_length_label.setFont(font)
        self.result_length_label.setObjectName("result_length_label")
        self.result_lands_label = QtWidgets.QLabel(self.results_groupBox_3)
        self.result_lands_label.setGeometry(QtCore.QRect(10, 90, 181, 16))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        font.setPointSize(11)
        self.result_lands_label.setFont(font)
        self.result_lands_label.setObjectName("result_lands_label")
        self.result_path_label = QtWidgets.QLabel(self.results_groupBox_3)
        self.result_path_label.setGeometry(QtCore.QRect(10, 120, 181, 16))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        font.setPointSize(11)
        self.result_path_label.setFont(font)
        self.result_path_label.setObjectName("result_path_label")
        self.result_base_textBrowser = QtWidgets.QTextBrowser(self.results_groupBox_3)
        self.result_base_textBrowser.setGeometry(QtCore.QRect(200, 20, 261, 31))
        self.result_base_textBrowser.setObjectName("result_base_textBrowser")
        self.result_length_textBrowser = QtWidgets.QTextBrowser(self.results_groupBox_3)
        self.result_length_textBrowser.setGeometry(QtCore.QRect(200, 50, 261, 31))
        self.result_length_textBrowser.setObjectName("result_length_textBrowser")
        self.result_lands_textBrowser = QtWidgets.QTextBrowser(self.results_groupBox_3)
        self.result_lands_textBrowser.setGeometry(QtCore.QRect(200, 80, 261, 31))
        self.result_lands_textBrowser.setObjectName("result_lands_textBrowser")
        self.result_path_textBrowser = QtWidgets.QTextBrowser(self.results_groupBox_3)
        self.result_path_textBrowser.setGeometry(QtCore.QRect(200, 110, 261, 31))
        self.result_path_textBrowser.setObjectName("result_path_textBrowser")
        self.result_cost_label = QtWidgets.QLabel(self.results_groupBox_3)
        self.result_cost_label.setGeometry(QtCore.QRect(10, 150, 181, 16))
        font = QtGui.QFont()
        font.setFamily("Bahnschrift")
        font.setPointSize(11)
        self.result_cost_label.setFont(font)
        self.result_cost_label.setObjectName("result_cost_label")
        self.result_cost_textBrowser = QtWidgets.QTextBrowser(self.results_groupBox_3)
        self.result_cost_textBrowser.setGeometry(QtCore.QRect(200, 140, 261, 31))
        self.result_cost_textBrowser.setObjectName("result_cost_textBrowser")
        self.tabWidget.addTab(self.statistics_tab, "")
        self.db_tab = QtWidgets.QWidget()
        self.db_tab.setObjectName("db_tab")
        self.button_db_add = QtWidgets.QPushButton(self.db_tab)
        self.button_db_add.setGeometry(QtCore.QRect(10, 720, 321, 61))
        self.button_db_add.setObjectName("button_db_add")
        self.button_db_delete = QtWidgets.QPushButton(self.db_tab)
        self.button_db_delete.setGeometry(QtCore.QRect(350, 720, 341, 61))
        self.button_db_delete.setObjectName("button_db_delete")
        self.db_groupBox_all = QtWidgets.QGroupBox(self.db_tab)
        self.db_groupBox_all.setGeometry(QtCore.QRect(10, 0, 1191, 701))
        self.db_groupBox_all.setObjectName("db_groupBox_all")
        self.db_table = QtWidgets.QTableWidget(self.db_groupBox_all)
        self.db_table.setGeometry(QtCore.QRect(0, 60, 1181, 631))
        self.db_table.setObjectName("db_table")
        self.db_table.setColumnCount(0)
        self.db_table.setRowCount(0)
        self.db_comboBox_sel = QtWidgets.QComboBox(self.db_groupBox_all)
        self.db_comboBox_sel.setGeometry(QtCore.QRect(20, 30, 401, 22))
        self.db_comboBox_sel.setObjectName("db_comboBox_sel")
        self.db_comboBox_sel.addItem("")
        self.db_comboBox_sel.addItem("")
        self.db_message_label = QtWidgets.QLabel(self.db_tab)
        self.db_message_label.setGeometry(QtCore.QRect(730, 720, 341, 61))
        self.db_message_label.setTextFormat(QtCore.Qt.AutoText)
        self.db_message_label.setScaledContents(False)
        self.db_message_label.setAlignment(QtCore.Qt.AlignCenter)
        self.db_message_label.setIndent(0)
        self.db_message_label.setObjectName("db_message_label")
        self.tabWidget.addTab(self.db_tab, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1249, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Диплом"))
        self.start_button.setText(_translate("MainWindow", "Выполнить расчёт"))
        self.region_groupBox.setTitle(_translate("MainWindow", "Населённые пункты"))
        self.region_comboBox.setCurrentText(_translate("MainWindow", "Выберите регион"))
        self.region_comboBox.setItemText(0, _translate("MainWindow", "Выберите регион"))
        self.district_comboBox.setCurrentText(_translate("MainWindow", "Выберите район"))
        self.district_comboBox.setItemText(0, _translate("MainWindow", "Выберите район"))
        self.region_sel_en_checkBox.setText(_translate("MainWindow", "В сети"))
        self.tasks_map_groupBox.setTitle(_translate("MainWindow", "ТАБЛИЦА ЗАДАЧ"))
        self.heli_groupBox.setTitle(_translate("MainWindow", "Вертолёты"))
        self.heli_comboBox.setCurrentText(_translate("MainWindow", "Выберите вертолёт"))
        self.heli_comboBox.setItemText(0, _translate("MainWindow", "Выберите вертолёт"))
        self.heli_label_chars.setText(_translate("MainWindow", " ХАРАКТЕРИСТИКИ"))
        self.heli_speed_label.setText(_translate("MainWindow", "Кр.скорость, км/ч:"))
        self.heli_dist_label.setText(_translate("MainWindow", "Дальн. (нагр.), км:"))
        self.heli_mass_label.setText(_translate("MainWindow", "Масса (пуст.), кг:"))
        self.heli_mass_label_param.setText(_translate("MainWindow", "NaN"))
        self.heli_speed_label_param.setText(_translate("MainWindow", "NaN"))
        self.heli_dist_label_param.setText(_translate("MainWindow", "NaN"))
        self.heli_dist_label_2.setText(_translate("MainWindow", "Дальн. (пуст.), км:"))
        self.heli_dist_label_param_2.setText(_translate("MainWindow", "NaN"))
        self.tasks_groupBox.setTitle(_translate("MainWindow", "Задачи"))
        self.add_task_button.setText(_translate("MainWindow", "Добавить"))
        self.delete_task_button.setText(_translate("MainWindow", "Удалить"))
        self.task_from_label.setText(_translate("MainWindow", " Из:"))
        self.task_to_label.setText(_translate("MainWindow", "В:"))
        self.task_amount_label.setText(_translate("MainWindow", "Задач:"))
        self.task_amount_num_label.setText(_translate("MainWindow", " 10"))
        self.task_all_amount_label.setText(_translate("MainWindow", "Всего задач:"))
        self.task_all_amount_num_label.setText(_translate("MainWindow", " 10"))
        self.import_task_button.setText(_translate("MainWindow", "Импортировать задачи"))
        self.save_task_button.setText(_translate("MainWindow", "Сохранить задачи"))
        self.generate_task_button.setText(_translate("MainWindow", "Сгенерировать задачи"))
        self.len_map_groupBox.setTitle(_translate("MainWindow", "ТАБЛИЦА РАССТОЯНИЙ"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.setup_tab), _translate("MainWindow", "Исходные данные"))
        self.barc_path_groupBox.setTitle(_translate("MainWindow", "РЕЗУЛЬТАТЫ (длина маршрута)"))
        self.barc_money_groupBox.setTitle(_translate("MainWindow", "РЕЗУЛЬТАТЫ (денежные затраты)"))
        self.results_groupBox.setTitle(_translate("MainWindow", "Данные обо всех вариантах размещения базы"))
        self.results_groupBox_2.setTitle(_translate("MainWindow", "Данные о маршруте "))
        self.results_groupBox_3.setTitle(_translate("MainWindow", "Данные о рациональном варианте размещения базы"))
        self.result_base_label.setText(_translate("MainWindow", "ВЕРТОДРОМ БАЗИРОВАНИЯ:"))
        self.result_length_label.setText(_translate("MainWindow", "ДЛИНА МАРШРУТА, КМ:"))
        self.result_lands_label.setText(_translate("MainWindow", "КОЛ-ВО РЕЙСОВ:"))
        self.result_path_label.setText(_translate("MainWindow", "ПУТЬ (КОЛ-ВО НП):"))
        self.result_cost_label.setText(_translate("MainWindow", "СТОИМОСТЬ, РУБ:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.statistics_tab), _translate("MainWindow", "Результаты"))
        self.button_db_add.setText(_translate("MainWindow", "Добавить запись"))
        self.button_db_delete.setText(_translate("MainWindow", "Удалить запись"))
        self.db_groupBox_all.setTitle(_translate("MainWindow", "DataBase"))
        self.db_comboBox_sel.setItemText(0, _translate("MainWindow", "Cities"))
        self.db_comboBox_sel.setItemText(1, _translate("MainWindow", "Helicopters"))
        self.db_message_label.setText(_translate("MainWindow", "Готов к работе"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.db_tab), _translate("MainWindow", "Базы Данных"))