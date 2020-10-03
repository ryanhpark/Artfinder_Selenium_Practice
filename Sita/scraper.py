from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import numpy as np
# from collections import defaultdict
import pandas as pd

# get a list of all slugs
artists = pd.read_csv("../artists.csv", usecols=['slug']).drop_duplicates()
slugs = artists.slug.to_list()

# establish driver
driver = webdriver.Firefox(executable_path='C:\Program Files\geckodriver.exe')

# store strings from each page for each artist
titles = []
texts = []
dates = []
slugs = []

for slug in slugs[0:4]:
  print(f'https://www.artfinder.com/artist/{slug}/me-at-work/#/')
  # open webpage
  driver.get(f'https://www.artfinder.com/artist/{slug}/me-at-work/#/')
  time.sleep(2)

  # close pop-up
  close_pop_up = driver.find_element_by_xpath('//div[@class="af-register-modal--b"]//a[@class="close"]')
  try:
    close_pop_up.click()
    time.sleep(2)
  except:
    print('No pop-up')

  # scroll to bottom to access all HTML elements
  driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

  # check for multiple pages
  try:
    # if there are multiple pages
    driver.find_element_by_xpath('//ul[@class="af-pagination "]')
    # get total number of relevant pages
    tot_pages = driver.find_element_by_xpath('//ul[@class="af-pagination "]').text[-1]
  # if not multiple pages, use the number 1 for url
  except NoSuchElementException:
    tot_pages = '1'

  print(tot_pages)
  driver.close()

  # get posts from each 'Me at Work' page
  for page in np.arange(1, (int(tot_pages) + 1)):
    driver.get(f'https://www.artfinder.com/artist/{slug}/me-at-work/?page={page}#/')
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # get post titles, texts, and dates
    posts = driver.find_elements_by_xpath('//summary')
    posts = [post.text.split('\n') for post in posts]

    print(posts)

    # if text is missing, insert 'N/A' string where text should be
    for post in posts:
      if len(post) == 2:
        post.insert(1, 'N/A')
      # add strings to storage outside loop
      titles.append(post[0])
      texts.append(post[1])
      dates.append(post[2])
      slugs.append(slug)

      print(titles)
      print(texts)
      print(dates)
      print(slugs)

    driver.close()

# add stored lists to dictionary
posts = {'post_title': titles, 'post_text': texts,
         'post_date': dates, 'slug': slugs}

print(posts)

# convert dictionary to df and export as .csv
df = pd.DataFrame.from_dict(posts, orient='index')
df_final = df.transpose()
df_final.to_csv('posts.csv', index=False, header=True, encoding='utf-8')

driver.quit()