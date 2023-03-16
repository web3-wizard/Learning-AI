import os
import time
import requests
import random
from bs4 import BeautifulSoup
import ctypes

# Set your wallpaper genres here
# genres = ["nature", "cars", "words", "space", "vector", "love", "dark", "city", "hi-tech", "abstract"]


# Set the time interval in seconds for changing the wallpaper
time_interval = 10


def set_wallpaper(image_path):
    """Set the desktop wallpaper using the given image path"""
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER, 0, image_path, 0)


page = 2

while True:
    # Choose a random genre
    # genre = genres[random.randint(0, len(genres)-1)]
    genre = "nature"  # vector  minimalism  food

    # Set the URL of the website that generates random wallpapers for the genre
    url = f"https://wallpaperscraft.com/catalog/{genre}/3840x2400/page{page}"
    print("url : ", url)
    print("*" * 50)

    # Fetch the webpage content
    response = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the image links
    image_links = soup.find_all('a', {'class': 'wallpapers__link'})

    for image_link in image_links:
        # Choose a random image link
        # random_link = image_links[random.randint(0, len(image_links)-1)]
        random_link = image_link
        # print("random link : ", random_link['href'])
        # print("*" * 50)

        # Fetch the image file from the link
        image_url = "https://images.wallpaperscraft.com/image/single/" + \
            random_link['href'].split('/')[2] + "_3840x2400.jpg"

        print("Image URL: ", image_url)
        print("*" * 50)

        response = requests.get(image_url)

        image_name = random_link['href'].split('/')[2] + "_rahul.jpg"

        # Save the image to a file
        image_path = os.path.join(os.path.expanduser(
            '~'), 'Pictures\\Random-bg', image_name)
        with open(image_path, 'wb') as f:
            f.write(response.content)

        # Set the wallpaper
        set_wallpaper(image_path)

        # Wait for the specified time interval before changing the wallpaper again
        time.sleep(time_interval)

    if page == 6:
        print("done")
        break
    else:
        page += 1
