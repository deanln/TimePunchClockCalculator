# -*- coding: iso-8859-1 -*-
import sys
from datetime import timedelta
from PyQt4.QtCore import *
from PyQt4.QtGui import *

SOFTWARE_VERSION = "Version 1.0"

class punch_clock(QWidget):
    def __init__(self, parent = None):
        super(punch_clock, self).__init__(parent)

        layout = QFormLayout()

        self.logo = QLabel()
        self.logo.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap('logo.png')
        self.logo.setPixmap(pixmap)
        layout.addRow(self.logo)

        self.hr_text = QLabel("HOUR (24-HR):")
        self.min_text = QLabel("MINUTE (60-MIN):")
        layout.addRow(self.hr_text, self.min_text)

        self.one_in_hr = QLineEdit()
        self.one_in_hr.setPlaceholderText("Shift 1 - IN")
        self.one_in_min = QLineEdit()
        self.one_in_min.setPlaceholderText("Shift 1 - IN")
        layout.addRow(self.one_in_hr, self.one_in_min)

        self.fivehourlimit = QPushButton("5-Hour shift clock-OUT Target")
        layout.addRow(self.fivehourlimit)

        self.one_out_hr = QLineEdit()
        self.one_out_hr.setPlaceholderText(("Shift 1 - OUT"))
        self.one_out_min = QLineEdit()
        self.one_out_min.setPlaceholderText("Shift 1 - OUT")
        layout.addRow(self.one_out_hr, self.one_out_min)

        self.fivehourlimit.clicked.connect(self.fivehour_calculation)
        self.lunch = QPushButton("30 min Lunch clock-IN Target")
        layout.addRow(self.lunch)
        self.lunch.clicked.connect(self.lunch_calculation)

        self.two_in_hr = QLineEdit()
        self.two_in_hr.setPlaceholderText("Shift 2 - IN")
        self.two_in_min = QLineEdit()
        self.two_in_min.setPlaceholderText("Shift 2 - IN")
        layout.addRow(self.two_in_hr, self.two_in_min)

        self.hw_label = QLabel("Total Hours Working:")
        self.hours_working = QLineEdit()
        self.hours_working.setPlaceholderText("# of Hours")
        layout.addRow(self.hw_label, self.hours_working)

        self.btn = QPushButton("End of Day clock-OUT Time")
        layout.addRow(self.btn)
        self.btn.clicked.connect(self.calculate)

        self.solution = QLabel("--:--")
        layout.addRow(self.solution)

        self.setLayout(layout)
        self.setWindowTitle("TPCC " + SOFTWARE_VERSION)

    def calculate(self):
        ONE_HOUR_TO_MIN = 60
        try:
            if int(self.hours_working.text()) > 24:
                self.solution.setText("There's only 24 hours in a day...")
            else:
                try:
                    s1_in_total_min = float(self.one_in_hr.text())*ONE_HOUR_TO_MIN+float(self.one_in_min.text())
                    s1_out_total_min = float(self.one_out_hr.text())*ONE_HOUR_TO_MIN+float(self.one_out_min.text())
                    s1_diff_min = float(s1_out_total_min) - float(s1_in_total_min)

                    total_hours_worked = float(self.hours_working.text())*ONE_HOUR_TO_MIN
                    s2_diff_min = float(total_hours_worked) - float(s1_diff_min)

                    s2_in_total_min = float(self.two_in_hr.text())*ONE_HOUR_TO_MIN+float(self.two_in_min.text())
                    sub_clock_out_value = float(s2_in_total_min)+float(s2_diff_min)
                    clock_out_by = str(timedelta(minutes=sub_clock_out_value))[:-3]

                    self.solution.setText("Shift 1 Total Hours: %s \n"
                                          "Shift 2 Total Hours: %s \n"
                                          "Total Hours Working: %s \n"
                                          "MUST CLOCK OUT BY: %s " % (s1_diff_min/60, s2_diff_min/60, self.hours_working.text(), clock_out_by))
                except ValueError:
                    pass
        except ValueError:
            pass

    def lunch_calculation(self):
        try:
            s1_out_total_min = float(self.one_out_hr.text()) * 60 + float(self.one_out_min.text())
            lunch_clock_in_by = str(timedelta(minutes=s1_out_total_min + 30))[:-3]

            self.solution.setText("YOU NEED TO BACK FROM LUNCH AT: %s" % lunch_clock_in_by)
        except ValueError:
            pass

    def fivehour_calculation(self):
        try:
            s1_in_total_min = float(self.one_in_hr.text()) * 60 + float(self.one_in_min.text())
            shift_out_by = str(timedelta(minutes=s1_in_total_min + 300))[:-3]

            self.solution.setText("YOU CLOCK OUT FROM YOUR 1ST SHIFT BY: %s" % shift_out_by)
        except ValueError:
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    appinstance = punch_clock()
    appinstance.show()
    sys.exit(app.exec_())
