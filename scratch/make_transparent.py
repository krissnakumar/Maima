
from PIL import Image
import sys

def make_transparent(image_path, output_path):
    img = Image.open(image_path).convert("RGBA")
    datas = img.getdata()

    new_data = []
    for item in datas:
        # If the pixel is mostly black, make it transparent
        if item[0] < 50 and item[1] < 50 and item[2] < 50:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)

    img.putdata(new_data)
    img.save(output_path, "PNG")

if __name__ == "__main__":
    make_transparent(sys.argv[1], sys.argv[2])
