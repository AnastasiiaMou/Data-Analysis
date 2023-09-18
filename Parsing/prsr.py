import requests
from bs4 import BeautifulSoup
import csv

headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
}

city_uk = [
    "Івано-Франківськ",
    "Вінниця",
    "Луцьк",
    "Дніпро",
    "Донецьк",
    "Житомир",
    "Ужгород",
    "Запоріжжя",
    "Кропивницький",
    "Київ",
    "Сімферополь",
    "Луганськ",
    "Львів",
    "Миколаїв",
    "Одеса",
    "Полтава",
    "Рівне",
    "Суми",
    "Тернопіль",
    "Харків",
    "Херсон",
    "Хмельницький",
    "Черкаси",
    "Чернівці",
    "Чернігів",
]
city_en = [
    "ivano-frankovsk",
    "vinnitsa",
    "lutsk",
    "dnepr",
    "donetsk",
    "zhitomir",
    "uzhgorod",
    "zaporozhe",
    "kropivnitskiy",
    "kiev",
    "simferopol",
    "lugansk",
    "lvov",
    "nikolaev_106",
    "odessa",
    "poltava",
    "rovno",
    "sumy",
    "ternopol",
    "kharkov",
    "kherson",
    "khmelnitskiy",
    "cherkassy",
    "chernovtsy",
    "chernigov",
]

rooms_uk = ["1", "2", "3", "4"]
rooms_en = [
    "odnokomnatnye",
    "dvuhkomnatnye",
    "trehkomnatnye",
    "chetyrehkomnatnye",
    "pyatikomnatnye",
]

pets_uk = ["Так", "Ні"]
pets_en = ["yes_cat", "no"]


city = input("Enter a city: ")
start_range = int(input("Start range: "))
end_range = int(input("End range: "))
rooms = input("How many rooms?: ")
pet = input("Do you have a pets? ")

city_en_value = city_en[city_uk.index(city)] if city in city_uk else city
rooms_en_value = rooms_en[rooms_uk.index(rooms)] if rooms in rooms_uk else rooms
pet_en_value = pets_en[pets_uk.index(pet)] if pet in pets_uk else pet

page_url = f"https://www.olx.ua/uk/nedvizhimost/kvartiry/dolgosrochnaya-arenda-kvartir/{city_en_value}/?currency=UAH&search%5Bfilter_float_price:from%5D={start_range}&search%5Bfilter_float_price:to%5D={end_range}&search%5Bfilter_enum_number_of_rooms_string%5D%5B0%5D={rooms_en_value}&search%5Bfilter_enum_pets%5D%5B0%5D={pet_en_value}"


def get_page_data(page_url):
    r = requests.get(page_url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    table = soup.find_all(class_="css-1sw7q4x")

    data = []

    for item in table:
        title_element = item.find(class_="css-16v5mdi")
        title = title_element.get_text() if title_element else None

        city_element = item.find(class_="css-veheph")
        city_en_value = city_element.get_text() if city_element else None

        price_element = item.find(class_="css-10b0gli er34gjf0")
        price = price_element.get_text() if price_element else None

        link_element = item.find(class_="css-rc5s2u")
        link = link_element["href"] if link_element else None

        data.append(
            {
                "title": title,
                "city": city_en_value,
                "price": price,
                "link": link,
            }
        )

    return data


def main():
    page_data = get_page_data(page_url)
    if page_data:
        write_csv(page_data)


def write_csv(data):
    with open("file.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


if __name__ == "__main__":
    main()
