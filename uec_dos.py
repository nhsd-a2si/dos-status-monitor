import config
import requests


s = requests.session()

s.auth = (config.UEC_DOS_USERNAME,
          config.UEC_DOS_PASSWORD)


def get_services(postcode, search_distance, number_results_per_type):
    url = 'https://uat.pathwaysdos.nhs.uk/app/controllers/api/v1.0/services/' \
          f'byServiceType/12345/{postcode}/{search_distance}/0/0/0/0/13,116/{number_results_per_type}'
    
    r = s.get(url)
    data = r.json()
    services = data['success']['services']
    return services


def get_service_by_service_id(service_id):
    result = s.get(f'https://uat.pathwaysdos.nhs.uk/app/controllers/api/v1.0/services/byServiceId/{service_id}')
    return result.json()
