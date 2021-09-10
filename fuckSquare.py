from time import sleep
from datetime import datetime
from random import randint
from pynput.keyboard import Controller
from copy import deepcopy
from argparse import ArgumentParser
import ctypes

SendInput = ctypes.windll.user32.SendInput


def press_key_circle(keyboard, times, rand_down, rand_up):
    i = 0
    n = 0
    flag = True
    while i < times:
        PressKey(0xd2)
        ReleaseKey(0xd2)
        PressKey(0xcb)
        ReleaseKey(0xcb)
        ran = randint(rand_down, rand_up)
        sleep(ran / 10000)
        n = deepcopy(i)
        if n % 100 == 1:
            flag = random_sleep(flag, n)
        if n % 150 == 1 and flag is False:
            flag = random_sleep(flag, n)
        i = i + 1


def random_sleep(my_bool, i):
    ran = randint(1, 100)
    if ran < 50:
        sleep(randint(1, 2))
        print("zzzzzzZZZZZZ 正在摸鱼,已经按了 " + str(i) + " 下啦，淦哦square")
        if my_bool is False:
            my_bool = True
        else:
            my_bool = False
    return my_bool


# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


# Actuals Functions

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--time', '-t', type=int, help='设置运行的时间（大概会准', default=10)
    parser.add_argument('--down', '-d', type=int, help='设置手速的下限，单位为毫秒', default=100)
    parser.add_argument('--up', '-u', type=int, help='设置手速的下限，单位为毫秒', default=150)
    args = parser.parse_args()

    finish_time = datetime.now()
    start_time = datetime.now()
    keyboard = Controller()
    PressKey(0x45)
    ReleaseKey(0x45)
    press_key_circle(keyboard, args.time * 12 * 60, args.down*10, args.up*10)
    print("运行完毕，共运行：" + str(args.time) + " 分钟，不会有人还没抢到吧，不会吧不会吧")
