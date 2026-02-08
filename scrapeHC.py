from bs4 import BeautifulSoup
import requests

# somehow get the Weiss card tag and rarity from the user or something
cardTag = "CCS/W113-001"
rarity = "RR"

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

print(link)