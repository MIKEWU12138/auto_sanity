import cv2
import subprocess
import time
import os

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
##def install(route):
##    adb("adb shell input keyevent 82")
# unlock()
def start():
    unlock()
    home()
    menu()

os.system('adb push /Users/ahq09/Desktop/platform-tools/screenshots/. /sdcard/Pictures/')
# home()
# take_screenshot("screen")
