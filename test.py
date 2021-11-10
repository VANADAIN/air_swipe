from pynput.keyboard import Key, Controller
from time import sleep
 
k = Controller() 

k.press(Key.cmd_l)
k.press(Key.right)


k.release(Key.cmd_l)
k.release(Key.right)
