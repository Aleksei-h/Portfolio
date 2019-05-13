from selenium import webdriver
import unittest
import datetime
from time import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Selectors:
    sender_city = "Одеса"   # insert sender city here
    recipient_city = "Київ" # insert recipient city here
# Calendar
    date_field_xpath = "//*[@id = 'EstimateDateForm_date']"
    current_date_xpath = "//*[@id = 'EstimateDateForm_date']"
    date_xpath = "//*[@class = 'ui-datepicker-calendar']//a"
# Service Types
    type_field_xpath = "//*[@id = 'EstimateDateForm_ServiceType']"
    doors_doors_xpath = "//*[@data-value= 'DoorsDoors']"
    doors_warehouse_xpath = "//*[@data-value= 'DoorsWarehouse']"
    warehouse_warehouse_xpath = "//*[@data-value= 'WarehouseWarehouse']"
    warehouse_doors_xpath = "//*[@data-value= 'WarehouseDoors']"
# Sender
    sender_field_xpath = "//*[@id = 'EstimateDateForm_senderCity']"
    sender_suggest_dropdown_xpath = "//*[@id = 'EstimateDateForm_senderCity']/../..//ul/li[@class = 'c']/span"
    sender_suggest_dropdown = "//*[@id = 'EstimateDateForm_senderCity']/../..//ul/li[@class = 'c']/span/.."
# Recipient
    recipient_field_xpath = "//*[@id = 'EstimateDateForm_recipientCity']"
    recipient_suggest_dropdown_xpath = "//*[@id = 'EstimateDateForm_recipientCity']/../..//ul/li[@class = 'c']/span"
    recipient_suggest_dropdown = "//*[@id = 'EstimateDateForm_recipientCity']/../..//ul/li[@class = 'c']/span/.."

    submit_button = "//*[@class = 'btn submit']"

    delivery_date_xpath = "//div[@class = 'response']/div/b"

    current_date = datetime.datetime.now().strftime("%d %B %Y %A")
    current_day = current_date.split()[0]
    current_weekday = [current_date.split()[3]]
    district_cities_list = ["Вінниця", "Дніпро", "Донецьк", "Житомир", "Запоріжжя", "Івано-Франківськ", "Київ",
                            "Краматорськ", "Кропивницький", "Луганськ", "Луцьк", "Львів", "Миколаїв", "Одеса",
                            "Полтава", "Рівне", "Суми", "Тернопіль", "Ужгород", "Харків", "Херсон", "Хмельницький",
                            "Черкаси", "Чернівці", "Чернігів"]


class TestDeliveryTerms(unittest.TestCase, Selectors):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.get("https://novaposhta.ua/onlineorder/estimatedate")

    def setUp(self):
        self.driver.find_element_by_xpath(self.date_field_xpath).click()
        daytext = self.driver.find_element_by_xpath(self.date_xpath).text
        if daytext == self.current_day:
            self.driver.find_element_by_xpath(self.date_xpath).click()
        WebDriverWait(self.driver, 5).until(EC.invisibility_of_element_located((By.XPATH, self.date_xpath)))

        self.driver.find_element_by_xpath(self.sender_field_xpath).click()
        self.driver.find_element_by_xpath(self.sender_field_xpath).send_keys(self.sender_city)
        sender_suggest = self.driver.find_element_by_xpath(self.sender_suggest_dropdown_xpath).text
        if self.sender_city in sender_suggest:
            self.driver.find_element_by_xpath(self.sender_suggest_dropdown).click()

        self.driver.find_element_by_xpath(self.recipient_field_xpath).send_keys(self.recipient_city)
        recipient_suggest = self.driver.find_element_by_xpath(self.recipient_suggest_dropdown_xpath).text
        if self.recipient_city in recipient_suggest:
            self.driver.find_element_by_xpath(self.recipient_suggest_dropdown).click()

    def test_id_1(self):
        # Doors-Doors District cities delivery time check.

        self.service_type_name = "Doors-Doors"

        self.driver.find_element_by_xpath(self.type_field_xpath).click()
        self.driver.find_element_by_xpath(self.doors_doors_xpath).click()
        self.driver.find_element_by_xpath(self.submit_button).click()

        assert self.recipient_city and self.sender_city in self.district_cities_list, \
            "\nSender city and(or) recipient city is not a district city(ies)" \
            "\nActual sender city is: %s" \
            "\nActual recipient city is: %s" \
            "\nAcceptable district cities are: %s" \
            % (self.sender_city, self.recipient_city, self.district_cities_list)

        self.delivery_date_text = self.driver.find_element_by_xpath(self.delivery_date_xpath).text
        self.delivery_date = self.delivery_date_text.split()

        for item in self.current_weekday:
            if item == "Saturday" or item == "Sunday":
                assert int(self.delivery_date[0]) - int(self.current_day) >= 2, \
                    "\nDelivery time between district cities, service type '%s' when sending on " \
                    "weekends is longer than two (2) days." \
                    "\nCurrent day is: %s" \
                    "\nDelivery day is: %s" % (self.service_type_name, self.current_day, int(self.delivery_date[0]))

        for item in self.current_weekday:
            if item != "Saturday" and item != "Sunday":
                assert int(self.delivery_date[0]) - int(self.current_day) >= 1, \
                    "\nDelivery time between district cities, service type '%s' when sending on " \
                    "weekdays is longer than one (1) day." \
                    "\nCurrent day is: %s" \
                    "\nDelivery day is: %s" % (self.service_type_name, self.current_day, int(self.delivery_date[0]))

    def test_id_2(self):
        # Doors-Warehouse District cities delivery time check.

        self.service_type_name = "Doors-Warehouse"

        self.driver.find_element_by_xpath(self.type_field_xpath).click()
        self.driver.find_element_by_xpath(self.doors_warehouse_xpath).click()
        self.driver.find_element_by_xpath(self.submit_button).click()

        assert self.recipient_city and self.sender_city in self.district_cities_list, \
            "\nSender city and(or) recipient city is not a district city(ies)" \
            "\nActual sender city is: %s" \
            "\nActual recipient city is: %s" \
            "\nAcceptable district cities are: %s" \
            % (self.sender_city, self.recipient_city, self.district_cities_list)

        self.delivery_date_text = self.driver.find_element_by_xpath(self.delivery_date_xpath).text
        self.delivery_date = self.delivery_date_text.split()
        for item in self.current_weekday:
            if item == "Saturday" or item == "Sunday":
                assert int(self.delivery_date[0]) - int(self.current_day) >= 2, \
                 "\nDelivery time between district cities, service type '%s' when sending on " \
                 "weekends is longer than two (2) days." \
                 "\nCurrent day is: %s" \
                 "\nDelivery day is: %s" % (self.service_type_name, self.current_day, int(self.delivery_date[0]))

        for item in self.current_weekday:
            if item != "Saturday" and item != "Sunday":
                assert int(self.delivery_date[0]) - int(self.current_day) >= 1, \
                 "\nDelivery time between district cities, service type '%s' when sending on " \
                 "weekdays is longer than one (1) day." \
                 "\nCurrent day is: %s" \
                 "\nDelivery day is: %s" % (self.service_type_name, self.current_day, int(self.delivery_date[0]))

    def test_id_3(self):
        # Warehouse-Warehouse District cities delivery time check.

        self.service_type_name = "Warehouse-Warehouse"

        self.driver.find_element_by_xpath(self.type_field_xpath).click()
        self.driver.find_element_by_xpath(self.warehouse_warehouse_xpath).click()
        self.driver.find_element_by_xpath(self.submit_button).click()

        assert self.recipient_city and self.sender_city in self.district_cities_list, \
            "\nSender city and(or) recipient city is not a district city(ies)" \
            "\nActual sender city is: %s" \
            "\nActual recipient city is: %s" \
            "\nAcceptable district cities are: %s" \
            % (self.sender_city, self.recipient_city, self.district_cities_list)

        self.delivery_date_text = self.driver.find_element_by_xpath(self.delivery_date_xpath).text
        self.delivery_date = self.delivery_date_text.split()
        for item in self.current_weekday:
            if item == "Saturday" or item == "Sunday":
                assert int(self.delivery_date[0]) - int(self.current_day) >= 2, \
                    "\nDelivery time between district cities, service type '%s' when sending on " \
                    "weekends is longer than two (2) days." \
                    "\nCurrent day is: %s" \
                    "\nDelivery day is: %s" % (self.service_type_name, self.current_day, int(self.delivery_date[0]))

        for item in self.current_weekday:
            if item != "Saturday" and item != "Sunday":
                assert int(self.delivery_date[0]) - int(self.current_day) >= 1, \
                    "\nDelivery time between district cities, service type '%s' when sending on " \
                    "weekdays is longer than one (1) day." \
                    "\nCurrent day is: %s" \
                    "\nDelivery day is: %s" % (self.service_type_name, self.current_day, int(self.delivery_date[0]))

    def test_id_4(self):
        # Warehouse-Doors District cities delivery time check.

        self.service_type_name = "Warehouse-Doors"

        self.driver.find_element_by_xpath(self.type_field_xpath).click()
        self.driver.find_element_by_xpath(self.warehouse_doors_xpath).click()
        self.driver.find_element_by_xpath(self.submit_button).click()

        assert self.recipient_city and self.sender_city in self.district_cities_list, \
            "\nSender city and(or) recipient city is not a district city(ies)" \
            "\nActual sender city is: %s" \
            "\nActual recipient city is: %s" \
            "\nAcceptable district cities are: %s" \
            % (self.sender_city, self.recipient_city, self.district_cities_list)

        self.delivery_date_text = self.driver.find_element_by_xpath(self.delivery_date_xpath).text
        self.delivery_date = self.delivery_date_text.split()
        for item in self.current_weekday:
            if item == "Saturday" or item == "Sunday":
                assert int(self.delivery_date[0]) - int(self.current_day) >= 2, \
                    "\nDelivery time between district cities, service type '%s' when sending on " \
                    "weekends is longer than two (2) days." \
                    "\nCurrent day is: %s" \
                    "\nDelivery day is: %s" % (self.service_type_name, self.current_day, int(self.delivery_date[0]))

        for item in self.current_weekday:
            if item != "Saturday" and item != "Sunday":
                assert int(self.delivery_date[0]) - int(self.current_day) >= 1, \
                    "\nDelivery time between district cities, service type '%s' when sending on " \
                    "weekdays is longer than one (1) day." \
                    "\nCurrent day is: %s" \
                    "\nDelivery day is: %s" % (self.service_type_name, self.current_day, int(self.delivery_date[0]))

    def tearDown(self):
        # self.driver.save_screenshot("screenshot_%s.png" % str(int(time())))
        self.driver.get("https://novaposhta.ua/onlineorder/estimatedate")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == '__main__':
    unittest.main()
