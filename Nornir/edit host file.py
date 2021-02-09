from nornir import InitNornir
import ruamel
import sys
nr = InitNornir(core={"num_workers": 50},
                inventory={
                    "plugin": "nornir.plugins.inventory.simple.SimpleInventory",
                    "options": {
                        "host_file": "inventory/all-hosts2.yaml",
                        "group_file": "inventory/groups.yaml",
                        "default_file": "inventory/defaults.yaml"
                    }
                }
                )


yaml = ruamel.yaml.YAML()
with open("inventory/hosts2.yaml") as filename:
    data = yaml.load(filename)

for host in data:
    site = data[host]['data']['site']
    if site in ("MIT", "Westbury"):
        data[host]['data']['building'] = 'Datacenter'
    elif site in ("Forest Hills Hospital", "Glen Cove Hospital", "Huntington Hospital", "LHH", "LIJ", "Mather Hospital",
             "MEETH", "NSUH", "NWH", "PBMC", "Phelps Hospital", "Plainview Hospital", "SIUH",
             "South Oaks Hospital", "Southshore Hospital", "Syosset Hospital", "Valley Stream Hospital"):
        data[host]['data']['building'] = 'Hospital'
    else:
        data[host]['data']['building'] = 'Remote'

yaml.indent(mapping=2, sequence=4, offset=2)
# yaml.dump(data, sys.stdout)
with open("inventory/hosts3.yaml", 'w') as finished:
    yaml.dump(data, finished)
