import cv2
import subprocess
import time
import os
rows=[600,1000,1300,1500]
cols=[160,320,480,700,900]
#first col 160
#second col 320
#third col 480
#fourth col 700
#fifth col 900
#first row 600
#second row 1000
#third row 1300
#fourth 1500
def adb(command):
    proc=subprocess.Popen(command.split(' '), stdout=subprocess.PIPE,shell=True)
    (out,_)=proc.communicate()
    return out.decode('utf-8')

def check():
    adb("adb devices")

def swipe(start_x, start_y, end_x, end_y, duration_ms=100):
    adb("adb shell input swipe {} {} {} {} {}".format(start_x, start_y, end_x, end_y, duration_ms))
    time.sleep(1)

def unlock():
    info=adb('adb shell dumpsys window policy')
    getInfo=sorted(info.split())
    if 'screenState=SCREEN_STATE_OFF' in getInfo:
        adb('adb shell input keyevent 82')
        time.sleep(1)
        swipe(540,2000,540,200,100)
    else:
        pass

def take_screenshot(final):
    adb(f"adb exec-out screencap -p /sdcard/Pictures/{final}.png")
    time.sleep(1)

def tap(tap_x, tap_y):
    adb("adb shell input tap {} {}".format(tap_x, tap_y))
    time.sleep(1)

def home():
    tap(540,2300)

def menu():
    swipe(540,1500,540,500,100)

def image_position(small_image, big_image):
    img_rgb = cv2.imread(big_image)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(small_image, 0)
    height, width = template.shape[::]
    res = cv2.matchTemplate(img_gray, template, cv2.TM_SQDIFF)
    _, _, top_left, _ = cv2.minMaxLoc(res)
    bottom_right = (top_left[0] + width, top_left[1] + height)
    return (top_left[0]+bottom_right[0])//2, (top_left[1]+bottom_right[1])//2


##def install(route):
##    adb("adb shell input keyevent 82")
# unlock()
def start():
    unlock()
    home()
    menu()

def tapDebug():
    start()
    tap(cols[1],rows[1])
def tapMessage():
    start()
    tap(cols[0],rows[2])
def tapPhone():
    start()
    tap(cols[2],rows[2])
def tapPing():
    start()
    tap(cols[3],rows[2])
def tapSettings():
    start()
    tap(cols[0],rows[3])
# os.system('adb push /Users/ahq09/Desktop/platform-tools/screenshots/. /sdcard/Pictures/')
# screen="screen"
# final="browserIcon"
# start()
# take_screenshot(screen)
# os.system("adb pull /sdcard/Pictures/screen.png /Users/ahq09/Desktop/platform-tools/screenshots/")
#
#
# x, y  = image_position(f"./screenshots/{final}.png", f"./screenshots/{screen}.png")
# start()
# print("x=",x)
# print("y=",y)

tapDebug()
tapMessage()
tapPhone()

tapPing()
tapSettings()
#first col 160
#second col 320
#third col 480
#fourth col 700
#fifth col 900
#first row 600
#second row 1000
#third row 1300
#fourth 1500



# home()
# take_screenshot("screen")
