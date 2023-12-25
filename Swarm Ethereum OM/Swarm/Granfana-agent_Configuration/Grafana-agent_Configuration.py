import yaml
import sys
select_location = sys.argv[1]
ip = sys.argv[2]
with open(f'E:\\Swarm Ethereum OM\\Swarm\\Swarm-TOP\\Automated O&M\\Ultimate\PORT\\{select_location+"_PORT"}\\{ip+"port.txt"}', 'r') as f:   
    port_list = [line.strip() for line in f]  
basic_auth={
    "username": "<username>",
    "password": "<password>"
}
static_configuration=[
         {
            'targets': [f'localhost:{port}'],
            'labels': {
                'instance': f'{ip}:{port}',
                'top': '<top_name>',          # Change your own top name
                'cluster': f'{ip}' 
            }  
         }
         for port in port_list
     ]
scrape_configurations=[
    {
        'job_name': 'bee',
        'static_configs': static_configuration
    }
]
configs=[
    {
        'name': 'default',
        'scrape_configs': scrape_configurations
    }
]
headers={
    "X-Scope-OrgID": "<top_name>"
}
labels=[
    '__name__'
]
write_relabel_configs=[
    {'source_labels': labels,
     "regex": 'bee_(.*)',
     "action": "keep"   
    }
]
remote_write=[
    {'url':'<remote_write_address>',
     'headers': headers,
     "basic_auth": basic_auth,
     "write_relabel_configs": write_relabel_configs  
    }    
]
globals={
    "remote_write": remote_write
}
metrics={
    "wal_directory":"/var/lib/grafana-agent",
    "global": globals,
    "configs": configs
}
server={"log_level": "info"}
node_exporter={
    "enabled": True
}
agent={
    "enabled": True
}
integrations={
    "agent": agent,
    "node_exporter": node_exporter
}
grafanaconfig={
    'server': server,
    'metrics': metrics, 
    'integrations': integrations         
}
with open(f'E:\\Swarm Ethereum OM\\Swarm-TOP\\Automated O&M\\Ultimate\\GRAFANA-AGENT\\{ip+"grafana-agent.yaml"}', 'w') as file:  
    yaml.dump(grafanaconfig, file,default_flow_style=False,sort_keys=False)
