def is_keys_in_data(response_data, data_keys=None):
    if data_keys is None:
        return True
    return all(key in data_keys for key in response_data)


def is_response_successful(response):
    return response.status_code == 200 and len(response.data['error_messages']) == 0 and \
        len(response.data['success_messages']) > 0 and response.data['data'] != []


def is_response_unsuccessful(response):
    return response.status_code == 403 and len(response.data['error_messages']) > 0 and \
        len(response.data['success_messages']) == 0 and \
        (response.data['data'] is None or len(response.data['data']) >= 0)


def is_response_empty(response):
    return response.status_code == 200 and len(response.data['error_messages']) == 0 and \
        len(response.data['success_messages']) > 0 and response.data['data'] == []
