import requests
import json


def get_endpoint_server(context):
    config = context.config
    endpoint = config["endpoint"]
    return endpoint


def get_headers(context):
    headers = {'content-type': 'application/json'}
    if "token" in context:
        if context.token is not None:
            headers["Authorization"] = "Bearer " + context.token
    return headers


def make_get_request(context, url, params=None):
    headers = get_headers(context)
    return requests.get(url, headers=headers, params=params, verify=False)


def make_post_request(context, url, data):
    headers = get_headers(context)
    return requests.post(url, data=json.dumps(data), headers=headers, verify=False)


def make_delete_request(context, url):
    headers = get_headers(context)
    return requests.delete(url, headers=headers, verify=False)


def retrieve_context_table(context):
    def row_to_dict(row, properties):
        result = {}
        for property in properties:
            result[property] = str(row[property])
        return result

    properties = context.table.headings
    result = []
    for row in context.table:
        result.append(row_to_dict(row, properties))
    return result


def check_list_elements_by_keys(l1, l2):
    if len(l1) != len(l2):
        raise AssertionError(
            f'Expected {len(l1)} elements, found {len(l2)}'
        )
    for e1, e2 in zip(l1, l2):
        for key in e1.keys():
            if str(e1.get(key)) != str(e2[key]):
                raise AssertionError("row:" + str(e1) + ", row[" + key + "]:" +
                                     str(e1.get(key)) + "; element[" + key + "]:" + str(e2[key]))
