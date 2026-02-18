import os
import requests
from bs4 import BeautifulSoup
import time
import random

def downloadImg(imgURL, savePath, fileName):
    
    response = requests.get(imgURL)

    fullPath = os.path.join(savePath, fileName)

    if response.status_code == 200:
        with open(fullPath, 'wb') as file:
            file.write(response.content)
            print(f"Image downloaded successfully to {savePath}")
    else:
        print(f"Failed to download image. Status code: {response.status_code}")

def createDir(directory):
    try:
        os.mkdir(directory)
        print(f"Directory '{directory}' created successfully.")
    except FileExistsError:
        print(f"Directory '{directory}' already exists.")
    except PermissionError:
        print(f"Permission denied: Unable to create '{directory}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

def dlHolo(url):
    fake_id = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"}
    page = requests.get(url, headers=fake_id)

    soup = BeautifulSoup(page.text, 'html.parser')

    cardSrc = soup.select_one('div.img.w100').find('img')['src'].split('/')

    cardInfo = cardSrc[-2:]

    set = cardInfo[0]
    card = cardInfo[1]
    cardName = set + "_" + card

    url2download = "https://en.hololive-official-cardgame.com/wp-content/images/cardlist/" + set + "/" + card

    downloadImg(url2download, "hololive_images", cardName)

createDir("hololive_images")

with open("files2download.txt") as file:
    for line in file:
        dlHolo(line)
        time.sleep(random.uniform(1, 3))