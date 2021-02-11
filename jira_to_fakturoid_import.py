import argparse
import base64
import csv

import requests

post_url_fakturoid = "https://app.fakturoid.cz/api/v2/accounts/aronde/invoices.json"


def parse_file_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', required=True, type=str, help='Insert path of the jira.csv file')
    parser.add_argument('--api_key', required=True, type=str, help='Insert API KEY')
    parser.add_argument('--email', required=True, type=str, help='Insert valid email to authorize the account')
    return parser.parse_args()


arguments = vars(parse_file_argument())


def create_json_line(row):
    value_key = row['Issue Key']
    value_summary = row['Issue summary']
    value_hours = row['Hours']
    return {"name": (f'{value_key} - {value_summary}'),
            "quantity": float(value_hours),
            "unit_name": "h",
            "unit_price": "1000",
            "vat_rate": "21"}


def create_json_lines():
    with open(arguments['path']) as jira_file:
        jira_reader = csv.DictReader(jira_file)
        json_lines = []
        for row in jira_reader:
            line = create_json_line(row)
            json_lines.append(line)
    return json_lines


def send_post_request_to_fakturoid(json_lines, requestpost):
    body = {
        "subject_id": 11505804,
        "currency": "CZK",
        "payment_method": "bank",
        "due": 14,
        "bank_account_id": 175480,
        "lines": json_lines
    }
    b64_string = base64.b64encode(bytes(arguments['email'] + ':' + arguments['api_key'], 'utf-8'))

    headers = {'Content-Type': 'application/json',
               'User-Agent': 'fakturoid-jira-csv-importer' + arguments['email'],
               'Authorization': 'Basic ' + b64_string.decode('ascii')
               }

    response_fakturoid = requestpost(url=post_url_fakturoid, json=body, headers=headers)
    print(response_fakturoid)


if __name__ == '__main__':
    json_lines = create_json_lines()
    send_post_request_to_fakturoid(json_lines, requests.post)
