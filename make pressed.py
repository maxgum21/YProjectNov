from PIL import Image


def darken(source, dest, am):
    pic = Image.open(source)
    p = pic.load()
    x, y = pic.size

    for i in range(x):
        for j in range(y):
            r, g, b = p[i, j]
            c = (r + g + b) // 3 - am
            p[i, j] = c, c, c

    pic.save(dest)


# def jpgToPng(jpg, png):
#     im = Image.open(jpg)
#     im.save(png)


for i in range(16):
    darken(f'KeyImgs/Key{i + 1}.jpg', f'KeyImgsPressed/KeyP{i + 1}.jpg', 40)
    # jpgToPng(f'KeyImgs/Key{i + 1}.jpg', f'KeyImgs/Key{i + 1}.png')

#  darken('KeyAddPressed.jpg', 'KeyAddPressed.jpg', 0)
