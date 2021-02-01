import re

links = []
regex = "(?P<url>https?://[^\s]+)"

with open('whatsapp.txt', encoding="utf8") as f:
    lines = f.readlines()
    for l in lines:
        if "youtube.com" in l:
            link = re.findall("(?P<url>https?://[^\s]+)", l)
            try:
                links.append(link[0])
            except:
                print("An exception occured")