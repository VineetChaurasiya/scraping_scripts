'''
This script uses Selenium, pytesseract and PIL libraries to login to a public website by solving captcha.  
Website to login to : https://esearchigr.maharashtra.gov.in/testingeSearch/Login.aspx
'''

from bs4 import BeautifulSoup
import requests
import urllib.request
from pytesseract import image_to_string 
from PIL import Image

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def get_captcha_text(location, size):
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'
    im = Image.open('screenshot.png') # uses PIL library to open image in memory

    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']


    im = im.crop((left, top, right, bottom)) # defines crop points
    im.save('screenshot.png')
    captcha_text = image_to_string(Image.open('screenshot.png'))
    return captcha_text

def login_to_website():
    url = 'https://esearchigr.maharashtra.gov.in/testingesearch/Login.aspx'
    driver = webdriver.Chrome(executable_path = "C:/Users/Vineet/Downloads/chromedriver_win32/chromedriver.exe")
    driver.get(url)
    driver.set_window_size(1120, 550)
    element = driver.find_element_by_xpath('//*[@id="form1"]/center/div[2]/div[3]/div[2]/div[2]/div/table/tbody/tr[3]/td[1]/img') # find part of the page you want image of
    location = element.location
    size = element.size
    driver.save_screenshot('screenshot.png')
    user_id = driver.find_element_by_xpath('//*[@id="txtUserid"]')
    user_id.clear()
    user_id.send_keys('user-id')
    password = driver.find_element_by_xpath('//*[@id="txtPswd"]')
    password.clear()
    password.send_keys('password')
    captcha = driver.find_element_by_xpath('//*[@id="txtcaptcha"]')
    captcha.clear()
    captcha_text = get_captcha_text(location, size)
    captcha.send_keys(captcha_text)
    driver.find_element_by_xpath('//*[@id="btnLogin"]').click()
  
      
login_to_website()
