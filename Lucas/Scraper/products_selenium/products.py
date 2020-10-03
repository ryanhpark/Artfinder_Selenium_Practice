from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
import re
import csv
import pandas as pd


# Go to the page that we want to scrape
driver = webdriver.Chrome()
driver.get("https://www.artfinder.com/product/sparrow-bird-watercolor-sparrow-chinese-watercolor-bird-steadfa/#/")

# csv_file = open('products.csv', 'w', encoding='utf-8', newline='')
# writer = csv.writer(csv_file)

# Click review button to go to the shipping section
close_pop_up = driver.find_element_by_xpath(
    '//div[@class="af-register-modal--b"]//a[@class="close"]')
close_pop_up.click()
time.sleep(2)

wait_shipping = WebDriverWait(driver, 10)
shipping_button = driver.find_element_by_xpath(
    '//div[@class="accordion-navigation"]//span[@class="toggler"]')
shipping_button.click()
time.sleep(3)

# here we create a dictionary of things we want
product_dict = {}

product_dict['title'] = driver.find_elements_by_xpath(
    '//h1[@class="h2 af-underline-links"]')[0].text
product_dict['type'] = driver.find_element_by_xpath(
    '//h2[@class="p af-underline-links margin margin-s"]/a').text

try:
    product_dict['price'] = driver.find_elements_by_xpath(
        '//p[@class="h2 margin margin-m margin-bottom"]/span[@class="main-price js-price"]')[0].text
    product_dict['sold'] = "False"
except:
    product_dict['price'] = driver.find_elements_by_xpath(
        '//p[@class="h2 margin margin-m margin-bottom"]/span[@class="linethrough"]')[0].text
    product_dict['sold'] = driver.find_elements_by_xpath(
        '//p[@class="h2 margin margin-m margin-bottom"]/span[@class="gray-text"]')[0].text

bulletPoints_raw = driver.find_elements_by_xpath(
    '//ul[@class="af-underline-links"]/li/span')
product_dict['bulletPoints'] = list(map(lambda x: x.text, bulletPoints_raw))

product_dict['shipping_price'] = driver.find_element_by_xpath(
    '//p[@class="clearfix af-bg-dots"]//span[@class="right af-bold"]/strong').text

product_dict['description'] = driver.find_element_by_xpath(
    '//div[@id="product-description"]/p').text
product_dict['materialsUsed'] = driver.find_elements_by_xpath(
    '//div[@id="product-description"]/p')[1].text.split(",")

tags_raw = driver.find_elements_by_xpath(
    '//p[@class="af-line-height-l"]/a')
product_dict['tags'] = list(
    filter(None, list(map(lambda x: x.text, tags_raw))))

try:
    featured_raw = driver.find_element_by_xpath(
        '//div[@class="show-for-large-up margin margin-m margin-top"]//a')
    product_dict['featuredByEditors'] = list(
        map(lambda x: x.text, featured_raw))
except:
    product_dict['featuredByEditors'] = "---"


# write to csv
df = pd.DataFrame.from_dict(product_dict, orient='index')
df_final = df.transpose()
df_final.to_csv('products.csv', index=False, header=True, encoding='utf-8')

# close bot
time.sleep(1)
driver.close()
