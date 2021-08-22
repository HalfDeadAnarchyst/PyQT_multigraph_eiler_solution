import main
import sql_lib
import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtChart import *
from design import Ui_MainWindow
from tqdm import tqdm


def calc_money(distance, heli, k_vp, dist_k):
    c_vp = (heli.mass_full / 1000) * 9500 * heli.koef_diff
    cost_aeno = (heli.cost_aeno * 1000 * heli.fuel * 2) * 10 ** (-2)
    c_to = 5.2 * heli.cost_service * (heli.mass_empty / 1000) ** 0.845
    c_zp = 7.45 * heli.cost_crew * (heli.mass_empty / 1000) ** 0.069
    c_gsm = (float(heli.fuel_consum) / float(heli.time_engine)) * float(heli.cost_fuel) * float(heli.koef_gsm)
    c_per = 1.1 * (c_to + c_zp + c_gsm)
    c_ker = 5.85 * heli.cost_crew * (heli.mass_empty / 1000) ** 0.83
    c_lch = c_per + c_ker
    hours = distance / heli.curce_speed
    cost_all = c_lch * hours + (c_vp + cost_aeno) * k_vp
    return cost_all


class design(QtWidgets.QMainWindow):
    def __init__(self):
        super(design, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # self state vars
        self.region_ready = False
        self.tasks_ready = False
        self.helicopter_ready = False
        self.launched_once = False

        self.chosen_region = str(self.ui.region_comboBox.currentText())
        self.chosen_district = ""
        self.chosen_city = ""
        self.cities_list = []
        self.city_state = False

        self.chosen_heli = main.Helicopter("Mi-8P", 1, 550.0, 1, 225.0, 7000.0, 11570.0, 1470.0, 3.0,
                                           1.04, 1.0, 300.0, 100.0, 27.0, 214.0, 550.0)

        self.current_tasks = []
        self.current_graph = main.Graph()
        # connect functions
        # main
        self.ui.start_button.clicked.connect(self.run_calculation)

        # region
        self.ui.region_comboBox.currentTextChanged.connect(self.trigger_region_check)
        self.ui.district_comboBox.currentTextChanged.connect(self.trigger_district_check)
        self.ui.region_sel_comboBox.currentTextChanged.connect(self.trigger_city_check)
        self.ui.region_sel_en_checkBox.stateChanged.connect(self.trigger_region_checkbox)
        self.load_regions()

        # helicopter
        self.ui.heli_comboBox.currentTextChanged.connect(self.check_heli_state)
        self.load_helis()

        # tasks
        self.ui.generate_task_button.clicked.connect(self.gen_tasks)
        self.ui.import_task_button.clicked.connect(self.load_tasks)
        self.ui.save_task_button.clicked.connect(self.save_tasks)
        self.ui.add_task_button.clicked.connect(self.add_task)
        self.ui.delete_task_button.clicked.connect(self.delete_task)
        self.ui.task_to_comboBox.currentTextChanged.connect(self.tasks_combobox_status)
        self.ui.task_from_comboBox.currentTextChanged.connect(self.tasks_combobox_status)
        self.ui.task_amount_num_label.setText("0")
        self.ui.task_all_amount_num_label.setText("0")

        # db_tab
        self.chosen_db = self.ui.db_comboBox_sel.currentText()
        self.ui.db_comboBox_sel.currentTextChanged.connect(self.db_load)
        self.le = QtWidgets.QLineEdit()
        # self.le.textChanged.connect(self.db_upload_data)
        self.ui.db_table.itemChanged.connect(self.db_upload_data)
        self.db_load()
        self.ui.button_db_delete.clicked.connect(self.db_delete_row)
        self.ui.button_db_add.clicked.connect(self.db_add_row)

        # progress bar
        self.ui.start_progressBar.setValue(0)
        self.progress_len = 0
        self.progress = 0

        # results
        self.dist_maximum_height = 0.0
        self.dist_minimum_height = 0.0
        self.money_maximum_height = 0.0
        self.money_minimum_height = 0.0

        self.dist_k_high = QBarSet("Км_k")
        self.dist_high = QBarSet("Км")
        self.money_high = QBarSet("Руб")

        self.results_cities_names = []

        self.usable_vertices = []
        self.red_names = []

    def find_non_full_run(self, paths, heli, g):
        results = []
        # k = 1  # dist_full/dist_empty
        k = heli.fuel / heli.dist_empty
        vertices = g.vertices.copy()
        for vertice in vertices:
            if vertice.name in self.red_names:
                vertices.remove(vertice)
        for v1 in tqdm(vertices):
            self.progress = self.progress + 1
            self.ui.start_progressBar.setValue(int((self.progress / self.progress_len) * 100))
            copy_paths = paths.copy()
            # results.append([v1, find_best_path(v1, v1, copy_paths, [v1], 0, heli.fuel, heli.fuel, 0)])
            results.append([v1, main.find_longest_path(v1, v1, copy_paths, [v1], 0, heli.fuel, heli.fuel, 0, heli, k)])
        return results

    def find_rest_full_run(self, results, heli):
        output = []
        # k = 1  # dist_full/dist_empty
        k = heli.fuel / heli.dist_empty
        for res in tqdm(results):
            self.progress = self.progress + 1
            self.ui.start_progressBar.setValue(int((self.progress / self.progress_len) * 100))
            if res[1][1][-1] != res[0]:
                res[1] = list(res[1])
                res[1][1].append(res[0])
                res[1][2] += float(res[1][1][-2].conns[res[1][1][-1]]) * k
                res[1] = tuple(res[1])
            res = main.find_best_path(res[0], res[0], res[1][3].copy(), res[1][1], res[1][2], heli.fuel, heli.fuel,
                                      res[1][0], heli, k)
            if res[0][-1] != res[0][0]:
                res = list(res)
                res[0].append(res[0][0])
                res[1] += res[0][-2].conns[res[0][-1]] * k
                res = tuple(res)
            # print(len(res[0]), res)
            output.append(res)
        return output

    def get_best_result(self, results):
        best_calced_money = 0
        best_result = []
        for res in results:
            base_count = 0
            for city in res[0]:
                if city == res[0][0]:
                    base_count = base_count + 1
            calced_money = calc_money(res[1], self.chosen_heli, base_count, 1)
            if len(best_result) == 0:
                best_result = res
                best_calced_money = calced_money
            else:
                if best_calced_money > calced_money:
                    best_result = res
                    best_calced_money = calced_money
        self.progress = self.progress + 1
        self.ui.start_progressBar.setValue(int((self.progress / self.progress_len) * 100))
        return best_result

    def run_calculation(self):

        self.ui.region_groupBox.setEnabled(False)
        self.ui.tasks_groupBox.setEnabled(False)
        self.ui.heli_groupBox.setEnabled(False)
        self.ui.start_progressBar.setValue(0)

        self.progress_len = len(self.current_graph.vertices) * 2
        self.progress = -1

        self.current_graph.make_edges(self.chosen_heli.seats)
        paths_list = main.prepare_paths(self.current_graph)

        non_full_run_list = self.find_non_full_run(paths_list, self.chosen_heli, self.current_graph)
        best_runs_list = self.find_rest_full_run(non_full_run_list, self.chosen_heli)
        best_run = self.get_best_result(best_runs_list)

        edge_base = 0
        for res in non_full_run_list:
            if res[0] == best_run[0][0]:
                edge_base = res[1][0]

        base_count = 0
        for city in best_run[0]:
            if city == best_run[0][0]:
                base_count = base_count + 1

        # for res in non_full_run_list:
        # print(res)

        self.dist_maximum_height = 0.0
        self.dist_minimum_height = 0.0
        self.money_maximum_height = 0.0
        self.money_minimum_height = 0.0

        self.dist_k_high = QBarSet("Км_k")
        self.dist_high = QBarSet("Км")
        self.money_high = QBarSet("Руб")

        len_list = []
        base_count_list = []
        money_list = []
        v_count_list = []
        names_list = []
        self.results_cities_names = []
        for res in best_runs_list:
            names_list.append(res[0][0].name)
            base_count = 0
            vertice_count = 0
            for city in res[0]:
                vertice_count += 1
                if city == res[0][0]:
                    base_count = base_count + 1

            distance = 0
            for i in range(0, len(res[0]) - 1):
                distance += res[0][i].conns[res[0][i + 1]]

            if self.dist_minimum_height == 0:
                self.dist_minimum_height = distance
            elif distance < self.dist_minimum_height:
                self.dist_minimum_height = distance
            if distance > self.dist_maximum_height:
                self.dist_maximum_height = distance
            len_list.append(str(res[1]))
            base_count_list.append(base_count)
            v_count_list.append(vertice_count)
            dist_k = res[1]/distance
            calced_money = calc_money(res[1], self.chosen_heli, base_count, dist_k)
            if self.money_maximum_height < calced_money:
                self.money_maximum_height = calced_money
            money_list.append(calced_money)
            self.money_high << calced_money
            self.dist_high << distance
            self.dist_k_high << res[1]
            self.results_cities_names.append(str(res[0][0].name))
        self.res_make_dist_barchart()
        self.res_make_money_barchart()

        column_names = ['id', 'name', 'distance', 'is_base']
        self.ui.result_path_tableview.setRowCount(len(best_run[0]))
        self.ui.result_path_tableview.setColumnCount(4)
        self.ui.result_path_tableview.setHorizontalHeaderLabels(column_names)

        rows = []
        distance = 0
        for i in range(0, len(best_run[0])-1):
            row = [str(i), str(best_run[0][i].name), str("{:.2f}".format(distance))]
            distance = distance + best_run[0][i].conns[best_run[0][i + 1]]
            if best_run[0][i] == best_run[0][0]:
                if i == edge_base:
                    row.append("True •")
                else:
                    row.append("True")
            else:
                row.append("False")
            rows.append(row)
        if best_run[0][-1] == best_run[0][0]:
            rows.append([str(len(best_run[0])-1), str(best_run[0][-1].name), str("{:.2f}".format(distance)), "True"])
        else:
            rows.append([str(len(best_run[0])-1), str(best_run[0][-1].name), str("{:.2f}".format(distance)), "False"])
        for i, row in enumerate(rows):
            for j, col in enumerate(row):
                item = QtWidgets.QTableWidgetItem(str(col))
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.ui.result_path_tableview.setItem(i, j, item)

        calced_money = calc_money(best_run[1], self.chosen_heli, base_count, 1)

        column_names_summary = []
        rows = []
        for i in range(0, len(names_list)):
            column_names_summary.append(names_list[i])
            rows.append([names_list[i], len_list[i], base_count_list[i], v_count_list[i], money_list[i]])

        row_names_summary = ['Вертодром', 'Путь, км',
                             'Рейсов', 'Путь, нп', 'Стоимость']
        self.ui.result_stats_tableview.setRowCount(len(len_list))
        self.ui.result_stats_tableview.setColumnCount(5)
        self.ui.result_stats_tableview.setHorizontalHeaderLabels(row_names_summary)
        # self.ui.result_stats_tableview.setVerticalHeaderLabels(column_names_summary)

        for i, row in enumerate(rows):
            for j, col in enumerate(row):
                item = QtWidgets.QTableWidgetItem(str(col))
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                self.ui.result_stats_tableview.setItem(i, j, item)

        self.ui.result_stats_tableview.setSortingEnabled(True)
        self.ui.result_stats_tableview.sortByColumn(4, QtCore.Qt.AscendingOrder)

        self.ui.result_base_textBrowser.setText(str(best_run[0][0].name))
        self.ui.result_length_textBrowser.setText(str("{:.2f}".format(best_run[1])))
        self.ui.result_length_textBrowser.setText(str("{:.2f}".format(distance)))
        self.ui.result_lands_textBrowser.setText(str(base_count))
        self.ui.result_path_textBrowser.setText(str(len(best_run[0])))
        self.ui.result_cost_textBrowser.setText(str("{:.2f}".format(calced_money)))

        self.ui.region_groupBox.setEnabled(True)
        self.ui.tasks_groupBox.setEnabled(True)
        self.ui.heli_groupBox.setEnabled(True)
        self.ui.statistics_tab.setEnabled(True)

        self.ui.start_progressBar.setValue(100)

        # main.test_launch()

    def check_main_state(self):
        if self.region_ready is True and self.helicopter_ready is True:
            self.ui.tasks_groupBox.setEnabled(True)
        else:
            self.ui.tasks_groupBox.setEnabled(False)

        if self.region_ready is True and self.helicopter_ready is True and self.tasks_ready is True:
            self.ui.start_button.setEnabled(True)
        else:
            self.ui.start_button.setEnabled(False)

        if self.launched_once is True:
            self.ui.statistics_tab.setEnabled(True)
        else:
            self.ui.statistics_tab.setEnabled(False)

    def state_to_default(self):
        self.load_regions()
        self.load_helis()
        self.ui.task_amount_num_label.setText("0")
        self.ui.task_all_amount_num_label.setText("0")
        self.check_heli_state()
        self.ui.start_progressBar.setValue(0)

    def find_usable_vertices(self):
        self.usable_vertices = []
        for v1 in self.current_graph.vertices:
            self.usable_vertices.append(v1)

        for v1 in self.current_graph.vertices:
            max_distance = 0
            for v2 in self.current_graph.vertices:
                for v3 in self.current_graph.vertices:
                    distance = v1.conns[v2] + v2.conns[v3] + v3.conns[v1]
                    if distance > max_distance:
                        max_distance = distance
                    if distance >= self.chosen_heli.fuel:
                        if v1 in self.usable_vertices:
                            pop_v = self.usable_vertices.pop(self.usable_vertices.index(v1))
                            self.red_names.append(pop_v.name)
            print(v1, max_distance)
        if len(self.usable_vertices) == 0:
            self.tasks_ready = False

        # print(self.usable_vertices)

    # RESULTS ##########################################################################################################

    def res_make_money_barchart(self):
        series = QStackedBarSeries()
        series.append(self.money_high)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Затраты")
        chart.setAnimationOptions(QChart.SeriesAnimations)

        categories = self.results_cities_names

        axis = QBarCategoryAxis()
        axis.append(categories)
        axis.setTitleText("Город")
        chart.createDefaultAxes()
        chart.setAxisX(axis, series)
        chart.axisY(series).setRange(0, self.money_maximum_height)
        chart.axisY(series).setTitleText("Стоимость Руб")

        chartview = QChartView(chart)
        self.ui.barc_money_widget.setContentsMargins(0, 0, 0, 0)
        lay = QtWidgets.QHBoxLayout(self.ui.barc_money_widget)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(chartview)

    def res_make_dist_barchart(self):

        series = QStackedBarSeries()
        series.append(self.dist_high)
        # series_k = QStackedBarSeries()
        # series_k.append(self.dist_k_high)

        chart = QChart()
        chart.addSeries(series)
        # chart.addSeries(series_k)
        chart.setTitle("Пройденная дистанция")
        chart.setAnimationOptions(QChart.SeriesAnimations)

        categories = self.results_cities_names

        axis = QBarCategoryAxis()
        axis.append(categories)
        axis.setTitleText("Город")
        chart.createDefaultAxes()
        chart.setAxisX(axis, series)
        chart.axisY(series).setRange(0, self.dist_maximum_height)
        chart.axisY(series).setTitleText("Дистанция Км")

        chartview = QChartView(chart)
        self.ui.barc_path_widget.setContentsMargins(0, 0, 0, 0)
        lay = QtWidgets.QHBoxLayout(self.ui.barc_path_widget)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.addWidget(chartview)

    # DATABASE #########################################################################################################

    def db_load(self):
        column_names = []
        self.ui.db_table.itemChanged.disconnect(self.db_upload_data)
        if self.ui.db_comboBox_sel.currentText() == "Cities":
            db_data = sql_lib.sql_get_all("SELECT * FROM `cities`")
            for line in sql_lib.sql_get_columns("cities"):
                column_names.append(line[1])
        else:
            db_data = sql_lib.sql_get_all("SELECT * FROM `helicopters`")
            for line in sql_lib.sql_get_columns("helicopters"):
                column_names.append(line[1])
        self.ui.db_table.setRowCount(len(db_data))
        self.ui.db_table.setColumnCount(len(db_data[0]))
        for i, row in enumerate(db_data):
            for j, col in enumerate(row):
                item = QtWidgets.QTableWidgetItem(str(col))
                self.ui.db_table.setItem(i, j, item)
                # print(self.ui.db_table.item(i, j).flags())
                if j == 0:
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    # self.ui.db_table.currentItem().setFlags(QtCore.Qt.ItemIsEnabled)
        self.ui.db_table.setHorizontalHeaderLabels(column_names)
        self.ui.db_table.itemChanged.connect(self.db_upload_data)
        self.ui.db_message_label.setText("Готово к работе")

    def db_upload_data(self):
        number_columns = ["lat", "lon", "cruise_speed", "max_distance", "mass_empty", "mass_full", "fuel_consum",
                          "time_engine", "cost_service", "cost_crew", "cost_fuel", "koef_gsm", "koef_diff", "c_aeno",
                          "dist_empty"]
        bool_columns = ["enabled"]
        item = self.ui.db_table.currentItem()
        # print(item.text(), item.column(), item.row())
        # data_id = self.ui.db_table.item(item.row(), 0)
        column = self.ui.db_table.horizontalHeaderItem(item.column()).text()
        name = self.ui.db_table.item(item.row(), 1).text()
        if self.ui.db_comboBox_sel.currentText() == "Cities":
            table = "cities"
        else:
            table = "helicopters"
        self.ui.db_table.itemChanged.disconnect(self.db_upload_data)
        if column in number_columns or column in bool_columns:
            if item.text().replace('.', '', 1).isdigit():
                sql_lib.sql_update_data(table, column, item.text(), name)
                self.ui.db_message_label.setText("Успешно обновлено")
            else:
                old_data = sql_lib.sql_get_previous_data(table, column, name)[0]
                new_item = QtWidgets.QTableWidgetItem(str(old_data))
                self.ui.db_table.setItem(item.row(), item.column(), new_item)
                self.ui.db_message_label.setText("Неправильный тип данных")
        self.ui.db_table.itemChanged.connect(self.db_upload_data)
        self.state_to_default()

    def db_delete_row(self):
        item = self.ui.db_table.currentItem()
        if self.ui.db_comboBox_sel.currentText() == "Cities":
            table = "cities"
        else:
            table = "helicopters"
        name = self.ui.db_table.item(item.row(), 1).text()
        self.ui.db_table.removeRow(item.row())
        sql_lib.sql_delete_row(table, name)
        self.state_to_default()

    def db_add_row(self):
        if self.ui.db_comboBox_sel.currentText() == "Cities":
            sql_lib.sql_cities_add_empty_row()
        else:
            sql_lib.sql_helicopters_add_empty_row()
        self.db_load()
        self.state_to_default()

    # TASKS ############################################################################################################

    def tasks_combobox_status(self):
        # rewrite on vertices!
        city_name_from = self.ui.task_from_comboBox.currentText()
        city_name_to = self.ui.task_to_comboBox.currentText()
        if city_name_from == city_name_to:
            self.ui.add_task_button.setEnabled(False)
            self.ui.delete_task_button.setEnabled(False)
            self.ui.task_amount_num_label.setText("0")
        else:
            city_from = self.get_vertice(city_name_from)
            city_to = self.get_vertice(city_name_to)
            if self.current_graph.tasks == {}:
                self.ui.add_task_button.setEnabled(True)
                self.ui.delete_task_button.setEnabled(False)
            else:
                task_amount = self.current_graph.tasks[city_from][city_to]
                if task_amount == 0:
                    self.ui.add_task_button.setEnabled(True)
                    self.ui.delete_task_button.setEnabled(False)
                    self.ui.task_amount_num_label.setText(str(task_amount))
                else:
                    self.ui.add_task_button.setEnabled(True)
                    self.ui.delete_task_button.setEnabled(True)
                    self.ui.task_amount_num_label.setText(str(task_amount))
        self.trigger_tasks_status()

    def get_vertice(self, city_name):
        for city in self.cities_list:
            if city_name in city:
                city_obj = city
                break
        for vertice in self.current_graph.vertices:
            if str(vertice) == f'city_{city_obj[0]}':
                print(vertice)
                return vertice

    def add_task(self):
        if self.current_graph.tasks == {}:
            self.gen_empty_tasks()
        v1 = self.get_vertice(self.ui.task_from_comboBox.currentText())
        v2 = self.get_vertice(self.ui.task_to_comboBox.currentText())
        self.current_graph.add_task(v1, v2)
        self.tasks_combobox_status()
        self.get_all_tasks_num()

    def delete_task(self):
        v1 = self.get_vertice(self.ui.task_from_comboBox.currentText())
        v2 = self.get_vertice(self.ui.task_to_comboBox.currentText())
        self.current_graph.delete_task(v1, v2)
        self.tasks_combobox_status()
        self.get_all_tasks_num()

    def tasks_to_comboxes(self):
        cities_names = [item[1] for item in self.cities_list]
        self.ui.task_to_comboBox.clear()
        self.ui.task_from_comboBox.clear()
        self.ui.task_to_comboBox.addItems(cities_names)
        self.ui.task_from_comboBox.addItems(cities_names)
        self.trigger_tasks_status()

    def load_cities_to_graph(self):
        for city in self.current_graph.vertices:
            del city
        self.current_graph.vertices.clear()
        for city in self.cities_list:
            self.current_graph.vertices.append(main.Vertex(city[1], city[2], city[3], f'city_{city[0]}'))
        self.current_graph.calc_distances()

    def save_tasks(self):
        with open("save.txt", "w+") as save_file:
            save_file.write(f'{self.current_graph.tasks}')

    def load_tasks(self):
        with open("save.txt", "r") as load_file:
            # надо написать собственный обработчик, сопоставляющий city_X с вершинами. Eval не подходит
            # Запилить загрузку-выгрузку в SQL
            self.trigger_tasks_status()
            self.tasks_combobox_status()

    def gen_empty_tasks(self):
        self.current_graph.generate_empty_tasks()
        self.trigger_tasks_status()
        self.tasks_combobox_status()
        self.get_all_tasks_num()

    def gen_tasks(self):
        self.current_graph.generate_tasks()
        self.trigger_tasks_status()
        self.tasks_combobox_status()
        self.get_all_tasks_num()

    def gather_tasks_amount(self):
        if self.current_graph.tasks == {}:
            return False
        else:
            amount = 0
            for vertice in self.current_graph.tasks:
                if self.current_graph.tasks[vertice] != {}:
                    for task in self.current_graph.tasks[vertice]:
                        if self.current_graph.tasks[vertice][task] > 0:
                            amount = amount + 1
            if amount < 2:
                return False
            else:
                return True

    def get_all_tasks_num(self):
        try:
            # adds tasks to table and all num
            task_number = 0
            cities_list = []
            for city in self.current_graph.tasks:
                cities_list.append(city.name)

            self.ui.len_table.reset()
            # create len table
            self.ui.len_table.setRowCount(len(self.current_graph.vertices))
            self.ui.len_table.setColumnCount(len(self.current_graph.vertices))

            rows = []
            cities_names = []
            for v1 in self.current_graph.vertices:
                row = []
                cities_names.append(v1.name)
                for v2 in self.current_graph.vertices:
                    row.append(v1.conns[v2])
                rows.append(row)

            self.find_usable_vertices()

            self.ui.len_table.setHorizontalHeaderLabels(cities_names)
            self.ui.len_table.setVerticalHeaderLabels(cities_names)

            # for i, name in enumerate(cities_names):
            #     item = QtWidgets.QTableWidgetItem(str(name))
            #     if name in self.red_names:
            #         item.setForeground(QtGui.QColor(255, 0, 0))
            #     self.ui.len_table.setHorizontalHeaderItem(i, item)
            #     self.ui.len_table.setVerticalHeaderItem(i, item)

            '''
            for city in cities_names:
                if city in self.red_names:
                    id = cities_names.index(city)
                    item = QtWidgets.QTableWidgetItem(str(city))
                    item.setBackground(QtGui.QColor(0, 0, 255))
                    self.ui.len_table.setHorizontalHeaderItem(0, item)
            '''

            for i, row in enumerate(rows):
                for j, col in enumerate(row):
                    dis = str("{:.1f}".format(col))
                    item = QtWidgets.QTableWidgetItem(str(dis))
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.ui.len_table.setItem(i, j, item)

            for i, row in enumerate(rows):
                header = self.ui.len_table.takeHorizontalHeaderItem(i)
                if header.text() in self.red_names:
                    header.setForeground(QtGui.QColor(255, 0, 0))
                self.ui.len_table.setHorizontalHeaderItem(i, header)
                self.ui.len_table.setVerticalHeaderItem(i, header)

            self.ui.tasks_table.setRowCount(len(self.current_graph.tasks))
            self.ui.tasks_table.setColumnCount(len(self.current_graph.tasks))

            rows = []
            for city in self.current_graph.tasks:
                row = []
                for task in self.current_graph.tasks[city]:
                    task_number = task_number + self.current_graph.tasks[city][task]
                    row.append(self.current_graph.tasks[city][task])
                    # item = QtWidgets.QTableWidgetItem(str(self.current_graph.tasks[city][task]))
                    # item.setFlags(QtCore.Qt.ItemIsEnabled)
                    # self.ui.tasks_table.setItem(i, j, item)
                    # print(self.current_graph.tasks[city][task])
                rows.append(row)

            for i, row in enumerate(rows):
                for j, col in enumerate(row):
                    item = QtWidgets.QTableWidgetItem(str(col))
                    item.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.ui.tasks_table.setItem(i, j, item)

            self.ui.task_all_amount_num_label.setText(str(task_number))

            self.ui.tasks_table.setHorizontalHeaderLabels(cities_list)
            self.ui.tasks_table.setVerticalHeaderLabels(cities_list)
            print("get_all_tasks_num - 3")
        except Exception as e:
            print(e)

    def trigger_tasks_status(self):
        self.tasks_ready = self.gather_tasks_amount()
        self.check_main_state()

    # REGIONS ##########################################################################################################

    def load_regions(self):
        self.ui.region_comboBox.clear()
        regions_list = sql_lib.sql_get_all_regions()
        for region in regions_list:
            if region == "Регион" or region == []:
                regions_list.pop(regions_list.index(region))
        self.ui.region_comboBox.addItems(regions_list)
        self.ui.region_comboBox.setCurrentIndex(0)

    def load_districts(self):
        self.ui.district_comboBox.clear()
        districts_list = sql_lib.sql_get_all_districts(self.chosen_region)
        for district in districts_list:
            if district == "Район" or district == []:
                districts_list.pop(districts_list.index(district))
        self.ui.district_comboBox.addItems(districts_list)

    def load_cities(self):
        for city in self.cities_list:
            if "0.0" in city or "Город" in city:
                self.cities_list.pop(self.cities_list.index(city))
        cities_names = [item[1] for item in self.cities_list]
        self.ui.region_sel_comboBox.clear()
        self.ui.region_sel_comboBox.addItems(cities_names)

    def trigger_region_check(self):
        if str(self.ui.region_comboBox.currentText()) == 'Выберите регион':
            self.ui.region_sel_en_checkBox.stateChanged.disconnect(self.trigger_region_checkbox)
            self.ui.district_comboBox.currentTextChanged.disconnect(self.trigger_district_check)
            self.ui.region_sel_comboBox.currentTextChanged.disconnect(self.trigger_city_check)
            print("A1")
            self.ui.tasks_table.reset()
            self.ui.len_table.reset()
            print("A2")
            self.ui.len_table.setRowCount(0)
            print("A3")
            # self.ui.len_table.setColumnCount(0)
            print("A4")
            self.ui.tasks_table.setColumnCount(0)
            print("A5")
            self.ui.tasks_table.setRowCount(0)
            print("B")
            self.chosen_region = str(self.ui.region_comboBox.currentText())
            self.ui.district_comboBox.setCurrentIndex(0)
            self.ui.district_comboBox.setEnabled(False)
            self.ui.region_sel_comboBox.setEnabled(False)
            self.ui.region_sel_en_checkBox.setEnabled(False)
            print("C")
            self.ui.region_sel_en_checkBox.stateChanged.connect(self.trigger_region_checkbox)
            self.ui.district_comboBox.currentTextChanged.connect(self.trigger_district_check)
            self.ui.region_sel_comboBox.currentTextChanged.connect(self.trigger_city_check)
            self.region_ready = False
            self.current_graph = main.Graph()
            self.check_main_state()

        if str(self.ui.region_comboBox.currentText()) != self.chosen_region:
            self.ui.region_sel_en_checkBox.stateChanged.disconnect(self.trigger_region_checkbox)
            self.ui.district_comboBox.currentTextChanged.disconnect(self.trigger_district_check)
            self.ui.region_sel_comboBox.currentTextChanged.disconnect(self.trigger_city_check)
            self.chosen_region = str(self.ui.region_comboBox.currentText())
            self.load_districts()
            self.ui.district_comboBox.setEnabled(True)
            self.ui.region_sel_comboBox.clear()
            self.ui.region_sel_comboBox.setEnabled(False)
            self.ui.region_sel_en_checkBox.setEnabled(False)
            self.ui.region_sel_en_checkBox.stateChanged.connect(self.trigger_region_checkbox)
            self.ui.district_comboBox.currentTextChanged.connect(self.trigger_district_check)
            self.ui.region_sel_comboBox.currentTextChanged.connect(self.trigger_city_check)
            self.region_ready = False
            self.check_main_state()

    def trigger_district_check(self):
        if str(self.ui.district_comboBox.currentText()) == "Выберите район":
            self.chosen_district = str(self.ui.district_comboBox.currentText())
            self.ui.region_sel_en_checkBox.stateChanged.disconnect(self.trigger_region_checkbox)
            self.ui.region_sel_comboBox.currentTextChanged.disconnect(self.trigger_city_check)
            self.ui.len_table.setRowCount(0)
            self.ui.tasks_table.setRowCount(0)
            # self.ui.len_table.setColumnCount(0)
            self.ui.tasks_table.setColumnCount(0)
            self.ui.region_sel_comboBox.clear()
            self.ui.region_sel_comboBox.setCurrentIndex(0)
            self.ui.region_sel_comboBox.setEnabled(False)
            self.ui.region_sel_en_checkBox.setEnabled(False)
            self.region_ready = False
            self.current_graph = main.Graph()
            self.check_main_state()
            self.ui.region_sel_en_checkBox.stateChanged.connect(self.trigger_region_checkbox)
            self.ui.region_sel_comboBox.currentTextChanged.connect(self.trigger_city_check)

        if str(self.ui.district_comboBox.currentText()) != self.chosen_district:
            self.chosen_district = str(self.ui.district_comboBox.currentText())
            self.cities_list = sql_lib.sql_get_all_cities_in_district(self.chosen_district)
            self.ui.region_sel_en_checkBox.stateChanged.disconnect(self.trigger_region_checkbox)
            self.ui.region_sel_comboBox.currentTextChanged.disconnect(self.trigger_city_check)
            # add here
            self.load_cities()
            self.ui.region_sel_comboBox.currentTextChanged.connect(self.trigger_city_check)
            self.ui.region_sel_comboBox.setCurrentIndex(0)
            self.ui.region_sel_comboBox.setEnabled(True)
            self.ui.region_sel_en_checkBox.setEnabled(True)
            self.ui.region_sel_en_checkBox.stateChanged.connect(self.trigger_region_checkbox)
            self.trigger_city_check()
            self.tasks_to_comboxes()
            self.region_ready = True
            self.load_cities_to_graph()
            self.check_main_state()
            self.check_cities_list()

    def trigger_city_check(self):
        self.chosen_city = self.ui.region_sel_comboBox.currentText()
        self.ui.region_sel_en_checkBox.stateChanged.disconnect(self.trigger_region_checkbox)
        enabled_status = sql_lib.sql_get_city_enabled_status(self.chosen_city)
        if enabled_status == "True":
            self.ui.region_sel_en_checkBox.setChecked(True)
        else:
            self.ui.region_sel_en_checkBox.setChecked(False)
        self.ui.region_sel_en_checkBox.stateChanged.connect(self.trigger_region_checkbox)

    def trigger_region_checkbox(self):
        if self.ui.region_sel_en_checkBox.isChecked():
            sql_lib.sql_set_city_enable_status(self.chosen_city)
        else:
            sql_lib.sql_set_city_disable_status(self.chosen_city)
        self.check_cities_list()

    def check_cities_list(self):
        self.cities_list = sql_lib.sql_get_all_enabled_cities(self.chosen_district)
        if not self.cities_list:
            self.region_ready = False
            self.check_main_state()
        else:
            self.region_ready = True
            self.check_main_state()

    # HELICOPTER #######################################################################################################

    def load_helis(self):
        self.ui.heli_comboBox.currentTextChanged.disconnect(self.check_heli_state)
        heli_names = sql_lib.sql_get_helis_names()
        for name in heli_names:
            data = sql_lib.sql_get_cur_heli(name)
            if data != [] and (("0.0" in data[0]) or ("Название" in data[0])):
                heli_names.pop(heli_names.index(data[0][1]))
        self.ui.heli_comboBox.clear()
        self.ui.heli_comboBox.addItems(heli_names)
        self.ui.heli_comboBox.setCurrentIndex(0)
        self.ui.heli_comboBox.currentTextChanged.connect(self.check_heli_state)

    def check_heli_state(self):
        if str(self.ui.heli_comboBox.currentText()) == "Выберите вертолёт":
            self.helicopter_ready = False
            self.check_main_state()
            self.ui.heli_mass_label_param.setText(" ")
            self.ui.heli_dist_label_param.setText(" ")
            self.ui.heli_dist_label_param_2.setText(" ")
            self.ui.heli_speed_label_param.setText(" ")
            self.ui.heli_picture.clear()
        else:
            heli_name = str(self.ui.heli_comboBox.currentText())
            data = sql_lib.sql_get_cur_heli(heli_name)
            data = data[0]
            # print(data)
            pixmap = QtGui.QPixmap("heli_images/" + data[2])
            self.ui.heli_picture.setPixmap(pixmap)
            self.ui.heli_picture.setScaledContents(True)
            self.ui.heli_mass_label_param.setText(str(data[6]))
            self.ui.heli_dist_label_param.setText(str(data[4]))
            self.ui.heli_dist_label_param_2.setText(str(data[15]))
            self.ui.heli_speed_label_param.setText(str(data[3]))
            self.chosen_heli = main.Helicopter(data[1], 1, data[4], data[0], data[3], data[5], data[6], data[7],
                                               data[8], data[12], data[13], data[9], data[10], data[11], data[14],
                                               data[15])
            self.helicopter_ready = True
            self.check_main_state()


application = QtWidgets.QApplication([])
app = design()
app.show()
sys.exit(application.exec())
