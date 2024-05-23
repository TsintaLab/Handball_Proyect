import cv2
import numpy as np
import glob
from tqdm import tqdm
 


fin = 9

for j in  tqdm(range(1, fin), desc="Procesando", unit="iter"):
  img_array = []
  for filename in glob.glob(f'Frames/Jugador1Sec1/Tiro{j}/skeleton_region/*.jpg'):
      img = cv2.imread(filename)
      height, width, layers = img.shape
      size = (width,height)
      img_array.append(img)
 
 
  out = cv2.VideoWriter(f'Tiro{j}_Sec1.mp4',cv2.VideoWriter_fourcc(*'mp4v'), 7, size) #para 180 frames = 7, para 240 frames = 9
 
  for i in range(len(img_array)):
      out.write(img_array[i])
      
  out.release()
  