'''
Copyright (c) 2018 Doomhawk

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

import ctypes
import json
import os
import time
import urllib.request

try:
    from pycsapi import constant
    from pycsapi import util
    from pycsapi import win32
except:
    import constant
    import util
    import win32

def load(show_error = True):
    try:
        return PyCSAPI()
    except Exception as e:
        if show_error:
            ctypes.windll.user32.MessageBoxW(0, e.args[0]['message'], 'PyCSAPI', 16)

class Convar:
    def __init__(self, pycsapi, address):
        self.pycsapi = pycsapi
        self.address = address
    
    def get_name(self):
        convar_name_entry = win32.read_memory(self.pycsapi.game, self.address + 0xc, 'i')
        convar_name = ''
        for i in range(constant.CONVAR_NAME_SIZE):
            char = win32.read_memory(self.pycsapi.game, convar_name_entry + i, 'c')
            if char == b'\x00':
                break
            convar_name += char.decode()
        return convar_name
    
    def set(self, value):
        if isinstance(value, str):
            return self.set_string(value)
        elif isinstance(value, int):
            return self.set_int(value)
        elif isinstance(value, float):
            return self.set_float(value)
        return False
    
    def get_size(self):
        return win32.read_memory(self.pycsapi.game, self.address + 0x28, 'i')
    
    def get_flags(self):
        return util.ConvarFlags(win32.read_memory(self.pycsapi.game, self.address + 0x14, 'i'))
    
    def set_flags(self, value):
        flag = 0
        if isinstance(value, int):
            flag = value
        else:
            flag = value.compile()
        win32.write_memory(self.pycsapi.game, self.address + 0x14, flag, 'i')
        return True
    
    def get_float(self):
        return win32.read_memory(self.pycsapi.game, self.address + 0x2C, 'f') - self.address
    
    def set_float(self, value):
        win32.write_memory(self.pycsapi.game, self.address + 0x2C, value + self.address, 'f')
        return True
    
    def get_int(self):
        return win32.read_memory(self.pycsapi.game, self.address + 0x30, 'i') - self.address
    
    def set_int(self, value):
        win32.write_memory(self.pycsapi.game, self.address + 0x30, value + self.address, 'i')
        return True
    
    def get_string(self):
        convar_string_entry = win32.read_memory(self.pycsapi.game, self.address + 0x24, 'i')
        convar_string = ''
        for i in range(constant.CONVAR_STRING_SIZE):
            char = win32.read_memory(self.pycsapi.game, convar_string_entry + i, 'c')
            if char == b'\x00':
                break
            try:
                convar_string += char.decode()
            except:
                break
        return convar_string
    
    def set_string(self, value):
        convar_string_entry = win32.read_memory(self.pycsapi.game, self.address + 0x24, 'i')
        win32.write_memory(self.pycsapi.game, convar_string_entry, value, 'c', len(value))
        for i in range(len(value), constant.CONVAR_STRING_SIZE):
            char = win32.read_memory(self.pycsapi.game, convar_string_entry + i, 'c')
            if char != b'\x00':
                win32.write_memory(self.pycsapi.game, convar_string_entry + i, 0, 'b')
            else:
                break
        return True

class ConvarManager:
    def __init__(self, pycsapi):
        self.pycsapi = pycsapi
        self.convars = {}
    
    def load(self):
        convar_base = win32.find_pattern(self.pycsapi.game, constant.VSTDLIB_DLL, constant.PATTERN_CONVAR, True) + constant.PATTERN_CONVAR_OFFSET
        convar_base_pointer = win32.read_memory(self.pycsapi.game, convar_base, 'i')
        short_cuts = win32.read_memory(self.pycsapi.game, convar_base_pointer + 0x34, 'i')
        hash_map_entry = win32.read_memory(self.pycsapi.game, short_cuts, 'i')
        while hash_map_entry:
            convar_address = win32.read_memory(self.pycsapi.game, hash_map_entry + 0x4, 'i')
            convar = Convar(self.pycsapi, convar_address)
            if convar.get_name():
                self.convars[convar.get_name()] = convar
            hash_map_entry = win32.read_memory(self.pycsapi.game, hash_map_entry + 0x4, 'i')
    
    def find_convar(self, name):
        return self.convars[name] if name in self.convars else None

class PyCSAPI:
    def __init__(self):
        self.game = win32.get_process(constant.PROCESS_NAME)
        if not self.game:
            raise Exception({'id': 1, 'message': 'Process ' + constant.PROCESS_NAME + ' is not found!'})
        self.client = win32.get_module_offset(win32.get_module(self.game, constant.CLIENT_DLL))
        self.engine = win32.get_module_offset(win32.get_module(self.game, constant.ENGINE_DLL))
        if not self.client or not self.engine:
            self.client = win32.get_module_offset(win32.get_module(self.game, constant.CLIENT_DLL), False)
            self.engine = win32.get_module_offset(win32.get_module(self.game, constant.ENGINE_DLL), False)
        if not self.client or not self.engine:
            raise Exception({'id': 2, 'message': 'Unable to load required modules!'})
        self.offset = self.load_offsets()
        if not self.offset:
            raise Exception({'id': 3, 'message': 'Unable to update offsets!'})
        self.dwClientCMD = win32.find_pattern(self.game, constant.ENGINE_DLL, constant.PATTERN_DWCLIENTCMD, True)
        self.convar_manager = ConvarManager(self)
        self.convar_manager.load()
        self.player = Player(self)
    
    def _get_engine_pointer(self): return win32.read_memory(self.game, self.engine + self.offset['signatures']['dwClientState'], 'i')
    def _get_flags(self): return win32.read_memory(self.game, self._get_local_player() + self.offset['netvars']['m_fFlags'], 'i')
    def _get_local_player(self): return win32.read_memory(self.game, self.client + self.offset['signatures']['dwLocalPlayer'], 'i')
    def _get_radar(self): return win32.read_memory(self.game, self.client + self.offset['signatures']['dwRadarBase'], 'i')
    def _get_radar_pointer(self): return win32.read_memory(self.game, self._get_radar() + constant.RADAR_POINTER_OFFSET, 'i')
    
    def is_sending_packets(self):
        return bool(win32.read_memory(self.game, self.engine + self.offset['signatures']['dwbSendPackets'], 'b'))
    
    def execute_command(self, command, safe = True):
        if not self.get_player().is_in_game() or not self.dwClientCMD:
            return False
        win32.write_in_thread(self.game, self.dwClientCMD, str(command), 'c', len(command))
        if safe:
            time.sleep(.006)
        return True
    
    def find_entities(self, in_range = 1024, func = True):
        entities = []
        if not self.get_player().is_in_game():
            return entities
        for entity in range(in_range):
            e = Entity(self, self.get_player(), entity)
            if (isinstance(func, bool) and func) or func(e):
                entities.append(e)
        return entities
    
    def get_bsp_file(self):
        game_dir = self.get_game_dir()
        map_dir = self.get_map_directory()
        if not game_dir or not map_dir:
            return ''
        return '{}\\{}'.format(game_dir, map_dir)
    
    def get_game_dir(self):
        name = ''
        if not self.get_player().is_in_game():
            return name
        for char in win32.read_memory(self.game, self.engine + self.offset['signatures']['dwGameDir'], 'c', constant.GAME_DIR_SIZE):
            if char == b'\x00':
                return name
            name += char.decode()
        return name
    
    def get_map(self):
        name = ''
        if not self.get_player().is_in_game():
            return name
        for char in win32.read_memory(self.game, self._get_engine_pointer() + self.offset['signatures']['dwClientState_Map'], 'c', constant.MAP_NAME_SIZE):
            if char == b'\x00':
                return name
            name += char.decode()
        return name
    
    def get_map_directory(self):
        name = ''
        if not self.get_player().is_in_game():
            return name
        for char in win32.read_memory(self.game, self._get_engine_pointer() + self.offset['signatures']['dwClientState_MapDirectory'], 'c', constant.MAP_DIRECTORY_SIZE):
            if char == b'\x00':
                return name
            name += char.decode()
        return name
    
    def get_max_players(self):
        if not self.get_player().is_in_game():
            return 0
        return win32.read_memory(self.game, self._get_engine_pointer() + self.offset['signatures']['dwClientState_MaxPlayer'], 'i')
    
    def get_player(self):
        return self.player
    
    def get_players(self, max_players = 64, func = True):
        entities = []
        if not self.get_player().is_in_game():
            return entities
        for entity in range(max_players):
            e = Entity(self, self.get_player(), entity)
            if e.is_player() and ((isinstance(func, bool) and func) or func(e)):
                entities.append(e)
        return entities
    
    def get_view_matrix(self):
        matrix = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        if not self.get_player().is_alive():
            return matrix
        for row in range(4):
            for column in range(4):
                matrix[row][column] = win32.read_memory(self.game, self.client + self.offset['signatures']['dwViewMatrix'] + ((row * 4) + (column)) * constant.TYPE_FLOAT_SIZE, 'f')
        return matrix
    
    def load_offsets(self):
        return json.loads(urllib.request.urlopen(constant.URL_OFFSETS).read().decode())
    
    def print(self, message):
        self.execute_command('echo {}'.format(message))
    
    def set_sending_packets(self, status = True):
        win32.write_memory(self.game, self.engine + self.offset['signatures']['dwbSendPackets'], constant.STATE_SENDING_PACKETS_ENABLE if status else constant.STATE_SENDING_PACKETS_DISABLE, 'b')
        return True
    
    def world_to_screen(self, coords):
        return util.world_to_screen(coords, self.get_view_matrix(), constant.PROCESS_TITLE)

class Entity:
    def __init__(self, pycsapi, player, id):
        self.pycsapi = pycsapi
        
        self.client = pycsapi.client
        self.engine = pycsapi.engine
        self.game = pycsapi.game
        self.offset = pycsapi.offset
        
        self._get_local_player = pycsapi._get_local_player
        self._get_flags = pycsapi._get_flags
        self._get_engine_pointer = pycsapi._get_engine_pointer
        self._get_radar = pycsapi._get_radar
        self._get_radar_pointer = pycsapi._get_radar_pointer
        
        self.player = player
        self.id = id
    
    def _get_class_id(self):
        vtable = win32.read_memory(self.game, self._get_offset() + 0x08, 'i')
        get_client_class = win32.read_memory(self.game, vtable + 0x08, 'i')
        get_client_class_pointer = win32.read_memory(self.game, get_client_class + 0x01, 'i')
        return win32.read_memory(self.game, get_client_class_pointer + 0x14, 'i')
    
    def _get_offset(self):
        return win32.read_memory(self.game, self.client + self.offset['signatures']['dwEntityList'] + ((self.id - 1) * constant.ENTITY_SIZE), 'i')
    
    def get_armor(self):
        return win32.read_memory(self.game, self._get_offset() + self.offset['netvars']['m_ArmorValue'], 'i')
    
    def get_collision(self):
        x_min, y_min, z_min, x_max, y_max, z_max = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
        if not self.is_alive():
            return ((x_min, y_min, z_min), (x_max, y_max, z_max))
        x_min = win32.read_memory(self.game, self._get_offset() + self.offset['netvars']['m_Collision'] + constant.VEC_MIN, 'f')
        y_min = win32.read_memory(self.game, self._get_offset() + self.offset['netvars']['m_Collision'] + constant.VEC_MIN + constant.TYPE_FLOAT_SIZE, 'f')
        z_min = win32.read_memory(self.game, self._get_offset() + self.offset['netvars']['m_Collision'] + constant.VEC_MIN + constant.TYPE_FLOAT_SIZE * 2, 'f')
        x_max = win32.read_memory(self.game, self._get_offset() + self.offset['netvars']['m_Collision'] + constant.VEC_MAX, 'f')
        y_max = win32.read_memory(self.game, self._get_offset() + self.offset['netvars']['m_Collision'] + constant.VEC_MAX + constant.TYPE_FLOAT_SIZE, 'f')
        z_max = win32.read_memory(self.game, self._get_offset() + self.offset['netvars']['m_Collision'] + constant.VEC_MAX + constant.TYPE_FLOAT_SIZE * 2, 'f')
        return ((x_min, y_min, z_min), (x_max, y_max, z_max))
    
    def get_health(self):
        if self.player.is_in_game() and self.get_team_id():
            health = win32.read_memory(self.game, self._get_offset() + self.offset['netvars']['m_iHealth'], 'i')
            if 100 >= health > 0:
                return health
        return 0
    
    def get_id(self):
        return self.id
    
    # TODO: FIX
    '''def get_name(self):
        name = ''
        if not self.player.is_in_game() or not self.is_player():
            return name
        radar_pointer = self._get_radar_pointer()
        for num in range(constant.NAME_SIZE):
            character = win32.read_memory(self.game, radar_pointer + (constant.RADAR_SIZE * (self.get_id() + 1) + constant.RADAR_NAME_OFFSET) + num, 'c')
            if character == b'\x00':
                break
            name += character.decode()
        return name'''
    
    def get_origin(self):
        x, y, z = 0.0, 0.0, 0.0
        if not self.is_alive():
            return (x, y, z)
        x = win32.read_memory(self.game, self._get_offset() + self.offset['netvars']['m_vecOrigin'], 'f')
        y = win32.read_memory(self.game, self._get_offset() + self.offset['netvars']['m_vecOrigin'] + constant.TYPE_FLOAT_SIZE, 'f')
        z = win32.read_memory(self.game, self._get_offset() + self.offset['netvars']['m_vecOrigin'] + constant.TYPE_FLOAT_SIZE * 2, 'f')
        return (x, y, z)
    
    def get_position(self, bone_id = constant.HITBOX_ID_HEAD, player = False):
        x, y, z = 0.0, 0.0, 0.0
        if not self.is_alive():
            return (x, y, z)
        if player:
            x = win32.read_memory(self.game, self._get_offset() + self.offset['netvars']['m_vecOrigin'], 'f')
            y = win32.read_memory(self.game, self._get_offset() + self.offset['netvars']['m_vecOrigin'] + constant.TYPE_FLOAT_SIZE, 'f')
            z = win32.read_memory(self.game, self._get_offset() + self.offset['netvars']['m_vecOrigin'] + constant.TYPE_FLOAT_SIZE * 2, 'f') + win32.read_memory(self.game, self._get_offset() + self.offset['netvars']['m_vecViewOffset'] + constant.TYPE_FLOAT_SIZE * 2, 'f')
        else:
            entity_bones = win32.read_memory(self.game, self._get_offset() + self.offset['netvars']['m_dwBoneMatrix'], 'i')
            x = win32.read_memory(self.game, entity_bones + constant.BONE_MATRIX_SIZE * bone_id + 0x0C, 'f')
            y = win32.read_memory(self.game, entity_bones + constant.BONE_MATRIX_SIZE * bone_id + 0x1C, 'f')
            z = win32.read_memory(self.game, entity_bones + constant.BONE_MATRIX_SIZE * bone_id + 0x2C, 'f')
        return (x, y, z)
    
    def get_punch(self):
        x, y = 0.0, 0.0
        if not self.is_alive():
            return (x, y)
        x = win32.read_memory(self.game, self._get_offset() + self.offset['netvars']['m_aimPunchAngle'], 'f')
        y = win32.read_memory(self.game, self._get_offset() + self.offset['netvars']['m_aimPunchAngle'] + constant.TYPE_FLOAT_SIZE, 'f')
        return (x, y)
    
    def get_shots_fired(self):
        if not self.is_alive():
            return 0
        return win32.read_memory(self.game, self._get_offset() + self.offset['netvars']['m_iShotsFired'], 'i')
    
    def get_spectator_target(self):
        if not self.player.is_in_game() or self.is_alive():
            return False
        return Entity(self.pycsapi, self.player, win32.read_memory(self.game, self._get_offset() + self.offset['netvars']['m_hObserverTarget'], 'i') & 0xFFF)
    
    def get_team_id(self):
        if self.player.is_in_game():
            state = win32.read_memory(self.game, self._get_offset() + self.offset['netvars']['m_iTeamNum'], 'i')
            if state == constant.TEAM_ID_SPECTATOR or state == constant.TEAM_ID_T or state == constant.TEAM_ID_CT:
                return state
        return 0
    
    def get_view_angle(self):
        x, y = 0.0, 0.0
        if not self.player.is_alive():
            return (x, y)
        x = win32.read_memory(self.game, self._get_engine_pointer() + self.offset['signatures']['dwClientState_ViewAngles'], 'f')
        y = win32.read_memory(self.game, self._get_engine_pointer() + self.offset['signatures']['dwClientState_ViewAngles'] + constant.TYPE_FLOAT_SIZE, 'f')
        return (x, y)
    
    def get_weapon(self):
        if not self.is_player() or not self.is_alive():
            return 0
        active_weapon = win32.read_memory(self.game, self._get_offset() + self.offset['netvars']['m_hActiveWeapon'], 'i') & 0xFFF
        entity = win32.read_memory(self.game, self.client + self.offset['signatures']['dwEntityList'] + ((active_weapon - 1) * constant.ENTITY_SIZE), 'i')
        return win32.read_memory(self.game, entity + self.offset['netvars']['m_iItemDefinitionIndex'], 'i')
    
    def is_able_to_shoot(self):
        if not self.is_alive():
            return False
        active_weapon = win32.read_memory(self.game, self._get_offset() + self.offset['netvars']['m_hActiveWeapon'], 'i') & 0xFFF
        entity = win32.read_memory(self.game, self.client + self.offset['signatures']['dwEntityList'] + ((active_weapon - 1) * constant.ENTITY_SIZE), 'i')
        next_attack = win32.read_memory(self.game, entity + self.offset['netvars']['m_flNextPrimaryAttack'], 'f')
        server_time = win32.read_memory(self.game, self._get_offset() + self.offset['netvars']['m_nTickBase'], 'i') * constant.INTERVAL_PER_TICK
        return next_attack <= server_time
    
    def is_alive(self):
        return self.player.is_in_game() and 0 < self.get_health() <= 100
    
    def is_bspotted(self):
        if not self.is_player() or not self.is_alive():
            return False
        return win32.read_memory(self.game, self._get_offset() + self.offset['netvars']['m_bSpotted'], 'b') == constant.STATE_SPOTTED
    
    def is_dormant(self):
        if not self.is_player() or not self.is_alive():
            return False
        return win32.read_memory(self.game, self._get_offset() + self.offset['netvars']['m_bGunGameImmunity'], 'b') == constant.STATE_DORMANT
    
    def is_has_defuser(self):
        if not self.is_player() or not self.is_alive():
            return False
        return bool(win32.read_memory(self.game, self._get_offset() + self.offset['netvars']['m_bHasDefuser'], 'b'))
    
    def is_has_helmet(self):
        if not self.is_player() or not self.is_alive():
            return False
        return bool(win32.read_memory(self.game, self._get_offset() + self.offset['netvars']['m_bHasHelmet'], 'b'))
    
    def is_player(self):
        return self.player.is_in_game() and self.is_alive()
    
    def is_scoped(self):
        if not self.is_player() or not self.is_alive():
            return False
        return win32.read_memory(self.game, self._get_offset() + self.offset['netvars']['m_bIsScoped'], 'b') == constant.STATE_SCOPED
    
    def set_bspotted(self, status = True):
        if not self.is_player() or not self.is_alive():
            return False
        win32.write_memory(self.game, self._get_offset() + self.offset['netvars']['m_bSpotted'], constant.STATE_SPOTTED if status else constant.STATE_NOT_SPOTTED, 'b')
        return True
    
    def set_glow(self, color = (255, 255, 255, 255)):
        if not self.player.is_alive() or not self.is_alive() or not self.player.get_team_id():
            return False
        if len(color) == 3:
            color = (color[0], color[1], color[2], 255)
        elif len(color) != 4:
            color = (255, 255, 255, 255)
        r, g, b, a = color[0] / 255, color[1] / 255, color[2] / 255, color[3] / 255
        if r > 1.0 or r < 0.0: r = 1.0
        if g > 1.0 or g < 0.0: g = 1.0
        if b > 1.0 or b < 0.0: b = 1.0
        if a > 1.0 or a < 0.0: a = 1.0
        entity_glow_index = win32.read_memory(self.game, self._get_offset() + self.offset['netvars']['m_iGlowIndex'], 'i')
        glow_pointer = win32.read_memory(self.game, self.client + self.offset['signatures']['dwGlowObjectManager'], 'i')
        win32.write_memory(self.game, glow_pointer + (entity_glow_index * constant.GLOW_INDEX_SIZE) + constant.TYPE_FLOAT_SIZE, r, 'f')
        win32.write_memory(self.game, glow_pointer + (entity_glow_index * constant.GLOW_INDEX_SIZE) + constant.TYPE_FLOAT_SIZE * 2, g, 'f')
        win32.write_memory(self.game, glow_pointer + (entity_glow_index * constant.GLOW_INDEX_SIZE) + constant.TYPE_FLOAT_SIZE * 3, b, 'f')
        win32.write_memory(self.game, glow_pointer + (entity_glow_index * constant.GLOW_INDEX_SIZE) + constant.TYPE_FLOAT_SIZE * 4, a, 'f')
        win32.write_memory(self.game, glow_pointer + (entity_glow_index * constant.GLOW_INDEX_SIZE) + 0x24, 1, 'i')
        win32.write_memory(self.game, glow_pointer + (entity_glow_index * constant.GLOW_INDEX_SIZE) + 0x25, 0, 'i')
        return True

class Player:
    def __init__(self, pycsapi):
        self.pycsapi = pycsapi
        
        self.client = pycsapi.client
        self.engine = pycsapi.engine
        self.game = pycsapi.game
        self.offset = pycsapi.offset
        
        self.bsp = None
        
        self._get_local_player = pycsapi._get_local_player
        self._get_flags = pycsapi._get_flags
        self._get_engine_pointer = pycsapi._get_engine_pointer
        self._get_radar = pycsapi._get_radar
        self._get_radar_pointer = pycsapi._get_radar_pointer
    
    def _get_class_id(self):
        return constant.CLASS_CCSPLAYER
    
    def _get_offset(self):
        return self._get_local_player()
    
    def get_armor(self):
        return self.get_entity().get_armor()
    
    def get_crosshair_entity(self):
        if not self.is_alive():
            return None
        id = win32.read_memory(self.game, self._get_offset() + self.offset['netvars']['m_iCrosshairId'], 'i')
        if not id:
            return None
        return Entity(self.pycsapi, self, id)
    
    def get_distance_to(self, entity, bone_id = constant.HITBOX_ID_HEAD):
        if not self.is_alive():
            return
        entity_pos = entity.get_position(bone_id)
        self_pos = self.get_position()
        return (entity_pos[0] - self_pos[0], entity_pos[1] - self_pos[1], entity_pos[2] - self_pos[2])
    
    def get_entity(self):
        return Entity(self.pycsapi, self, win32.read_memory(self.game, self._get_engine_pointer() + self.offset['signatures']['dwClientState_GetLocalPlayer'], 'i') + 1)
    
    def get_health(self):
        return self.get_entity().get_health()
    
    # TODO: FIX
    '''def get_name(self):
        return self.get_entity().get_name()'''
    
    def get_position(self):
        return self.get_entity().get_position(None, True)
    
    def get_punch(self):
        return self.get_entity().get_punch()
    
    def get_shots_fired(self):
        return self.get_entity().get_shots_fired()
    
    def get_spectator_target(self):
        return self.get_entity().get_spectator_target()
    
    def get_team_id(self):
        return self.get_entity().get_team_id()
    
    def get_view_angle(self):
        return self.get_entity().get_view_angle()
    
    def get_weapon(self):
        return self.get_entity().get_weapon()
    
    def is_able_to_shoot(self):
        return self.get_entity().is_able_to_shoot()
    
    def is_alive(self):
        return self.get_entity().is_alive()
    
    def is_dormant(self):
        return self.get_entity().is_dormant()
    
    def is_has_defuser(self):
        return self.get_entity().is_has_defuser()
    
    def is_has_helmet(self):
        return self.get_entity().is_has_helmet()
    
    def is_in_game(self):
        return win32.read_memory(self.game, self._get_engine_pointer() + self.offset['signatures']['dwClientState_State'], 'i') == constant.STATE_IN_GAME_CONNECTED
    
    def is_on_ground(self):
        return self.is_alive() and self.get_team_id() > 1 and bool(self._get_flags() & (1 << 0))
    
    def is_player(self):
        return True
    
    def is_scoped(self):
        return self.get_entity().is_scoped()
    
    def is_visible(self, entity):
        if not self.bsp:
            self.bsp = util.BSPParsing(self.pycsapi.get_bsp_file())
        return self.bsp.is_visible(self.get_position(), entity.get_position())
    
    def is_visible_fov(self, entity):
        if not self.is_alive():
            return False
        mask = win32.read_memory(self.game, entity._get_offset() + self.offset['netvars']['m_bSpottedByMask'], 'i')
        base = win32.read_memory(self.game, self._get_offset() + 0x64, 'i') - 1
        return (mask & (1 << base)) > 0
    
    def reload(self):
        if not self.is_alive():
            return False
        self.pycsapi.execute_command('+reload')
        time.sleep(.01)
        self.pycsapi.execute_command('-reload')
        return True
    
    def send_chat(self, message, only_team = False):
        if not self.is_in_game():
            return False
        return self.pycsapi.execute_command('{} {}'.format('say' if not only_team else 'say_team', message))
    
    def set_backward(self, status = True):
        if not self.is_alive():
            return False
        win32.write_memory(self.game, self.client + self.offset['signatures']['dwForceBackward'], constant.STATE_MOVING_ENABLE if status else constant.STATE_MOVING_DISABLE, 'i')
        return True
    
    def set_duck(self, status = True):
        if not self.is_alive():
            return False
        self.pycsapi.execute_command('+duck' if status else '-duck')
        return True
    
    def set_flash_alpha(self, value):
        if not self.is_alive():
            return False
        win32.write_memory(self.game, self._get_offset() + self.offset['netvars']['m_flFlashMaxAlpha'], float(value), 'f')
        return True
    
    def set_forward(self, status = True):
        if not self.is_alive():
            return False
        win32.write_memory(self.game, self.client + self.offset['signatures']['dwForceForward'], constant.STATE_MOVING_ENABLE if status else constant.STATE_MOVING_DISABLE, 'i')
        return True
    
    def set_left(self, status = True):
        if not self.is_alive():
            return False
        win32.write_memory(self.game, self.client + self.offset['signatures']['dwForceLeft'], constant.STATE_MOVING_ENABLE if status else constant.STATE_MOVING_DISABLE, 'i')
        return True
    
    def set_jump(self, status = True):
        if not self.is_alive():
            return False
        win32.write_memory(self.game, self.client + self.offset['signatures']['dwForceJump'], constant.STATE_JUMPING_ENABLE if status else constant.STATE_JUMPING_DISABLE, 'i')
        return True
    
    def set_right(self, status = True):
        if not self.is_alive():
            return False
        win32.write_memory(self.game, self.client + self.offset['signatures']['dwForceRight'], constant.STATE_MOVING_ENABLE if status else constant.STATE_MOVING_DISABLE, 'i')
        return True
    
    def set_shift(self, status = True):
        if not self.is_alive():
            return False
        self.pycsapi.execute_command('+speed' if status else '-speed')
        return True
    
    def set_shoot(self, status = True):
        if not self.is_alive():
            return False
        win32.write_memory(self.game, self.client + self.offset['signatures']['dwForceAttack'], constant.STATE_SHOOTING_ENABLE if status else constant.STATE_SHOOTING_DISABLE, 'i')
        return True
    
    def set_view_angle(self, x, y):
        if not self.is_alive():
            return False
        win32.write_memory(self.game, self._get_engine_pointer() + self.offset['signatures']['dwClientState_ViewAngles'], x, 'f')
        win32.write_memory(self.game, self._get_engine_pointer() + self.offset['signatures']['dwClientState_ViewAngles'] + constant.TYPE_FLOAT_SIZE, y, 'f')
        return True