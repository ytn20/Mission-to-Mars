# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

def scrape_all():

    scrape_data = {} 

    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit the Mars news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    slide_elem = news_soup.select_one('div.list_text')

    slide_elem.find('div', class_='content_title')

    # Use the parent element to find the first a tag and save it as `news_title`
    news_title = slide_elem.find('div', class_='content_title').get_text()
    

    # Use the parent element to find the paragraph text
    news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    

    scrape_data["news_title"] = news_title
    scrape_data["news_paragraph"] = news_p
    

    # ## JPL Space Images Featured Image

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # find the relative image url
    img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    

    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    

    scrape_data["feature_image"] = img_url


    # ## Mars Facts

    df = pd.read_html('https://galaxyfacts-mars.com')[0]
    

    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)
    

    mars_facts = df.to_html()

    scrape_data["facts"] = mars_facts

    browser.quit()

    return scrape_data

if __name__ == "__main__":

# If running as script, print scraped data
    print(scrape_all())

