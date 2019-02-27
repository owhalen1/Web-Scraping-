
from bs4 import BeautifulSoup as bs
from splinter import Browser
from selenium import webdriver
import pandas as pd
import time
import pymongo
import requests


executable_path = {'executable_path' : 'C://Users//Owner//Documents//Data Science Bootcamp//Web Scraping HW//chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

# Initialize PyMongo to work with MongoDBs
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

#define database
db = client.mars
mars_collection = db.mars_collection

def get_data():
    # 1 Nasa news *** USING BROWSER = SPLINTER ***
    browser = Browser('chrome')
    url = "https://mars.nasa.gov/news/"
    #visit url
    browser.visit(url)
    # HTML object
    mars_html = browser.html
    # Parse HTML 
    soup = bs(mars_html, "html.parser")
    # Collect News Title and Paragraph
    news_title = soup.find("div", class_ = "content_title").text.strip()
    print(news_title)
    news_paragraph = soup.find('div', class_="article_teaser_body").text
    print(news_paragraph)

    # Close the browser after scraping
    browser.quit()

    #2- JPL Mars Space Images - Featured Image  
    browser = Browser('chrome')
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars)"
    #go to url
    browser.visit(image_url)
    #navigate to link
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)
    browser.click_link_by_partial_text('more info')
    image_html = browser.html
    image_soup = bs(image_html, "html.parser")
    image_path = image_soup.find('figure', class_='lede').a['href']
    featured_image_url = "https://www.jpl.nasa.gov/" + image_path
    print(featured_image_url)
    # Close  

    #3- Mars Weather
    browser = Browser('chrome')
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    weather_soup = bs(html, 'html.parser')
    mars_weather = weather_soup.find("p", class_ = "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text.strip()
    print(mars_weather)
    # Close 
    browser.quit()
    

    #5-Mars Hemispheres
    #create dictionaries
    hemisphere_img_urls = []
    hemisphere_dicts = {"title": [] , "img_url": []}
    # url
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser = Browser("chrome")
    browser.visit(url)
    home_page = browser.html
    #HTML & Parsing
    hemispheres_soup = bs(home_page, "html.parser")
    results = hemispheres_soup.find_all("h3")
    # Use loop
    for result in results:
        title = result.text
        print(title)
        #title 
        title = title[:-9]
        print(title)
        browser.click_link_by_partial_text(title)
        img_url = browser.find_link_by_partial_href("download")["href"]
        print(img_url)
        hemisphere_dicts = {"title": title, "img_url": img_url}
        hemisphere_img_urls.append(hemisphere_dicts)
        browser.visit(url)
    # Close 
    browser.quit()


    mars_data = {
        "title": title,
        "content": news_p,
        "featured_image_url": featured_image_url,
        "latest_weather": mars_weather,
        "image_data": hemisphere_img_urls,
    }
    existing = mars_collection.find_one()
    if existing:
        mars_data['_id'] = existing['_id']
        mars_collection.save(mars_data)
    else:
        mars_collection.save(mars_data)
    return mars_data


def get_from_db():
    return mars_collection.find_one()