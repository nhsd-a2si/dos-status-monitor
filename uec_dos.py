import config
import requests


s = requests.session()

s.auth = (config.UEC_DOS_USERNAME,
          config.UEC_DOS_PASSWORD)


def get_services():
    url = f'{config.UEC_DOS_BASE_URL}/app/controllers/api/v1.0/services/' \
          f'byServiceType/TEST/{config.UEC_DOS_POSTCODE}/{config.UEC_DOS_SEARCH_DISTANCE}/0/0/0/0/' \
          f'{config.UEC_DOS_SERVICE_TYPES}/{config.UEC_DOS_NUMBER_PER_TYPE}'
    
    r = s.get(url)
    data = r.json()
    services = data['success']['services']
    return services


def get_service_by_service_id(service_id):
    result = s.get(f'https://uat.pathwaysdos.nhs.uk/app/controllers/api/v1.0/services/byServiceId/{service_id}')
    return result.json()
