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
import sys

# Make sure that you run CS:GO before running this script, otherwise you will get an error
if __name__ == '__main__':
    aimfov = 5.0
    api = pycsapi.PyCSAPI()
    player = api.get_player()
    print('Press Page Up to increase aim fov')
    print('Press Page Down to decrease aim fov')
    sys.stdout.write('\rCurrent aim fov: ' + str(aimfov) + ' degrees   ')
    pressed = False
    iter = 0
    while True:
        if (not pressed or iter >= 20) and util.is_key_pressed(constant.VK_PRIOR) and aimfov < 70:
            aimfov += 0.5
            sys.stdout.write('\rCurrent aim fov: ' + str(aimfov) + ' degrees   ')
            pressed = True
        elif (not pressed or iter >= 20) and util.is_key_pressed(constant.VK_NEXT) and aimfov > 0:
            aimfov -= 0.5
            sys.stdout.write('\rCurrent aim fov: ' + str(aimfov) + ' degrees   ')
            pressed = True
        if not util.is_key_pressed(constant.VK_PRIOR) and not util.is_key_pressed(constant.VK_NEXT):
            pressed = False
            iter = 0
        if pressed:
            iter += 1
        if player.is_in_game() and player.is_alive():
            for entity in api.get_players():
                if entity.get_team_id() != player.get_team_id() and not entity.is_dormant() and player.is_visible(entity):
                    player_angle = player.get_view_angle()
                    pitch, yaw = util.distance_to_angle(player.get_distance_to(entity), player.get_punch())
                    distance_x, distance_y = util.calc_distance(player_angle[0], player_angle[1], pitch, yaw)
                    if distance_x < aimfov and distance_y < aimfov:
                        player.set_view_angle(pitch, yaw)
                        break
        time.sleep(1 / 4)