# Automated Tiktok video creation
This tool can be used for automated tiktok video creation, automated youtube shorts creation and automated instagram reels creation.

The default settings allow you to create content for the following topics:
+ crypto
+ politics
+ general news
+ stock market news

You can change the topic of the video very easily (you can find a detailed explanation in the setup guide)


# Examples:
https://user-images.githubusercontent.com/108469512/199298996-37aed67d-2c4f-43e7-bf8b-67b609edc6de.mp4
https://user-images.githubusercontent.com/108469512/199299076-af476bf0-b337-4372-85c8-536d4a5d5cc7.mp4

see all examples here

# Explanation:
This tools goes to finance.yahoo.com and searches for articles about crypto, politics, general news and about the stock market. It uses open ai's GPT-3 to summarize the articles and synthesia to make a robot read the summary. It then edits the video by changing the format, removing the silences, adding subtitles and more.

It then gives the user the possibility to create variations of the videos that he wants. As of now there are 3 different types of variations. It would be very though to add more.

Example of a variation:
https://user-images.githubusercontent.com/108469512/199299152-d137b805-b4e5-410d-b37f-b4fe1f6753f6.mp4

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
