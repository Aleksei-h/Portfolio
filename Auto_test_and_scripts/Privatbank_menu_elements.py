from selenium import webdriver
import unittest


class TestPrivatBank(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.get("https://privatbank.ua")
        cls.driver.maximize_window()

    def test_menu_items(self):
        self.menu_items_xpath = "//*[@id='cbp-hrmenu']//a[@class = 'dropdown-toggle' or @class='hovered']"
        self.menu_items = self.driver.find_elements_by_xpath(self.menu_items_xpath)
        actual_menu_items = []
        for item in self.menu_items:
            actual_menu_items.append(item.text)

        with open("privat.txt", "r", encoding='utf-8-sig') as o:
            for line in o:
                line = line.strip()
                expected_menu_items = line.split("|")
                assert actual_menu_items == expected_menu_items, "\nMenu items has been changed or invalid:" \
                                                                 "\nActual menu items are: %s" \
                                                                 "\nExpected menu items are: %s"\
                                                                 % (actual_menu_items, expected_menu_items)

    @classmethod
    def tearDownClass(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()
