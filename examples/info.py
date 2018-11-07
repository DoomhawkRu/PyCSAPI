'''
Copyright (c) 2018 Doomhawk

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

import pycsapi
import os
import time

if __name__ == '__main__':
    api = pycsapi.load()
    player = api.get_player()
    while True:
        os.system('cls')
        start_time = int(time.time() * 1000)
        print('Player In Game: {}'.format(player.is_in_game()))
        if player.is_in_game():
            print('Player Armor: {}'.format(player.get_armor()))
            print('Player Crosshair Entity: {}'.format(True if player.get_crosshair_entity() else False))
            print('Player Health: {}'.format(player.get_health()))
            print('Player Name: {}'.format(player.get_name()))
            print('Player Position: {}'.format(player.get_position()))
            print('Player Punch: {}'.format(player.get_punch()))
            print('Player Shots Fired: {}'.format(player.get_shots_fired()))
            print('Player Team ID: {}'.format(player.get_team_id()))
            print('Player View Angle: {}'.format(player.get_view_angle()))
            print('Player Weapon ID: {}'.format(player.get_weapon()))
            print('Player\'s Weapon Able To Shoot: {}'.format(player.is_able_to_shoot()))
            print('Player Alive Status: {}'.format(player.is_alive()))
            print('Player Dormant Status: {}'.format(player.is_dormant()))
            print('Player Has Defuser/Helmet: {}/{}'.format(player.is_has_defuser(), player.is_has_helmet()))
            print('Player On Ground: {}'.format(player.is_on_ground()))
            print('Player Scoped: {}'.format(player.is_scoped()))
            spec_target = player.get_entity().get_spectator_target()
            if spec_target:
                print('Player Spectator Target: {}'.format(spec_target.get_name()))
            print()
            print('BSP File: {}'.format(api.get_bsp_file()))
            print('Game Directory: {}'.format(api.get_game_dir()))
            print('Map Name: {}'.format(api.get_map()))
            print('Max Players: {}'.format(api.get_max_players()))
            print('Players Loaded: {}'.format(len(api.get_players())))
            print('Players Alive: {}'.format(len(api.get_players(func = lambda entity: entity.is_alive()))))
            print()
            print('ConVars:')
            print('sv_cheats: {}'.format(api.convar_manager.find_convar('sv_cheats').get_int()))
        end_time = int(time.time() * 1000)
        print('Receiving information took {} ms.'.format(end_time - start_time))
        time.sleep(1 / 8)