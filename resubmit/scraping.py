# Import Splinter, BeautifulSoup, and Pandas
from turtle import title
from matplotlib.pyplot import text
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

executable_path = {'executable_path': ChromeDriverManager().install()}


def scrape_all():

    # Set up Splinter
    browser = Browser('chrome', **executable_path, headless=False)

    news_title, news_paragraph = mars_news(browser)

    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemisphere_data": hemisphere_image(browser)
    }

    browser.quit()
    return data

# Mars News
def mars_news(browser):

    # Visit the Mars news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    try:
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        news_title = slide_elem.find("div", class_="content_title").get_text()
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()
    
    except AttributeError:
        return None, None
    
    return news_title, news_p
    
# ## JPL Space Images Featured Image
def featured_image(browser):

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
    
    return img_url


# ## Mars Facts
def mars_facts():

    df = pd.read_html('https://galaxyfacts-mars.com')[0]
    
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)
    
    mars_facts = df.to_html()

    return mars_facts     

# Mars Hemisphere 
def hemisphere_image(browser):
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    hemisphere_image_urls = []

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    hemisphere_soup = soup(html, 'html.parser')

    hemisphere_links = hemisphere_soup.find_all('h3')

    for hemisphere in hemisphere_links:
        img_page = browser.find_by_text(hemisphere.text)
        img_page.click()

        html = browser.html

        img_soup = soup(html, 'html.parser')
        
        # image
        img_url = 'https://astrogeology.usgs.gov/' + str(img_soup.find('img', ))

        # title
        title = img_soup.find('h2', class_='title').text

        # Dictionary
        hemisphere_mars = {
            "img_url": img_url, 
            "title": title
        }
        
        hemisphere_image_urls.append(hemisphere_mars)

        browser.back()

    return hemisphere_image_urls

if __name__ == "__main__":

# If running as script, print scraped data
    print(scrape_all())

