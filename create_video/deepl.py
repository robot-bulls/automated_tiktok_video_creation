import requests

video_text = ["India is planning to tax any money made from cryptocurrencies at a rate as high as 50%. This comes as the government is trying to figure out how to regulate the new asset class. Many young investors are moving their businesses out of the country to places with more crypto-friendly policies. Follow the channel for the latest crypto news!", "OpenSea is the world's largest online marketplace for non-fungible tokens. The company has announced that it is cutting about 20% of its staff. This is the latest in a series of layoffs that have rocked the crypto industry as digital-asset prices continue to plummet.", "The Russian president has signed a bill into law that prohibits the use of digital assets, such as cryptocurrency and NFTs, to pay for goods and services. In addition, the new law also requires crypto exchanges and providers to refuse transactions in which digital transfers can be interpreted as a form of payment. This means that people in Russia will soon no longer be able to use digital assets as a form of payment."]

API_KEY = 'XXXXX'

def deepl(text, lang):

    result = requests.get( 
        "https://api-free.deepl.com/v2/translate", 
        params={ 
            "auth_key": API_KEY, 
            "target_lang": lang, 
            "text": text, 
        }, 
    ) 
    print("result2",result)
    translated_text = result.json()["translations"][0]["text"]
    print(translated_text)
    return translated_text
