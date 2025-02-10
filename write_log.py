import csv
import time


class Log:
    def __init__(self, headers):
        self.headers = headers
        self.init_log()

    def init_log(self):
        with open("donnees_gps.csv", mode='w', newline='') as fichier_csv:
            writer = csv.writer(fichier_csv)
            writer.writerow(['t']+self.headers)

    def write_log(self, variables):
        with open("donnees_gps.csv", mode='a', newline='') as fichier_csv:
            writer = csv.writer(fichier_csv)
            writer.writerow([time.time()]+variables)
            print([self.headers[i], " : ", variables[i]] for i in range (len(variables)))