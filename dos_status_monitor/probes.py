from dos_status_monitor import config, database, logger


def get_probe_list():
    
    probe_config = config.PROBE_LIST
    
    probe_list = probe_config.split('|')
    
    new_probe_list = []
    
    for probe_item in probe_list:
        if probe_item == '':
            print("No valid config - skipping")
            continue

        probe_config_items = probe_item.split(':')
        
        probe = {
            'postcode': probe_config_items[0],
            'search_distance': probe_config_items[1],
            'service_types': probe_config_items[2],
            'number_per_type': probe_config_items[3]
        }
        
        new_probe_list.append(probe)

    return new_probe_list


def get_watched_search_list():
    new_search_list = []
    search_list = database.get_watched_searches()

    for search in search_list:
        probe = {
            'postcode': search['search_postcode'],
            'search_distance': str(search['search_distance']),
            'service_types': ",".join(search['search_service_types']),
            'number_per_type': str(search['search_results_limit']),
            'description': search['description']
        }
        new_search_list.append(probe)

    return new_search_list


def get_watched_service_list():
    service_list = database.get_watched_services()
    return list(service_list)


