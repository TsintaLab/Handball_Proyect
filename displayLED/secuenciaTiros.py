from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text
from luma.core.legacy.font import proportional, CP437_FONT, LCD_FONT
from luma.led_matrix.device import max7219
import time
import random
from PIL import Image

memoria = random.sample(range(1,10), 9)

print(memoria)
# Configura la interfaz SPI
serial = spi(port=0, device=0, gpio=noop())

device = max7219(serial, cascade = 9, width = 72, height = 8)
paused = False

# Save the sequence to a text file

with open("exp_sec1.txt", "w") as file:

    for number in memoria:

        file.write(str(number) + "\n")

print("Sequence saved to sequence.txt")

def pause_resume():

    global paused

    paused = not paused



    if paused:

        print("Paused. Press any key to resume...")

    else:

        print("Paused. Press any key to continue...")



    # Wait for user input to resume

    input()

for i in range(9):

  if memoria[i] == 7:
   print(memoria[i])
   with canvas(device) as draw:
       text(draw, (1, 1), "O", fill="white", font=proportional(CP437_FONT))
   time.sleep(15)
   #pause_resume()
  elif memoria[i] == 4:
   print(memoria[i])
   with canvas(device) as draw:
       text(draw, (9, 1), "O", fill="white", font=proportional(CP437_FONT))
   time.sleep(15)
   #pause_resume()  
  elif memoria[i] == 1:
   print(memoria[i])
   with canvas(device) as draw:
       text(draw, (17, 1), "O", fill="white", font=proportional(CP437_FONT))
   time.sleep(15)
   #pause_resume()  
  elif memoria[i] == 2:
   print(memoria[i])
   with canvas(device) as draw:
       text(draw, (25,1), "O", fill="white", font=proportional(CP437_FONT))
   time.sleep(15)
   #pause_resume()  
  elif memoria[i] == 5:
   print(memoria[i])
   with canvas(device) as draw:
       text(draw, (33, 1), "O", fill="white", font=proportional(CP437_FONT))
   time.sleep(15)
   #pause_resume()  
  elif memoria[i] == 8:
   print(memoria[i])
   with canvas(device) as draw:
       text(draw, (41, 1), "O", fill="white", font=proportional(CP437_FONT))
   time.sleep(15)
   #pause_resume()  
  elif memoria[i] == 9:
   print(memoria[i])
   with canvas(device) as draw:
       text(draw, (49,1), "O", fill="white", font=proportional(CP437_FONT))
   time.sleep(15)
   #pause_resume()  
  elif memoria[i] == 6:
   print(memoria[i])
   with canvas(device) as draw:
       text(draw, (57, 1), "O", fill="white", font=proportional(CP437_FONT))
   time.sleep(15)
   #pause_resume()  
  elif memoria[i] == 3:
   print(memoria[i])
   with canvas(device) as draw:
       text(draw, (65, 1), "O", fill="white", font=proportional(CP437_FONT))
   time.sleep(15)
   #pause_resume()  

print("Prueba terminada!!")