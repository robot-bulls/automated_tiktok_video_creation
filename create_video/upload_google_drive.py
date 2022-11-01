from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
def upload_to_google_drive(video_index_array, language):
    folder_array = [["XXXXX", "XXXXX", "XXXXX", "XXXXX"], ["XXXXX", "XXXXX", "XXXXX", "XXXXX"]]
    for i,topic in enumerate(video_index_array):
        for video_index in topic:
            if language == "en":
                currentfolder = folder_array[0][i]
            if language == "de":
                currentfolder = folder_array[1][i]
            print("currentfolder:",currentfolder)
            gauth = GoogleAuth()
            if gauth.credentials is None:
                gauth.LoadCredentialsFile("mycreds.txt")
                # Authenticate if they're not there
                gauth.LocalWebserverAuth()
            elif gauth.access_token_expired:
                #Refresh them if expired
                gauth.Refresh()
            else:
                #Initialize the saved creds
                gauth.Authorize()
            # Save the current credentials to a file
            gauth.SaveCredentialsFile("mycreds.txt")

            drive = GoogleDrive(gauth)
            file = drive.CreateFile({"title": str(video_index)+".mp4", 'parents': [{'id': currentfolder}]})
            file.SetContentFile("videos/"+language+"/"+str(i)+"/"+str(video_index).zfill(4)+".mp4")
            file.Upload({'convert': True})
    print("Finished Uploading")


def upload_variations(video_index_array, language):
    variations_folder = [[[["XXXXX"],["XXXXX"],["XXXXX"]],[["XXXXX"],["XXXXX"],["XXXXX"]],[["XXXXX"],["XXXXX"],["XXXXX"]],[["XXXXX"],["XXXXX"],["XXXXX"]]], [[["XXXXX"],["XXXXX"],["XXXXX"]],[["XXXXX"],["XXXXX"],["XXXXX"]],[["XXXXX"],["XXXXX"],["XXXXX"]],[["XXXXX"],["XXXXX"],["XXXXX"]]]]
    for i,topic in enumerate(video_index_array):
        print("topic:",topic)
        for video_index in topic:
            print("video_index:",video_index)
            if language == "en":
                currentfolder = variations_folder[0][i]
            if language == "de":
                currentfolder = variations_folder[1][i]
            print("currentfolder:",currentfolder)
            for v,current_variation in enumerate(currentfolder):
                gauth = GoogleAuth()
                if gauth.credentials is None:
                    gauth.LoadCredentialsFile("mycreds.txt")
                    # Authenticate if they're not there
                    gauth.LocalWebserverAuth()
                elif gauth.access_token_expired:
                    #Refresh them if expired
                    gauth.Refresh()
                else:
                    #Initialize the saved creds
                    gauth.Authorize()
                # Save the current credentials to a file
                gauth.SaveCredentialsFile("mycreds.txt")
                drive = GoogleDrive(gauth)
                file = drive.CreateFile({"title": str(video_index)+".mp4", 'parents': [{'id': current_variation}]})
                file.SetContentFile("videos/"+language+"/"+str(i)+"/"+"variation_"+str(v+1)+"/"+str(video_index).zfill(4)+".mp4")
                file.Upload({'convert': True})
    print("Finished Uploading Variations")