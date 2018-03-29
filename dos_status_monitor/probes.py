from dos_status_monitor import database


def get_watched_search_list():
    new_search_list = []
    search_list = database.get_watched_searches()

    for search in search_list:
        probe = {
            'postcode': search['search_postcode'],
            'gp': search['search_gp'],
            'search_distance': str(int(search['search_distance'])),
            'service_types': ",".join(search['search_service_types']),
            'number_per_type': str(int(search['search_results_limit'])),
            'description': search['description']
        }
        new_search_list.append(probe)

    return new_search_list


def get_watched_service_list():
    service_list = database.get_watched_services()
    return list(service_list)


