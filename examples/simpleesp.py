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
if __name__ == '__main__':
    api = pycsapi.PyCSAPI()
    player = api.get_player()
    drawer = util.ScreenDrawer(constant.PROCESS_TITLE)
    list = []
    while True:
        if player.is_in_game() and player.is_alive():
            for entity in api.get_players():
                if entity.is_alive() and entity.get_team_id() != player.get_team_id() and not entity.is_dormant():
                    entity_head = entity.get_position()
                    entity_top = [entity_head[0], entity_head[1], entity_head[2] + 10]
                    entity_foot = entity.get_origin()
                    vHead = api.world_to_screen(entity_top)
                    vFoot = api.world_to_screen(entity_foot)
                    health = entity.get_health()
                    if vHead and vFoot:
                        h = abs(vFoot[1] - vHead[1])
                        w = h / 2
                        if entity.get_id() not in list:
                            list.append(entity.get_id())
                        drawer.draw_rectangle(entity.get_id(), vHead[0] - w / 2, vHead[1], vHead[0] + w / 2, vHead[1] + h)
                        drawer.draw_rectangle(entity.get_id() + 64, vHead[0] - w / 2 - 7, vHead[1] + (h / 100 * (100 - health)), vHead[0] - w / 2 - 2, vHead[1] + h, (255 - health * 2.55, health * 2.55, 0))
                    else:
                        if entity.get_id() in list and str(entity.get_id()) in drawer.rectangles:
                            del drawer.rectangles[str(entity.get_id())]
                            del drawer.rectangles[str(entity.get_id() + 64)]
                else:
                    if entity.get_id() in list and str(entity.get_id()) in drawer.rectangles:
                        del drawer.rectangles[str(entity.get_id())]
                        del drawer.rectangles[str(entity.get_id() + 64)]
        time.sleep(1 / 1024)