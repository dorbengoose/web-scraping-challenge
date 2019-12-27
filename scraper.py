# ## Mission To Mars

# Import All Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import time
import config


def scrape():
#Scraping for All Data
# ### NASA Mars News
    executable_path = {"executable_path": "chromedriver"}
    browser = Browser('chrome', **executable_path, headless=False)
    url_news = 'https://mars.nasa.gov/news/'
    browser.visit(url_news)

    html_news = browser.html
    soup_news = BeautifulSoup(html_news, 'html.parser')

    News_header = (soup_news.find('div', class_='content_title')).string
    News_article = (soup_news.find('div', class_='article_teaser_body')).string

    # ### JPL Mars Space Images - Featured Image

    url_feat = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_feat)
    browser.find_by_css('a.button').click()
    time.sleep(10)
    soup = BeautifulSoup(browser.html,'html.parser')
    end = soup.find('img',class_='fancybox-image')['src']
    JPL_image = "https://www.jpl.nasa.gov"+end

    # ### Mars Weather

    marsweatertw = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(marsweatertw)
    marsweatherws = browser.html
    soup = BeautifulSoup(marsweatherws, 'html.parser')
    marsweather = soup.find('p', class_= 'TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
    print(f"The recent weather in Mars is as follows: {marsweather}")

    # ### Mars Facts

    url_facts = "https://space-facts.com/mars/"
    tables = pd.read_html(url_facts)[0]
    table_build = tables.to_html()

    # ### Mars Hemisphers
    url_hemi = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_hemi)
    soup = BeautifulSoup(browser.html, 'html.parser')

    headers=[]
    titles = soup.find_all('h3')
    for title in titles:
        headers.append(title.text)

    images=[]
    count=0
    for thumb in headers:
        browser.find_by_css('img.thumb')[count].click()
        images.append(browser.find_by_text('Sample')['href'])
        browser.back()
        count=count+1

    hemisphere_image_urls = []
    counter = 0
    for item in images:
        hemisphere_image_urls.append({"title":headers[counter],"img_url":images[counter]})
        counter = counter+1

    data = {"News_Header":News_header,"News_Article":News_article,"JPL_Image":JPL_image,"Weather":marsweather,"Facts":table_build,"Hemispheres":hemisphere_image_urls}

    return data
# scrape()