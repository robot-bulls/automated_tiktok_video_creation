import ffmpeg
import datetime
from moviepy.editor import VideoFileClip
import re
# from string import punctuation
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
import requests
from bs4 import BeautifulSoup
import urllib.request
from urllib.request import Request, urlopen
from pytube import YouTube 
import os
import random
from random import randrange
import traceback


def cropVideo(input, output):
    stream = ffmpeg.input(input)
    audio = stream.audio
    stream2 = ffmpeg.crop(stream, 656.25, 0, 607.5, 1080)
    out = ffmpeg.output(stream2, audio, output)
    out.run(overwrite_output=True)

def create_srt(video_text, topic_i, video_index, language):
    print("video_text: ", video_text)
    punctuation = "!#$%&(*+, -./:;<=>?@[\]^_{|~"
    clip = VideoFileClip("raw_videos/"+language+'/'+str(topic_i)+'/'+str(video_index)+".mp4")
    video_duration = clip.duration*60

    words_array = video_text.split()
    subtitles = [""]
    amount_sub = 0
    for i,word in enumerate(words_array):
        if any(p in word for p in punctuation) or (len(subtitles[0+amount_sub])+len(word)) >= 24:
            subtitles[0+amount_sub] = subtitles[0+amount_sub]+word+" "
            amount_sub += 1
            subtitles.append("")
            print("len = ",(len(subtitles[0+amount_sub])+len(word)) )
        elif not any(p in word for p in punctuation):
            subtitles[0+amount_sub] = subtitles[0+amount_sub]+word+" "
    subtitles = subtitles[:-1]


    print("subtitles = ", subtitles)

    for i,word_sequence in enumerate(subtitles):
        if i == 0:
            start_time = datetime.datetime(100,1,1,0,0,0)
            str_start_time = "00:00:00,000000"
        else:
            start_time = old_endtime
            str_start_time = str(start_time.time())

        time_add = (len(word_sequence.split()) * video_duration/len(words_array)/60)
        print("time_add = ",time_add)
        end_time = start_time + datetime.timedelta(0,time_add)
        print("end_time = ",end_time) 
        str_end_time = str(end_time.time())
        old_endtime = end_time
        str_end_time = str_end_time[:-3]
        str_start_time = str_start_time[:-3]

        str_start_time = str_start_time.replace(".", ",")
        str_end_time = str_end_time.replace(".", ",")

        with open("raw_videos/"+language+'/'+str(topic_i)+'/'+"subtitles"+str(video_index)+".srt", "a") as f:
            f.write(str(i+1))
            f.write("\n")
            f.write(str_start_time)
            f.write(" --> ")
            f.write(str_end_time)
            f.write("\n")
            f.write("{\\an8}"+word_sequence)
            f.write("\n")
            f.write("\n")

    return subtitles
        
def addsubtitles(topic_i, index, language):

    # generator = lambda txt: TextClip(txt, font='Arial', fontsize=50, color='white', stroke_color="black", stroke_width=2)
    # subs = [((0, 4), 'subs1'),
    #         ((4, 9), 'subs2'),
    #         ((9, 12), 'subs3'),
    #         ((12, 16), 'subs4')]

    # subtitles = SubtitlesClip("raw_videos/subtitles"+str(index)+".srt", generator)

    # video = VideoFileClip("raw_videos/"+str(index)+".mp4")
    # result = CompositeVideoClip([video, subtitles.set_pos(('center','bottom'))])

    # result.write_videofile("output.mp4", fps=video.fps, temp_audiofile="temp-audio.m4a", remove_temp=True, codec="libx264", audio_codec="aac")

    #stream = ffmpeg.input("raw_videos/"+str(index)+".mp4")
    # stream = ffmpeg.input("out.mp4")
    # stream2 = ffmpeg.filter(stream, "subtitles", "raw_videos/subtitles"+str(index)+".srt")
    # out = ffmpeg.output(stream2, "output.mp4")
    # out.run()

    #video = ffmpeg.input("raw_videos/"+str(index)+".mp4")

    current_names_in_path = os.listdir("videos/"+language+"/"+str(topic_i)+"/")
    print("mylist:",current_names_in_path)
    names_in_path = []
    for name in current_names_in_path:
        head, sep, tail = name.partition(".")
        names_in_path.append(head)
    names_in_path = sorted(names_in_path)
    names_in_path = [ x for x in names_in_path if "variation" not in x ]
    print("names_in_path:",names_in_path)
    print("names_in_path[-1]", names_in_path[-1])

    if names_in_path == [] or names_in_path == [""]: #if emty folder add -1 to array
        names_in_path.append("-1")
    end_video_index = int(names_in_path[-1])+1
    print("end_video_index:",end_video_index)

    video = ffmpeg.input("raw_videos/"+language+'/'+str(topic_i)+'/'+str(index)+".mp4")
    audio = video.audio
    # srt_index = index.split(".", 1)[0]
    stream = ffmpeg.concat(video.filter("subtitles", "raw_videos/"+language+'/'+str(topic_i)+'/'+"subtitles"+str(index)+".srt"), audio, v=1, a=1)
    out = ffmpeg.output(stream, "videos/"+language+'/'+str(topic_i)+"/"+str(end_video_index).zfill(4)+".mp4")
    out.run(overwrite_output=True)
    return end_video_index

def addsubtitles_variations(topic_i, video_index, video_name, language, variation_index):
    # current_names_in_path = os.listdir("videos/"+language+"/"+str(topic_i)+"/")
    # print("mylist:",current_names_in_path)
    # names_in_path = []
    # for name in current_names_in_path:
    #     head, sep, tail = name.partition(".")
    #     names_in_path.append(head)
    # names_in_path = sorted(names_in_path)
    # names_in_path = [ x for x in names_in_path if "variation" not in x ]
    # print("names_in_path:",names_in_path)
    # print("names_in_path[-1]", names_in_path[-1])

    # if names_in_path == [] or names_in_path == [""]: #if emty folder add -1 to array
    #     names_in_path.append("-1")
    # end_video_index = int(names_in_path[-1])+1
    # print("end_video_index:",end_video_index)

    video = ffmpeg.input("raw_videos/"+language+'/'+str(topic_i)+'/'+str(video_index)+".1.mp4")
    audio = video.audio
    # srt_index = video_index.split(".", 1)[0]
    stream = ffmpeg.concat(video.filter("subtitles", "raw_videos/"+language+'/'+str(topic_i)+'/'+"subtitles"+str(video_index)+".srt"), audio, v=1, a=1)
    out = ffmpeg.output(stream, "videos/"+language+'/'+str(topic_i)+"/variation_"+str(variation_index+1)+"/"+str(video_name).zfill(4)+".mp4")
    out.run(overwrite_output=True)
    # return end_video_index

def getbackgroundvideos(i, subtitles):
    for y,word_sequence in enumerate(subtitles):
            
        print("video: ",i," word_sequence: ",y)

        # --- search for keywords (subtitles)
        new_word_sequence = word_sequence.replace(' ', '+')
        search = new_word_sequence
        url = 'https://www.google.com/search'
        headers = {
            'Accept' : '*/*',
            'Accept-Language': 'en-US,en;q=0.5',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82',
        }
        parameters = {'q': search, 'tbm': 'vid'}
        content = requests.get(url, headers = headers, params = parameters).text
        soup = BeautifulSoup(content, 'html.parser')
        search = soup.find(id = 'search')
        # first_link = search.find('a')
        potential_video_links = search.find_all('a')
        for z,link in enumerate(potential_video_links):
            print("video: ",i,", word_sequence: ",y, ", url: ",z)
            page_url = link['href']
            print("page_url = ",page_url)

            #check if url contains https://
            if "https://" not in page_url or any(p in page_url for p in "{@}[]"):
                break

            # create  new directory
            dir = os.getcwd() + "/raw_videos/"+str(i)+"/"+str(y)+"/"
            if not os.path.exists(dir):
                os.makedirs(dir)

            if "youtube.com" in page_url: 
                print("Youtube Link")
                try:
                    YouTube(page_url).streams.filter(res="1080p").first().download(output_path='raw_videos/'+str(i)+'/'+str(y)+'/', filename='0.mp4')
                    break
                except:
                    print("Could not download Youtube video")
            else:
                content_video_page = requests.get(page_url, headers = headers).text
                soup_video_page = BeautifulSoup(content_video_page, 'html.parser')
                # search_video_page = soup_video_page.find(id = 'search')
                # video_url = search.find('video')
                try:
                    video_url = re.findall("https.*.mp4", soup_video_page.script.string)
                except:
                    pass
                # video_url = soup_video_page.find('source', type='video/mp4')
                # .select_one('source[type="video/mp4"]')["src"]
                    
                print("video_url",video_url)
                # if video_url is not None:
                if len(video_url) != 0:
                    if any(p in video_url[0] for p in "{@}[]"):
                        break
                    else:
                        urllib.request.urlretrieve(video_url[0], 'raw_videos/'+str(i)+'/'+str(y)+'/'+'0.mp4') 
                        print("video downloaded")
                        break

def createVariations(videos_array, language): 
    variations_videos_array = ["minecraft.mp4", "subwaysurfers.mp4", "gta.mp4"]
    for v, file_name in enumerate(variations_videos_array):
        variation_clip = VideoFileClip("variation_backgrounds/"+file_name)
        variation_clip_duration = variation_clip.duration
        print("variation_clip_duration",variation_clip_duration)
        for i,array in enumerate(videos_array):
            for vid_i,video_index in enumerate(array):
                print("video_index:",video_index,"vid_i:",vid_i)
                try:
                    original_video = VideoFileClip("raw_videos/"+language+'/'+str(i)+'/'+str(vid_i)+".mp4")
                    video_duration = original_video.duration
                    print("video_duration",video_duration)
                except Exception as e:
                    print(traceback.format_exc())
                # clip = VideoFileClip("variation_backgrounds/minecraft.mp4")
                clip = variation_clip
                start = random.randint(0, int(variation_clip_duration-200))
                print("start:",start)
                print("end:",start+video_duration)
                clip = clip.subclip(start, start+video_duration)
                # clip = clip.crop(x1=1166.6, y1=0, x2=2246.6, y2=1920)
                # clip = clip.crop(x1=0, y1=0, x2=1920, y2=1080)
                # clip = clip.resize(height=540)
                # clip = clip.resize(width=608)
                height=400
                clip = clip.resize(height=height)
                clip = clip.set_position((608/(1920/height)/2*-1, 1080-height))
                clip = clip.without_audio()
                original_video = original_video.set_position((0, -200))
                # clip.write_videofile("variation_backgrounds/temp/"+str(video_index)+".mp4")
                # final = CompositeVideoClip([clip, original_video])
                final = CompositeVideoClip([original_video,clip])
                final.write_videofile("raw_videos/"+language+"/"+str(i)+"/"+str(vid_i)+".1.mp4")
                addsubtitles_variations(i, vid_i, video_index, language, v)
        print("Finished Variation:"+str(v+1)+"/"+str(len(variations_videos_array)))

