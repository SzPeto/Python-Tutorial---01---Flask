import datetime
import os.path


class Functions:

    def __init__(self):
        self.log_file = self.create_file("Log\\log.txt")
        self.first_log = True
        self.write_log("****************************************************************************************")

    def create_dir(self, dir_name):
        try:
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
            self.write_log(f"Directory {dir_name} successfully created")
        except Exception as e:
            self.write_log(f"def create_dir : {e}")

    def create_file(self, path_and_file):

        try:
            dir_name = os.path.dirname(path_and_file)
            if dir_name and not os.path.exists(dir_name):
                os.makedirs(dir_name)
                if os.path.exists("Log\\log.txt"):
                    self.write_log(f"Directory {dir_name} successfully created")
        except Exception as e:
            print(f"Something went wrong creating the file or directory : {e}")

        return path_and_file

    def write_log(self, text):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d, %H:%M:%S - ")
        if self.first_log:
            with open(self.log_file, "a", encoding="utf-8") as log_file:
                log_file.write(f"\n{timestamp}{text}\n")
                self.first_log = False
        else:
            with open(self.log_file, "a", encoding = "utf-8") as log_file:
                log_file.write(f"{timestamp}{text}\n")
