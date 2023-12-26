import paramiko
import time
import os
import pymysql
import configparser

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
        self.ip_config_sections = []
        self.ip_config_dict = {}
        for section in self.config.sections():  
            if "IP" in section:  
                self.ip_config_sections.append(section)
        for ip_config_section in self.ip_config_sections:
            for key, value in self.config.items(ip_config_section):  
                self.ip_config_dict[key] = value
        return self.ip_config_dict

class FileFinder:  
    def __init__(self, file_or_folder_name):  
        self.file_or_folder_name = file_or_folder_name  
      
    def finder(self):  
        for root, dirs, files in os.walk(os.getcwd()):  # 遍历根目录下的所有文件和文件夹  
            if self.file_or_folder_name in dirs:  # 如果文件夹名称匹配，则输出文件夹路径  
                return os.path.join(root, self.file_or_folder_name)  
            for file in files:  
                if file == self.file_or_folder_name:  # 如果文件名称匹配，则输出文件路径  
                    return os.path.join(root, file)  
        return None  # 如果没有找到文件或文件夹，则返回None
    

class Swarm_OM:
    def __init__(self,ip,user,pwd):
        self.ip = ip
        self.user = user
        self.pwd = pwd

    def SSHConnect(self):
        self.ssh = paramiko.SSHClient()  
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
        try: 
            self.ssh.connect(self.ip,username=self.user,password=self.pwd)
            print(f'{self.ip} connect success')
        except Exception as error:
            print(f'{self.ip} connect fail, Reason: {error}')
        return self.ssh
    
    def SSHExecute(self, command):  
        try:  
            self.SSHConnect() 
            stdin, stdout, stderr = self.ssh.exec_command(command)  
            output = stdout.read().decode()  
            print(output) 
            self.SSHClose() 
        except Exception as error:  
            print(f'Error executing command: {error}')

    def SSHClose(self):
        if self.ssh:  
            self.ssh.close()

class Upload_file(Swarm_OM):  
    def __init__(self, ip, user, pwd, local_path, remote_path):  
        super().__init__(ip, user, pwd)  
        self.local_path = local_path  
        self.remote_path = remote_path  
  
    def upload_file(self):   
        try: 
            self.SSHConnect() 
            sftp = self.ssh.open_sftp()    
            sftp.put(self.local_path, self.remote_path)    
            sftp.close()  
            print('File uploaded successfully, wait to check again')
            self.SSHClose()  
        except Exception as error:  
            print(f'File upload failed, Reason: {error}')
    
    def check_upload_status(self):  
        try:  
            sftp = self.ssh.open_sftp()
            if sftp.exists(self.remote_path): 
                print("File uploaded successfully or File already exists")
            else :  
                sftp.close()  
                print('File does not exist on remote path, applying 777 permissions...')  
                self.ssh.execute('chmod 777 {}'.format(self.remote_path))  
                print('Retrying file upload...')  
                self.upload_file()  
        except Exception as error:  
            print(f'Error while checking upload status or changing permissions: {error}')
    
    def get_local_file_size(self):  
        try:  
            file_info = os.stat(self.local_path) 
            print(f"File: {self.local_path}")
            print(f"Size: {file_info.st_size} bytes")   
            return file_info.st_size  
        except OSError:  
            print("Error: Check the local file path.")

class Download_file(Swarm_OM):
    def __init__(self, ip, user, pwd,local_path,remote_path):
        super().__init__(ip, user, pwd)
        self.local_path = local_path
        self.remote_path = remote_path
    
    def download_file(self):  
        try:
            self.SSHConnect() 
            sftp = self.ssh.open_sftp()  
            sftp.get(self.remote_path, self.local_path)  
            sftp.close()
            print('download success')
            self.SSHClose() 
        except Exception as error:
            print(f'download fail, Reason: {error}')

class Substract_dcdir:
    def __init__(self,select_location,ip):
        self.select_location  = select_location 
        self.ip = ip
    
    def substract_dcdir(self):
        self.dc_path = FileFinder(f'{self.select_location +"_DIR"}').finder()
        with open(os.path.join(self.dc_path,f'{self.ip+"dcdir.txt"}'), 'r') as f:   
            lines = f.readlines()  
        dcdir = [line.strip() for line in lines]  
        return dcdir

class Substract_port(Substract_dcdir):
    def __init__(self, select_location , ip):
        super().__init__(select_location , ip)

    def substract_port(self):
        self.port_path = FileFinder(f'{self.select_location+"_PORT"}').finder()
        with open(os.path.join(self.port_path,f'{self.ip+"port.txt"}'), 'r') as f:   
            lines = f.readlines()  
        port = [line.strip() for line in lines]  
        return port

class Split:
    def __init__(self,str):
        self.str = str

    def split_string(self):
        new_dir=self.str[:self.str.find('/docker-compose.yaml')]
        return new_dir

class Rename:
    def __init__(self,dirname):
        self.dirname = dirname
    
    def rename_path(self):
        new_dir_name = self.dirname.replace('/', '')  
        return new_dir_name

class Replace:
    def __init__(self,dir_path,old_str,new_str):
        self.dir_path = dir_path
        self.old_str = old_str
        self.new_str = new_str
    
    def replace_in_dir(self):  
        for root, dirs, files in os.walk(self.dir_path):  
            for file in files:  
                file_path = os.path.join(root, file)
                try:  
                    with open(file_path, "r", encoding="utf-8") as f:  
                        file_data = f.read()  
                    if self.old_str in file_data:  
                        file_data = file_data.replace(self.old_str, self.new_str)  
                    with open(file_path, "w", encoding="utf-8") as f:  
                        f.write(file_data)
                    print('replace success')
                except Exception as error:
                    print(f'replace fail, Reason: {error}')


class Comment:  
    def __init__(self, root_path, file_name, start_line, end_line):  
        self.root_path = root_path  
        self.file_name = file_name  
        self.start_line = start_line  
        self.end_line = end_line  
  
    def comment_lines_in_file(self, file_path):  
        with open(file_path, 'r') as file:  
            lines = file.readlines()  
  
        for i in range(self.start_line - 1, self.end_line):  
            if i < len(lines):  
                lines[i] = '#' + lines[i]  
        with open(file_path, 'w') as file:  
            file.writelines(lines)  
  
    def find_and_comment_lines(self):  
        for dirpath, dirnames, filenames in os.walk(self.root_path):  
            if self.file_name in filenames:  
                file_path = os.path.join(dirpath, self.file_name)  
                self.comment_lines_in_file(file_path)


class Cancel_Comment:  
    def __init__(self, root_path, file_name, start_line, end_line):  
        self.root_path = root_path  
        self.file_name = file_name  
        self.start_line = start_line  
        self.end_line = end_line  
  
    def cancel_comment_lines(self):  
        for dirpath, dirnames, filenames in os.walk(self.root_path):  
            if self.file_name in filenames:  
                file_path = os.path.join(dirpath, self.file_name)  
                self.cancel_comment_lines_in_file(file_path)  
  
    def cancel_comment_lines_in_file(self, file_path):  
        with open(file_path, 'r') as file:  
            lines = file.readlines()  
  
        for i in range(self.start_line - 1, self.end_line):  
            if i < len(lines):  
                if lines[i].startswith('#'):  
                    lines[i] = lines[i][1:]  
  
        with open(file_path, 'w') as file:  
            file.writelines(lines)



class Generate_Grafana_Agent_File:
    def __init__(self,parameter_location,parameter_ip):
        self.parameter_location = parameter_location
        self.parameter_ip = parameter_ip

    def generate_grafna_agent_file(self):
        path = FileFinder('Grafana-agent_Configuration.py').finder()
        if os.path.isfile(path):  
            os.system(f"python {path} {self.parameter_location} {self.parameter_ip}")  
        else:  
            print(f"File {path} does not exist.")





class Build_Functions_choice_Dictionary:
    def __init__(self,index,choice):
        self.choice_dictionary =  {         # Add any function here
        0: 'generate docker-compose.yaml',  
        1: 'replace .env',  
        2: 'replace docker-compose.yaml',  
        3: 'substract port',  
        4: 'function 4',  
        5: 'function 5',  
        6: 'function 6',  
        7: 'function 7',  
        8: 'generate grafana-agent.yaml',  
        9: 'substract port from mysql',
        10: 'upload grafana-agent.tar.gz',
        11: 'upload start.sh',
        12: 'function 12'  
    }  
      
        self.index = index
        self.choice = choice

    def get_function_choice(self):
        for index,function_choice in self.choice_dictionary.items():
            print(f"{index} {function_choice}")

    def add_choice(self):
        self.choice_dictionary[self.index]= self.choice    

class Build_IP_Dictionary:
    def __init__(self,location,ip_addresses):  
        self.IP_dictionary = {     # Add your ip list here
            'x1' : ['127.0.0.1'],
            'x2' : ["xxxx"],
            '<location>' : ['ssh_ip1','ssh_ip2']
        }
        self.location = location
        self.__ip_addresses = ip_addresses

    def add_ip(self):  
        if self.location in self.__IP_dictionary:  
            self.IP_dictionary[self.location].append(self.__ip_addresses)  
        else:  
            self.IP_dictionary[self.location] = [self.__ip_addresses]


class Build_Password_Dictionary(Build_IP_Dictionary):
    def __init__(self, location, ip_address, password, new_password):
        super().__init__(location, ip_address)
        self.password_dictionary = {               # Add your password correspond to ip here
            'x1' : '<ssh passsword for x1>',
            'x2' : 'xxxxx',
            '<location>' : 'ssh password for <location>'
        }
        self.password = password
        self.new_password = new_password

    def add_location_password(self):
        self.password_dictionary[self.location] = self.password
    
    def update_existing_location_password(self):
        if self.location in self.password_dictionary:
            self.password_dictionary[self.location] = self.new_password
        else:
            print(f"The key '{self.location}' does not exist in the password dictionary")
        
class Build_Username_Dictionary(Build_IP_Dictionary):
    def __init__(self, location, ip_addresses, username, new_username):
        super().__init__(location, ip_addresses)
        self.username_dictionary = {            # Add your username correspond to ip here
            'x1' : 'ssh username for x1',
            'x2' : 'xxxx',
            '<location>' : 'ssh username for <location>'
        }
        self.username = username
        self.new_username = new_username

    def add_location_username(self):
        self.username_dictionary[self.location] = self.username
    
    def update_existing_location_username(self):
        if self.location in self.username_dictionary:
            self.username_dictionary[self.location] = self.new_username
        else:
            print(f"The key '{self.location}' does not exist in the username dictionary")

class QueryMySQL:  
    def __init__(self, host, user, password, db,port):  
        self.host = host  
        self.user = user  
        self.password = password  
        self.db = db 
        self.port = port 
        self.connection = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.db, port = self.port)  
  
    def close_connection(self):  
        if self.connection:  
            self.connection.close()  
  
    def query_ports(self, ip):  
        cursor = self.connection.cursor()  
        query = f"SELECT port FROM <database_name>.<table_name> WHERE ip_address = '{ip}'"  # query need to be modified by your own
        cursor.execute(query)  
        ports = cursor.fetchall()  
        return ports  
  
    def save_ports(self, ip, file_name):  
        ports = self.query_ports(ip)  
        with open(file_name, 'w') as f:  
            for port in ports:  
                f.write(str(port[0]) + '\n') 


def execute_function(select_location,select_function):
    match select_function:
        case 0:
            print('xxxx')
        case 1:
            ip_list=Build_IP_Dictionary(f'{select_location}',None).IP_dictionary[f'{select_location}']
            username = Build_Username_Dictionary(f'{select_location}',None,None,None).username_dictionary[f'{select_location}']
            password = Build_Password_Dictionary(f'{select_location}',None,None,None).password_dictionary[f'{select_location}']
            env_path = FileFinder(f'{select_location+"_.env"}').finder()
            for ip in ip_list:
                Replace(os.path.join(env_path,'.env'),'<old text need to be replaced>','<The new text that was replaced>').replace_in_dir()
        case 2:
            ip_list=Build_IP_Dictionary(f'{select_location}',None).IP_dictionary[f'{select_location}']
            username = Build_Username_Dictionary(f'{select_location}',None,None,None).username_dictionary[f'{select_location}']
            password = Build_Password_Dictionary(f'{select_location}',None,None,None).password_dictionary[f'{select_location}']
            shell_path = FileFinder('SCRIPTS').finder()
            DIR_path = FileFinder(f'{select_location+"_DIR"}').finder()
            Location_DC_path = FileFinder(f'{select_location+"_DC"}').finder()
            DC_path = FileFinder('DC').finder()
            if select_location != 'customer1':
                for ip in ip_list:
                    Upload_file(f'{ip}',f'{username}',f'{password}',os.path.join(shell_path,f'{select_location+"_dir.sh"}'),'<remote dir.sh file path>').upload_file()
                    time.sleep(1)
                    Swarm_OM(f'{ip}',f'{username}',f'{password}').SSHExecute(f'echo {password} | sudo -S bash <remote dir.sh file path>')
                    time.sleep(10)
                    Download_file(f'{ip}',f'{username}',f'{password}',os.path.join(DIR_path,f'{ip+"dcdir.txt"}'),'<remote dir.txt path>',).download_file()
                    dcdirs = Substract_dcdir(f'{select_location}',f'{ip}').substract_dcdir()
                    for dcdir in dcdirs:
                        newdir = Split(dcdir).split_string()
                        finaldir = Rename(newdir).rename_path()
                        Download_file(f'{ip}',f'{username}',f'{password}', os.path.join(Location_DC_path,f'{ip+finaldir+"_docker-compose.yaml"}'),f'{newdir}/docker-compose.yaml').download_file()
                    Replace(DC_path,"<old bee version>","<new bee version>").replace_in_dir()
                    for dcdir in dcdirs:
                        newdir = Split(dcdir).split_string()
                        finaldir = Rename(newdir).rename_path()
                        Upload_file(f'{ip}',f'{username}',f'{password}', os.path.join(Location_DC_path,f'{ip+finaldir+"_docker-compose.yaml"}'), f'{newdir}/docker-compose.yaml').upload_file()
            
            elif select_location == 'customer1':
                for ip in ip_list:
                    Upload_file(f'{ip}',f'{username}',f'{password}',os.path.join(shell_path,f'{select_location+"_dir.sh"}'),'<remote dir.sh file path>').upload_file()
                    time.sleep(1)
                    Swarm_OM(f'{ip}',f'{username}',f'{password}').SSHExecute(f'echo {password} | sudo -S bash /usr/local/script/dcdir.sh')
                    time.sleep(10)
                    Download_file(f'{ip}',f'{username}',f'{password}',os.path.join(DIR_path,f'{ip+"dcdir.txt"}'),'<remote dir.txt file path>',).download_file()
                    dcdirs = Substract_dcdir(f'{select_location}',f'{ip}').substract_dcdir()
                    for dcdir in dcdirs:
                        newdir = Split(dcdir).split_string()
                        finaldir = Rename(newdir).rename_path()
                        Download_file(f'{ip}',f'{username}',f'{password}',os.path.join(Location_DC_path,f'{ip+finaldir+"_docker-compose.yaml"}'),f'{newdir}/docker-compose.yaml').download_file()
                    Replace(DC_path,"<old bee version>","<new bee version>").replace_in_dir()
                    # Comment(Location_DC_path,f'{ip+"docker-compose.yaml"}',<start line need to be commented>(number), <end line need to be commented>(number)).find_and_comment_lines()
                    # Cancel_Comment(Location_DC_path,f'{ip+"swarm1swarm-new_docker-compose.yaml"}', <start line need to be commented> (number), <end line need to be commented>(number)).cancel_comment_lines()
                    for dcdir in dcdirs:
                        newdir = Split(dcdir).split_string()
                        finaldir = Rename(newdir).rename_path()
                        Upload_file(f'{ip}',f'{username}',f'{password}', os.path.join(Location_DC_path,f'{ip+finaldir+"_docker-compose.yaml"}')).upload_file()
        case 3:
            print('xxxx')
        case 4:
            print('xxxx')
        case 5:
            print('xxxx')
        case 6:
            print('xxxx')
        case 7:
            print('xxxx')      
        case 8:
            ip_list=Build_IP_Dictionary(f'{select_location}',None).IP_dictionary[f'{select_location}']
            username = Build_Username_Dictionary(f'{select_location}',None,None,None).username_dictionary[f'{select_location}']
            password = Build_Password_Dictionary(f'{select_location}',None,None,None).password_dictionary[f'{select_location}']
            grafana_agent_path = FileFinder('GRAFANA-AGENT').finder()
            for ip in ip_list:
                Generate_Grafana_Agent_File(f'{select_location}',f'{ip}').generate_grafna_agent_file()
                Upload_file(f'{ip}',f'{username}',f'{password}',os.path.join(grafana_agent_path,f'{ip+"grafana-agent.yaml"}'),'/usr/local/bin/grafana-agent.yaml').upload_file()
        
        case 9:
            ip_list=Build_IP_Dictionary(f'{select_location}',None).IP_dictionary[f'{select_location}']
            port_path = FileFinder(f'{select_location+"_PORT"}')
            for ip in ip_list:
                connect_xxx_db=QueryMySQL('<database_address>','<database_username>','<database_password>','<database_name>',1234) # 1234 is database_port,you need to change your own database
                connect_xxx_db.query_ports(f'{ip}')
                connect_xxx_db.save_ports(f'{ip}',os.path.join(port_path,f'{ip+"port.txt"}'))
                connect_xxx_db.close_connection()
        case 10:
            ip_list=Build_IP_Dictionary(f'{select_location}',None).IP_dictionary[f'{select_location}']
            username = Build_Username_Dictionary(f'{select_location}',None,None,None).username_dictionary[f'{select_location}']
            password = Build_Password_Dictionary(f'{select_location}',None,None,None).password_dictionary[f'{select_location}']
            grafana_agent_zip_path = FileFinder('grafana-agent-linux-amd64.zip').finder()
            for ip in ip_list:
                Upload_file(f'{ip}',f'{username}',f'{password}',grafana_agent_zip_path,'/usr/local/bin/grafana-agent.zip').upload_file()

        case 11:
            ip_list=Build_IP_Dictionary(f'{select_location}',None).IP_dictionary[f'{select_location}']
            username = Build_Username_Dictionary(f'{select_location}',None,None,None).username_dictionary[f'{select_location}']
            password = Build_Password_Dictionary(f'{select_location}',None,None,None).password_dictionary[f'{select_location}']
            shell_path = FileFinder(f'SCRIPTS').finder()
            for ip in ip_list:
                Upload_file(f'{ip}',f'{username}',f'{password}',os.path.join(shell_path,f'{select_location+"_start.sh"}'),'<remote start.sh file path>').upload_file()                
        case 12:
            print('xxx')
            
      

def main():
    Build_Functions_choice_Dictionary(None,None).get_function_choice()
    select_function = int(input("which function do you wanna do: (0/1/2...)"))
    select_location = str(input("where machine do you wannna do: (x1,x2,location1,location2 ....)"))
    execute_function(select_location,select_function)
        

if __name__ == "__main__":  
    main()
