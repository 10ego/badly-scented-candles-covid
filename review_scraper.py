import json
import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.headless = True
driver = webdriver.Chrome(options=options)

def get_review_url(product_url, page):
    url = re.search(r'.*\/dp\/\S{8,14}\/', product_url).group()
    review_url = url.replace('/dp/', '/product-reviews/')
    review_url += f"ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber={page}"
    return review_url

def parse_date(element):
    date = re.search(r'\w+ \d+, \d+', element.find_element(By.CSS_SELECTOR, '.a-size-base.a-color-secondary.review-date').text).group()
    datep = datetime.strptime(date, '%B %d, %Y').strftime('%Y-%m-%d')
    return datep

def get_reviews(product_url, page=1):
    global reviews_data
    url = get_review_url(product_url, page)
    driver.get(url)
    reviews = driver.find_elements(By.CSS_SELECTOR, '.a-section.review.aok-relative')
    for review in reviews:
        d = {}
        d['date'] = parse_date(review)
        last_date = d['date']
        d['title'] = review.find_element(By.CSS_SELECTOR, '.a-size-base.a-link-normal.review-title.a-color-base.review-title-content.a-text-bold').text
        d['stars'] = review.find_element(By.CSS_SELECTOR, 'a.a-link-normal').get_attribute("title")
        d['review'] = review.find_element(By.CSS_SELECTOR, '.a-size-base.review-text.review-text-content').text
        reviews_data.append(d)
    return last_date
    
url = input("Input the amazon product page url:")
last_date = get_reviews(url, 1)

reviews_data = []
c=0
while datetime.strptime(last_date, '%Y-%m-%d') >= datetime.strptime('2020-01-20', '%Y-%m-%d'):
    c+=1
    last_date = get_reviews(url, c)
    time.sleep(3)

filename = input("Define file name to save data:")
with open('data/{filename}', 'w+') as f:
    json.dump(reviews_data, f)
with open('data/{reviews_data_source.txt}', 'a+') as f:
    f.write(f'data/{filename} : {url}\n')