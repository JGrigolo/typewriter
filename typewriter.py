#########################################################################
# This program is free software: you can redistribute it and/or modify  #
# it under the terms of the GNU General Public License as published by  #
# the Free Software Foundation, either version 3 of the License, or     #
# (at your option) any later version.                                   #
#                                                                       #
# This program is distributed in the hope that it will be useful,       #
# but WITHOUT ANY WARRANTY; without even the implied warranty of        #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
# GNU General Public License for more details.                          #
#                                                                       #
# You should have received a copy of the GNU General Public License     #
# along with this program.  If not, see <https://www.gnu.org/licenses/> #
#                                                                       #
#                       Joel Grigolo - https://matehacker.org - 06/2020 #
#########################################################################

from pynput.keyboard import Key, Controller
from distutils.spawn import find_executable
import argparse
import time
import random
import subprocess
import string
import os

proc = None

keySound = ""
keyVolume = 50
musicVolume = 70
soundVolume = 70

CRED = '\33[31m'
CBLUE = '\33[34m'
CGREEN = '\33[32m'
CYELLOW = '\33[33m'
CNORMAL = '\33[0m'

keyboard = Controller()

# Command line arguents

Command_parser = argparse.ArgumentParser(description='Typewriter')

Command_parser.add_argument('txt', type=str, help="Txt file to be processed")

arg = Command_parser.parse_args()

# Keys dictionary

tKeys = [Key.alt, Key.alt_gr, Key.alt_l, Key.alt_r, Key.backspace, Key.caps_lock,
         Key.caps_lock, Key.cmd, Key.cmd_l, Key.cmd_r, Key.ctrl, Key.ctrl_l, Key.ctrl_r,
         Key.delete, Key.down, Key.end, Key.enter, Key.esc, Key.f1, Key.f10, Key.f11, Key.f12,
         Key.f13, Key.f14, Key.f15, Key.f16, Key.f17, Key.f18, Key.f19, Key.f2, Key.f20, Key.f3,
         Key.f4, Key.f5, Key.f6, Key.f7, Key.f8, Key.f9, Key.home, Key.insert, Key.left,
         Key.media_next, Key.media_play_pause, Key.media_previous, Key.media_volume_down,
         Key.media_volume_mute, Key.media_volume_up, Key.menu, Key.num_lock, Key.page_down,
         Key.page_up, Key.pause, Key.print_screen, Key.right, Key.scroll_lock, Key.shift,
         Key.shift_l, Key.shift_r, Key.space, Key.tab, Key.up]

cKeys = ["alt", "alt_gr", "alt_l", "alt_r", "backspace", "caps_lock", "caps_lock", "cmd", "cmd_l",
         "cmd_r", "ctrl", "ctrl_l", "ctrl_r", "delete", "down", "end", "enter", "esc", "f1", "f10",
         "f11", "f12", "f13", "f14", "f15", "f16", "f17", "f18", "f19", "f2", "f20", "f3", "f4", "f5",
         "Fey.f6", "f7", "f8", "f9", "home", "insert", "left", "media_next", "media_play_pause",
         "media_previous", "media_volume_down", "media_volume_mute", "media_volume_up", "menu", "num_lock",
         "page_down", "page_up", "pause", "print_screen", "right", "scroll_lock", "shift", "shift_l",
         "shift_r", "space", "tab", "up"]


def handleMessages(message, color):

    print("[typewritter|" + str(time.localtime().tm_hour) + ":" +
          str(time.localtime().tm_min) + ":" + str(time.localtime().tm_sec) + "]: " + color + message + CNORMAL)


def testConditions():

    try:

        find_executable('mplayer')

        handleMessages("Mplayer found!", CGREEN)

    except:

        handleMessages(
            'Mplayer not found, please install: the script will break if try to play sound!', CRED)

    try:

        f = open(arg.txt)
        f.close()

        handleMessages(arg.txt + " found!", CGREEN)

    except FileNotFoundError:

        handleError(arg.txt + " file does NOT exist!")


def handleError(error):

    print("[typewritter|" + str(time.localtime().tm_hour) + ":" +
          str(time.localtime().tm_min) + ":" + str(time.localtime().tm_sec) + "]: " + CRED +
          "ERROR> " + CNORMAL + error + "\n")

    exit()


def type_Key(tChar):

    keyboard.type(tChar)

    vol = random.uniform(25, 35)

    subprocess.Popen(['mplayer', ' -volume 50', keySound, '-really-quiet'])


def count_Down():

    count = 5

    while count >= 0:

        print("[typewritter|" + str(time.localtime().tm_hour) + ":" +
              str(time.localtime().tm_min) + ":" + str(time.localtime().tm_sec) + "]: Typewriter will start in " +
              CRED + str(count) + CNORMAL + " seconds. Click on yours target window before that!", end='\r')

        count = count-1
        time.sleep(1)

    print('\n', end='\r')


def play_Music(soundFile):

    global proc

    handleMessages("Start Mplayer, file: " + soundFile +
                   ", volume " + str(musicVolume) + "%.", CBLUE)

    proc = subprocess.Popen(
        ['mplayer', ' -volume' + str(musicVolume), soundFile,  '-really-quiet'])


def play_Sound(soundFile):

    handleMessages("Start Mplayer, file: " + soundFile +
                   ", volume " + str(soundVolume) + "%.", CBLUE)

    subprocess.Popen(['mplayer', ' -volume 70', soundFile, '-really-quiet'])


def special_Keys(commandString):

    tempStr = ""

    if tempStr.join(commandString)[:9] == '<keySound':

        try:

            global keySound

            keySound = tempStr.join(commandString)[10:(len(commandString)-2)]

            f = open(keySound)
            f.close()

            handleMessages("Found sound file for keys", CNORMAL)

        except FileNotFoundError:

            handleError("Key sound file NOT found!")

        return

    if tempStr.join(commandString) == '<delay>\n':

        handleMessages("Starting 2 seconds delay.", CNORMAL)

        time.sleep(2)

        return

    if tempStr.join(commandString)[:6] == '<music':

        try:

            f = open(tempStr.join(commandString)[7:(len(commandString)-2)])
            f.close()

            handleMessages("Found sound file for music.", CNORMAL)
            
            play_Music(tempStr.join(commandString)[7:(len(commandString)-2)])

        except FileNotFoundError:

            handleError("Music sound file NOT found!")

        return

    if tempStr.join(commandString)[:6] == '<sound':

        try:

            f = open(tempStr.join(commandString)[7:(len(commandString)-2)])
            f.close()

            play_Sound(tempStr.join(commandString)[7:(len(commandString)-2)])

            handleMessages("Found sound file.", CNORMAL)

        except FileNotFoundError:

            handleError("Sound file NOT found!")

        return

    if tempStr.join(commandString) == '<start>\n':

        handleMessages('Marking the start video point.', CNORMAL)

        play_Sound('start.wav')

        return

    if tempStr.join(commandString) == '<end>\n':

        handleMessages('Marking the end video point.', CNORMAL)

        play_Sound('end.wav')

        return

    if tempStr.join(commandString)[:9] == '<VolSound':

        handleMessages('Setting Sound Volume to:' +
                       tempStr.join(commandString)[11:len(commandString)-2] + '%.')

        global soundVolume

        soundVolume = tempStr.join(commandString)[:-2]

        return

    if tempStr.join(commandString)[:9] == '<VolMusic':

        handleMessages('Setting Sound Volume to:' +
                       tempStr.join(commandString)[11:len(commandString)-2] + '%.')

        global musicVolume

        musicVolume = tempStr.join(commandString)[:-2]

        return

    commandString.remove('<')
    commandString.remove('>')
    commandString.remove('\n')

    tempStr = (tempStr.join(commandString))

    commandString = tempStr.split('+')

    numKeys = len(commandString)

    key01 = commandString[0]
    key02 = commandString[1]
    if numKeys == 3:
        key03 = commandString[2]
    else:
        key03 = ""

    if key01 in cKeys:
        key01 = tKeys[cKeys.index(key01)]

    if key02 in cKeys:
        key02 = tKeys[cKeys.index(key02)]

    if key03 and key03 in cKeys:
        key03 = tKeys[cKeys.index(key03)]

    with keyboard.pressed(key01):

        keyboard.press(key02)

        if key03:

            keyboard.press(key03)
            keyboard.release(key03)

        keyboard.release(key02)

# Main


os.system('clear')

if arg.txt:

    handleMessages("Typewritter starting ...", CNORMAL)
    handleMessages("Testing variables.", CNORMAL)
    testConditions()

    handleMessages("Starting CountDown!", CNORMAL)
    count_Down()

    handleMessages("Starting text interpreter.", CNORMAL)

    with open(arg.txt) as reader:

        line = reader.readline()
        lineChar = list(line)

        currentChar = 0

        while line != "":

            if lineChar[0] == "<" and lineChar[(len(lineChar)-2)] == ">":

                handleMessages("Special key: " + line[:len(line)-1], CGREEN)
                special_Keys(lineChar)
                line = reader.readline()
                lineChar = list(line)

            else:

                handleMessages("Starting new line. Typing ...", CNORMAL)
                handleMessages(line[:len(line)-1], CYELLOW)
                while currentChar < len(lineChar):

                    keyChar = lineChar[currentChar]

                    type_Key(keyChar)

                    r = random.uniform(0.01, 0.10)
                    currentChar = currentChar + 1
                    time.sleep(r)

                currentChar = 0
                line = reader.readline()
                lineChar = list(line)

    handleMessages("Reach end of file " + arg.txt, CNORMAL)

    handleMessages("Killing subprocesses", CNORMAL)
    try:

        proc.terminate()
        proc.wait()

    except:

        handleMessages("No subprocesss to kill", CNORMAL)

    pEnd = subprocess.Popen(['stty', 'sane'])
    pEnd.wait()
    pEnd.terminate()
    pEnd = subprocess.Popen(['stty', 'erase', '^H'])
    pEnd.wait()
    pEnd.terminate()

    handleMessages("Exiting.", CNORMAL)
