from PIL import Image
from PIL import ImageSequence
from PIL import ImageFont
from PIL import ImageDraw
import time


lighting = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", ".", " "]
lighting.reverse()
lightRange = 255/(len(lighting) - 1)


def ResizeImage(image, boundary):
    width, height = image.size
    highest = width if width > height else height
    ratio = boundary / highest
    newheight = round(height * ratio)
    newwidth = round(width * ratio)

    return image.resize((newwidth, newheight))


def GetLight(value):
    index = round(value/lightRange)
    return lighting[index]+" "


def GetDotLight(value):
    if value > 100:
        return "."
    
    return ""


def ToAscii(image, resize=None):
    if resize:
        image = ResizeImage(image, resize)

    image = image.convert("RGBA")
    txt = ""
    width, height = image.size

    for y in range(height):
        for x in range(width):
            r, g, b, a = image.getpixel((x, y))
            color = round((r + g + b) / 3) * (a / 255)
            txt += str(GetLight(color))
        if y != height-1:
            txt += "\n"

    return txt


def GifToAscii(gif, resize=None):
    frames = ImageSequence.Iterator(gif)
    index = 0
    frames_list = []
    for frame in frames:
        if resize:
            frame = ResizeImage(frame, resize)
        frames_list.append((ToAscii(frame)))
        index += 1

    return frames_list

def ImageToAsciiImage(image, path, resize=None):
    AsciiToImage(ToAscii(image, resize), 16).save(path)


def AsciiToImage(string, textSize):
    start = time.time()
    chars = string.split("\n")
    width = round(len(chars[0]) / 2)
    heigth = len(chars)

    image = Image.new("RGB", (width*textSize, heigth*textSize), (0, 0, 0))

    font = ImageFont.truetype("consolab.ttf", textSize)
    draw = ImageDraw.Draw(image)

    for y in range(heigth):
        for x in range(width):
            draw.text((x * textSize, y * textSize), chars[y][x * 2], (255, 255, 255), font)


   #  print("image time: ", (time.time() - start))
    return image


def GifToAsciiGif(gif, path, res=None):
    start_time = time.time()
    frames = ImageSequence.all_frames(gif)
    ascii_frames = []

    print(len(frames), " Frames total")
    index = 0
    for frame in frames:
        frame_time = time.time()
        index += 1
        if res:
            txt = ToAscii(frame, res)

        else:
            txt = ToAscii(frame)

        ascii_frames.append(AsciiToImage(txt, 16))
        print("frame" + str(index) + " time: %.2f" % (time.time() - frame_time))

    ascii_frames[0].save(path, save_all=True, append_images=ascii_frames[1:], duration = gif.info["duration"], loop=0)
    print("time elapsed: %.2f" % (time.time() - start_time), "seconds")


# ImageToAsciiImage(image, "ascii.png", 200)
# GifToAsciiGif(gif, "ascii.gif", 200)

# with open("ascii.txt", "w") as f:
#     f.write(ToAscii(image, 50))
