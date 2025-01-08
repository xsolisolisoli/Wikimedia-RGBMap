import requests
import random
from PIL import Image, UnidentifiedImageError
from io import BytesIO
import urllib.request
import json
from pymongo import MongoClient

def get_extension(url_str):
    return '.' + url_str.split('.')[-1]

def get_random_image():
    url = "https://commons.wikimedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "generator": "random",
        "grnnamespace": "6",
        "prop": "imageinfo",
        "iiprop": "url|mime"
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    pages = data["query"]["pages"]
    image_info = next(iter(pages.values()))["imageinfo"][0]
    image_url = image_info["url"]
    
    # Ensure the URL points to an image
    if "mime" in image_info and image_info["mime"].startswith("image/"):
        image_response = requests.get(image_url)
        try:
            ext = get_extension(image_url)
            urllib.request.urlretrieve(image_url, "tmp"+ ext)

            img = Image.open("tmp" + ext) 
            img.verify()  
            img = Image.open("tmp" + ext) 
            return img
        except UnidentifiedImageError:
            print("Error: Cannot identify image file.")
            return None
    else:
        print("Error: URL does not point to an image.")
        return None
    
    return img

def save_image(image_url, file_name):
    image_response = requests.get(image_url)
    with open(file_name, 'wb') as file:
        file.write(image_response.content)

def rgb_to_hex(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'

def get_hexes(img): 
    pixels = img.load()
    width, height = img.size
    unique_hexes = set()
    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]
            hex_color = rgb_to_hex(r, g, b)
            unique_hexes.add(hex_color)
    return list(unique_hexes)

if __name__ == "__main__":
    conx = "your_mongodb_connection_string_here"
    client = MongoClient(conx)
    db = client['your_database_name']
    collection = db['your_collection_name']

    img = get_random_image()
    if img:
        img.show()  # Display the image
        image_url = img.filename
        print(f"Random Image URL: {image_url}")
        
        hex_colors = get_hexes(img)
        print(f"Unique Hex Colors: {hex_colors}")
        
        # Convert hex colors to JSON
        hex_colors_json = json.dumps(hex_colors)
        
        # Insert JSON into MongoDB
        collection.insert_one({"hex_colors": hex_colors_json})
        print("Hex colors inserted into MongoDB")