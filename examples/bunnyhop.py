'''
Copyright (c) 2018 Doomhawk

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

from pycsapi import constant
from pycsapi import util
import pycsapi
import time

# Make sure that you run CS:GO before running this script, otherwise you will get an error
if __name__ == '__main__':
    api = pycsapi.PyCSAPI()
    player = api.get_player()
    jump = False
    while True:
        if player.is_in_game() and player.is_alive():
            if util.is_key_pressed(constant.VK_SPACE):
                if jump:
                    if not player.is_on_ground():
                        player.set_jump(True)
                        jump = False
                elif player.is_on_ground():
                    player.set_jump(False)
                    jump = True
        time.sleep(.005)