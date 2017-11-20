
# coding: utf-8

# In[6]:


import sys
import signal
from time import sleep
import random
import csv

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys


def sigint(signal, frame):
    sys.exit(0)

class Scraper(object):
    def __init__(self):
        self.url = 'http://registration.telangana.gov.in/ts/UnitRateMV.do?method=getDistrictList&uType=U'
        self.driver = webdriver.Chrome(executable_path = "C:/Users/Vineet/Downloads/chromedriver_win32/chromedriver.exe")
        self.driver.set_window_size(1120, 550)

    #--- DISTRICT-----------------------------------------------------
    def get_district_select(self):
        path = '//select[@id="districtCode"]'
        district_select_elem = self.driver.find_element_by_xpath(path)
        district_select = Select(district_select_elem)
        return district_select

    def select_district_option(self, value, dowait=True):
        '''
        Select district value from dropdown. Wait until mandal dropdown
        has loaded before returning.

        path = '//select[@id="mandalCode"]'
        mandal_select_elem = self.driver.find_element_by_xpath(path)

        def mandal_select_updated(driver):
            try:
                mandal_select_elem.text
            except StaleElementReferenceException:
                return True
            except:
                pass

            return False
        '''
        district_select = self.get_district_select()
        district_select.select_by_value(value)

        if dowait:
            wait = WebDriverWait(self.driver, 10)
            #wait.until(mandal_select_updated)

        return self.get_district_select()

    #--- MANDAL --------------------------------------------------
    def get_mandal_select(self):
        path = '//select[@id="mandalCode"]'
        mandal_select_elem = self.driver.find_element_by_xpath(path)
        mandal_select = Select(mandal_select_elem)
        return mandal_select

    def select_mandal_option(self, value, dowait=True):
        '''
        Select mandal value from dropdown. Wait until village dropdown
        has loaded before returning.
        
        path = '//select[@id="villageCode"]'
        vllage_select_elem = self.driver.find_element_by_xpath(path)

        def mandal_select_updated(driver):
            try:
                village_select_elem.text
            except StaleElementReferenceException:
                return True
            except:
                pass

            return False
        '''
        mandal_select = self.get_mandal_select()
        mandal_select.select_by_value(value)

        if dowait:
            wait = WebDriverWait(self.driver, 10)
            #wait.until(village_select_updated)

        return self.get_mandal_select()

    #--- VILLAGE ---------------------------------------------------
    def get_village_select(self):
        path = '//select[@id="villageCode"]'
        village_select_elem = self.driver.find_element_by_xpath(path)
        village_select = Select(village_select_elem)
        return village_select

    def select_village_option(self, value, dowait=True):
        village_select = self.get_village_select()
        village_select.select_by_value(value)
        return self.get_village_select()

    def load_page(self):
        self.driver.get(self.url)
        #self.driver.refresh()
        path = '//*[@id="rate1"]'
        def page_loaded(driver):
            return driver.find_element_by_xpath(path)

        wait = WebDriverWait(self.driver, 10)
        wait.until(page_loaded) 
        self.driver.find_element_by_xpath(path).click()
        
    def scrape(self):
        def districts():
            district_select = self.get_district_select()
            district_select_option_values = [ 
                '%s' % o.get_attribute('value') 
                for o 
                in district_select.options[1:2]
            ]

            for v in district_select_option_values:
                district_select = self.select_district_option(v)
                yield district_select.first_selected_option.text

        def mandals():
            mandal_select = self.get_mandal_select()
            mandal_select_option_values = [ 
                '%s' % o.get_attribute('value') 
                for o 
                in mandal_select.options[1:2]
            ]

            for v in mandal_select_option_values:
                mandal_select = self.select_mandal_option(v)
                yield mandal_select.first_selected_option.text
            
        def villages():
            village_select = self.get_village_select()
            try:
                village_select_option_values = [ 
                    '%s' % o.get_attribute('value') 
                    for o 
                    in village_select.options[1:]
                ]

                for v in village_select_option_values:
                    village_select = self.select_village_option(v)
                    yield village_select.first_selected_option.text
            except:
                pass
        self.load_page()
        for district in districts():
                
            print (district)
            for mandal in mandals():
                print (2*' ', mandal)
                for village in villages():
                    data = {}
                    print (4*' ', village)
                    main_window = self.driver.current_window_handle
        
                    submit_link = self.driver.find_element_by_name('submit')
                    submit_link.send_keys(Keys.SHIFT + Keys.RETURN)
                    #self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)
                    windows = self.driver.window_handles
                    self.driver.switch_to.window(windows[1])

                    
                    #sleep(random.randint(1,5))
                    
                    try:
                        data['district'] = self.driver.find_element_by_xpath('//*[@id="Table8"]/tbody/tr[1]/td[2]').text.strip()
                        data['Mandal'] = self.driver.find_element_by_xpath('//*[@id="Table8"]/tbody/tr[1]/td[4]').text.strip()
                        data['Village'] = self.driver.find_element_by_xpath('//*[@id="Table8"]/tbody/tr[2]/td[2]').text.strip()
                        data['Locality'] = self.driver.find_element_by_xpath('//*[@id="Table8"]/tbody/tr[3]/td[3]/b').text.strip()
                        data['Ward-Block'] = self.driver.find_element_by_xpath('//*[@id="Table8"]/tbody/tr[3]/td[2]').text.strip()
                        data['Land_Rate'] = self.driver.find_element_by_xpath('//*[@id="Table8"]/tbody/tr[3]/td[4]/b').text.strip()
                        data['Composite_Rate_Ground Floor'] = self.driver.find_element_by_xpath('//*[@id="Table8"]/tbody/tr[3]/td[5]/b').text.strip()
                        data['Composite_Rate_First_Floor'] = self.driver.find_element_by_xpath('//*[@id="Table8"]/tbody/tr[3]/td[6]/b').text.strip()
                        data['Composite_Rate_Other_Floors'] = self.driver.find_element_by_xpath('//*[@id="Table8"]/tbody/tr[3]/td[7]/b').text.strip()
                        data['Classification'] = self.driver.find_element_by_xpath('//*[@id="Table8"]/tbody/tr[3]/td[8]/b').text.strip()
                        data['Effective_Date'] = self.driver.find_element_by_xpath('//*[@id="Table8"]/tbody/tr[3]/td[9]/b').text.strip()
                    #data['Ward-Block'] = self.driver.find_element_by_xpath('//*[@id="Table8"]/tbody/tr[3]/td[3]/b').text
                    except:
                        pass
                    Data.append(data)
                    
                    self.driver.close()
                    #self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')
                    self.driver.switch_to_window(main_window)
                    
if __name__ == '__main__':
    signal.signal(signal.SIGINT, sigint)
    Data = []
    scraper = Scraper()
    scraper.scrape()


# In[151]:


import pandas as pd
df = pd.DataFrame(Data)


# In[152]:


df.to_excel('land_data2.xlsx')

