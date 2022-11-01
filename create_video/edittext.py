from ast import While
from newspaper import Article
import time
import urllib.request
from urllib.request import Request, urlopen

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

# from create_video.summary import summarize
from create_video.synthesia import create_synthesia
from create_video.synthesia import createWebhook
from create_video.synthesia import retrieveWebhook
from create_video.synthesia import retrieveVideo

from create_video.jumpcutter import jumpcutter
from create_video.edit_video import cropVideo
from create_video.edit_video import create_srt
from create_video.edit_video import getbackgroundvideos
from create_video.edit_video import addsubtitles
import os

import asyncio
from pyppeteer import launch


def get_page(url):
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, verify=False, timeout=30)
    if not response.ok:
        print('Status code:', response.status_code)
        raise Exception('Failed to load page {}'.format(url))
    page_content = response.text
    doc = BeautifulSoup(page_content, 'html.parser')

    #with urllib.request.urlopen(url,headers={'User-Agent': 'Mozilla/5.0'}) as response:
    #    doc = response.read().decode('utf-8')

    # req = Request(url)
    # req.add_header('User-Agent', 'Mozilla/5.0')
    # doc = urlopen(req).read()

    # req = urllib.request.Request(url.format(0))
    # page = urllib.request.urlopen(req).read()
    # doc = BeautifulSoup(page,'lxml')

    return doc

def not_full_article(doc, BASE_URL):
    button_class = "link caas-button"  # continue reading buttun
    button = doc.find('a', {'class': button_class})
    if button is not None:
        # if the link doesnt have the base url
        if BASE_URL not in button['href']:
            return True
        else:
            return False
    else:
        return False

def cleanArticle(article, string):
    head, sep, tail = article.partition(string)
    return head

def isfloat(inputString):
    return any(char.isdigit() for char in inputString)

def remove_files(f):
    if os.path.isfile(f):
        os.unlink(f)
    elif os.path.isdir(f):
        for fi in os.listdir(f):
            remove_files(os.path.join(f, fi))

#returns urls array
async def en():
    BASE_URL = 'https://finance.yahoo.com'
    page_list = ["/topic/crypto", "/live/politics", "/news", "/topic/stock-market-news"]
    yahoo_urls = []
    for page in page_list:
        yahoo_urls.append(BASE_URL+page)
    allowed_authors = ["Yahoo Finance", "SmartAsset", "MoneyWise", "Engadget", "Fortune", "Reuters", "MoneyWise", "TipRanks", "USA TODAY"]
    article_urls = []

    #Get Past Articles
    past_articles = []
    with open('past_articles.txt', 'r') as fd:
        reader = fd.read()
        l = reader.split()
        for row in l:
            past_articles.append(row)
    print("past_articles:", past_articles)

    browser = await launch()
    page = await browser.newPage()
    
    for i,url in enumerate(yahoo_urls):
        print("--"+str(i)+"--")
        await page.goto(url)
        # await page.screenshot({'path': 'example.png'})
        print("Allowing Cookies")
        try:
            await page.click("#consent-page > div > div > div > form > div.wizard-body > div.actions.couple > button.btn.secondary.accept-all.consent_reject_all_2")
            await page.waitFor(5000)
        except:
            pass
        print("Scroll down")
        i = 0
        while i < 70:
            print(i)
            try:
                await page.evaluate('''(i) => {
                    let article_element = document.getElementsByClassName("Ov(h) Pend(44px) Pstart(25px)")[(i+1)]
                    article_element.scrollIntoView();
                }''',i)
                # await page.waitFor(500)
                await page.waitForSelector("#Fin-Stream > ul > li:nth-child("+(i+1)+") > div > div > div.Ov\(h\).Pend\(44px\).Pstart\(25px\)")
            except:
                pass
            i += 1
        # await page.evaluate('''
        #     article_element = document.getElementsByClassName("Ov(h) Pend(44px) Pstart(25px)")[19]
        #     article_element.scrollIntoView();
        # ''')
        # await page.waitFor(1000)
        # await page.screenshot({'path': 'example2.png'})

        current_urls = await page.evaluate('''(allowed_authors, article_urls, BASE_URL) => {
            article_elements = document.getElementsByClassName("Ov(h) Pend(44px) Pstart(25px)");
            console.log("docs: ", article_elements)
            let urls = []
            for (let i = 0; i < article_elements.length; i++) {
                let article_source = document.getElementsByClassName("Ov(h) Pend(44px) Pstart(25px)")[i].getElementsByClassName("Fz(11px)")[0].querySelector("span").textContent;
                console.log("article_source: ", article_source)

                if (allowed_authors.includes(article_source)) {
                    let article_url = document.getElementsByClassName("Ov(h) Pend(44px) Pstart(25px)")[i].querySelector("a").getAttribute("href");
                    urls.push(BASE_URL+article_url);
                }
            }
            return urls
            }''',allowed_authors, article_urls, BASE_URL)

        print("current_urls:",current_urls)
        current_urls = [i for i in current_urls if i not in past_articles]
        print("current_urls EDITED:",current_urls)
        # article_urls = article_urls+current_urls
        article_urls.append(current_urls)

    print("avaialbe videos:",len(article_urls[0]),len(article_urls[1]),len(article_urls[2]),len(article_urls[3]))
    # print("article_urls:",article_urls)
    await browser.close()
    return article_urls

async def de():
    pass

#returns cleaned articles array
def urlarray2text_old(article_urls, language, max_numer_of_videos):
    # article_array = []
    # for url in article_urls:
    #     article = Article(url)
    #     article.download()
    #     article.parse()
    #     article.nlp()
    #     article_array.append(article.text)

    if language == "en":
        articles_array = []
        for i,array in enumerate(article_urls):
            # print("array",array)
            print("Current Topic:",i)
            current_array = []
            for url in array:
                if len(current_array) >= (max_numer_of_videos[i]):
                    break
                print("url",url)
                article = Article(url)
                article.download()
                article.parse()
                article.nlp()
                article = article.text
                red_flags_array = ["This article provides information only and ", "©iStock.com", "For More Details: www.myzooverse.com", "Read more:", "Read the original post on", "This article is excerpted from", "See also:", "This content is not available due", "Update your settings", "Yahoo Finance. Follow ", "Click here for the latest", "Read the latest financial", "Download the Yahoo Finance app", "Follow Yahoo Finance on"]
                delete_string = ["Story continues"]
                for remove_text in red_flags_array:
                    try:
                        article = cleanArticle(article, remove_text)
                    except:
                        pass
                for remove_text in delete_string:
                    try:
                        article = article.replace(remove_text, "")
                    except:
                        pass

                article = article.rstrip()
                current_array.append(article)
            articles_array.append(current_array)

    if language == "de":
        articles_array = []
        for url in article_urls:
            article = Article(url)
            article.download()
            article.parse()
            article.nlp()
            article = article.text
            red_flags_array = ["Bildquellen:", "Redaktion finanzen", "Olga Rogler"]
            for remove_text in red_flags_array:
                try:
                    article = cleanArticle(article, remove_text)
                except:
                    pass
            article = article.rstrip()
            articles_array.append(article)

    # print("articles_array:", articles_array)
    print("Current Articles length:", len(articles_array[0]), len(articles_array[1]), len(articles_array[2]), len(articles_array[3]))
    return articles_array

def urlarray2text(article_urls, language, max_numer_of_videos):
    if language == "en":
        red_flags_array = ["This article provides information only and ", "©iStock.com", "For More Details: www.myzooverse.com", "Read more:", "Read the original post on", "This article is excerpted from", "See also:", "This content is not available due", "Update your settings", "Yahoo Finance. Follow ", "Click here for the latest", "Read the latest financial", "Download the Yahoo Finance app", "Follow Yahoo Finance on","is a writer and producer for Yahoo Finance in Washington", "reporter for Yahoo Finance.", "With additional reporting by", "Got a tip? Email", "Click here for", "sign up for", "the latest stock market news and in-depth analysis", "This story was originally featured on", "Reporting by"]
        articles_array = []
        for i,array in enumerate(article_urls):
            print("Current Topic:",i)
            current_array = []
            for url in array:
                print("len(current_array):",str(len(current_array)),"max_numer_of_videos[i]:",str(i))
                if len(current_array) >= (max_numer_of_videos[i]):
                    break
                print("url",url)

                # article = get_content_from_article(url)

                article_body_class = "caas-body"
                response = requests.get(url, headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari/537.36"})
                if not response.ok:
                    print('Status code:', response.status_code)
                    raise Exception('Failed to load page {}'.format(url))
                page_content = response.text
                doc = BeautifulSoup(page_content, 'html.parser')
                removals = doc.find_all('figure', {'class':'caas-figure'})
                for match in removals:
                    match.decompose()
                removals = doc.find_all('div', {'class':'caas-readmore'})
                for match in removals:
                    match.decompose()
                removals = doc.find_all('div', {'class':'caas-3p-blocked'})
                for match in removals:
                    match.decompose()
                article = doc.find('div', {'class': article_body_class})
                for elem in article.find_all(["a"]):
                        elem.replace_with(elem.text)
                for elem in article.find_all(["p"]):
                        elem.replace_with(elem.text, "")
                article = article.get_text(separator="\n")
                article = cleanArticle(article, "Read the latest financial")
                article_array = article.split('\n')
                for y,sentence in enumerate(article_array):
                    for red_flag_word in red_flags_array:
                        if red_flag_word in sentence:
                            article_array.pop(y)
                article = '\n'.join(article_array)
                article = article.rstrip('\n')
                article = article.rstrip('—')
                article = article.rstrip('\n')
                print("\n\n--------\n\narticle:",article)


                # article = article.rstrip()
                current_array.append(article)
            articles_array.append(current_array)

    if language == "de":
        articles_array = []
        for url in article_urls:
            article = Article(url)
            article.download()
            article.parse()
            article.nlp()
            article = article.text
            red_flags_array = ["Bildquellen:", "Redaktion finanzen", "Olga Rogler"]
            for remove_text in red_flags_array:
                try:
                    article = cleanArticle(article, remove_text)
                except:
                    pass
            article = article.rstrip()
            articles_array.append(article)

    # print("articles_array:", articles_array)
    print("Current Articles length:", len(articles_array[0]), len(articles_array[1]), len(articles_array[2]), len(articles_array[3]))
    return articles_array


def article2video(topic_i, i, video_text, language):
    video_id = create_synthesia(video_text, language)

    if video_id is not False:
        starttime = time.time()
        retrieveVideobool = False
        while retrieveVideobool == False:
            print("Requesting Video")
            status = retrieveVideo(video_id)
            if status.json()['status'] == "complete":
                retrieveVideobool = True
                print("video processed")
            time.sleep(60.0 - ((time.time() - starttime) % 60.0))

        print("download url", status.json()['download'])

        urllib.request.urlretrieve(
            status.json()['download'], 'raw_videos/'+language+'/'+str(topic_i)+'/'+str(i)+'.mp4')
        print("video downloaded")

        cropVideo('raw_videos/'+language+'/'+str(topic_i)+'/'+str(i)+'.mp4', 'raw_videos/'+language+'/'+str(topic_i)+'/'+str(i)+'.'+str(i)+'.mp4')
        jumpcutter('raw_videos/'+language+'/'+str(topic_i)+'/'+str(i)+'.'+str(i)+'.mp4', 'raw_videos/'+language+'/'+str(topic_i)+'/'+str(i)+'.mp4')
        subtitles = create_srt(video_text, topic_i, i, language)
        # getbackgroundvideos(i, subtitles)
        new_video_index = addsubtitles(topic_i, i, language)
        print("Video "+str(i)+" Finished")
        return new_video_index
    else:
        return False
