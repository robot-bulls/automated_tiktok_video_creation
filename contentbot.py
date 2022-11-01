from math import nan
import time
import random
from numpy import NaN
import numpy as np
import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib.request
# import cv2

from create_video.summary import summarize
from create_video.deepl import deepl
from create_video.keywords import keywords
from create_video.synthesia import create_synthesia
from create_video.synthesia import createWebhook
from create_video.synthesia import retrieveWebhook
from create_video.synthesia import retrieveVideo

from create_video.jumpcutter import jumpcutter
from create_video.edit_video import cropVideo
from create_video.edit_video import create_srt
from create_video.edit_video import getbackgroundvideos
from create_video.edit_video import addsubtitles
from create_video.edit_video import createVariations

from create_video.edittext import urlarray2text
from create_video.edittext import article2video
from create_video.edittext import get_page
from create_video.edittext import en
from create_video.edittext import de
from create_video.edittext import not_full_article
from create_video.edittext import cleanArticle
from create_video.edittext import remove_files
from create_video.telegram import send_msg
from create_video.upload_google_drive import upload_to_google_drive
from create_video.upload_google_drive import upload_variations

from urllib.request import Request, urlopen

from pytube import YouTube
import re
from pathlib import Path
import traceback
import sys
import os
import cv2
import ffmpeg
from newspaper import Article

import asyncio

# video_text = [ "The Russian president has signed a bill into law that prohibits the use of digital assets, such as cryptocurrency and NFTs, to pay for goods and services. In addition, the new law also requires crypto exchanges and providers to refuse transactions in which digital transfers can be interpreted as a form of payment. This means that people in Russia will soon no longer be able to use digital assets as a form of payment."]
# video_text = ["India is planning to tax any money made from cryptocurrencies at a rate as high as 50%. This comes as the government is trying to figure out how to regulate the new asset class. Many young investors are moving their businesses out of the country to places with more crypto-friendly policies. Follow the channel for the latest crypto news!", "OpenSea is the world's largest online marketplace for non-fungible tokens. The company has announced that it is cutting about 20% of its staff. This is the latest in a series of layoffs that have rocked the crypto industry as digital-asset prices continue to plummet.", "The Russian president has signed a bill into law that prohibits the use of digital assets, such as cryptocurrency and NFTs, to pay for goods and services. In addition, the new law also requires crypto exchanges and providers to refuse transactions in which digital transfers can be interpreted as a form of payment. This means that people in Russia will soon no longer be able to use digital assets as a form of payment."]
# video_text = ["Snapchat's stock is crashing after a dismal second-quarter earnings report and a brutal call, with one analyst explaining that the company is going through a 'near-death experience.'"]
video_text = []
# article_urls = ["https://www.dw.com/de/exit-scam-und-betrug-mit-cannabis-bei-juicyfields-stehen-tausende-anleger-vor-gesperrten-konten/a-62551560"]
article_urls = [[]]

language = "en"  # en, fr, de, it
video_type = "automated" #text, url, automated 
# max_numer_of_videos = [3, 3, 3, 3]  # only for automated videos | Crypto, Politics, News, Stock-Market"
max_numer_of_videos = [9, 9, 9, 9]
# max_numer_of_videos = [0, 0, 0, 0]

try:
    remove_files("raw_videos/")
    if video_type == "text":  # check if using local text
        print(" #1 --- Local TEXT")
        for i, summary in enumerate(video_text):
            article2video(i, summary, language)
        print("Finished")
        send_msg("Finished Generating "+str(len(video_text))+" Videos in "+ language+ " | Method #1")
    
    elif video_type == "url":  # check for handpicked urls
        print(" #2 --- Local URL")
        articles_array = urlarray2text(article_urls, language, max_numer_of_videos)

        for i, article in enumerate(articles_array):
            summary = summarize(article, language)
            print("summary: ", summary)
            article2video(i, summary, language)
        print("Finished")
        send_msg("Finished Generating "+str(len(articles_array))+" Videos in "+ language+ " | Method #2")
    
    elif video_type == "automated":
        print(" #3 --- NO Text or Url")
        # Get Article URLS    
        if language == "en":
            article_urls = asyncio.run(en())

        video_index_array = []
        articles_array = urlarray2text(article_urls, language, max_numer_of_videos)
        for topic_i,array in enumerate(articles_array):
            new_video_array = []
            for i, article in enumerate(array):
                print("article:", article)
                summary = summarize(article, language)
                print("summary: ", summary)
                new_video_index = article2video(topic_i, i, summary, language)
                #translate to fr
                summary_translated = deepl(summary, "fr")
                article2video(topic_i, i, summary_translated, "fr")
                if new_video_index == False:
                    break
                new_video_array.append(new_video_index)
            video_index_array.append(new_video_array)

        print("video_index_array:",video_index_array)
        createVariations(video_index_array, "en")
        createVariations(video_index_array, "fr")

        #Finished
        send_msg("Finished Generating "+str(len(articles_array))+" Videos in "+ language+ " | Method 3")
        print("article_urls:",article_urls)
        approve_results = input("Do want to save the URLs: ")
        if approve_results == "y" or approve_results == "Y" or approve_results == "yes" or approve_results == "Yes":
            with open("past_articles.txt", "a") as f:
                for i,array in enumerate(article_urls):
                    for y,url in enumerate(array):
                        if y >= (max_numer_of_videos[i]):
                            break
                        f.write("\n"+str(url))
        # Upload Videos
        print("video_index_array:",video_index_array)
        upload_videos = input("Do want to upload the videos: ")
        if upload_videos == "y" or upload_videos == "Y" or upload_videos == "yes" or upload_videos == "Yes":
            upload_to_google_drive(video_index_array, language)
            upload_variations(video_index_array, language)
        #Deleting Temp Files
        print("Deleting temp files")
        remove_files("raw_videos/")
        print("Finished")

except Exception as e:
    send_msg("An Error Occured: \n"+str(e))
    print(traceback.format_exc())
