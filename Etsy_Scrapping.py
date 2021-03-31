
import re
from csv import writer
from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup as bs 
import os 
import pandas as pd
import sqlite3 as sql

browser = webdriver.Chrome(executable_path = "C:/Users/ssingh/Downloads/chromedriver")
def scrap():
    #scrapping 1 to 10 pages 
    for page in range(1,11):
        os.system("cls")
        print("we are in page {}".format(page))
        url = 'https://www.etsy.com/in-en/c/jewelry/earrings/ear-jackets-and-climbers?ref=pagination&page={}'.format(page)
        browser.get(url)
        sleep(2)
        for productscount in range(1,60):
            nproduct=browser.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/div[3]/div[2]/div[2]/div[2]/div/div/ul/li[{0}]/div/a/div[1]/div/div/div/div/div/img'.format(productscount))
            nproduct.click()
            sleep(2)
            windows = browser.window_handles
            for handle in windows[1:]:
                browser.switch_to.window(handle)
                html_source=browser.page_source
                bssoup=bs(html_source,'lxml')
                bssoup.encode("utf-8")
                reviews=bssoup.find_all('p',id=re.compile('^review-preview-toggle-\d+'))
                for rev in reviews:
                    text=[]
                    text.append(rev.getText())
                    with open('Etsyreviews1.csv', 'a') as f:
                        writer_object = writer(f) 
                        try:
                            writer_object.writerow(text) 
                        except UnicodeEncodeError:
                            pass
                        f.close()
                sleep(2)
                browser.close()
                browser.switch_to.window(windows[0])
            sleep(2)

scrap()

df = pd.read_csv('Etsy_Scrapped_Reviews.csv')
df.columns=['reviews']
conn = sql.connect('reviewsScrapped.db')
df.to_sql('reviewsScrappedTable', conn)


