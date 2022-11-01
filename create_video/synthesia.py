import requests

API_KEY = "XXXXX"

def create_synthesia(content, language):
    if language == "en":
        voice = '70ded880-ad19-4673-956c-20aeaa5d1695'
    elif language == "fr":
        voice = 'b4962a67-ce24-4a3e-935b-e695b860d9cf'
    elif language == "de":
        voice = '58a9cbbd-ab42-4560-9c4f-e801a34e92a1'
    elif language == "it":
        voice = 'b605a26e-14ab-46ff-b3ba-e440199f3cd4'        

    headers = {
        'Authorization': f"{API_KEY}",
    }

    json_data = {
        'test': False,
        'title': 'RobotBulls News',
        'description': 'Crypto and economic News!',
        'visibility': 'public',
        'ctaSettings': {
            'label': 'More News!',
            'url': 'https://www.robotbulls.com',
        },
        'callbackId': 'support@robotbulls.com',
        'input': [
            {
                'scriptText': content,
                'avatar': '6784e07c-9f71-428f-a43d-a27df9965833',
                'avatarSettings': {
                    'voice': voice,
                    'horizontalAlign': 'center',
                    'scale': 0.8,
                    'style': 'rectangular',
                },
                'background': 'off_white', #off_white #green_screen
            },
        ]
    }

    response = requests.post('https://api.synthesia.io/v2/videos', headers=headers, json=json_data)
    print(response.json())
    try:
        video_id = response.json()['id']
        print("videoid = ",video_id)
        return video_id
    except:
        return False


def createWebhook():

    headers = {
        'Authorization': f"{API_KEY}",
    }

    json_data = {
        'url': 'https://eonv6y6swez638t.m.pipedream.net',
        'events': [
            'video.completed',
        ],
    }

    response = requests.post('https://api.synthesia.io/v2/webhooks', headers=headers, json=json_data)
    print(response.json())
    webhook_id = response.json()['id']
    return webhook_id


def retrieveWebhook(webhook_id):

    headers = {
        'Authorization': f"{API_KEY}",
    }

    response = requests.get('https://api.synthesia.io/v2/webhooks/'+webhook_id, headers=headers)
    print(response.json())
    

def retrieveVideo(video_id):

    headers = {
        'Authorization': f"{API_KEY}",
    }
    url = 'https://api.synthesia.io/v2/videos/'+video_id

    response = requests.get(url, headers=headers)
    try:
        print(response)
        print(response.json())
    except:
        pass
    #status = response.json()['status']
    return response
