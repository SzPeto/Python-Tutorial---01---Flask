import datetime
import os.path


class Functions:

    def __init__(self):
        self.log_file = self.create_file("Log\\log.txt")

    def create_file(self, path_and_file):

        try:
            dir_name = os.path.dirname(path_and_file)
            if dir_name and not os.path.exists(dir_name):
                os.makedirs(dir_name)
        except Exception as e:
            print(f"Something went wrong creating the file or directory : {e}")

        return path_and_file

    def write_log(self, text):
        with open(self.log_file, "a", encoding = "utf-8") as log_file:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d, %H:%M:%S - ")
