from selenium import webdriver
import time
import re
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait

df = pd.read_csv("artists.csv", usecols=['slug']).drop_duplicates()
slugs = df['slug'].to_list()

driver = webdriver.Chrome()

slugss = []
joined_dates = []
nationality = []
products = []


for slug in slugs[6:10]:
	# Get to the artist's page
	print(slug)
	driver.get(f'https://www.artfinder.com/{slug}/sort-artist_order/page-1/#/')

	# Close the pop up for discount
	close_pop_up = driver.find_element_by_xpath('//div[@class="af-register-modal--b"]//a[@class="close"]')
	try:
		close_pop_up.click()
	except:
		pass	
	time.sleep(5)

	# Scroll till the end
	driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
	time.sleep(5)
	# Find two elements
	joined_artfinder = driver.find_element_by_xpath('//p[@class="af-small-text margin margin-none"]').text.split(": ")[1]
	country = driver.find_element_by_xpath('//p[@class="af-small-text"]').text

	# Find number of pages
	if driver.find_elements_by_xpath('//ul[@class="af-pagination margin margin-s margin-top"]') == []:
		prod_names = driver.find_elements_by_xpath('//div[@class="af-card af-card-product-variant af-show-element-on-hover"]/a')
		print(len(prod_names))
		for product in prod_names:
			prod = product.get_attribute('href').split('/')[-1]
			slugss.append(slug)
			joined_dates.append(joined_artfinder)
			nationality.append(country)
			products.append(prod)
	else:
		num_page = driver.find_element_by_xpath('//ul[@class="af-pagination margin margin-s margin-top"]').text.split("\n")[-1]
		# Iterate through the pages
		for page in range(1,int(num_page)+1):
			driver.get(f'https://www.artfinder.com/{slug}/sort-artist_order/page-{page}/#/')
			time.sleep(5)
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
			time.sleep(5)
			prod_names = driver.find_elements_by_xpath('//div[@class="af-card af-card-product-variant af-show-element-on-hover"]/a')
			print(len(prod_names))
			for product in prod_names:
				prod = product.get_attribute('href').split('/')[-1]
				slugss.append(slug)
				joined_dates.append(joined_artfinder)
				nationality.append(country)
				products.append(prod)

posts = {'slugss': slugss, 'joined_dates': joined_dates,
         'nationality': nationality, 'products': products}

# convert dictionary to df and export as .csv
df = pd.DataFrame.from_dict(posts, orient='index')
df_final = df.transpose()
df_final.to_csv('posts.csv', index=False, header=True, encoding='utf-8')

driver.quit()







