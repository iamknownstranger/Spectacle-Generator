import json
import numpy as np
from skimage.draw import *
from skimage.io import *
from PIL import Image

"""
Jotter AI Problem Statement Solution
    Automated Spectacle Generation
        Teckzite 2020
        RGUKT Nuzvid
        @author Chandra Sekhar Mullu
                N160252
                E2-CSE3
        @co-author Ponith Atthili
                N160226
                E2-CSE3
"""

class SpectacleGenerator:
    """
    Generates spectacles according to the measurements specified in the json file
  """

    def __init__(self, json_file, outfile_name):
        """
        Reading the data from the json_file and assigning data to variables
    """
        with open(json_file, 'rb') as f:
            data = json.load(f)

        if data['lens']['type'] == "round":
            diameter = data['lens']['diameter']
            bridge_w = data['bridge_w']
            bridge_h = data['bridge_h']
            temple_holder_h = data['temple_holder_h']
            temple_holder_w = data['temple_holder_w']
            frame_color = data['color']['frame']
            lens_color = data['color']['lens']

            self.image_array = self.generate_round_spectacle(
                diameter, bridge_w, bridge_h, temple_holder_h, temple_holder_w,
                frame_color, lens_color)
            image = Image.fromarray(self.image_array)
            image.save(outfile_name)

        if data['lens']['type'] == "rectangle":
            height = data['lens']['height']
            width = data['lens']['width']
            bridge_w = data['bridge_w']
            bridge_h = data['bridge_h']
            temple_holder_h = data['temple_holder_h']
            temple_holder_w = data['temple_holder_w']
            frame_color = data['color']['frame']
            lens_color = data['color']['lens']

            self.image_array = self.generate_rectangle_spectacle(
                height, width, bridge_w, bridge_h, temple_holder_h,
                temple_holder_w, frame_color, lens_color)
            im = Image.fromarray(self.image_array)
            im.save(outfile_name)

    def hex_to_rgb(self, color):
        """
      converts the given color in hex string format to rgb values
      return rgb values in a tuple
    """
        rgb = color.lstrip('#')
        return tuple(int(rgb[i:i + 2], 16) for i in (0, 2, 4))

    def generate_rectangle_spectacle(self, height, width, bridge_w, bridge_h,
                                     temple_holder_h, temple_holder_w,
                                     frame_color, lens_color):
        """
      generates a spectacle image with the given measurements in the json file
      measurements
        height,
        width,
        bridge_w,
        bridge_h,
        temple_holder_h,
        temple_holder_w,
        frame_color,
        lens_color
    """

        # intializing 4 empty arrays of size 256 * 512 to store the values 
        imgr = np.zeros((256, 512), dtype=np.uint8)
        imgg = np.zeros((256, 512), dtype=np.uint8)
        imgb = np.zeros((256, 512), dtype=np.uint8)
        imga = np.zeros((256, 512), dtype=np.uint8)

        # converting the measurement values from json to appropriate values in centimeter
        height = int(height * 36)
        width = int(width * 36)
        bridge_w = int(bridge_w * 36)
        bridge_h = int(bridge_h * 36)
        temple_holder_h = int(temple_holder_h * 36)
        temple_holder_w = int(temple_holder_w * 36)

        # converting the color values in hex string format to RGB values
        frame_red, frame_green, frame_blue = self.hex_to_rgb(frame_color)
        lens_red, lens_green, lens_blue = self.hex_to_rgb(lens_color)

        # calculating the co-ordinates of the bridge aligning it to the center of the image
        bridge_start = (int(128 - (bridge_h) / 2), int(256 - (bridge_w /2 - temple_holder_w / 1.5)))
        bridge_end = (int(128 + (bridge_h) / 2), int(256 + (bridge_w /2) - temple_holder_w / 1.5))

        # obtaining the co-ordinates of the bridge
        bridger, bridgec = rectangle(bridge_start, bridge_end)

        # co-ordinates to the lenses
        lens1_start = (int(128 - (height / 2)), int(256 - (bridge_w / 2)))
        lens1_end = (int(128 + (height / 2)),
                      int(256 - (bridge_w / 2) - width))

        lens2_start = (int(128 - (height / 2)), int(256 + (bridge_w / 2)))
        lens2_end = (int(128 + (height / 2)),
                      int(256 + (bridge_w / 2) + width))


        # obtaining the co-ordinates of lenses
        lens1r, lens1c = rectangle(lens1_start, lens1_end)
        lens2r, lens2c = rectangle(lens2_start, lens2_end)


        # calculating the co-ordinates of the frames
        frame1_start = (int(128 - (height / 2) - (temple_holder_w / 1.5)),
                        int(256 - (bridge_w / 2) + (temple_holder_w / 1.5)))
        frame1_end = (
            int(128 + (height / 2) + (temple_holder_w / 1.5)),
            int(256 - (bridge_w / 2) - width - (temple_holder_w / 1.5)))


        frame2_start = (int(128 - (height / 2) - (temple_holder_w / 1.5)),
                        int(256 + (bridge_w / 2) - (temple_holder_w / 1.5)))
        frame2_end = (
            int(128 + (height / 2) + (temple_holder_w / 1.5)),
            int(256 + (bridge_w / 2) + width + (temple_holder_w / 1.5)))
        
        # obtaining the co-ordinates of frame
        frame1r, frame1c = rectangle(frame1_start, frame1_end)
        frame2r, frame2c = rectangle(frame2_start, frame2_end)

        # calculating the co-ordinates of the temples
        temple_1_start = (int(128 - (temple_holder_h) / 2),
                          int(256 - width - ((temple_holder_w) * 4)))
        temple_1_end = (int(128 + (temple_holder_h) / 2),
                        int(256 - width - ((temple_holder_w) * 2.1)))

        temple_2_start = (int(128 - (temple_holder_h) / 2),
                          int(256 + width + ((temple_holder_w) * 4)))
        temple_2_end = (int(128 + (temple_holder_h) / 2),
                        int(256 + width + ((temple_holder_w) * 2.1)))

        # obtaing the co-ordinates of temples
        temple1r, temple1c = rectangle(temple_1_start, temple_1_end)

        temple2r, temple2c = rectangle(temple_2_start, temple_2_end)

        # coloring the values with respective colors in each arrays
        imgr[frame2r, frame2c] = frame_red
        imgr[frame1r, frame1c] = frame_red

        imgr[lens1r, lens1c] = lens_red
        imgr[lens2r, lens2c] = lens_red

        imgr[bridger, bridgec] = frame_red
        imgr[temple1r, temple1c] = frame_red
        imgr[temple2r, temple2c] = frame_red

        imgg[frame2r, frame2c] = frame_green
        imgg[frame1r, frame1c] = frame_green

        imgg[lens1r, lens1c] = lens_green
        imgg[lens2r, lens2c] = lens_green

        imgg[bridger, bridgec] = frame_green
        imgg[temple1r, temple1c] = frame_green
        imgg[temple2r, temple2c] = frame_green

        imgb[frame2r, frame2c] = frame_blue
        imgb[frame1r, frame1c] = frame_blue

        imgb[lens1r, lens1c] = lens_blue
        imgb[lens2r, lens2c] = lens_blue

        imgb[bridger, bridgec] = frame_blue
        imgb[temple1r, temple1c] = frame_blue
        imgb[temple2r, temple2c] = frame_blue

        # coloring the alpha channel having the lenses a bit transaparent
        imga[frame2r, frame2c] = 255
        imga[frame1r, frame1c] = 255
        imga[lens1r, lens1c] = 50
        imga[lens2r, lens2c] = 50

        imga[bridger, bridgec] = 255
        imga[temple1r, temple1c] = 255
        imga[temple2r, temple2c] = 255

        # an array of the desired size image
        final_image = np.zeros((256, 512, 4), dtype=np.uint8)

        # appending the color arrays RGBA to complete the final image
        final_image[:, :, 0] = imgr
        final_image[:, :, 1] = imgg
        final_image[:, :, 2] = imgb
        final_image[:, :, 3] = imga

        # imshow(final_image)
        # imsave('test.png', final_image)
        return final_image

    def generate_round_spectacle(self, diameter, bridge_w, bridge_h,
                                 temple_holder_h, temple_holder_w, frame_color,
                                 lens_color):
        """
      generates a spectacle image with the given measurements in the json file
      measurements
        diameter,
        bridge_w,
        bridge_h,
        temple_holder_h,
        temple_holder_w,
        frame_color,
        lens_color
    """

        # intializing 4 empty arrays of size 256 * 512 to store the values 
        imgr = np.zeros((256, 512), dtype=np.uint8)
        imgg = np.zeros((256, 512), dtype=np.uint8)
        imgb = np.zeros((256, 512), dtype=np.uint8)
        imga = np.zeros((256, 512), dtype=np.uint8)

        # converting the measurement values from json to appropriate values in centimeter
        radius = (diameter * 36) / 2
        bridge_w = int(bridge_w * 36)
        bridge_h = int(bridge_h * 36)
        temple_holder_h = int(temple_holder_h * 36)
        temple_holder_w = int(temple_holder_w * 36)

        # converting the color values in hex string format to RGB values
        frame_red, frame_green, frame_blue = self.hex_to_rgb(frame_color)
        lens_red, lens_green, lens_blue = self.hex_to_rgb(lens_color)

        # calculating the co-ordinates of the bridge aligning it to the center of the image
        bridge_start = (int(128 - (bridge_h) / 2), int(256 - (bridge_w / 2)))
        bridge_end = (int(128 + (bridge_h) / 2), int(256 + (bridge_w / 2)))

        # obtaining the co-ordinates of the bridge
        bridger, bridgec = rectangle(bridge_start, bridge_end)

        # co-ordinates to the lenses
        lens1r, lens1c = circle(128, 256 - radius - (bridge_w / 2), radius)
        lens2r, lens2c = circle(128, 256 + radius + (bridge_w / 2), radius)


        # obtaining the co-ordinates of frame
        frame1r, frame1c = circle(128, 256 - radius - (bridge_w / 2),
                                  radius + (temple_holder_w / 1.5))
        frame2r, frame2c = circle(128, 256 + radius + (bridge_w / 2),
                                  radius + (temple_holder_w / 1.5))

        # calculating the co-ordinates of the temples
        temple_1_start = (
            int(128 - temple_holder_h / 2),
            int(256 - (bridge_w / 2) - radius * 2 - (temple_holder_w * 2)))
        temple_1_end = (
            int(128 + temple_holder_h / 2),
            int(256 - (bridge_w / 2) - radius * 2 - temple_holder_w / 2))
        
        temple_2_start = (
            int(128 - (temple_holder_h) / 2),
            int(256 + (bridge_w / 2) + radius * 2 + (temple_holder_w) * 2))
        temple_2_end = (
            int(128 + (temple_holder_h) / 2),
            int(256 + (bridge_w / 2) + radius * 2 + (temple_holder_w) / 2))

        # obtaing the co-ordinates of temples
        temple1r, temple1c = rectangle(temple_1_start, temple_1_end)
        temple2r, temple2c = rectangle(temple_2_start, temple_2_end)

        # coloring the values with respective colors in each arrays
        imgr[frame1r, frame1c] = frame_red
        imgr[frame2r, frame2c] = frame_red

        imgr[lens1r, lens1c] = lens_red
        imgr[lens2r, lens2c] = lens_red

        imgr[bridger, bridgec] = frame_red
        imgr[temple1r, temple1c] = frame_red
        imgr[temple2r, temple2c] = frame_red

        imgg[frame1r, frame1c] = frame_green
        imgg[frame2r, frame2c] = frame_green 

        imgg[lens1r, lens1c] = lens_green
        imgg[lens2r, lens2c] = lens_green

        imgg[bridger, bridgec] = frame_green
        imgg[temple1r, temple1c] = frame_green
        imgg[temple2r, temple2c] = frame_green

        imgb[frame2r, frame2c] = frame_blue
        imgb[frame1r, frame1c] = frame_blue

        imgb[lens1r, lens1c] = lens_blue
        imgb[lens2r, lens2c] = lens_blue

        imgb[bridger, bridgec] = frame_blue
        imgb[temple1r, temple1c] = frame_blue
        imgb[temple2r, temple2c] = frame_blue

        # coloring the alpha channel having the lenses a bit transaparent
        imga[frame2r, frame2c] = 255
        imga[frame1r, frame1c] = 255

        imga[lens1r, lens1c] = 50
        imga[lens2r, lens2c] = 50

        imga[bridger, bridgec] = 255

        imga[temple1r, temple1c] = 255
        imga[temple2r, temple2c] = 255

        # an array of the desired size image
        final_image = np.zeros((256, 512, 4), dtype=np.uint8)

        # appending the color arrays RGBA to complete the final image
        final_image[:, :, 0] = imgr
        final_image[:, :, 1] = imgg
        final_image[:, :, 2] = imgb
        final_image[:, :, 3] = imga

        # imshow(final_image)
        # imsave('test.png', final_image)
        return final_image
if __name__ == "__main__":

    # Testing
    SpectacleGenerator("rectangle_glasses.json", "rectange_spectacle.png")
    SpectacleGenerator("round_glasses.json", "round_spectacle.png")
