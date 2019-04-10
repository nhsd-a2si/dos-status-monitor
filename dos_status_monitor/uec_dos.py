import time

import requests

from dos_status_monitor import config, logger


def get_session(search_role) -> requests.Session:

    s = requests.session()

    if search_role == "DIGITAL_REFERRAL":
        s.auth = (config.UEC_DOS_USERNAME_DIGITAL,
                  config.UEC_DOS_PASSWORD_DIGITAL)
        logger.debug(f"Using account {config.UEC_DOS_USERNAME_DIGITAL}")
    else:
        s.auth = (config.UEC_DOS_USERNAME,
                  config.UEC_DOS_PASSWORD)
        logger.debug(f"Using account {config.UEC_DOS_USERNAME}")
    return s


def get_services_by_service_search(postcode: str,
                                   search_distance: int,
                                   service_types: list,
                                   number_per_type: int,
                                   gp: str,
                                   search_role: str = "PATHWAYS_REFERRAL") -> dict:

    # This is to make sure we don't spam the DoS API with more than 2 requests per second.
    time.sleep(0.5)

    url = f'{config.UEC_DOS_BASE_URL}/app/controllers/api/v1.0/' \
          f'services/byServiceType/CAPMON/{postcode}/{search_distance}/' \
          f'{gp}/0/0/0/{service_types}/{number_per_type}'

    s = get_session(search_role)

    r = s.get(url)
    data = r.json()
    if r.status_code == 200:
        services = data['success']['services']
        return services
    elif r.status_code == 401:
        raise requests.RequestException(f"{r.status_code} - Authentication Denied")
    else:
        raise requests.RequestException(f"{r.status_code} - Request failed")
    

def get_service_by_service_id(service_id: str,
                              search_role: str = "PATHWAYS_REFERRAL") -> dict:

    # This is to make sure we don't spam the DoS API with more than 2 requests per second.
    time.sleep(0.5)

    pathways_session = get_session('PATHWAYS_REFERRAL')
    digital_session = get_session('DIGITAL_REFERRAL')

    url = f'{config.UEC_DOS_BASE_URL}/app/controllers/api/v1.0/' \
          f'services/byServiceId/{service_id}'
    result = pathways_session.get(url)
    service_json = result.json()

    if service_json['success']['serviceCount'] == 0:
        logger.debug("Trying Digital Referral search role")
        result = digital_session.get(url)
        service_json = result.json()

    try:
        service = service_json['success']['services'][0]
        return service

    except IndexError:
        logger.exception('Service not found in JSON response')
        return None
