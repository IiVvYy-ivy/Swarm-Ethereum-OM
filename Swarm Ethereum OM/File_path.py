import platform
import os
class filepath:
    def __init__(self):
        os_name = platform.system()  
        self.os_name = os_name
    
    def find_file_in_directory(directory, filename):  
        for root, dirs, files in os.walk(directory):  
            if filename in files:  
                return os.path.join(root, filename)  
        return None  

    def generate_path(self,os_name):
        if os_name.lower() == "windows":
            self.work_path = os.getcwd()
            dest_file_path = filepath.find_file_in_directory(self.work_path,self.filename)
            

