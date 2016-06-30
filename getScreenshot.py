from os import listdir
from os.path import isfile, join
from random import randint
import requests
import requests.exceptions
from PIL import Image, ImageQt
import configuration


class ScreenshotError(Exception):
    pass


class Screenshot:
    VPS_URL = configuration.preview_server
    BACKGROUND_LOCATION = configuration.backgrounds
    PREFIX = configuration.prefix
    CROP_RECTANGLE = (0, 0, 1920 - int(configuration.hd_offset), 1080)
    PASTE_RECTANGLE = (int(configuration.hd_offset), 0)

    def __init__(self, scene_name, frame_index, mode):
        self.scene_name = scene_name

        if mode == 'frame':
            self.frame = "<fposition>%s</fposition>" % frame_index
        elif mode == 'named':
            self.frame = "<namedposition>%s</namedposition>" % frame_index
        elif mode == 'absolute':
            self.frame = "<absoluteposition>%s</absoluteposition>" % frame_index

        self.raw_image = None
        self.composite_image = None
        self.qt_image = None
        self._background = None

        self.__raw_image()
        self.__background()
        self.__composite_image()
        self.__qt_image()

    @property
    def __payload_string(self):
        settings = {'scene_name': self.PREFIX + self.scene_name,
                    'position': self.frame,
                    'seed': randint(0, 1000)}

        payload = {
            "sc": "SCENE*{scene_name}".format(**settings),
            "p": "<payload xmlns='http://www.vizrt.com/types'><field name='01'><value>{seed}</value></field></payload>".format(**settings),
            "s": "<snapshotrequest xmlns='http://www.vizrt.com/snapshotrequest'><position>{position}</position></snapshotrequest>".format(**settings)
        }
        return payload


    def __raw_image(self):

        try:
            image = self.__image(payload=self.__payload_string)
            tmp_background = Image.new('RGBA', (1920, 1080), (255, 255, 255, 0))
            tmp_background.paste(image.crop(self.CROP_RECTANGLE), self.PASTE_RECTANGLE)
            self.raw_image = tmp_background
        except:
            raise

    def __image(self, payload):
        viz_response = requests.get(self.VPS_URL, params=payload, stream=True)

        if viz_response.status_code == 200:
            return Image.open(viz_response.raw)
        elif viz_response.status_code == 404:
            raise FileNotFoundError

    def __composite_image(self):
        try:
            self.composite_image = Image.alpha_composite(self._background, self.raw_image)
        except:
            raise

    def __background(self):
        backgrounds = [join(self.BACKGROUND_LOCATION, f)
                       for f in listdir(self.BACKGROUND_LOCATION) if isfile(join(self.BACKGROUND_LOCATION, f))]

        if len(backgrounds) > 0:
            self._background = Image.open(backgrounds[randint(0, len(backgrounds)) - 1]).convert('RGBA')
        else:
            self._background = Image.new('RGB', (1920, 1080), (255, 255, 255))

    def __qt_image(self):
        try:
            self.qt_image = ImageQt.ImageQt(self.composite_image)
        except:
            raise


if __name__ == "__main__":
    image1 = Screenshot(scene_name='41769', frame_index='$2', mode='named')
    print(image1.composite_image.save("d:\s.jpg"))
