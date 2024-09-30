import requests
from bs4 import BeautifulSoup
import random

url = "https://povar.ru/list/salad/"

response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.text, 'html.parser')

# Извлечение информации о 5 блюдах
dishes = []
for item in soup.select('.recipe')[:8]:
    name = item.select_one('.listRecipieTitle').get_text(strip=True)
    link = 'https://povar.ru'+item.select_one('a')['href']
    image = item.select_one('span.a img[src]')['src']
    rating = random.randint(1, 10)

    dishes.append({
        "name": name,
        "rating": rating,
        "recipe_link": link,
        "image_src": image
    })

html_content = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="style.css">
    <title>Список Салатов</title>
</head>
<body>
    <h1>Список Салатов</h1>
    <div class="cards">
"""
for dish in dishes:
    html_content += (f"\n"
                     f"        <div class=\"card\">\n"
                     f"           <div class=\"photo\">\n"
                     f"               <img src=\"{dish['image_src']}\" alt=\'{dish['name']}\'>\n"
                     f"           </div>\n"
                     f"           <div class=\"info\">\n"
                     f"                <h1 class=\"name\">{dish['name']}</h1>               \n"
                     f"                <a href=\"{dish['recipe_link']}\" target=\"_blank\">Рецепт</a>\n"
                     f"                <p class=\"rating\">Оценка: {dish['rating']}</p>\n"
                     f"           </div>\n"
                     f"        </div>\n"
                     f"     ")

html_content += """
    </div>
</body>
</html>
"""

with open("salads.html", "w", encoding="utf-8") as file:
    file.write(html_content)

print("Файл 'salads.html' успешно создан.")