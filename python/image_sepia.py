import os
from PIL import Image

files_path = input("Please type in the path of the image files: ")

for filename in os.listdir(files_path):
    with Image.open(os.path.join(files_path, filename)) as img:
        width, height = img.size
        pixels = img.load()

        for x in range(0, width):
            for y in range(0, height):
                R, G, B = pixels[x, y]
                newR = int (R * 0.393 + G * 0.769 + B * 0.189)
                newG = int (R * 0.349 + G * 0.686 + B * 0.168)
                newB = int (R * 0.272 + G * 0.534 + B * 0.131)

                pixels[x, y] = (newR, newG, newB)

    base, ext = os.path.splitext(filename)
    save_path = os.path.join(files_path, base + "_sepia" + ext)
    img.save(save_path)