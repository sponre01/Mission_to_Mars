from splinter import Browser
from bs4 import BeautifulSoup
import requests

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)



def scrape():

    browser = init_browser()

# Nasa Mars News

    # URL of page to be scraped
    url_news = 'https://mars.nasa.gov/news/'
    browser.visit(url_news)
    # Parse HTML with Beautiful Soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # Save the results
    headline = soup.find('div', class_='content_title').find('a').text
    blurb = soup.find('div', class_='rollover_description_inner').text

# JPL Mars Space Images - Featured Image

    # URL of page to be scraped
    url_images = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_images)
    # Parse HTML with Beautiful Soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # Save results
    featured_image = soup.find('a', class_='button fancybox')['data-fancybox-href']
    featured_image_url = 'https://www.jpl.nasa.gov' + featured_image

# Mars Weather

    # URL of page to be scraped
    url_weather = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_weather)
    # Parse HTML with Beautiful Soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # Save Results
    all_weather = soup.find_all('div', class_='js-tweet-text-container')
    for tweet in all_weather: 
        if tweet.text.strip().startswith('InSight'):
            mars_weather=tweet.text.strip()
            break

# Mars Facts

    # URL of page to be scraped
    url_facts = 'https://space-facts.com/mars/'
    browser.visit(url_facts)
    # Use pandas to convert to HTML string
    html = browser.html
    facts = pd.read_html(url_facts)

# Mars Hemispheres

    # URL of page to be scraped
    url_hemispheres = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_hemispheres)
    hemispheres = []

    for x in range(0,4):
    
        # URL of page to be scraped
        hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(hemisphere_url)
    
        #Find and save titles
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        hemisphere_title = soup.find_all('h3')[x].text
    
        # Find and save image urls
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        browser.find_link_by_partial_text('Hemisphere')[x].click()
    
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        block = soup.find_all(class_='downloads')

        for link in block:
            hemisphere_img = link.find('a')['href']
        
        hemispheres.append({'title':hemisphere_title,'img_url':hemisphere_img})

    # Store data in a dictionary
    mars_data = {
        "mars_headline": headline,
        "mars_blurb": blurb, 
        "mars_featured_image": featured_image_url,
        "mars_weather": mars_weather,
        "hemisphere_info": hemispheres
        }

    # Close the browser after scraping
    browser.quit()

    return mars_data