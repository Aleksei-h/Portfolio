from selenium import webdriver
import datetime
from datetime import timedelta
import calendar

date_entry = input('Enter a date in YYYY-MM-DD format: ')
year, month, day = map(int, date_entry.split('-'))
date = datetime.datetime(year, month, day)
input_date = date.strftime('%d.%m').lstrip("0").replace(" 0", " ")

driver = webdriver.Chrome()
driver.get("https://www.gismeteo.ua/ua/weather-odessa-4982/")

two_days = datetime.datetime.now() + timedelta(days=2)
three_five_days = datetime.datetime.now() + timedelta(days=4)
five_seven_days = datetime.datetime.now() + timedelta(days=6)
seven_nine_days = datetime.datetime.now() + timedelta(days=8)
two_weeks = datetime.datetime.now() + timedelta(days=13)
now = datetime.datetime.now()
days_in_month = calendar.monthrange(now.year, now.month)[1]
month = (now + timedelta(days=days_in_month) - timedelta(days=1))

three_five_days_link = "//div[@class='wtitle h2']/a[contains(@href, '3-5')]"
five_seven_days_link = "//div[@class='wtitle h2']/a[contains(@href, '5-7')]"
seven_nine_days_link = "//div[@class='wtitle h2']/a[contains(@href, '7-9')]"
two_weeks_link = "//div[@class='wtitle h2']/a[contains(@href, '14')]"
month_link = "//div[@class='wtitle h2']/a[contains(@href, 'month')]"

day_xpath = "//div[contains(@id, 'tab_wdaily')]/dl/dd"
two_weeks_day_xpath = "//div[@id='weather-weekly']//div[@class='s_date']"
month_days_xpath = "//*[@id='weather-month']//td[@class='weekend tip' or @class='tip']//span"


temp_xpath = "//div[@class='wtabs wrap']//div/div/em/span[@class='value m_temp c']"
two_weeks_temp_xpath = "//div[@id='weather-weekly']//td[@class='temp'][2]/span[@class='value m_temp c']"
month_temps_xpath = "//div[@id='weather-month']//td[@class='weekend tip' or @class='tip']" \
                    "//div[@class='temp max']/dd[@class='value m_temp c']"

day_list = []
temp_list = []
day_temp = {}


if date < now:
    print("Sorry, can't parse for date in the past.")

elif date <= two_days:
    day = driver.find_elements_by_xpath(day_xpath)
    temp = driver.find_elements_by_xpath(temp_xpath)
    for item in day:
        day_list.append(item.text)
    for item in temp:
        temp_list.append(item.text)
    for i in range(len(day_list)):
        day_temp[day_list[i]] = temp_list[i]
    for k, v in day_temp.items():
        if input_date == k:
            print(v)

elif date <= three_five_days:
    driver.find_element_by_xpath(three_five_days_link).click()
    day = driver.find_elements_by_xpath(day_xpath)
    temp = driver.find_elements_by_xpath(temp_xpath)
    for item in day:
        day_list.append(item.text)
    for item in temp:
        temp_list.append(item.text)
    for i in range(len(day_list)):
        day_temp[day_list[i]] = temp_list[i]
    for k, v in day_temp.items():
        if input_date == k:
            print(v)

elif date <= five_seven_days:
    driver.find_element_by_xpath(five_seven_days_link).click()
    day = driver.find_elements_by_xpath(day_xpath)
    temp = driver.find_elements_by_xpath(temp_xpath)
    for item in day:
        day_list.append(item.text)
    for item in temp:
        temp_list.append(item.text)
    for i in range(len(day_list)):
        day_temp[day_list[i]] = temp_list[i]
    for k, v in day_temp.items():
        if input_date == k:
            print(v)

elif date <= seven_nine_days:
    driver.find_element_by_xpath(seven_nine_days_link).click()
    day = driver.find_elements_by_xpath(day_xpath)
    temp = driver.find_elements_by_xpath(temp_xpath)
    for item in day:
        day_list.append(item.text)
    for item in temp:
        temp_list.append(item.text)
    for i in range(len(day_list)):
        day_temp[day_list[i]] = temp_list[i]
    for k, v in day_temp.items():
        if input_date == k:
            print(v)

elif date <= two_weeks:
    driver.find_element_by_xpath(two_weeks_link).click()
    day = driver.find_elements_by_xpath(two_weeks_day_xpath)
    temp = driver.find_elements_by_xpath(two_weeks_temp_xpath)
    for item in day:
        day_list.append(item.text)
    for item in temp:
        temp_list.append(item.text)
    for i in range(len(day_list)):
        day_temp[day_list[i]] = temp_list[i]
    for k, v in day_temp.items():
        if input_date == k:
            print(v)

elif date < month:
    driver.find_element_by_xpath(month_link).click()
    day = driver.find_elements_by_xpath(month_days_xpath)
    temp = driver.find_elements_by_xpath(month_temps_xpath)
    for item in day:
        day_list.append(item.text)
    for item in temp:
        temp_list.append(item.text)
    for i in range(len(day_list)):
        day_temp[day_list[i]] = temp_list[i]

    input_day = input_date.split(".")

    for k, v in day_temp.items():
        if input_day[0] == k:
            print(v)
else:
    print("Sorry, it appears your date is more than one month in the future.")

driver.close()
