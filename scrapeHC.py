from bs4 import BeautifulSoup
import requests

# https://cdn.yuyu-tei.jp/images/icon/ws/icon_tri_0.png = empty trigger
# https://cdn.yuyu-tei.jp/images/icon/ws/icon_tri_1.png = normal trigger icon
# double soul just puts two normal trigger icons
# https://cdn.yuyu-tei.jp/images/icon/ws/icon_tri_I.png = choice icon
# https://cdn.yuyu-tei.jp/images/icon/ws/icon_tri_1A.png = wind icon
# https://cdn.yuyu-tei.jp/images/icon/ws/icon_tri_1E.png = shot icon
# https://cdn.yuyu-tei.jp/images/icon/ws/icon_tri_F.png = goldbar icon
# https://cdn.yuyu-tei.jp/images/icon/ws/icon_tri_B.png = bag icon
# https://cdn.yuyu-tei.jp/images/icon/ws/icon_tri_1G.png = pants icon
# https://cdn.yuyu-tei.jp/images/icon/ws/icon_tri_D.png = book icon
# https://cdn.yuyu-tei.jp/images/icon/ws/icon_tri_C.png = door icon
# https://cdn.yuyu-tei.jp/images/icon/ws/icon_tri_1H.png = standby icon

# somehow get the Weiss card tag and rarity from the user or something
cardTag = "CCS/W113-079"
rarity = "R"

# search for the card on yuyutei
url = "https://yuyu-tei.jp/sell/ws/s/search?search_word=" + cardTag

# getting the page
page = requests.get(url)

# BeautifulSoup object 
soup = BeautifulSoup(page.text, 'html.parser')

# selecting this thing because it has the info we need
cardOptions = soup.select('div.position-relative.product-img')

# empty string for the needed card which we will fill when we find the card we need
neededCard = ""

# iterate through the cards available, when we find the correct rarity, we set that as the needed card
for card in cardOptions:
    
    imageTag = card.find('img')

    # split the alt text so we can check rarity
    altText = imageTag['alt'].split(" ")

    # need to ensure the alt text has at least 2 elements
    if len(altText) >= 2:
        # altText[1] should have the rarity of the card, if it the correct rarity, we set the needed card and break
        if rarity == altText[1]:
            neededCard = card
            break

if neededCard == "":
    print("Something is wrong")
    exit()

# the parent of this has the link to the page of the card we wanted to find (in the href)
cardParent = neededCard.find_parent()
link = cardParent.get('href')

# now that we have the link we need, lets set get the page and set up the new BeautifulSoup object
page = requests.get(link)
soup = BeautifulSoup(page.text, 'html.parser')

円 = soup.select_one('h4.fw-bold.d-inline-block').text[:-1].strip()

cardImg = soup.select_one('img.vimg')
cardImgLink = cardImg['src']

rawCardClassif = soup.select("th.text-primary.w-25.border-end-0")
rawCardInfo = soup.select('td.text-dark.w-25.border-start-0')

cardDict = {}
cardDict.update({"カードショップ" : "遊々亭"})
cardDict.update({"値段" : int(円)})
cardDict.update({"レアリティ" : rarity})

if rawCardInfo[0].text.strip() == "クライマックス" or rawCardInfo[0].text.strip() == "イベント":
    rawCardInfo.pop()

if len(rawCardClassif) == len(rawCardInfo):
    for x in range(len(rawCardClassif)):
        cardDict.update({rawCardClassif[x].text.strip() : rawCardInfo[x].text.strip()})
else:
    print("These lists should be the same size, something went wrong")
    exit()

print(cardDict)