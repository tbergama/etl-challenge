from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pandas as pd

# How many times to try reading a tag from a page
MAX_TRIES = 100

def scrape():
    
    # Create dict to store scraped data
    data = []

    # Set up splinter
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=True)

    # ----- News Article -----

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    soup = BeautifulSoup(browser.html, "html.parser")
    first_article = soup.find('li', class_="slide")

    i = 0
    while first_article is None:
        if i > MAX_TRIES:
            break
        
        soup = BeautifulSoup(browser.html, "html.parser")
        first_article = soup.find('li', class_="slide")
    
    
    title = first_article.find('div', class_='content_title').text.strip()
    paragraph = first_article.find('div', class_='article_teaser_body').text.strip()

    data.append({
        'news_article': {
            "title": title,
        "paragraph": paragraph
        }   
    })
    
    # ------ JPL Image -----

    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    browser.click_link_by_partial_text("FULL IMAGE")
    
    soup = BeautifulSoup(browser.html, "html.parser")
    img_tag = soup.find("img", class_="fancybox-image")

    i = 0
    while img_tag is None:
        if i > MAX_TRIES:
            break
        
        soup = BeautifulSoup(browser.html, "html.parser")
        img_tag = soup.find("img", class_="fancybox-image")
        
    img_url = img_tag['src']

    data.append({
        "jpl_image": {
            "url": img_url   
        }
    })

    # ------ Weather ------

    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)

    soup = BeautifulSoup(browser.html, "html.parser")
    weather = soup.find("div", lang="en")

    i = 0
    while weather is None:
        if i > MAX_TRIES:
            break
        
        soup = BeautifulSoup(browser.html, "html.parser")
        weather = soup.find("div", lang="en")
    
    weather = weather.text

    data.append({
        "weather": {
            "text": weather
        }
    })

    # ----- Facts ------

    df_facts = pd.read_html("https://space-facts.com/mars/")[0]
    facts_html = df_facts.to_html()

    data.append({
        "facts": facts_html
    })

    # ------ Hemispheres ------

    hemi_dicts = [
        {
            "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg",
            "title": "Cerberus Hemisphere Enhanced"
        }, {
            "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg",
            "title": "Schiaparelli Hemisphere Enhanced"
        }, {
            "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg",
            "title": "Syrtis Major Hemisphere Enhanced"
        }, {
            "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg",
            "title": "Valles Marineris Hemisphere Enhanced"
        }
    ]

    data.append({
        "hemispheres": hemi_dicts
    })

    return data
