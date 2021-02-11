import unittest

from jira_to_fakturoid_import import create_json_line, send_post_request_to_fakturoid


class MyTestCase(unittest.TestCase):
    def test_when_function_create_json_lines_is_called_then_json_lines_is_not_empty(self):
        dict = {'Issue Key': '01', 'Issue summary': 'CTA01', 'Hours': 0.25}
        result = create_json_line(dict)
        self.assertEqual(result, {"name": '01 - CTA01',
                                  "quantity": 0.25,
                                  "unit_name": "h",
                                  "unit_price": "1000",
                                  "vat_rate": "21"})

    def test_when_argument_hours_is_missing_then_error_is_thrown(self):
        dict = {'Issue Key': '01', 'Issue summary': 'CTA01'}
        self.assertRaises(KeyError, create_json_line, dict)

    def test_when_json_lines_is_send_correctly_then_body_is_send_correctly_too(self):
        argument_for_func = {}

        def fake_requestpost(url, json, headers):
            argument_for_func.setdefault('json', json)
            return 'foo'

        json_lines = {"name": '01 - CTA01',
                      "quantity": 0.25,
                      "unit_name": "h",
                      "unit_price": "1000",
                      "vat_rate": "21"}
        send_post_request_to_fakturoid(json_lines, fake_requestpost)
        self.assertEqual(argument_for_func['json'], {"subject_id": 11505804,
                                                     "currency": "CZK",
                                                     "payment_method": "bank",
                                                     "due": 14,
                                                     "bank_account_id": 175480,
                                                     "lines": json_lines
                                                     })


if __name__ == '__main__':
    unittest.main()
