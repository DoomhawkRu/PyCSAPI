'''
Copyright (c) 2018 Doomhawk

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

from pycsapi import constant
from pycsapi import util
import math
import pycsapi
import time

# Make sure that you run CS:GO before running this script, otherwise you will get an error
# WARNING: This script working really bad due to some issues described in the pycsapi/util.py file. We are working hard to find a way to fix it
if __name__ == '__main__':
    api = pycsapi.PyCSAPI()
    player = api.get_player()
    drawer = util.ScreenDrawer(constant.PROCESS_NAME, True)
    while True:
        if player.is_in_game() and player.is_alive():
            to_draw = []
            for _player in api.get_players():
                if _player.is_alive() and _player.get_team_id() != player.get_team_id():
                    coords = util.world_to_screen(_player.get_position(), api.get_view_matrix(), constant.PROCESS_NAME)
                    if coords:
                        health = _player.get_health()
                        distance = player.get_distance_to(_player)
                        distance = int(math.sqrt(distance[0] ** 2 + distance[1] ** 2 + distance[2] ** 2))
                        if distance < 3000:
                            to_draw.append([coords[0], coords[1], _player.get_name() + '\nDistance: ' + str(distance), (255 - health * 2.55, health * 2.55, 0)])
            for data in to_draw:
                drawer.draw_text(data[0], data[1], data[2], data[3])
        time.sleep(.001)