import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from textblob import TextBlob
import cv2
import description as ds

# Read from the text file
file = open('speech.txt', 'rt')
temp_lst = file.readlines()
text = '\n'.join(temp_lst).strip()

# Define the 3-word input and sentiment analysis rating
input_str = ds.generate_description(text)
sentiment_rating = ds.get_sentiments(text)

# Define the Google Image Search API endpoint and query parameters
api_endpoint = "https://www.googleapis.com/customsearch/v1"
api_key = "AIzaSyBzanGRpltEDOomXrkrvP3c_mvLtfIh3cg"
search_engine_id = "b3fdb9739a8c444de"

# Define the image size for each downloaded image
image_size = (256, 256)

# Define the weight for each image when combining
image_weights = [0.5, 0.3, 0.2]

# Define the color adjustments based on the sentiment rating
if sentiment_rating > 0:
    saturation_factor = 1.2
    brightness_factor = 1.1
    text_color = (255, 255, 255)
else:
    saturation_factor = 0.8
    brightness_factor = 0.9
    text_color = (0, 0, 0)

# Initialize an empty list to store the pixel arrays of the downloaded images
pixel_arrays = []

# Loop over each word in the input and download an image for it
for i, word in enumerate(input_str.split()):
    # Define the query parameters for the Google Image Search API
    params = {
        "key": api_key,
        "cx": search_engine_id,
        "q": word,
        "imageSize": "large",
        "searchType": "image",
        "num": 1,
        "imgType": "photo"
    }

    # Make a GET request to the Google Image Search API
    response = requests.get(api_endpoint, params=params)
    print(response.json())
    
    # Parse the response to extract the URL of the first image result
    image_url = response.json()["items"][0]["link"]
    # Download the image and open it using PIL
    try:
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))
    except Exception as e:
        print(f"Error opening image: {e}")
        print(f"Response content: {response.content}")

    # Resize the image to a fixed size
    img = img.resize(image_size)

    # Convert the image to a numpy array of pixels
    pixel_array = np.array(img)

    # Convert the pixel array to uint8
    pixel_array = np.uint8(pixel_array)

    # Add the pixel array to the list of pixel arrays
    pixel_arrays.append(pixel_array)

# Get the height and width of the pixel arrays from the first downloaded image
image_height, image_width, _ = pixel_arrays[0].shape

# Combine the pixel arrays into a single array, using the weights defined earlier
# Combine the pixel arrays into a weighted average
combined_pixel_array = np.zeros((image_height, image_width, 3), dtype=np.float32)
for i, pixel_array in enumerate(pixel_arrays):
    combined_pixel_array += image_weights[i] * pixel_array

# Normalize the combined pixel array to a depth of CV_8U
combined_pixel_array *= 255.0 / np.max(combined_pixel_array)
combined_pixel_array = combined_pixel_array.astype(np.uint8)

# Convert the pixel array to an image and resize it to a larger size
img = Image.fromarray(combined_pixel_array)
img = img.resize((512, 512))

# Adjust the color scheme of the resulting image based on the sentiment analysis rating
hsv_img = cv2.cvtColor(combined_pixel_array, cv2.COLOR_RGB2HSV)
hsv_img[:, :, 1] = np.clip(hsv_img[:, :, 1] * saturation_factor, 0, 255)
hsv_img[:, :, 2] = np.clip(hsv_img[:, :, 2] * brightness_factor, 0, 255)
combined_pixel_array = cv2.cvtColor(hsv_img, cv2.COLOR_HSV2RGB)

# Convert the pixel array to an image and resize it to a larger size
img = Image.fromarray(combined_pixel_array)
img = img.resize((512, 512))

# Add text to the image indicating the input and sentiment rating
draw = ImageDraw.Draw(img)


# Save the resulting image to a file
img.save(f"{input_str.replace(' ', '_')}_{sentiment_rating:.2f}.png")
