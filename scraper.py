import json
import os
import pathlib
import shutil

import requests
from bs4 import BeautifulSoup


def get_amount_pages():
    # Func for get amout of navigation pages
    number_page = 1
    ad = True
    while ad:
        request_data = requests.get(f"{site}{page}{number_page}").text
        soup = BeautifulSoup(request_data, "lxml")
        ad = soup.find("div", class_="ls-elem ls-elem-gap")
        if ad:
            number_page += 1
    print(f"\nObjects in the queue: {number_page - 1}\n")
    return number_page - 1


def get_info_car(amount_page):
    # Func for getting all data about car

    # The list that will contain the result of the parsing
    list_of_data = []

    # Cycle for get information from all pages of resource
    for current_page in range(1, amount_page + 1):
        data = {}

        # Get data for one of pages
        html_text = requests.get(f"{site}{page}{current_page}").text
        soup = BeautifulSoup(html_text, "lxml")

        # Get data from ad
        ad = soup.find("div", class_="ls-elem ls-elem-gap")

        # Get is for ad
        data["id"] = current_page

        # Get link for ad
        url_car = f"{site}{ad.find('div', class_='ls-titles').a['href']}"
        data["href"] = url_car

        # Get info for user
        print(f"[{data['id']}] Parsing URL: \t{data['href']}")

        # Go to the link_car and get data
        request_car = requests.get(f"{data['href']}").text
        soup_car = BeautifulSoup(request_car, "lxml")

        # Get description of ad
        data["title"] = soup_car.title.text

        # Get price
        try:
            data["price"] = int(
                soup_car.find("div", class_="d-price sc-font-xl").text.split(",")[0].replace("€", "").replace(".", "")
            )
        except BaseException:
            data["price"] = 0

        # Get mileage
        item_spaces = soup_car.find("div", class_="data-basic1").find_all("div", class_="itemspace")
        for item in item_spaces:
            if "Kilometer" in item.text:
                try:
                    data["mileage"] = int(item.text.split()[1].replace(".", ""))
                except BaseException:
                    data["mileage"] = 0

        # Get power and color
        tech_info = soup_car.find("div", class_="sc-expandable-box").find_all("li")
        for record in tech_info:
            if "Leistung" in record.text:
                try:
                    data["power"] = int(record.text.split()[1].replace(".", ""))
                except BaseException:
                    data["power"] = 0
            elif "Farbe" in record.text:
                try:
                    data["color"] = record.text.split()[1]
                except BaseException:
                    data["color"] = ""

        # Get description
        data["description"] = soup_car.find("div", class_="short-description").text

        # Get empty values if can't get data
        data = data_validation(data)

        # Get photos and download in dir
        get_photos(data["id"], soup_car)
        list_of_data.append(data)

    return list_of_data


def get_photos(dir_name, soup):
    # Download images
    car_photos = soup.find_all("div", class_="gallery-picture")[:3]
    dir_path = f"{data_path}/{dir_name}"
    os.mkdir(dir_path)
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    for index, photo in enumerate(car_photos):
        image = requests.get(photo.img["data-src"])
        image_file = open(f"{data_path}/{dir_name}/{index+1}.jpg", "wb")
        image_file.write(image.content)
        image_file.close()


def save_json(json_data: dict):
    with open("data/data.json", "w") as outfile:
        save_dict = {"ads": json_data}
        json.dump(save_dict, outfile, indent=3)


def data_validation(data: dict):
    if not data.get("mileage"):
        data["mileage"] = 0
    if not data.get("power"):
        data["power"] = 0
    if not data.get("color"):
        data["color"] = ""
    if not data.get("description"):
        data["description"] = ""
    return data


if __name__ == "__main__":
    # Input data for parsing
    site = "https://www.truckscout24.de"
    page = "/transporter/gebraucht/kuehl-iso-frischdienst/renault?currentpage="
    data_path = f"{pathlib.Path().absolute()}/data"
    json_path = data_path + "/data.json"

    # Clearing the "data" directory
    if os.path.exists(data_path):
        shutil.rmtree(data_path)
    os.mkdir(data_path)

    # Working code)
    amount_page = get_amount_pages()
    data = get_info_car(amount_page)
    print(f"\nSuccess!\nThe data is saved in the: {data_path}\n")
    save_json(data)
