from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
import numpy as np
import pandas as pd

# open webpage
driver = webdriver.Firefox(executable_path='C:\Program Files\geckodriver.exe')

driver.get('https://www.artfinder.com/artist/aarti-bartake/me-at-work/#/')

# close pop-ups
close_pop_up = driver.find_element_by_xpath('//div[@class="af-register-modal--b"]//a[@class="close"]')
close_pop_up.click()
time.sleep(2)

# scroll to bottom to get all HTML elements
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# get total number of relevant pages
tot_pages = driver.find_element_by_xpath('//ul[@class="af-pagination "]').text[-1]

# get text from each 'Me at Work' page
for page in np.arange(1, (int(tot_pages) + 1)):
  driver.get(f'https://www.artfinder.com/artist/aarti-bartake/me-at-work/?page={page}#/')
  driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
  time.sleep(2)

  # Artist 'Me at Work' page, scrape text
  image = driver.find_elements_by_xpath('//summary/p')
  video = driver.find_elements_by_xpath('//summary/h4')
  text = driver.find_elements_by_xpath('//div/summary/footer/div')
  dates = driver.find_elements_by_xpath('//div/summary/footer/p')

  # Artist 'Me at Work' page, save scraped text in lists
  image_titles = []
  video_titles = []
  caption_text = []
  caption_dates = []
  def make_lists(element, elem_list):
    for value in element:
      elem_list.append(value.text)
  make_lists(image, image_titles)
  make_lists(video, video_titles)
  make_lists(text, caption_text)
  make_lists(dates, caption_dates)

  posts = {'image_titles': image_titles, 'video_titles': video_titles,
           'caption_text': caption_text, 'caption_date': caption_dates}
  
  posts = pd.DataFrame(posts)
  posts.to_csv('posts.csv')



driver.close()