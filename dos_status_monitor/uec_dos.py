from dos_status_monitor import config
import requests
import time

s = requests.session()

s.auth = (config.UEC_DOS_USERNAME,
          config.UEC_DOS_PASSWORD)


def get_services_by_service_search(postcode: str,
                                   search_distance: int,
                                   service_types: list,
                                   number_per_type: int) -> dict:

    time.sleep(0.5)

    url = f'{config.UEC_DOS_BASE_URL}/app/controllers/api/v1.0/' \
          f'services/byServiceType/CAPMON/{postcode}/{search_distance}/' \
          f'0/0/0/0/{service_types}/{number_per_type}'
    
    r = s.get(url)
    data = r.json()
    if r.status_code == 200:
        services = data['success']['services']
        return services
    elif r.status_code == 401:
        raise requests.RequestException(f"Authentication Denied")
    else:
        raise requests.RequestException("Request failed")
    

def get_service_by_service_id(service_id: str) -> dict:
    time.sleep(1)
    url = f'{config.UEC_DOS_BASE_URL}/app/controllers/api/v1.0/' \
          f'services/byServiceId/{service_id}'
    result = s.get(url)
    return result.json()
