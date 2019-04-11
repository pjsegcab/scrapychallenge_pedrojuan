import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector

import selenium
from selenium import webdriver 
from selenium.common.exceptions import TimeoutException

import os
from time import sleep


MAX_PAGE_NUM = 4 # Number of pages the website has (to be improved --> not to be hardcoded)

if os.path.exists('dropdowns.json'): # Delete previous results (comment if you want to append results)
    os.remove('dropdowns.json')
else:
    pass


class DropdownSpider(scrapy.Spider):
    name = 'dropdown'
    start_urls = [
     'https://www.drukzo.nl.joao.hlop.nl/python.php',
    ]


    def parse(self, response):

        self.driver = webdriver.Chrome(os.path.join(os.getcwd(), 'chromedriver')) # Allocate Chrome Driver
        self.driver.get(response.url) # Execute Chrome Driver
        self.driver.implicitly_wait(10) 

        page = 1 # Clicks counter

        while page <= MAX_PAGE_NUM: # Until it reaches the maximum number of dropdowns  
            
            try:
                submit_click = self.driver.find_element_by_xpath('/html/body/form/button') # Find Submit button 
                submit_click.click() # Click Submit button to show other dropdowns
                sleep(1)
                
            except NoSuchElementException:
                self.logger.info('No Button element found.') 

            page += 1 # Next click 

        selen_html = self.driver.page_source 
        hxs = Selector(text=selen_html) # Select from the website from Selenium output, not from the original one.
        
        drop = 1 # Dropdown counter

        while drop <= MAX_PAGE_NUM: # Until it reaches the maximum number of dropdowns
            for dropdown in hxs.xpath('.//select[@id]'): # For each ID

                if len(dropdown.xpath('./option/self::*/text()').getall()) == 1: # If there is just one option available 
                    dropdown = dropdown.xpath('./option/self::*/text()') # Assign the only option
                
                else: # If there are several options available
                    dropdown = dropdown.xpath('./option[@selected]/self::*/text()') # Choose the one with the "selected" label

                yield {'drop' + str(drop): dropdown.get()} # Outputs drop number and option chosen
                drop += 1 # Next dropdown


        self.driver.close()




