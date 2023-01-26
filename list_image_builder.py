import os
from urllib.request import urlopen
from PIL import Image

""" 
    img = ListImageBuilder()
    img.downloadFromDC("DQioj")
    img.downloadFromDC("ZDltg")
    img.downloadFromDC("EtvVW")
    img.buildTable(200, 200, "table.png") """


def downloadFile(source, target):
    with open(target, "wb") as file:
        with urlopen(source) as response:
            file.write(response.read())


class ListImageBuilder:
    folder = "./images"

    # create ./images/ folder if it doesn't exist
    def ensureFolderExists(self):
        if os.path.isdir(self.folder) is False:
            os.makedirs(self.folder)

    def getCode(self, file: str):
        return file.split(".")[0]

    def downloadFromDC(self, code):
        target = self.folder + "/" + code + ".gif"

        # cached - already exists on server
        if os.path.isfile(target):
            return

        # we haven't downloaded it, so get to it.
        print("Downloading " + code)
        downloadFile(
            "https://dragcave.net/image/{code}.gif".format(code=code), target)

    def buildTable(self, height, width, dest):
        print('dest', dest)
        eggsize = {"w": 26, "h": 28}
        textWidth = 30
        colWidth = eggsize["w"] + textWidth

        # calculate how many columns across
        cols = width % colWidth
        base = Image.new('RGB', (500, 100), (250, 250, 250))

        images = os.listdir("./images/")

        print(images)
        i = 0
        for file in images:
            with Image.open("./images/" + file) as sprite:
                x = colWidth * i
                y = 0
                base.paste(sprite, (x, y))
            i += 1

        print('dest', dest)
        base.save(dest, "PNG")
