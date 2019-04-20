import re
from PIL import Image
import requests
import random

class Mozaika:
    def __init__(self, args):
        self.args = args
        self.valid = False
        self.invalidArguments = []
        self.losowo = False
        self.rozdzielczosc = (2048, 2048)
        self.images = []
        self.color = (0,0,0)
        self.extractParameters()

    def extractParameters(self):
        self.validateParameters()

        if self.valid:
            self.losowo = True if self.args.get('losowo', '0') == '1' else False

            self.rozdzielczosc = tuple(map(int, self.args.get('rozdzielczosc', '2048x2048').split('x')))

            self.color = tuple(map(int, self.args.get('kolor', '0,0,0').split(',')))

            urls = self.args.get('zdjecia', None).split(',')
            self.images = [Image.open(requests.get(url, stream=True).raw) for url in urls]


    def validateParameters(self):
        self.valid = True
        self.errorMessage = ''

        if not re.match('\d+', self.args.get('losowo', '0')):
            self.valid = False
            self.invalidArguments.append('losowo')

        if not re.match('\d+x\d+', self.args.get('rozdzielczosc', '2048x2048')):
            self.valid = False
            self.invalidArguments.append('rozdzielczosc')

        if not re.match('\d+,\d+,\d+', self.args.get('kolor', '0,0,0')):
            self.valid = False
            self.invalidArguments.append('kolor')

        urlsRegex = '(?:http(s)?:\/\/)?[\w.-]+(?:\.[\w\.-]+)+[\w\-\._~:/?#[\]@!\$&\'\(\)\*\+,;=.]+$'
        zdjecia = self.args.get('zdjecia', '')

        if not re.match(urlsRegex, zdjecia) or not len(zdjecia.split(',')) <=8:
            self.valid = False
            self.invalidArguments.append('zdjecia')

    def generateImage(self):
        output_image = Image.new('RGB', self.rozdzielczosc, self.color)
        self.validateParameters()

        if self.valid:
            positions = []

            if self.losowo:
                random.shuffle(self.images)


            number_of_images = len(self.images)

            if number_of_images == 1:
                rows = 1
                columns = 1

                positions = [(0,0)]

            elif number_of_images % 2 == 0:
                rows = 2
                columns = int(number_of_images/2)

                for i in range(columns):
                    for j in range(rows):
                        positions.append((i,j))

            elif number_of_images == 3:
                rows = 2
                columns = 2

                positions = [(0,0),(0,1),(1,1)]

            elif number_of_images == 5:
                rows = 3
                columns = 3

                for i in range(columns):
                    for j in range(rows):
                        positions.append((i,j))

                for index in range(1, 5):
                    positions.pop(index)

            elif number_of_images == 7:
                rows = 3
                columns = 3

                for i in range(columns):
                    for j in range(rows):
                        positions.append((i,j))

                positions.pop(0)
                positions.pop(-1)

            block_x_size = int(output_image.size[0]/columns)
            block_y_size = int(output_image.size[1]/rows)

            for image, position in zip(self.images, positions):
                image = image.resize((block_x_size, block_y_size))
                output_image.paste(image, (position[0]*block_x_size, position[1]*block_y_size))

            actual_x_size = block_x_size * columns
            actual_y_size = block_y_size * rows

            if actual_x_size != self.rozdzielczosc[0] or actual_y_size != self.rozdzielczosc[1]:
                image_region = output_image.crop((0, 0, actual_x_size, actual_y_size))
                output_image = Image.new('RGB', (actual_x_size, actual_y_size))
                output_image.paste(image_region, (0,0))
                output_image = output_image.resize(self.rozdzielczosc)

        return output_image