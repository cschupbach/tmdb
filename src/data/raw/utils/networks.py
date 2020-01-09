import json

def get_network_ids(fp='json/networks.json'):
    with open(fp) as f:
        network_dict = json.load(f)

    network_ids = []
    for k in network_dict.keys():
        network_ids += list(network_dict[k].keys())

    return network_ids
