import requests

from bs4 import BeautifulSoup

site = "https://www.truckscout24.de"

page = "/transporter/gebraucht/kuehl-iso-frischdienst/renault?currentpage="

def get_amount_pages():
    number_page = 1
    ad = True
    while(ad):
        request_data = requests.get(f"{site}{page}{number_page}").text
        soup = BeautifulSoup(request_data, "lxml")
        ad = soup.find('div', class_="ls-elem ls-elem-gap")
        if ad: number_page += 1
    return number_page



amount_page = get_amount_pages()

for current_page in range(1, amount_page):
    # Get data for one of pages
    html_text = requests.get(f"{site}{page}{current_page}").text
    soup = BeautifulSoup(html_text, "lxml")

    # Get data from ad
    ad = soup.find('div', class_="ls-elem ls-elem-gap")

    # Get link for ad
    url_car = ad.find('div', class_="ls-titles").a["href"]
    link_car = f"{site}{url_car}"

    # Go to the link_car and get data
    request_car = requests.get(f"{link_car}").text
    soup_car = BeautifulSoup(request_car, "lxml")

    # Get description of ad
    title = soup_car.title.text

    # Get price
    price = int(soup_car.find("div", class_="d-price sc-font-xl").text.split(',')[0].replace("€", "").replace('.', ''))
    
    # Get mileage
    item_spaces = soup_car.find("div", class_="data-basic1").find_all("div", class_="itemspace")
    for item in item_spaces:
        if "Kilometer" in item.text:
            mileage = int(item.text.split()[1].replace(".", ''))
    
    # Get power and color
    tech_datas = soup_car.find("div", class_="sc-expandable-box").find_all("li")
    for data in tech_datas:
        if "Leistung" in data.text:
            power = int(data.text.split()[1].replace(".", ''))
        elif "Farbe" in data.text:
            color = data.text.split()[1]

    # Get description
    description = soup_car.find("div", class_="short-description").text
