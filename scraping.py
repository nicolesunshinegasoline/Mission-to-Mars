# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

# Set up Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


#        ___  ___  __   __       ___  ___           __        __   __   __   __  
# | |\ |  |  |__  / _` |__)  /\   |  |__      |\/| /  \ |\ | / _` /  \ |  \ |__) 
# | | \|  |  |___ \__> |  \ /~~\  |  |___     |  | \__/ | \| \__> \__/ |__/ |__)

#        ___  __     ___       ___          ___  __           __   __  
# | |\ |  |  /  \     |  |__| |__     |  | |__  |__)     /\  |__) |__) 
# | | \|  |  \__/     |  |  | |___    |/\| |___ |__)    /~~\ |    |    


def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True) 
    
    ##### headless was set as False so we could see the scraping in action.
    
    # set our news title and paragraph variables
        # note: the function will return two values
    # tell Python to use the mars_news function to pull this data.
    news_title, news_paragraph = mars_news(browser)
    
    
    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres_image_urls": mars_hemispheres(browser)
    }
    
    # Stop webdriver and return data
    browser.quit()
    return data


#             __   __           ___       __  
# |\/|  /\  |__) /__`    |\ | |__  |  | /__` 
# |  | /~~\ |  \ .__/    | \| |___ |/\| .__/ 


# add browser as argument to the function.
# since our scraping code utilizes and automated browser
def mars_news(browser): 
    # Visit the Mars news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    
    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    
    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        #slide_elem.find('div', class_='content_title')
        
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None
    
    # tell python the function is complete
    return news_title, news_p


#       ___          __   __        ___  __   ___  __  
# |__| |__   |\/| | /__` |__) |__| |__  |__) |__  /__` 
# |  | |___  |  | | .__/ |    |  | |___ |  \ |___ .__/ 


def mars_hemispheres(browser): 
    
    # Visit the hemispheres website
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    
    # Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # Write code to retrieve the image urls and titles for each hemisphere.
    # links = browser.find_by_css("a.product-item h3")
    links = browser.find_by_css(".product-item")
    links = pd.Series([i["href"] for i in links]).drop_duplicates().tolist()
    print(len(links))
    
    for i in range(len(links)):
        try:
            
            # create empty dictionary
            hemisphere = {}
            browser.visit(links[i])
    
            # find and click on each hemisphere link
            # browser.find_by_css('a.product-item h3')[i].click()

            # navigate to the full-resolution image page
                # find the 'Sample' image anchor tag and extract the href
            sample_element = browser.find_link_by_text('Sample').first
            hemisphere['img_url'] = sample_element['href']

            # get the hemisphere title
            hemisphere['title'] = browser.find_by_css("h2.title").text

            # append hemisphere object to list
            hemisphere_image_urls.append(hemisphere)

            # navigate back to the beginning to get the next hemisphere image
            browser.back()
        except:
            continue

        # tell python the function is complete
    return hemisphere_image_urls

#  ___  ___      ___       __   ___  __                   __   ___ 
# |__  |__   /\   |  |  | |__) |__  |  \    |  |\/|  /\  / _` |__  
# |    |___ /~~\  |  \__/ |  \ |___ |__/    |  |  | /~~\ \__> |___ 


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

    try:
        # find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None
    
    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url


#             __   __      ___       __  ___  __  
# |\/|  /\  |__) /__`    |__   /\  /  `  |  /__` 
# |  | /~~\ |  \ .__/    |    /~~\ \__,  |  .__/ 


def mars_facts():
    
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    # BaseException is raised when any of the built-in exceptions 
    # are encountered and it won't handle any user-defined exceptions.
    # Use it here because we're using Pandas' read_html() function to pull data
    # instead of scraping with BeautifulSoup and Splinte
        # BaseException is a general exception
        # often used to catch multiple types of errors
    except BaseException:
        return None
    
    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)
    
    # Convert dataframe into HTML format, add bootstrap
    return df.to_html()


if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())


