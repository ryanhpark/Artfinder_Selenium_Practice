from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import numpy as np
# from collections import defaultdict
import pandas as pd

# get a list of all slugs
artists = pd.read_csv("../artists.csv", usecols=['slug']).drop_duplicates()
slugs_list = artists['slug'].to_list()

# store strings from each page for each artist
video = []
titles = []
texts = []
dates = []
slugs = []

# establish driver
driver = webdriver.Firefox(executable_path='C:\Program Files\geckodriver.exe')

for slug in slugs_list[19:26]:
  # open artist's Me at Work page
  driver.get(f'https://www.artfinder.com/artist/{slug}/me-at-work/#/')
  time.sleep(2)
  # close pop-up
  try:
    close_pop_up = driver.find_element_by_xpath(
      '//div[@class="af-register-modal--b"]//a[@class="close"]')
    close_pop_up.click()
  except:
    pass

  # scroll to bottom to access all HTML elements
  driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
  WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH,
        '//div[@class="scroll-to-top af-opacity"]')))


  # check for multiple pages
  try:
    # if there are multiple pages
    driver.find_element_by_xpath('//ul[@class="af-pagination "]')
    # get total number of relevant pages
    tot_pages = driver.find_element_by_xpath('//ul[@class="af-pagination "]'
      ).text.split("\n")[-1]
  # if not multiple pages, use the number 1 for url
  except NoSuchElementException:
    tot_pages = '1'

  try:
    # get posts from each 'Me at Work' page
    for page in np.arange(1, (int(tot_pages) + 1)):
      driver.get(f'https://www.artfinder.com/artist/{slug}/me-at-work/?page={page}#/')
      driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
      WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH,
        '//div[@class="scroll-to-top af-opacity"]')))

      # get post titles, texts, and dates
      WebDriverWait(driver, 10).until(
          EC.presence_of_element_located((By.XPATH, '//summary')))
      posts = driver.find_elements_by_xpath('//summary')
      posts = [post.text.split('\n') for post in posts]

      # if any text is missing, insert 'N/A'
      for post in posts:
        if len(post) == 2:
          post.insert(0, 'N/A')
        if len(post) == 1:
          post.insert(0, 'N/A')
          post.insert(1, 'N/A')
        try:
          driver.find_element_by_xpath(
            '//div[@class="af-card  af-video-text-card text-left margin margin-bottom margin-s"]')
          video.append(1)
        except:
          video.append(0)

        # add strings to storage outside loop
        titles.append(post[0])
        texts.append(post[1])
        dates.append(post[2])
        slugs.append(slug)
  except:
    pass

# add stored lists to dictionary
posts = {'is_video': video, 'post_title': titles, 'post_text': texts,
         'post_date': dates, 'slug': slugs}

# convert dictionary to df and export as .csv
df = pd.DataFrame.from_dict(posts, orient='index')
df_final = df.transpose()
df_final.to_csv('posts.csv', index=False, header=True, encoding='utf-8')

driver.quit()