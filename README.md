# typewriter

  This is a version on a very early stage of development, usefull but with care.
  Only used and tested in Linux (ubuntu based distributions), should work in other
  OS with some modifications.

Python script, interprets commands and text from a file and send keyboard events to a target window/application.
It was developed to help create simple text based videos like this one: https://youtu.be/PmkpPFxepaY ,
but should be useful in other ways.

# dependencies

mplayer should be installed. The script plays the sounds making a external call to mplayer.

In ubuntu systems:

  sudo apt install mplayer

To handle keyboard events the module pynput (1.6.8 or higher) should be installed.

  pip3 install pynput
  
# usage

See commands.txt for a list of avaiable commands and example.txt.

to run just:

python3 typewriter.py /path_to/text.file

and you have 10 seconds to click on the target window/application (the one that will receive the keyboard events).
