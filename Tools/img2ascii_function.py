# Python code to convert an image to ASCII image.
import sys
import numpy as np

sys.path.append('home/pi/local/lib/python3.7/site-packages/cv2/python-3.7')
import cv2, queue, threading, time, os

# gray scale level values from:
# http://paulbourke.net/dataformats/asciiart/

# 70 levels of gray
gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

# 10 levels of gray
gscale2 = '@%#*+=-:. '



class VideoCapture:

  def __init__(self, name):
    self.cap = cv2.VideoCapture(name)
    self.cap.set(3,160) # set Width
    self.cap.set(4,120) # set Height
    self.q = queue.Queue()
    t = threading.Thread(target=self._reader)
    t.daemon = True
    t.start()

  # read frames as soon as they are available, keeping only most recent one
  def _reader(self):
    while True:
      ret, frame = self.cap.read()
      if not ret:
        break
      if not self.q.empty():
        try:
          self.q.get_nowait()   # discard previous (unprocessed) frame
        except queue.Empty:
          pass
      self.q.put(frame)

  def read(self):
    return self.q.get()





def getAverageL(image):

    """
    Given PIL Image, return average value of grayscale value
    """
    # get image as numpy array
    im = np.array(image)

    # get shape
    w,h = im.shape

    # get average
    return np.average(im.reshape(w*h))

def covertImageToAscii(image, cols, scale, moreLevels):
    """
    Given Image and dims (rows, cols) returns an m*n list of Images
    """
    # declare globals
    global gscale1, gscale2

    # store dimensions
    W, H = image.shape[1], image.shape[0]

    # compute width of tile
    w = W/cols

    # compute tile height based on aspect ratio and scale
    h = w/scale

    # compute number of rows
    rows = int(H/h)


    # check if image size is too small
    if cols > W or rows > H:
        print("Image too small for specified cols!")
        exit(0)

    # ascii image is a list of character strings
    aimg = []
    # generate list of dimensions
    for j in range(rows):
        y1 = int(j*h)
        y2 = int((j+1)*h)

        # correct last tile
        if j == rows-1:
            y2 = H

        # append an empty string
        aimg.append("")

        for i in range(cols):

            # crop image to tile
            x1 = int(i*w)
            x2 = int((i+1)*w)

            # correct last tile
            if i == cols-1:
                x2 = W

            # crop image to extract tile
            img = image[y1:y2, x1:x2]

            # get average luminance
            avg = int(getAverageL(img))

            # look up ascii char
            if moreLevels:
                gsval = gscale1[int((avg*69)/255)]
            else:
                gsval = gscale2[int((avg*9)/255)]

            # append ascii char to string
            aimg[j] += gsval

    # return txt image
    return aimg

# main() function
def main():

    width = 40
    height = 30
    dim = (width, height)

    cap = VideoCapture(0)

    # set scale default as 0.43 which suits
    # a Courier font
    scale = 0.43

    # set cols
    cols = 40


    while True:
        img = cap.read()
        gray = gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        rescaledGray = cv2.resize(gray,dim)

        aimg = covertImageToAscii(rescaledGray, cols, scale, False)

        os.system('clear')
        time.sleep(0.1)
        for i in aimg:
            print(i)

# call main
if __name__ == '__main__':
    main()
