from selenium import webdriver

driver = webdriver.Firefox(executable_path='C:\Program Files\geckodriver.exe')
driver.implicitly_wait(20)

driver.get('https://www.artfinder.com/artists-az/#/')

prod_names = driver.find_elements_by_xpath('').text

print(names)