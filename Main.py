import requests
import random
from PIL import Image

def get_random_image():
    url = "https://commons.wikimedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "generator": "random",
        "grnnamespace": "6",
        "prop": "imageinfo",
        "iiprop": "url"
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    pages = data["query"]["pages"]
    image_info = next(iter(pages.values()))["imageinfo"][0]
    image_url = image_info["url"]
    img = Image.open(image_url)
    
    return image_url

def save_image(image_url, file_name):
    image_response = requests.get(image_url)
    with open(file_name, 'wb') as file:
        file.write(image_response.content)

if __name__ == "__main__":
    image_url = get_random_image()
    print(f"Random Image URL: {image_url}")
    save_image(image_url, "random_image.jpg")

def get_hexes(img): 
    pixels = img.load()
    width, height = img.size
    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x,y]