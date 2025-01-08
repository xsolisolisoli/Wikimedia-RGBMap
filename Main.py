import requests
import random
from PIL import Image, UnidentifiedImageError
from io import BytesIO
import urllib.request

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
            urllib.request.urlretrieve( 
            'https://media.geeksforgeeks.org/wp-content/uploads/20210318103632/gfg-300x300.png', 
            "tmp.png") 

            img = Image.open(BytesIO(image_response.content))
            img.verify()  # Verify that it is, in fact, an image
            img = Image.open(BytesIO(image_response.content))  # Reopen the image
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

if __name__ == "__main__":
    img = get_random_image()
    if img:
        img.show()  # Display the image
        image_url = img.filename
        print(f"Random Image URL: {image_url}")
        save_image(image_url, "random_image.jpg")

def get_hexes(img): 
    pixels = img.load()
    width, height = img.size
    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x,y]