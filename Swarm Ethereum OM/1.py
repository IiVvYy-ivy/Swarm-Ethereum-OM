import configparser  
  
# 创建配置解析器对象  
config = configparser.ConfigParser()  
  
# 读取INI配置文件  
config.read('E:\Git_Swarm-Ethereum-OM\Swarm-Ethereum-OM\Swarm Ethereum OM\configuration.ini')  
  
ip_config_sections = []
ip_config_dict = {}
for section in config.sections():  
    if "IP" in section:  
        ip_config_sections.append(section)
for ip_config_section in ip_config_sections:
    for key,value in config.items(ip_config_section):
        ip_config_dict[key]=value
    print(ip_config_dict)