import cv2
import subprocess
import time


def adb(command):
    proc=subprocess.Popen(command.split(' '), stdout=subprocess.PIPE,shell=True)
    (out,_)=proc.communicate()
    return out.decode('utf-8')

def check():
    adb("adb devices")

def swipe(start_x, start_y, end_x, end_y, duration_ms):
    adb("adb shell input swipe {} {} {} {} {}".format(start_x, start_y, end_x, end_y, duration_ms))

def unlock():
    adb("adb shell input keyevent 82")
    time.sleep(1)
    swipe(540,2000,540,200,100)

def take_screenshot(final):
    adb("adb exec-out screencap -p /sdcard/Pictures/{final}.png")

def tap(tap_x, tap_y):
    adb("adb shell input tap {} {}".format(tap_x, tap_y))

def home():
    tap(540,2300)

def menu():
    swipe(540,1500,540,500,100)
##def install(route):
##    adb("adb shell input keyevent 82")
# unlock()
# unlock()
# screen='screen'
# take_screenshot(screen)
# unlock()
take_screenshot("debug")
