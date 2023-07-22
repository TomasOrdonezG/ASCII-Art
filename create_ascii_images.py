import cv2
import numpy as np
from PIL import ImageFont, Image, ImageDraw

def collage():
   # Load three images
   img1 = cv2.imread('ascii/' + str(ord('[')) + '.jpg')
   img2 = cv2.imread('ascii/' + str(ord('p')) + '.jpg')
   img3 = cv2.imread('ascii/' + str(ord('g')) + '.jpg')
   img4 = cv2.imread('ascii/' + str(ord('t')) + '.jpg')
   img5 = cv2.imread('ascii/' + str(ord('d')) + '.jpg')
   img6 = cv2.imread('ascii/' + str(ord('o')) + '.jpg')
   img7 = cv2.imread('ascii/' + str(ord('n')) + '.jpg')
   img8 = cv2.imread('ascii/' + str(ord('e')) + '.jpg')

   # Concatenate horizontally
   collage1 = cv2.hconcat([img1, img2, img3, img4])
   collage2 = cv2.hconcat([img5, img6, img7, img8])
   
   collage = cv2.vconcat([collage1, collage2])

   # Save the collage image
   cv2.imwrite('collage.jpg', collage)
   
PIXEL_W = 8
PIXEL_H = 17
if __name__ == '__main__':
   # Set the font and other parameters
   font_path = "C:\\Users\\samal\\Downloads\\CascadiaCode-2111.01\\ttf\\Cascadiacode.ttf"
   font_size = 12
   thickness = 0

   # Create a font object with the Cascadia Code font
   font = ImageFont.truetype(font_path, int(font_size))

   # Loop through ASCII characters
   for i in range(32, 127):
      text = chr(i)

      # Create a blank black image
      img = np.zeros((PIXEL_H, PIXEL_W, 3), np.uint8)

      # Draw the text on the image
      img_pil = Image.fromarray(img)
      draw = ImageDraw.Draw(img_pil)
      draw.text((0, 0), text, font=font, fill=(255, 255, 255), stroke_width=thickness)
      img = np.array(img_pil)

      # Apply binary thresholding
      threshold_value = 127  # Change this value as desired
      ret, img = cv2.threshold(img, threshold_value, 255, cv2.THRESH_BINARY)

      # Save the image as a JPEG file with ASCII code as filename
      cv2.imwrite(f'ascii/{i}.jpg', img)


   # collage()
   print('test\ndone')
