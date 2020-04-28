from PIL import Image

offset = 0


class BMPImage:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        self.image = Image.new("RGB", (width, height))
        self.pixels = self.image.load()

        for i in range(self.image.size[0]):  # for every col:
            for j in range(self.image.size[1]):  # For every row
                # self.image.putpixel((i, j), (i, j, 100))
                # self.pixels[i, j] = (i, j, 200)  # set the colour accordingly
                self.pixels[i, j] = ((i + offset) % width, (j + offset) % height, offset % 25500)  # set the colour accordingly

    offset = (offset + 10)

    def tobmp(self) -> bytes:
        return self.image.tobitmap()
