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
def installPing():
    installPath=r"C:\Users\17345\Desktop\PingTools_Network_Utilities_v4.52_Free_apkpure.com.apk"
    commandInsideTerminal("adb install %s"%installPath)
def adb(command):
    proc=subprocess.Popen(command.split(' '), stdout=subprocess.PIPE,shell=True)
    (out,_)=proc.communicate()
    return out.decode('utf-8')
def commandInsideTerminal(command):
    proc=subprocess.Popen(command, stdout=subprocess.PIPE)
    proc.stdout.read()
def check():
    adb("adb devices")
def keyEvent(number):
    adb("adb shell input keyevent %s"%number)   #焦点去到发送按键
    time.sleep(2)

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
def image_position(small_image, big_image):
    img_rgb = cv2.imread(big_image)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(small_image, 0)
    height, width = template.shape[::]
    res = cv2.matchTemplate(img_gray, template, cv2.TM_SQDIFF)
    _, _, top_left, _ = cv2.minMaxLoc(res)
    bottom_right = (top_left[0] + width, top_left[1] + height)
    return (top_left[0]+bottom_right[0])//2, (top_left[1]+bottom_right[1])//2

def home():
    # tap(540,2300)
    adb("adb shell input keyevent 3")
    time.sleep(1)
def menu():
    swipe(540,1500,540,500,100)
def start():
    unlock()
    home()
    menu()

def tap(tap_x, tap_y):
    adb("adb shell input tap {} {}".format(tap_x, tap_y))
    time.sleep(2)
def tapDebug():
    start()
    tap(cols[0],rows[1])
def tapMessage():
    start()
    tap(cols[4],rows[1])
def tapPhone():
    start()
    tap(cols[1],rows[2])
def tapPing():
    start()
    tap(cols[2],rows[2])
def tapSettings():
    start()
    tap(cols[4],rows[2])
def tapbrowser():
    start()
    tap(cols[0],rows[0])
def tapSim1():
    tap(480,1250)
def tapSim2():
    tap(480,1400)

def logPlay():
    tapDebug()
    tap(540,2200)
    time.sleep(10)
def logStop():
    tapDebug()
    tap(540,2200)
    time.sleep(15)

def renameAndCompress(type):
    command1="adb shell cd sdcard"
    command2="mv debuglogger %s"%type
    command3="tar -czvf %s.zip ./%s"%(type,type)
    command=command1+"&&"+command2+"&&"+command3
    commandInsideTerminal(command)

def phone(number):
    sim1DataSet()
    adb("adb shell settings put global multi_sim_voice_call 3")
    adb("adb shell am start -a android.intent.action.CALL -d tel:%d"%number)
    time.sleep(2)
    tapSim1()
    time.sleep(8)
    adb("adb shell input keyevent 6") #6 is endcall

    time.sleep(5)

    sim2DataSet()
    adb("adb shell am start -a android.intent.action.CALL -d tel:%d"%number)
    time.sleep(2)
    tapSim2()
    time.sleep(10)
    adb("adb shell input keyevent 6")


def mms(number):
    unlock()
    time.sleep(2)
    adb("adb shell am start -a android.intent.action.SENDTO -d sms:%d --es sms_body '???'"%number)
    time.sleep(1)
    keyEvent("22")
    keyEvent("66")
    keyEvent("66")
    adb("adb shell am start -a android.intent.action.SENDTO -d sms:%d --es sms_body '???'"%number)
    time.sleep(1)
    keyEvent("22")
    keyEvent("66")
    keyEvent("61")
    keyEvent("66")



def taskPhone(number):
    airModeOn()
    airModeOff()
    start()
    logPlay()
    phone(number)
    logStop()
    renameAndCompress("4gmomt")

def taskMMS(number):
    airModeOn()
    airModeOff()
    start()
    logPlay()
    mms(number)
    logStop()
    renameAndCompress("MMS")

def wifiOn():
    adb("adb root")
    time.sleep(3)
    adb("adb shell wpa_cli -iwlan0 add_network  0")
    adb("adb shell wpa_cli -iwlan0 set_network   0  ssid 'sawtest_5G'")
    adb("adb shell wpa_cli -iwlan0 set_network   0  psk 'sawtest123'")
    adb("adb shell wpa_cli -iwlan0 save_config")
    adb("adb shell wpa_cli -iwlan0 select_network  0")            #选择第0个热点
    adb("adb shell wpa_cli -iwlan0 enable_network 0")


def taskWificall(number):#还没解决如何连上wifi
    start()
    logPlay()


    adb("adb shell settings put global multi_sim_voice_call 3")
    adb("adb shell am start -a android.intent.action.CALL -d tel:%d"%number)
    time.sleep(2)
    time.sleep(8)
    adb("adb shell input keyevent 6") #6 is endcall
    time.sleep(5)
    adb("adb shell am start -a android.intent.action.CALL -d tel:%d"%number)
    time.sleep(2)
    adb("adb shell input keyevent 6")
    time.sleep(2)
    logStop()
    renameAndCompress("Wificall")

def allow():
    adb("adb shell input keyevent 66")
    adb("adb shell input keyevent 61")
    adb("adb shell input keyevent 62")

def airModeOn():
    adb("adb root")
    time.sleep(3)
    adb('adb shell settings put global airplane_mode_on 1')
    adb('adb shell am broadcast -a android.intent.action.AIRPLANE_MODE')
def airModeOff():
    adb("adb root")
    time.sleep(3)
    adb('adb shell settings put global airplane_mode_on 0')
    adb('adb shell am broadcast -a android.intent.action.AIRPLANE_MODE')

def browser():
    sim1DataSet()
    time.sleep(10)
    adb("adb shell am start -a android.intent.action.VIEW -d https://yahoo.com/?.tsrc=mtkandroid")
    sim2DataSet()
    time.sleep(10)
    adb("adb shell am start -a android.intent.action.VIEW -d https://yahoo.com/?.tsrc=mtkandroid")


def sim1DataSet():
    unlock()
    tapSettings()
    tap(480,1050)#network and internet
    tap(480,1900)#sim card
    tap(480,1500)#mobile data
    tap(480,1250)
    time.sleep(10)
def sim2DataSet():
    unlock()
    tapSettings()
    tap(480,1050)#network and internet
    tap(480,1900)#sim card
    tap(480,1500)#mobile data
    tap(480,1400)
    time.sleep(10)

def pingSet():
    tapPing()
    tap(80,200)
    tap(80,800)

# pingSet()
# browser()
# tapbrowser()
installPing()
# taskPhone(9728355264)
# taskWificall(9728355264)


# mms(9452327569)
# tapSim2()
# unlock()
# adb("adb shell am start -a android.intent.action.SENDTO -d sms:%d --es sms_body '???'"%9452327569)
# print(1)
# adb shell start -a android.action.SENDTO -d sms:xxxxxxxxx --es sms_body "SMS BODY"
# taskPhone()

# take_screenshot(screen)
# os.system("adb pull /sdcard/Pictures/screen.png /Users/ahq09/Desktop/platform-tools/screenshots/")
#
#
# x, y  = image_position(f"./screenshots/{final}.png", f"./screenshots/{screen}.png")
# start()
# print("x=",x)
# print("y=",y)

# tapPing()
# tapSettings()
#first col 160
#second col 320
#third col 480
#fourth col 700
#fifth col 900
#first row 600
#second row 1000
#third row 1300
#fourth 1500
