# Automated Tiktok video creation
This tool can be used for automated tiktok video creation, automated youtube shorts creation and automated instagram reels creation.

The default settings allow you to create content for the following topics:
+ crypto
+ politics
+ general news
+ stock market news

You can change the topic of the video very easily (you can find a detailed explanation in the setup guide)


# Examples:
https://user-images.githubusercontent.com/108469512/199299482-2e469dda-fd37-4757-9383-18189167390c.mov

https://user-images.githubusercontent.com/108469512/199299646-7dc59e4b-9dc8-4983-9d46-58e14750d27d.mov

see all examples here

# Explanation:
This tools goes to finance.yahoo.com and searches for articles about crypto, politics, general news and about the stock market. It uses open ai's GPT-3 to summarize the articles and synthesia to make a robot read the summary. It then edits the video by changing the format, removing the silences, adding subtitles and more.

It then gives the user the possibility to create variations of the videos that he wants. As of now there are 3 different types of variations. It would be very though to add more.

Example of a variation:

https://user-images.githubusercontent.com/108469512/199299736-e6d567bb-5000-483e-bdbf-7b4fa475b068.mov

In the end you have the possibility to translate the videos and then to upload them automatically to your google drive.

# Requirements:
+ python3
+ gpt-3 (for summarization) (sign up here: https://openai.com/api/)
+ sythesia (to sync the text with the face)

# Optional:
+ Google Drive (for automatic uploads to your google drive)
+ telegram (for notifications on success or error)
+ deepl (for translation to different languages)

FOR ANY UPDATES OR CHANGES FEEL FREE TO MAKE A NEW PULL REQUEST AND UPLOAD YOUR CODE!!!

# Setup:
1. install the requirements in the requirements.txt file
```pip3 install -r /path/to/requirements.txt```

2. Add your api keys in the following files:
+ create_video/summary.py
+ create_video/synthesia.py

Optionally in the following files:
+ create_video/telegram.py
+ create_video/upload_google_drive.py
+ create_video/deepl.py

If you don't want to use the optional features, you have to comment out the corresponding section in the main contentbot.py file. Just press ctrl+f and search for "telegram, google, deepl" and comment out the corresponding section.

3. If you want to change the topics of the videos go to "create_video/edittext.py" and seach for the function "async def en():". Here you can edit the source of the article you want to summarize.

Choose a source online for articles that you like. Then edit the according links and selectors in the function.

You are good to go. If there are any questions feel free to ask in the issues tab. And for any suggestions hit me up in the pull requests.

More Examples:

https://user-images.githubusercontent.com/108469512/199300680-5f4cc734-c3f2-469a-94b0-7fb0392d237c.mov

https://user-images.githubusercontent.com/108469512/199300691-40fe00c6-a7c3-49b7-a86e-bc8e93c2ae0f.mov

https://user-images.githubusercontent.com/108469512/199300707-887a1413-7777-4341-a897-46b72153256c.mov

https://user-images.githubusercontent.com/108469512/199300724-08a9881e-e5c6-4cef-a21d-92fac3e1cc7d.mov

https://user-images.githubusercontent.com/108469512/199300733-7460cdcb-b9b1-4eaf-960d-9d3d2d352779.mov

https://user-images.githubusercontent.com/108469512/199300712-80b47f31-8451-4fcd-884f-fffee5d4f051.mov

https://user-images.githubusercontent.com/108469512/199300830-008d8835-8e92-4225-8a15-0ca1e31408fc.mov
