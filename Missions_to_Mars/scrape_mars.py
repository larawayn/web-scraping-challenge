from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
   
    mars = {}

    # Connect to first URL
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    news_title = soup.find('div', class_="content_title").text

    news_p = soup.find('div', class_="rollover_description_inner").text

    mars['news_title'] = news_title
    mars['news_p'] = news_p

    # Connect to second URL
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2) 

    featured_image_url = 'https://d2pn8kiwq2w21t.cloudfront.net/images/jpegPIA24488.2e16d0ba.fill-400x400-c50.jpg'
    mars['featured_image_url'] = featured_image_url

    # Connect to third URL
    url3 = 'https://space-facts.com/mars/'
    browser.visit(url3)

    tables = pd.read_html(url3)
    mars_facts_df=tables[0]
    mars_facts_df2=mars_facts_df.rename(columns={ 1 :'Mars', 0 : ''})
    mars_facts_df2=mars_facts_df2.set_index('')
    mars_facts_html = mars_facts_df2.to_html()
    mars['mars_facts_html'] = mars_facts_html

    # Connect to fourth URL
    url4 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url3)
    hemisphere_image_urls = [
    {"title": "Valles Marineris Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/b3c7c6c9138f57b4756be9b9c43e3a48_valles_marineris_enhanced.tif_full.jpg"},
    {"title": "Cerberus Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/f5e372a36edfa389625da6d0cc25d905_cerberus_enhanced.tif_full.jpg"},
    {"title": "Schiaparelli Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/3778f7b43bbbc89d6e3cfabb3613ba93_schiaparelli_enhanced.tif_full.jpg"},
    {"title": "Syrtis Major Hemisphere", "img_url": "https://astrogeology.usgs.gov/cache/images/555e6403a6ddd7ba16ddb0e471cadcf7_syrtis_major_enhanced.tif_full.jpg"},]

    mars['hemisphere_image_urls'] = hemisphere_image_urls
    
    return mars





if __name__ == "__main__":
    app.run(debug=True)
