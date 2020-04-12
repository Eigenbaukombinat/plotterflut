from PIL import Image
import requests
import time

# the provided png needs to be grayscale already.

img = Image.open('yourfile.png')

maxx, maxy = img.size
startx = 18
starty = 48
print (img.size)

def max_bright():
    # find maximum color value
    cols = []
    for y in range(maxy):
        for x in range(maxx):
            cols.append(img.getpixel((x,y)))
    return max(cols)


def scalecol(i, maxb):
    return int(8/maxb*i)-1

def printit(only23=False):
    maxb = max_bright()
    for y in range(maxy):
        line = []
        for x in range(maxx):
            i = img.getpixel((x,y))
            i = maxb - i
            if i==0:
                i = 23
                line.append(' ')
            else:
                i = scalecol(i, maxb)
                line.append(str(i))
            ok = False
            while not ok:
                if only23 and i == 23:
                    res = requests.get(f'http://localhost:5000/plotterflut/api?x={x+startx}&y={y+starty}&intensity={i}')
                if not only23:
                    res = requests.get(f'http://localhost:5000/plotterflut/api?x={x+startx}&y={y+starty}&intensity={i}')
                if res.status_code == 200:
                    ok = True
                elif res.status_code == 402:
                    ok = True
                time.sleep(0.1)
        print(' '.join(line))

printit(True)
printit()
