import configparser
import os

class Update_Configuration:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config_path = self.config.read(FileFinder('configuration.ini').finder())
    
    def get_database_configuration(self):
        self.database_config_dict = {}
        for key, value in self.config.items('DATABASE'):  
            self.database_config_dict[key] = value
        return self.database_config_dict
    
    def get_ip_configuraion(self):
        self.ip_config_dict = {} 
        for section in self.config.sections():
            if "IP" in section:
                self.ip_config_dict[section] = {}
                for key, value in self.config.items(section):  
                    self.ip_config_dict[section][key] = value
        return self.ip_config_dict

class FileFinder:  
    def __init__(self, file_or_folder_name):  
        self.file_or_folder_name = file_or_folder_name  
      
    def finder(self):  
        for root, dirs, files in os.walk(os.getcwd()):  
            if self.file_or_folder_name in dirs:   
                return os.path.join(root, self.file_or_folder_name)  
            for file in files:  
                if file == self.file_or_folder_name:    
                    return os.path.join(root, file)  
        return None  
    
ip_config = Update_Configuration().get_ip_configuraion()
print(ip_config)