import cv2, os
import numpy as np
from create_ascii_images import PIXEL_H, PIXEL_W
from random import randint as r

# Constants
PIXELS_AMOUNT = PIXEL_H*PIXEL_W

# Preload ASCII images
ascii_images_dict_gray = {}
for i in range(32, 127):
   image = cv2.imread(f'ascii/{i}.jpg')
   ascii_images_dict_gray[i] = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
ascii_images_dict_colour = {}
for i in range(32, 127):
   filepath = os.path.join('ascii', f'{i}.jpg')
   ascii_images_dict_colour[i] = cv2.imread(filepath, cv2.IMREAD_COLOR)

def mse(img1, img2):
   diff = cv2.subtract(img1, img2)
   err = np.sum(diff**2)
   mse = err/(float(PIXELS_AMOUNT))
   return mse

def pixel_match(pixel, colour, random):
   if colour:
      pixel_bw = cv2.cvtColor(pixel, cv2.COLOR_BGR2GRAY)
      best_match_image_rgb = None
   else:
      pixel_bw = pixel
   best_match_image_gray = None
   best_match_error = float('inf')
   if random:
      ri = r(32, 126)
      best_match_image_rgb = ascii_images_dict_colour[ri]
      best_match_image_gray = ascii_images_dict_gray[ri]
   else:
      for i in range(32, 127):
         # Load the current image and convert it to grayscale
         ascii_img = ascii_images_dict_gray[i]
         
         # Compute the difference between the pixel and the ASCII image
         diff = cv2.absdiff(pixel_bw, ascii_img)

         # Compute the sum of the difference
         s = np.sum(diff)

         if s < best_match_error:
            if colour:
               filepath = os.path.join('ascii', f'{i}.jpg')
               best_match_image_rgb = cv2.imread(filepath, cv2.IMREAD_COLOR)
               # best_match_image_rgb = ascii_images_dict_colour[i]
            best_match_image_gray = ascii_img
            best_match_error = s

   if colour:
      # Change colours
      avg_rgb = np.mean(pixel, axis=(0,1))

      # Define the threshold for white color
      white_threshold = 240

      # Create a mask for pure white pixels
      mask = cv2.inRange(best_match_image_rgb, (white_threshold, white_threshold, white_threshold), (255, 255, 255))

      # Apply avg_rgb to all pure white pixels in the mask
      best_match_image_rgb[np.where(mask == 255)] = avg_rgb.astype(np.uint8)

      return best_match_image_rgb
   else:
      return best_match_image_gray

def contrast(img):
   # Convert to grayscale
   gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

   # Increase the contrast by a factor of
   alpha = 3
   beta = 0
   adjusted = cv2.convertScaleAbs(gray, alpha=alpha, beta=beta)
   
   darkened_img = cv2.multiply(adjusted, 0.5)
   final = darkened_img.astype(np.uint8)
   
   return final

class Image:
   OUTFOLDER = 'ascii_images'
   def __init__(self, image, colour: bool, random, log) -> None:
      self.random = random
      self.log = log
      self.colour = colour
      if not colour:
         self.image = contrast(image)
         self.height, self.width = self.image.shape
      else:
         self.image = image
         self.height, self.width, _ = self.image.shape
      self.pixel_matrix = self.create_pixel_matrix()
      self.ascii_image = self.create_ascii_image()

   def create_ascii_image(self):
      # Create matrix
      ascii_matrix = []
      rows = len(self.pixel_matrix)
      row_i = 1
      if self.log:
         print('     Creating Rows')
      for row in self.pixel_matrix:
         arow = []
         for pixel in row:
            arow.append(pixel_match(pixel, self.colour, random=self.random))
         ascii_matrix.append(arow)
         if self.log:
            print('        %i/%i' % (row_i, rows))
         row_i += 1
      print()
      
      # Create image
      rows = []
      for row in ascii_matrix:
         row_img = cv2.hconcat(row)
         if not (row_img is None):
            rows.append(row_img)
           
      image = cv2.vconcat(rows)
      return image

   def create_pixel_matrix(self) -> list:
      row = -1
      col = -1
      pixel_matrix = []
      for y in range(0, self.height, PIXEL_H):
         arow = []
         row += 1
         for x in range(0, self.width, PIXEL_W): 
            col += 1
            yf = y+PIXEL_H
            xf = x+PIXEL_W
            pixel = self.image[y:yf, x:xf]
            if self.colour:
               pixel_h, pixel_w, _ = pixel.shape
            else:
               pixel_h, pixel_w = pixel.shape
            if pixel_h == PIXEL_H and pixel_w == PIXEL_W:
               arow.append(pixel)
         pixel_matrix.append(arow)
      return pixel_matrix

def save_image(image, outname):
   print('  Saving image\n')
   path_out = Image.OUTFOLDER + f'/{outname}_ascii.jpg'
   cv2.imwrite(path_out, image)
   print('  Image saved in ' + path_out)

def filter(image, colour=True, random=False, log=False):
   main_image = Image(image, colour, random=random, log=log)
   return main_image.ascii_image

if __name__ == '__main__':
   imgname = 'nyan'
   imagepath = f'images/{imgname}.jpg'
   image = cv2.imread(imagepath)
   ascii_img = filter(image, colour=True)
   save_image(ascii_img, imgname)
cv2.destroyAllWindows()