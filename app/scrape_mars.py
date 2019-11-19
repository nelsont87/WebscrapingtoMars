from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt


def scrape_all():

    browser = Browser("chrome", executable_path="chromedriver", headless=False)
    slide_title, slide_body = mars_news(browser)

    data = {
        "news_title": slide_title,
        "news_paragraph": slide_body,
        "featured_image": featured_image(browser),
        "hemispheres": hemispheres(browser),
        "weather": twitter_weather(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }

    browser.quit()
    return data


def mars_news(browser):
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    slide_title = soup.find("div", class_="content_title").text
    slide_body = soup.find("div", class_="article_teaser_body").text

    return slide_title, slide_body


def featured_image(browser):
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    image_link = browser.find_by_id("full_image")
    featured_image_url = image_link["data-fancybox-href"]
    

    img_url = f"https://www.jpl.nasa.gov{featured_image_url}"

    return img_url


def hemispheres(browser):

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    img_urls = []

    links = browser.find_by_css("a.product-item h3")

    for i in range(len(links)):
        hemisphere = {}
        

        browser.find_by_css("a.product-item h3")[i].click()
        

        sample_elem = browser.find_link_by_text('Sample').first
        hemisphere['img_url'] = sample_elem['href']
        

        hemisphere['title'] = browser.find_by_css("h2.title").text
        

        img_urls.append(hemisphere)
        

        browser.back()

    return img_urls


def twitter_weather(browser):
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html_test = browser.html
    soup_test = BeautifulSoup(html_test, "html.parser")
    mars_weather = soup_test.find("p", {"class": "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"}).text

    return mars_weather



def mars_facts():

    df = pd.read_html("http://space-facts.com/mars/")[0]

    df.columns = ["description", "value"]
    df.set_index("description", inplace=True)

    return df.to_html(classes="table table-striped")


if __name__ == "__main__":


    print(scrape_all())
