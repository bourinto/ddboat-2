import csv
import time
from datetime import datetime


class Log:
    def __init__(self, headers):
        self.file_name = "logs/" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".csv"

        self.headers = headers
        self.init_log()

    def init_log(self):
        with open(self.file_name, mode='w', newline='') as fichier_csv:
            writer = csv.writer(fichier_csv)
            writer.writerow(['t'] + self.headers)

    def write_log(self, variables):
        with open(self.file_name, mode='a', newline='') as fichier_csv:
            writer = csv.writer(fichier_csv)
            writer.writerow([time.time()] + variables)
            for i in range(len(variables)):
                print(self.headers[i], " : ", variables[i])
            print("")
