from PIL import Image, ImageFont, ImageDraw
import textwrap


def decode_image(file_location="images/UG_encode.png"):
    encoded_image = Image.open(file_location)
    red_channel = encoded_image.split()[0]

    x_size = encoded_image.size[0]
    y_size = encoded_image.size[1]

    decoded_image = Image.new("RGB", encoded_image.size)
    pixels = decoded_image.load()

    for i in range(x_size):
        for j in range(y_size):
            if bin(red_channel.getpixel((i, j)))[-1] == '0':
                pixels[i, j] = (255, 255, 255)
            else:
                pixels[i, j] = (0, 0, 0)

    decoded_image.save("images/UG_decode.png")


def write_text(text_to_write, image_size):
    image_text = Image.new("RGB", image_size)
    font = ImageFont.load_default().font
    drawer = ImageDraw.Draw(image_text)

    margin = offset = 10
    for line in textwrap.wrap(text_to_write, width=60):
        drawer.text((margin, offset), line, font=font)
        offset += 10
    return image_text


def encode_image(text_to_encode, template_image="images/UG.jpg"):
    image = Image.open(template_image)
    text = write_text(text_to_encode, image.size)
    bw_encode = text.convert('1')
    encoded_image = Image.new("RGB", image.size)
    pixels = encoded_image.load()
    r = image.split()[0]
    g = image.split()[1]
    b = image.split()[2]
    for i in range(0, image.size[0]):
        for j in range(0, image.size[1]):
            r_bin = bin(r.getpixel((i, j)))
            text = bin(bw_encode.getpixel((i, j)))
            if text[-1] == '1':
                new = ''
                for k in range(0, len(r_bin) - 1):
                    new += r_bin[k]
                new += '1'
                r_bin = new
            else:
                new = ''
                for k in range(0, len(r_bin) - 1):
                    new += r_bin[k]
                new += '0'
                r_bin = new
            pixels[i, j] = (int(r_bin, 2), g.getpixel((i, j)), b.getpixel((i, j)))
    encoded_image.save("images/UG_encode.png")


if __name__ == '__main__':
    print("Encoding the image...")
    encode_image("tekst")

    print("Decoding the image...")
    decode_image()
