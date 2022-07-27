from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_extension(r'D:\Log\3.17.2_0.crx')
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get('https://www.google.co.in')
print("Page Title is : %s" %driver.title)
driver.quit()