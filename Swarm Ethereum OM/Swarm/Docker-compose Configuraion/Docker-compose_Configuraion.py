
# IMPORT RELEVANT MOUDLE YAML(python to yaml) & ORDEREDDICT(output YAML in the original dictionary order)

import yaml
from collections import OrderedDict
print("Make docker-compose.yaml")

# SETTING PARAMETERS: START/END INDEX, IMAGE VERSION, DESTIONATION DIR, START API ADDR PORT, START P2P ADDR PORT, START DEBUG ADDR PORT, SERVICES DICT

IP=str(input('input ip of you wanna put docker-compose file:'))

directory=str(input("input bees generate dir:"))

num1=int(input('input start bee index:'))

num2=int(input('input end bee index:'))


services = {}

# SETTING PARAMETERS OF SERVICES
for i in range(num1, (num2+1)):
    service_name = f'bee-{i}'

    API_ADDR_PORT=int(input("Input api addr port:"))+(i-1)*3
    
    P2P_ADDR_PORT=int(input("Input p2p addr port:"))+(i-1)*3
    
    DEBUG_ADDR_PORT=int(input("Input debug addr port:"))+(i-1)*3
    
    enviroment_variable=[f'BEE_API_ADDR',f'BEE_BLOCK_TIME',f'BEE_BOOTNODE',f'BEE_BOOTNODE_MODE',f'BEE_CONFIG',f'BEE_CORS_ALLOWED_ORIGINS',f'BEE_DATA_DIR',f'BEE_CACHE_CAPACITY',f'BEE_DB_OPEN_FILES_LIMIT',f'BEE_DB_BLOCK_CACHE_CAPACITY',f'BEE_DB_WRITE_BUFFER_SIZE',f'BEE_DB_DISABLE_SEEKS_COMPACTION',f'BEE_DEBUG_API_ADDR',f'BEE_DEBUG_API_ENABLE',f'BEE_FULL_NODE',f'BEE_NAT_ADDR={IP}:{P2P_ADDR_PORT}',f'BEE_NETWORK_ID',f'BEE_P2P_ADDR',f'BEE_P2P_QUIC_ENABLE',f'BEE_P2P_WS_ENABLE',f'BEE_PASSWORD',f'BEE_PASSWORD_FILE',f'BEE_PAYMENT_EARLY_PERCENT',f'BEE_PAYMENT_THRESHOLD',f'BEE_PAYMENT_TOLERANCE_PERCENT',f'BEE_POSTAGE_STAMP_ADDRESS',f'BEE_RESOLVER_OPTIONS',f'BEE_SWAP_ENABLE',f'BEE_BLOCKCHAIN_RPC_ENDPOINT',f'BEE_SWAP_FACTORY_ADDRESS',f'BEE_SWAP_LEGACY_FACTORY_ADDRESSES',f'BEE_SWAP_INITIAL_DEPOSIT',f'BEE_SWAP_DEPLOYMENT_GAS_PRICE',f'BEE_TRACING_ENABLE',f'BEE_TRACING_ENDPOINT',f'BEE_TRACING_SERVICE_NAME',f'BEE_TRANSACTION',f'BEE_VERBOSITY',f'BEE_WELCOME_MESSAGE',f'BEE_MAINNET']
    
    ports_variable=[f'${{API_ADDR:-{API_ADDR_PORT}}}${{BEE_API_ADDR:-:1633}}',f'${{P2P_ADDR:-{P2P_ADDR_PORT}}}${{BEE_P2P_ADDR:-:1634}}',f'${{DEBUG_API_ADDR:-127.0.0.1:{DEBUG_ADDR_PORT}}}${{BEE_DEBUG_API_ADDR:-:1635}}']

    volumes_variable=[f'{directory}/bee-{i}:/home/bee/.bee',f'{directory}/password:/home/bee/.bee/password']
    
    services[service_name] = {
        'image': f'ethersphere/bee:1.18.2', 
        'restart': 'unless-stopped',
        'environment':enviroment_variable,
        'ports':ports_variable,
        'volumes':volumes_variable,
        'command': 'start'}

# SETTING BEECONGIURATION PARAMETER 
beeconfiguration = {'version':'3',
                    'services': services

                   }

# OUTPUT YAML
with open('docker-compose.yaml', 'w') as file:
    yaml.dump(beeconfiguration, file, sort_keys=False)

with open('docker-compose.yaml', 'a') as file:
    file.write("volumes:\n")
    for i in range(num1, (num2 + 1)):
        file.write("\x20\x20"+f'bee-{i}:\n')
