import requests
def send_msg(text):
    token="123:XXXXX"
    chat_id="XXXXX"
    url_req="https://api.telegram.org/bot"+ token+"/sendMessage"+"?chat_id="+chat_id+"&text="+text
    results=requests.get(url_req)
    # print(results.json())
    return results.json()
# send_msg("test")

# try:
#     array.push("test")
#     send_msg("test")
# except Exception as e:
#     send_msg("An Error Occured: \n"+str(e))
#     print(e)