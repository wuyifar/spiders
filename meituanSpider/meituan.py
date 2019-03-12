from selenium import webdriver
import time



driver = webdriver.Chrome('chromedriver.exe')
driver.get('http://waimai.meituan.com/')
cookies = {'name':'JSESSIONID', 'value':'60C376C8C9903DA59BFFDA1EBF3CB307'}
driver.add_cookie(cookie_dict = cookies)
# driver.add_cookie({'name':'w_uuid', 'value':'gsOtwShEgVmMaqtr9AHLRJUAdnOAtmMSbuI9UUXJpjBeVR-Pbt2QpKYVKHdKK1ck'})
# driver.add_cookie({'name':'w_utmz', 'value':'utm_campaign=(direct)&utm_source=(direct)&utm_medium=(none)&utm_content=(none)&utm_term=(none)'})

driver.get('http://waimai.meituan.com/')
time.sleep(5)
# driver.get('http://waimai.meituan.com/new/waimaiIndex/?stay=1')
# text_input = driver.find_element_by_id('searchKeywords')
# text_input.click()
# time.sleep(1)
# text_input.send_keys('兴义市兴义民族师范学院')
# search_btn = driver.find_element_by_id('search').click()
# time.sleep(1)
# temporary_btn = driver.find_element_by_id("map")
# time.sleep(5)
