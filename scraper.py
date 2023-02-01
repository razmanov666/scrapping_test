import requests

from bs4 import BeautifulSoup


site = "https://www.truckscout24.de"
page = "/transporter/gebraucht/kuehl-iso-frischdienst/renault?currentpage=1"
html_text = requests.get(f"{site}{page}").text
soup = BeautifulSoup(html_text, "lxml")

ad = soup.find('div', class_="ls-elem ls-elem-gap")

url_car = ad.find('div', class_="ls-titles").a["href"]
link_car = f"{site}{url_car}"
request_car = requests.get(f"{link_car}").text

soup_car = BeautifulSoup(request_car, "lxml")
title = soup_car.title.text
price = int(soup_car.find("div", class_="d-price sc-font-xl").text.split(',')[0].replace("€", "").replace('.', ''))
item_spaces = soup_car.find("div", class_="data-basic1").find_all("div", class_="itemspace")
for item in item_spaces:
    if "Kilometer" in item.text:
        mileage = int(item.text.split()[1].replace(".", ''))
tech_datas = soup_car.find("div", class_="sc-expandable-box").find_all("li")
for data in tech_datas:
    if "Leistung" in data.text:
        power = int(data.text.split()[1].replace(".", ''))
    elif "Farbe" in data.text:
        color = data.text.split()[1]
description = soup_car.find("div", class_="short-description").text

print(f"""Title: {title}
Link: {link_car}
Price: {price}
Mileage: {mileage}
Power: {power}
Color: {color}
Description: {description}

""")