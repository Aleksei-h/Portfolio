from selenium import webdriver
import unittest
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestTrackingStatus(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.get("https://novaposhta.ua")

    def test_api(self):
        api_key = "158b8f7af6601387cd3eb758e1defd83"
        tracking_request = {
            "apiKey": api_key,
            "modelName": "TrackingDocument",
            "calledMethod": "getStatusDocuments",
            "methodProperties": {
                "Documents": [
                    {
                        "DocumentNumber": "20400048799000",
                        "Phone": ""
                    },

                ]
            }

        }

        r = requests.post("https://api.novaposhta.ua/v2.0/json/", json=tracking_request)
        expected_status = ['Номер не знайдено']
        actual_status = []
        for item in r.json()['data']:
            actual_status.append(item['Status'])
        assert expected_status == actual_status, "\nUnexpected status description for non-existent Document Number:" \
                                                 "\nExpected status is: %s" \
                                                 "\nActual status is: %s" % (expected_status, actual_status)

    def test_ui(self):
        self.cargo_number_field_xpath = "//*[@id='cargo_number']"
        self.driver.find_element_by_xpath(self.cargo_number_field_xpath).send_keys("20400048799000\n")
        actual_status_xpath = "//*[@id='new_track_form']/div[@class = 'not-found']/span"
        expected_status = "Експрес-накладної з таким номером не знайдено."
        actual_status = self.driver.find_element_by_xpath(actual_status_xpath).text
        assert actual_status == expected_status, "\nUnexpected exception message for non-existent Document Number:" \
                                                 "\nExpected status is: %s" \
                                                 "\nActual status is: %s" % (expected_status, actual_status)


    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == '__main__':
    unittest.main()
