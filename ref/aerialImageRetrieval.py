import sys, io, os
from urllib import request
from PIL import Image
import os
from math import cos, sin, pi, log, atan, exp, floor
from itertools import chain
import re
import tqdm

class TileSystem(object):
    
    EARTHRADIUS = 6378137
    MINLAT, MAXLAT = -85.05112878, 85.05112878
    MINLON, MAXLON = -180., 180.
    MAXLEVEL = 23

    @staticmethod
    def clip(val, minval, maxval):
        return min(max(val, minval), maxval)

    @staticmethod
    def map_size(level):
        return 256 << level

    @staticmethod
    def ground_resolution(lat, level):
        lat = TileSystem.clip(lat, TileSystem.MINLAT, TileSystem.MAXLAT)
        return cos(lat * pi / 180) * 2 * pi * TileSystem.EARTHRADIUS / TileSystem.map_size(level)


    @staticmethod
    def map_scale (lat, level, screenDpi):
        return TileSystem.ground_resolution(lat, level) * screenDpi / 0.0254

    @staticmethod
    def latlong_to_pixelXY(lat, long, level):
        lat = TileSystem.clip(lat, TileSystem.MINLAT, TileSystem.MAXLAT)
        long = TileSystem.clip(long, TileSystem.MINLON,  TileSystem.MAXLON)

        x = (long + 180) / 360
        sinlat = sin(lat * pi / 180)
        y = 0.5 - log((1 + sinlat) / (1 - sinlat)) / (4 * pi)

        mapsize = TileSystem.map_size(level)
        pixelX, pixelY = floor(TileSystem.clip(x * mapsize + 0.5, 0, mapsize - 1)), \
                        floor(TileSystem.clip(y * mapsize + 0.5, 0, mapsize - 1))
        return pixelX, pixelY

    @staticmethod
    def pixelXY_to_latlong(pixelX, pixelY, level):
        mapsize = TileSystem.map_size(level)
        x = TileSystem.clip(pixelX, 0, mapsize - 1) / mapsize - 0.5
        y = 0.5 - 360 * TileSystem.clip(pixelY, 0, mapsize - 1) / mapsize

        lat = 90 - 360 * atan(exp(-y * 2 * pi)) / pi 
        long = 360 * x 
        return lat, long

    @staticmethod
    def pixelXY_to_tileXY(pixelX, pixelY):
        return floor(pixelX / 256), floor(pixelY / 256)

    @staticmethod
    def tileXY_to_pixelXY(tileX, tileY):
        return tileX * 256, tileY * 256

    @staticmethod
    def tileXY_to_quadkey(tileX, tileY, level):
        tileXbits = '{0:0{1}b}'.format(tileX, level)
        tileYbits = '{0:0{1}b}'.format(tileY, level)
        
        quadkeybinary = ''.join(chain(*zip(tileYbits, tileXbits)))
        return ''.join([str(int(num, 2)) for num in re.findall('..?', quadkeybinary)])
        #return ''.join(i for j in zip(tileYbits, tileXbits) for i in j)
        
    @staticmethod
    def quadkey_to_tileXY(quadkey):
        quadkeybinary = ''.join(['{0:02b}'.format(int(num)) for num in quadkey])
        tileX, tileY = int(quadkeybinary[1::2], 2), int(quadkeybinary[::2], 2)
        return tileX, tileY


BASEURL = "http://h0.ortho.tiles.virtualearth.net/tiles/h{0}.jpeg?g=131"
IMAGEMAXSIZE = 8192 * 8192 * 8 # max width/height in pixels for the retrived image
TILESIZE = 256              # in Bing tile system, one tile image is in size 256 * 256 pixels


class AerialImageRetrieval(object):
    def __init__(self, lat1, lon1, lat2, lon2):
        self.lat1 = lat1
        self.lon1 = lon1
        self.lat2 = lat2
        self.lon2 = lon2

        self.tgtfolder = './output/'
        try:
            os.makedirs(self.tgtfolder)
        except FileExistsError:
            pass
        except OSError:
            raise
        

    def download_image(self, quadkey):
        with request.urlopen(BASEURL.format(quadkey)) as file:
            return Image.open(file)



    def is_valid_image(self, image):
        if not os.path.exists('null.png'):
            nullimg = self.download_image('11111111111111111111')      # an invalid quadkey which will download a null jpeg from Bing tile system
            nullimg.save('./null.png')
        return not (image == Image.open('./null.png'))


    def max_resolution_imagery_retrieval(self):
        for levl in range(TileSystem.MAXLEVEL, 0, -1):
            pixelX1, pixelY1 = TileSystem.latlong_to_pixelXY(self.lat1, self.lon1, levl)
            pixelX2, pixelY2 = TileSystem.latlong_to_pixelXY(self.lat2, self.lon2, levl)

            pixelX1, pixelX2 = min(pixelX1, pixelX2), max(pixelX1, pixelX2)
            pixelY1, pixelY2 = min(pixelY1, pixelY2), max(pixelY1, pixelY2)

            
            #Bounding box's two coordinates coincide at the same pixel, which is invalid for an aerial image.
            #Raise error and directly return without retriving any valid image.
            if abs(pixelX1 - pixelX2) <= 1 or abs(pixelY1 - pixelY2) <= 1:
                print("Cannot find a valid aerial imagery for the given bounding box!")
                return

            if abs(pixelX1 - pixelX2) * abs(pixelY1 - pixelY2) > IMAGEMAXSIZE:
                print("Current level {} results an image exceeding the maximum image size (8192 * 8192), will SKIP".format(levl))
                continue
            
            tileX1, tileY1 = TileSystem.pixelXY_to_tileXY(pixelX1, pixelY1)
            tileX2, tileY2 = TileSystem.pixelXY_to_tileXY(pixelX2, pixelY2)

            # Stitch the tile images together
            result = Image.new('RGB', ((tileX2 - tileX1 + 1) * TILESIZE, (tileY2 - tileY1 + 1) * TILESIZE))
            retrieve_sucess = False
            for tileY in range(tileY1, tileY2 + 1):
                retrieve_sucess, horizontal_image = self.horizontal_retrieval_and_stitch_image(tileX1, tileX2, tileY, levl)
                if not retrieve_sucess:
                    break
                result.paste(horizontal_image, (0, (tileY - tileY1) * TILESIZE))

            if not retrieve_sucess:
                continue

            # Crop the image based on the given bounding box
            leftup_cornerX, leftup_cornerY = TileSystem.tileXY_to_pixelXY(tileX1, tileY1)
            retrieve_image = result.crop((pixelX1 - leftup_cornerX, pixelY1 - leftup_cornerY, \
                                        pixelX2 - leftup_cornerX, pixelY2 - leftup_cornerY))
            print("Finish the aerial image retrieval, store the image aerialImage_{0}.jpeg in folder {1}".format(levl, self.tgtfolder))
            filename = os.path.join(self.tgtfolder, 'aerialImage_{}.jpeg'.format(levl))
            retrieve_image.save(filename)
            return True
        return False    
            


    def horizontal_retrieval_and_stitch_image(self, tileX_start, tileX_end, tileY, level):
        imagelist = []
        for tileX in range(tileX_start, tileX_end + 1):
            quadkey = TileSystem.tileXY_to_quadkey(tileX, tileY, level)
            image = self.download_image(quadkey)
            if self.is_valid_image(image):
                imagelist.append(image)
            else:
                #print(quadkey)
                print("Cannot find tile image at level {0} for tile coordinate ({1}, {2})".format(level, tileX, tileY))
                return False, None
        result = Image.new('RGB', (len(imagelist) * TILESIZE, TILESIZE))
        for i, image in enumerate(imagelist):
            result.paste(image, (i * TILESIZE, 0))
        return True, result

def main():
    # decode the bounding box coordinates
    try:
        args = sys.argv[1:]
    except IndexError:
        sys.exit('Diagonal (Latitude, Longitude) coordinates of the bounding box must be input')
    if len(args) != 4:
        sys.exit('Please input Latitude, Longitude coordinates for both upper-left and lower-right corners!')
    
    try:
        lat1, lon1, lat2, lon2 = float(args[0]), float(args[1]), float(args[2]), float(args[3])
    except ValueError:
        sys.exit('Latitude and longitude must be float type')
    

    # Retrieve the aerial image
    imgretrieval = AerialImageRetrieval(lat1, lon1, lat2, lon2)
    if imgretrieval.max_resolution_imagery_retrieval():
        print("Successfully retrieve the image with maximum resolution!")
    else:
        print("Cannot retrieve the desired image! (Possible reason: expected tile image does not exist.)")


if __name__ == '__main__':
    main()

