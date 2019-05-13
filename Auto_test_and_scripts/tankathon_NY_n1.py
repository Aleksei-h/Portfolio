from selenium import webdriver
from time import time
import unittest


class TestTankathon(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_check_NY_first_place(self):
        self.driver.get("http://www.tankathon.com")
        new_york_xpath = "//td[@class='pick' and text()='1']/..//div[@class='desktop']"
        new_york_text = self.driver.find_element_by_xpath(new_york_xpath).text
        assert str("New York") == str(new_york_text), \
            "\nActual Team is: %s\nExpected Team is: %s" % (str(new_york_text), 'New York')
        # self.driver.save_screenshot("screenshot_%s.png" % str(int(time())))

    def tearDown(self):
        self.driver.close()


if __name__ == '__main__':
    unittest.main()
