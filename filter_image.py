import cv2
from filter import filter, save_image

if __name__ == '__main__':
   imgname = 'giraffe'
   imagepath = f'images/{imgname}.jpg'
   image = cv2.imread(imagepath)
   ascii_img = filter(image, colour=False, log=True)
   save_image(ascii_img, imgname)