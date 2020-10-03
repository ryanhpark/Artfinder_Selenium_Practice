from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
import numpy as np
import pandas as pd

# open webpage
driver = webdriver.Firefox(executable_path='C:\Program Files\geckodriver.exe')
driver.get('https://www.artfinder.com/artist/aarti-bartake/me-at-work/#/')

# close pop-up
close_pop_up = driver.find_element_by_xpath('//div[@class="af-register-modal--b"]//a[@class="close"]')
close_pop_up.click()
time.sleep(2)

# scroll to bottom to get all HTML elements
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# get total number of relevant pages
tot_pages = driver.find_element_by_xpath('//ul[@class="af-pagination "]').text[-1]

# Artist 'Me at Work' page, save scraped text in lists part 1/2
image_titles = []
video_titles = []
caption_text = []
caption_dates = []

# get text from each 'Me at Work' page
for page in np.arange(1, (int(tot_pages) + 1)):
  driver.get(f'https://www.artfinder.com/artist/aarti-bartake/me-at-work/?page={page}#/')
  driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
  time.sleep(2)

  # Artist 'Me at Work' page, scrape text
  image = driver.find_elements_by_xpath('//summary/p[@class="margin margin-m af-bold"]')
  video = driver.find_elements_by_xpath('//summary/h4[@class="margin margin-m"]')
  text = driver.find_elements_by_xpath('//div/summary/footer/div[@class="margin margin-m margin-bottom"]')
  dates = driver.find_elements_by_xpath('//div/summary/footer/p[@class="af-tiny-text af-picasso50-text"]')

  # Artist 'Me at Work' page, save scraped text in lists part 2/2
  def make_lists(element, elem_list):
    for value in element:
      elem_list.append(value.text)
  make_lists(image, image_titles)
  make_lists(video, video_titles)
  make_lists(text, caption_text)
  make_lists(dates, caption_dates)

  map(image_titles.append, image_titles)
  map(video_titles.append, video_titles)
  map(caption_text.append, caption_text)
  map(caption_dates.append, caption_dates)


# add lists to dictionary
posts = {'image_titles': image_titles, 'video_titles': video_titles,
         'caption_text': caption_text, 'caption_date': caption_dates}
##### SAVE SLUG AS COLUMN FOR JOINING LATER #####
##### SAVE SLUG AS COLUMN FOR JOINING LATER #####
##### SAVE SLUG AS COLUMN FOR JOINING LATER #####


# convert dictionary to df and export as .csv
df = pd.DataFrame.from_dict(posts, orient='index')
df_final = df.transpose()
df_final.to_csv('posts.csv', index=False, header=True, encoding='utf-8')


driver.close()