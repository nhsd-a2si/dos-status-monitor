from dos_status_monitor import config, database
import json
import logging

logging.basicConfig()
logger = logging.getLogger('DSM')


def get_probe_list():
    
    probe_config = config.PROBE_LIST
    
    probe_list = probe_config.split('|')
    
    new_probe_list = []
    
    for probe_item in probe_list:
        probe_config_items = probe_item.split(':')
        
        probe = {
            'postcode': probe_config_items[0],
            'search_distance': probe_config_items[1],
            'service_types': probe_config_items[2],
            'number_per_type': probe_config_items[3]
        }
        
        new_probe_list.append(probe)

    return new_probe_list


def get_probe_json():
    probe_json = probe_config = json.loads(config.PROBE_JSON)


def get_watched_service_list():
    service_list = database.get_service_watchlist()
    logger.debug(service_list)
    return service_list

