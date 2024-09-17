#importing custom libraries
import Thumbnail # print(Thumbnail.lastThumbnail)
#importing default libraries
import os
from pytube import YouTube
import re
import requests
import time
import subprocess
from send2trash import send2trash
import pandas
from deep_translator import GoogleTranslator

#system constants, simple
TEXT_RESET = "\033[0m"
TEXT_RED = "\033[31m"
TEXT_GREEN = "\033[32m"
TEXT_YELLOW = "\033[33m"
TEXT_BLUE = "\033[34m"
TEXT_BOLD = "\033[1m"
TEXT_DIM = "\033[2m"
TEXT_MAGENTA = "\033[35m"
TEXT_CYAN = "\033[36m"

#system constants, compound
TEXT_CUSTOM_1 = TEXT_YELLOW + TEXT_BOLD + "|" + TEXT_RESET

#program variables
main_urlList = []
main_oldFileName = []
main_newFileName = []
main_fileFormatList = []
current_fileFormat = 0
sub_TLedFileName = []

#objects
translatorObject = GoogleTranslator(source='auto', target='en')

#functions
def addYoutubeUrls():
    global current_fileFormat
    global main_fileFormatList
    global main_urlList
    global main_oldFileName
    global sub_TLedFileName
    
    while True:

        print(f"\n{TEXT_GREEN}0: Audio | 1: Video 1080p | 2: Video 720p | 3: Print table | 5: Contine{TEXT_RESET}")
        urlElement = input(f"{TEXT_BLUE}{TEXT_BOLD}Enter URL: {TEXT_RESET}")
        
        if urlElement == "0":
            print(f"The file format is: {TEXT_YELLOW}Audio{TEXT_RESET}.")
            current_fileFormat = 0
            continue
        elif urlElement == "1":
            print(f"The file format is: {TEXT_YELLOW}Video 1080p{TEXT_RESET}.")
            current_fileFormat = 1
            continue
        elif urlElement == "2":
            print(f"The file format is: {TEXT_YELLOW}Video 720p{TEXT_RESET}.")
            current_fileFormat = 2
            continue
        elif urlElement == "3":
            printTable()
            continue
        elif urlElement == "5":
            break
        
        if len(urlElement)>=43:        
            urlElement = urlElement[0:43]
        else:
            print(f"The URL is less than 43 characters long. {TEXT_RED}Invalid URL. Retry.{TEXT_RESET}")
            addYoutubeUrls()

        #checking if the url is valid #getting the original title of the youtube media
        try:
            youtubeObject = YouTube(urlElement)
            originalFileNameElement = youtubeObject.title
            print("\nOriginal title: " + TEXT_BOLD + TEXT_BLUE + originalFileNameElement + TEXT_RESET)
            translatedText = translatorObject.translate(originalFileNameElement)
            print(f"TLed title: {TEXT_CYAN}{translatedText}{TEXT_RESET}")
        except Exception:
            if checkInternetConnection():
                print(f"The URL might be incorrect. {TEXT_RED}Please recheck and retry.{TEXT_RESET}")            
            addYoutubeUrls()

        main_urlList.append(urlElement)
        main_oldFileName.append(originalFileNameElement)
        main_fileFormatList.append(current_fileFormat)
        sub_TLedFileName.append(translatedText)
        setNewFileName(originalFileNameElement, translatedText)

    confirmTable()

def setNewFileName(originalTitle, TLedTitle):
    global main_newFileName

    print(f"\n{TEXT_DIM}Enter: Default title | 0: TLed title{TEXT_RESET}")
    print(f"New Title: {TEXT_BOLD}{TEXT_BLUE}", end="")
    newFileNameElement = input()
    print(f"{TEXT_RESET}", end="")
    if not newFileNameElement:
        newFileNameElement = originalTitle
    if newFileNameElement == "0":
        newFileNameElement = TLedTitle
    if not isValidFileName_forWindows(newFileNameElement):
        setNewFileName(originalTitle)
    else:
        main_newFileName.append(newFileNameElement)

def isValidFileName_forWindows(fileName):
    if len(fileName)>230:
        print(f"New title is over 230 characters. {TEXT_RED}Invalid file name. Retry.{TEXT_RESET}")
        return 0
    if re.findall(r'[\\/<>|?:"*]', fileName):
        print(f"New title has invlid characters. {TEXT_RED}Invalid file name. Retry.{TEXT_RESET}")
        return 0
    osReservedFilenames = [
    "CON", "PRN", "AUX", "NUL",
    "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
    "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9"
    ]
    if fileName.upper() in osReservedFilenames:
        print(f"New title is an OS reserved file name. {TEXT_RED}Invalid file name. Retry.{TEXT_RESET}")
        return 0
    return 1

def printTable():
    global main_fileFormatList
    global main_urlList
    global main_oldFileName
    global main_newFileName

    print(f"\n{TEXT_YELLOW}Index | Original Name | New Name | Format | URL{TEXT_RESET}")
    if main_urlList:
        for element in range(len(main_urlList)):
            if main_fileFormatList[element] == 0:
                print(f"{element} {TEXT_CUSTOM_1} {main_oldFileName[element]} {TEXT_CUSTOM_1} {main_newFileName[element]} {TEXT_CUSTOM_1} Audio {TEXT_CUSTOM_1} {TEXT_DIM}{main_urlList[element]}{TEXT_RESET}")
            elif main_fileFormatList[element] == 1:
                print(f"{element} {TEXT_CUSTOM_1} {main_oldFileName[element]} {TEXT_CUSTOM_1} {main_newFileName[element]} {TEXT_CUSTOM_1} Video 1080p {TEXT_CUSTOM_1} {TEXT_DIM}{main_urlList[element]}{TEXT_RESET}")
            else:
                print(f"{element} {TEXT_CUSTOM_1} {main_oldFileName[element]} {TEXT_CUSTOM_1} {main_newFileName[element]} {TEXT_CUSTOM_1} Video 720p {TEXT_CUSTOM_1} {TEXT_DIM}{main_urlList[element]}{TEXT_RESET}")
    else:
        print("(The list is empty.)")
    print(f"{TEXT_YELLOW}--- --- --- --- ---{TEXT_RESET}")

def confirmTable():
    global main_fileFormatList
    global main_urlList
    global main_oldFileName
    global main_newFileName

    printTable()
    print(f"\n{TEXT_GREEN}0: Edit the table | Enter: Continue{TEXT_RESET}")
    print(f"Input: {TEXT_BOLD}{TEXT_BLUE}", end="")
    ifEditTable = input()
    print(f"{TEXT_RESET}")
    
    if ifEditTable != "0":
        ifEditTable = "1"
    while ifEditTable=="0":
        printTable()
        print(f"\n{TEXT_GREEN}'.': Continue to download | '...': Add more URLs | 'index': Delete index{TEXT_RESET}")
        print(f"Input: {TEXT_BOLD}{TEXT_BLUE}", end="")
        cmd = input()
        print(f"{TEXT_RESET}")

        if cmd == ".":
            break
        if cmd == "...":
            addYoutubeUrls()

        try:
            cmd = int(cmd)
        except Exception:
            print(f"{TEXT_RED}Invalid input. Retry.{TEXT_RESET}")
            continue

        main_urlList.pop(cmd)
        main_oldFileName.pop(cmd)
        main_newFileName.pop(cmd)
        main_fileFormatList.pop(cmd)
        print(f"{TEXT_MAGENTA}Formerly index '{cmd}' has been removed.{TEXT_RESET}")
    downloadAllUrls()

def downloadAllUrls():
    global main_urlList
    global main_fileFormatList
    
    print("\nStarting the download process.\n")
    
    for element in range(len(main_urlList)):
        whileWaitingForInternet()
        
        #downloading the media
        if main_fileFormatList[element]==0:
            hyper_downloadAudio(main_urlList[element])
        elif main_fileFormatList[element]==1:
            downloadVideo(main_urlList[element], 1)
        else:
            downloadVideo(main_urlList[element], 2)

def hyper_downloadAudio(url):
    try:
        commandToDownloadAudio = [
            "yt-dlp",
            "-f",
            "bestaudio",
            "--extract-audio",
            "--audio-format",
            "m4a",
            "--audio-quality",
            "0",
            url
        ]
        subprocess.run(commandToDownloadAudio, check=True)
    except subprocess.CalledProcessError:
        whileWaitingForInternet()
        print(f"{TEXT_RED}Attempting to resolve error:{TEXT_RESET} downloading audio.")
        hyper_downloadAudio(url)
    hyper_downloadThumbnail(url, 1)

def hyper_downloadThumbnail(url, count):
    urlElement = url[32:43]
    
    if count == 1:
        newUrl = f'https://img.youtube.com/vi/{urlElement}/maxresdefault.jpg'
    elif count == 2:
        newUrl = f'https://img.youtube.com/vi/{urlElement}/hddefault.jpg'
    elif count == 3:
        newUrl = f'https://img.youtube.com/vi/{urlElement}/sddefault.jpg'
    elif count == 4:
        newUrl = f'https://img.youtube.com/vi/{urlElement}/hqdefault.jpg'
    elif count == 5:
        newUrl = f'https://img.youtube.com/vi/{urlElement}/mqdefault.jpg'
    elif count == 6:
        newUrl = f'https://img.youtube.com/vi/{urlElement}/default.jpg'
    else:
        newUrl = Thumbnail.lastThumbnail
    
    newUrlResponse = requests.get(newUrl, stream=True)
    
    imagePath = "D:\\YouTube\\Thumbnails\\" + urlElement + ".jpg"
    if newUrlResponse.status_code == 200:
        with open(imagePath, "wb") as imageFile:
            for imageChunk in newUrlResponse.iter_content(chunk_size=8192):
                imageFile.write(imageChunk)
    else:
        whileWaitingForInternet()
        print(f"{TEXT_RED}Attempting to resolve error:{TEXT_RESET} downloading thumbnail.")
        hyper_downloadThumbnail(url, count+1)
    
    hyper_combineAudioAndThumbnail(url, urlElement, imagePath)

def hyper_combineAudioAndThumbnail(url, urlElement, imagePath):
    global main_urlList
    global main_oldFileName
    index = main_urlList.index(url)
    oldFileName = main_oldFileName[index]
    audioPath = "D:\\YouTube\\" + oldFileName + f" [{urlElement}].m4a"
    NEW_audioPath = "D:\\YouTube\\NEW_M4A_" + oldFileName + f" [{urlElement}].m4a"
    try:
        command = [
            "ffmpeg",
            "-i",
            audioPath,
            "-i",
            imagePath,
            "-map",
            "0",
            "-map",
            "1",
            "-c:a",
            "copy",
            "-c:v",
            "copy",
            "-disposition:v",
            "attached_pic",
            NEW_audioPath
        ]
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError:
        print(f"{TEXT_RED}Attempting to resolve error:{TEXT_RESET} merging audio and thumbnail.")
        hyper_combineAudioAndThumbnail(url, urlElement, imagePath)

def whileWaitingForInternet():
    ifInternetConnection = checkInternetConnection()
    if not ifInternetConnection:
        attempt = 1
        while not ifInternetConnection:
            print(f"{TEXT_RED}{TEXT_BOLD}Retrying in 10s.{TEXT_RESET} Attempt: {attempt}")
            attempt+=1
            time.sleep(10)
            ifInternetConnection = checkInternetConnection()
        print("Connected to the internet.\n")


def downloadVideo(url, quality):
    if quality == 1:
        command = ["yt-dlp", "-f", "bestvideo[height<=1080]+bestaudio/best[height<=1080]", "--merge-output-format", "webm", url]
    else:
        command = ["yt-dlp", "-f", "bestvideo[height<=720]+bestaudio/best[height<=720]", "--merge-output-format", "webm", url]

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError:
        whileWaitingForInternet()
        print(f"{TEXT_RED}Attempting to resolve error:{TEXT_RESET} downloading video.")
        downloadVideo(url, quality)    

def checkInternetConnection():
    try:
        googleResponse = requests.get(url="https://www.google.com/", timeout=5)
        if googleResponse.status_code == 200:
            return True
        else:
            print(f"{TEXT_BOLD}{TEXT_RED}No internet connection found. Please check your connection.{TEXT_RESET}")
            return False
    except requests.ConnectionError:
        print(f"{TEXT_BOLD}{TEXT_RED}No internet connection found. Please check your connection.{TEXT_RESET}")
        return False

def sendAllDataToCsv():
    global main_fileFormatList
    global main_newFileName
    global main_oldFileName
    global main_urlList
    global sub_TLedFileName
    fullFileFormatName = ["Audio", "Video 1080p", "Video 720p"]
    for element in range(len(main_urlList)):
        dataToAppend = [{"URL":main_urlList[element], "Original Name":main_oldFileName[element], "TLed Name":sub_TLedFileName[element], "New Name":main_newFileName[element], "File Type":fullFileFormatName[main_fileFormatList[element]]}]
        dataToAppend_dataFrame = pandas.DataFrame(dataToAppend)
        dataToAppend_dataFrame.to_csv(r"E:\Code\Laptop Code\YT-DLP CLI by Me\Database\Log of Commands by the User.csv", mode="a", index=False, header=False, encoding='utf-8-sig')

#the super function starts
def super_removeDuplicateAudio_And_renameAllMedia():
    global main_fileFormatList
    global main_urlList
    global main_newFileName
    global main_oldFileName
    folderPath = "D:\\YouTube\\"
    listOfFilesInYoutubeFolder = []
    
    for fileNameAppend in os.listdir(r"D:\YouTube"):
        listOfFilesInYoutubeFolder.append(fileNameAppend)

    for fileName in listOfFilesInYoutubeFolder:

        if fileName[-5:]==".webm":
            for index in range(len(main_urlList)):
                if fileName[-17:-6] == main_urlList[index][-11:]:
                    if main_fileFormatList[index] != 0:
                        oldFilePath = folderPath + fileName
                        newFilePath = folderPath + main_newFileName[index] + ".webm"
                        if not os.path.exists(newFilePath):
                            os.rename(oldFilePath, newFilePath)
                        else:
                            k=1
                            while True:
                                k+=1
                                newFilePath = folderPath + main_newFileName[index] + f"_{k}.webm"
                                if os.path.exists(newFilePath):
                                    continue
                                else:
                                    break
                            os.rename(oldFilePath, newFilePath)

        elif fileName[-4:]==".m4a":
            for index in range(len(main_urlList)):
                if fileName[-16:-5] == main_urlList[index][-11:]:
                    if main_fileFormatList[index] == 0:
                        
                        if fileName[:8] == "NEW_M4A_":
                            oldFilePath = folderPath + fileName
                            newFilePath = folderPath + main_newFileName[index] + ".m4a"
                            if not os.path.exists(newFilePath):
                                os.rename(oldFilePath, newFilePath)

                            else:
                                k=1
                                while True:
                                    k+=1
                                    newFilePath = folderPath + main_newFileName[index] + f"_{k}.m4a"
                                    if os.path.exists(newFilePath):
                                        continue
                                    else:
                                        break
                                os.rename(oldFilePath, newFilePath)

                        else:
                            send2trash(os.path.join(folderPath, fileName))
#the super function ends

def getDbSize():
    dbSize = os.path.getsize(r"E:\Code\Laptop Code\YT-DLP CLI by Me\Database\Log of Commands by the User.csv")
    if dbSize > 50000000:
        print("The past-logs' size is over 50 mb.\n")

#main function
if __name__ == "__main__":
    #opening the program
    getDbSize()
    print(f"{TEXT_DIM}(Note: Do not download the same URL as 1080p and 720p at the same time. Do not set audio file names beginning with 'NEW_M4A_'.){TEXT_RESET}")
    os.chdir(r"D:\YouTube")
    os.makedirs(r"D:\YouTube\Thumbnails", exist_ok=True)
    
    #part 1/2
    print(f"\nThe current file format is: {TEXT_YELLOW}Audio{TEXT_RESET}.")
    addYoutubeUrls()
    
    #part 2/2
    send2trash(r"D:\YouTube\Thumbnails")
    super_removeDuplicateAudio_And_renameAllMedia()
    sendAllDataToCsv()

    #closing the program
    input("\nAll downloads finished, successfully. Press Enter to exit.")

#the end
