from selenium import webdriver
import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestNpDelivery(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.get("https://novaposhta.ua")
        cls.cn_xpath = "//*[@id = 'cargo_number']"
        cls.invoice = str("20450110684280")  # insert invoice number here
        cls.driver.find_element_by_xpath(cls.cn_xpath).send_keys(cls.invoice)
        cls.button_xpath = "//div[@class = 'search_cargo_form']//*[@type = 'submit']"
        cls.driver.find_element_by_xpath(cls.button_xpath).click()

    def test_id_1_0(self):
        # Tracking page name check
        expected_page_title = "Відстежити/Оплатити"
        page_title_xpath = "//*[@class = 'page_title']"
        actual_page_title = self.driver.find_element_by_xpath(page_title_xpath).text
        assert expected_page_title == str(actual_page_title), \
            "\nActual Page name is: %s\nExpected Page name is %s" \
            % (str(actual_page_title), expected_page_title)

    def test_id_1_1(self):
        # Page description check
        page_description_xpath = "//div[@class = 'text desc']/p"
        actual_page_description = self.driver.find_element_by_xpath(page_description_xpath).text
        expected_page_description = "Даний сервіс допоможе Вам дізнатися, де зараз знаходиться Ваше відправлення"
        assert expected_page_description == actual_page_description, \
            "\nActual Page description is: %s\nExpected Page description is: %s" \
            % (str(actual_page_description), expected_page_description)

    def test_id_1_2(self):
        # Valid invoice page displayed check
        cn_input_xpath = "//*[@id= 'cargo_number_inp']"
        cn_input = self.driver.find_element_by_xpath(cn_input_xpath).get_attribute("value")
        assert self.invoice == cn_input, \
            "\nActual invoice number autofilled is: %s\nExpected is: %s" % (cn_input, self.invoice)

    def test_id_1_3(self):
        # "Clear" button check.
        clear_button_xpath = "//*[@id = 'clear-btn']"
        self.driver.find_element_by_xpath(clear_button_xpath).click()
        clear_button_hidden = self.driver.find_element_by_xpath(clear_button_xpath).get_attribute("style")
        assert clear_button_hidden == str("display: none;"), "\n'Clear' button is visible after clicking on it."

    def test_id_1_4(self):
        # "Відстежити" button check
        track_button_xpath = "//button [@id='button']"
        track_button_visible = self.driver.find_element_by_xpath(track_button_xpath).get_attribute("style")
        assert track_button_visible == str("display: inline-block;"), \
            "\n'Відстежити' button is not displayed after clicking on the 'Clear' button."
        self.driver.find_element_by_xpath("//*[@id= 'cargo_number_inp']").send_keys("11111")
        track_button_active = self.driver.find_element_by_xpath(track_button_xpath).get_attribute("class")
        assert track_button_active == str(""), \
            "\n'Відстежити' button is not active after entering text."

    def test_id_1_5(self):
        # Info description check
        info_description_xpath = "//div[@class = 'track-data']//span[@class = 'description']"
        info_description = self.driver.find_elements_by_xpath(info_description_xpath)
        expected_info_description = \
            ['Маршрут', 'Адреса доставки', 'Документи для отримання', 'Як замовити переадресацію']
        actual_info_description = []
        for item in info_description:
            actual_info_description.append(item.text)
        assert actual_info_description == expected_info_description, \
            "\nOne or more info description elements are absent" \
            "\nActual description elements: %s\nExpected description elements: %s" \
            % (actual_info_description, expected_info_description)

    def test_id_1_6(self):
        # Parcel status check
        parcel_status_xpath = "//div[contains(@class,'status')]"
        parcel_status = self.driver.find_elements_by_xpath(parcel_status_xpath)
        actual_parcel_status = []
        for item in parcel_status:
            actual_parcel_status.append(item.text)
        assert actual_parcel_status[0] != "", "\n Parcel status is missing."
        assert actual_parcel_status[1] != "", "\n Parcel status description is missing."

    def test_id_1_7(self):
        # Parcel info check
        route_info_xpath = "//td[contains(., 'Маршрут')]/div"
        route_info = self.driver.find_element_by_xpath(route_info_xpath).text
        assert route_info != "", "\n Route info is missing"
        delivery_address_xpath = "//td[contains(., 'Адреса')]/div/a"
        delivery_address = self.driver.find_element_by_xpath(delivery_address_xpath).text
        assert delivery_address != "", "\n Delivery address is missing"

    def test_id_1_8(self):
        # Info links check
        info_links_xpath = "//div[@class = 'track-data']//div/a"
        info_links = self.driver.find_elements_by_xpath(info_links_xpath)
        info_links_list = []
        for item in info_links:
            info_links_list.append(str(item.get_attribute("href")))
        assert "office" or "Address" in info_links_list[0], "\nDelivery address link is absent, broken or changed."
        assert "dokumenti" in info_links_list[1], "\nDocuments link is absent, broken or changed."
        assert "pereadresatsiya" in info_links_list[2], "\nForwarding link is absent, broken or changed."

    def test_id_1_9(self):
        # Full info phone form check
        payment_button_xpath = "//*[@id = 'payment-button']"
        full_info_form_xpath = "//div[@class = 'wrapper-phone-form']"
        assert not len(self.driver.find_elements_by_xpath(full_info_form_xpath)), \
            "\nFull info phone form is displayed without clicking on the Payment button"
        self.driver.find_element_by_xpath(payment_button_xpath).click()
        info_form_visible_after_click = \
            self.driver.find_element_by_xpath(full_info_form_xpath).get_attribute("class")
        assert info_form_visible_after_click == "wrapper-phone-form", \
            "\nFull info phone form is not displayed after clicking on the Payment button."

    def test_id_2_0(self):
        # Portmone field placeholder check
        self.driver.back()
        portmone_button_xpath = "//div[@class = 'block_left']//a[@class ='portmone-button']"
        bill_amount_xpath = "//*[@id = 'bill_amount']"
        self.driver.find_element_by_xpath(portmone_button_xpath).click()
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, bill_amount_xpath)))
        actual_bill_amount_placeholder = \
            self.driver.find_element_by_xpath(bill_amount_xpath).get_attribute("placeholder")
        expected_bill_amount_placeholder = \
            "від 1 до 25000 грн"
        assert actual_bill_amount_placeholder == expected_bill_amount_placeholder, \
            "\nActual bill amount placeholder is: %s\nExpected is: %s" \
            % (actual_bill_amount_placeholder, expected_bill_amount_placeholder)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == '__main__':
    unittest.main()
