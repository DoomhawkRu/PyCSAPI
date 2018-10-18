'''
Copyright (c) 2018 Doomhawk

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

import json
import requests
try:
    from pycsapi import constant
    from pycsapi import util
    from pycsapi import win32util
except:
    import constant
    import util
    import win32util

class PyCSAPI:
    def __init__(self):
        self.game = win32util.get_process(constant.PROCESS_TITLE)
        if not self.game:
            raise Exception('Process ' + constant.PROCESS_TITLE + ' is not found!')
        self.client = win32util.get_module_offset(win32util.get_module(self.game, constant.CLIENT_DLL))
        self.engine = win32util.get_module_offset(win32util.get_module(self.game, constant.ENGINE_DLL))
        if not self.client or not self.engine:
            raise Exception('Unable to load required modules!')
        self.offset = self.load_offsets()
        self.player = Player(self)
    
    def _get_engine_pointer(self):
        return win32util.read_memory(self.game, self.engine + self.offset['signatures']['dwClientState'], 'i')
    
    def _get_flags(self):
        return win32util.read_memory(self.game, self._get_local_player() + self.offset['netvars']['m_fFlags'], 'i')
    
    def _get_local_player(self):
        return win32util.read_memory(self.game, self.client + self.offset['signatures']['dwLocalPlayer'], 'i')
    
    def _get_radar(self):
        return win32util.read_memory(self.game, self.client + self.offset['signatures']['dwRadarBase'], 'i')
    
    def _get_radar_pointer(self):
        return win32util.read_memory(self.game, self._get_radar() + constant.RADAR_POINTER_OFFSET, 'i')
    
    def is_sending_packets(self):
        return bool(win32util.read_memory(self.game, self.engine + self.offset['signatures']['dwbSendPackets'], 'b'))
    
    def get_bsp_file(self):
        game_dir = self.get_game_dir()
        map_dir = self.get_map_directory()
        if not game_dir or not map_dir:
            return ''
        return game_dir + '\\' + map_dir
    
    def get_game_dir(self):
        name = ''
        if not self.get_player().is_in_game():
            return name
        for i in range(constant.GAME_DIR_SIZE):
            character = win32util.read_memory(self.game, self.engine + self.offset['signatures']['dwGameDir'] + i, 'c')
            if character == b'\x00':
                break
            name += character.decode()
        return name
    
    def get_map(self):
        name = ''
        if not self.get_player().is_in_game():
            return name
        for i in range(constant.MAP_NAME_SIZE):
            character = win32util.read_memory(self.game, self._get_engine_pointer() + self.offset['signatures']['dwClientState_Map'] + i, 'c')
            if character == b'\x00':
                break
            name += character.decode()
        return name
    
    def get_map_directory(self):
        name = ''
        if not self.get_player().is_in_game():
            return name
        for i in range(constant.MAP_DIRECTORY_SIZE):
            character = win32util.read_memory(self.game, self._get_engine_pointer() + self.offset['signatures']['dwClientState_MapDirectory'] + i, 'c')
            if character == b'\x00':
                break
            name += character.decode()
        return name
    
    def get_max_players(self):
        if not self.get_player().is_in_game():
            return 0
        return win32util.read_memory(self.game, self._get_engine_pointer() + self.offset['signatures']['dwClientState_MaxPlayer'], 'i')
    
    def get_player(self):
        return self.player
    
    def get_players(self, max_players = 64):
        entities = []
        if not self.get_player().is_in_game():
            return entities
        for entity in range(max_players):
            e = Entity(self, self.get_player(), entity)
            if e.is_player():
                entities.append(e)
        return entities
    
    def get_view_matrix(self):
        matrix = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        if not self.get_player().is_in_game() or not self.get_player().is_alive():
            return matrix
        for row in range(4):
            for column in range(4):
                matrix[row][column] = win32util.read_memory(self.game, self.client + self.offset['signatures']['dwViewMatrix'] + ((row * 4) + (column)) * constant.TYPE_FLOAT_SIZE, 'f')
        return matrix
    
    def load_offsets(self):
        return json.loads(requests.get(constant.URL_OFFSETS).text)
    
    def set_sending_packets(self, status = True):
        win32util.write_memory(self.game, self.engine + self.offset['signatures']['dwbSendPackets'], constant.STATE_SENDING_PACKETS_ENABLE if status else constant.STATE_SENDING_PACKETS_DISABLE, 'b')
        
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
    
    def _get_offset(self):
        return win32util.read_memory(self.game, self.client + self.offset['signatures']['dwEntityList'] + ((self.id - 1) * constant.ENTITY_SIZE), 'i')
    
    def get_health(self):
        if self.player.is_in_game() and self.get_team_id():
            health = win32util.read_memory(self.game, self._get_offset() + self.offset['netvars']['m_iHealth'], 'i')
            if 100 >= health > 0:
                return health
        return 0
    
    def get_id(self):
        return self.id
    
    def get_name(self):
        name = ''
        if not self.player.is_in_game() or not self.player.get_team_id() or not self.is_player():
            return name
        radar_pointer = self._get_radar_pointer()
        for num in range(constant.NAME_SIZE):
            character = win32util.read_memory(self.game, radar_pointer + (constant.RADAR_SIZE * (self.get_id() + 1) + constant.RADAR_NAME_OFFSET) + num, 'c')
            if character == b'\x00':
                break
            name += character.decode()
        return name
    
    def get_position(self, bone_id = constant.HITBOX_ID_HEAD, player = False):
        x, y, z = 0.0, 0.0, 0.0
        if not self.player.is_in_game() or not self.is_alive():
            return (x, y, z)
        if player:
            x = win32util.read_memory(self.game, self._get_offset() + self.offset['netvars']['m_vecOrigin'], 'f')
            y = win32util.read_memory(self.game, self._get_offset() + self.offset['netvars']['m_vecOrigin'] + constant.TYPE_FLOAT_SIZE, 'f')
            z = win32util.read_memory(self.game, self._get_offset() + self.offset['netvars']['m_vecOrigin'] + constant.TYPE_FLOAT_SIZE * 2, 'f') + win32util.read_memory(self.game, self._get_offset() + self.offset['netvars']['m_vecViewOffset'] + constant.TYPE_FLOAT_SIZE * 2, 'f')
        else:
            entity_bones = win32util.read_memory(self.game, self._get_offset() + self.offset['netvars']['m_dwBoneMatrix'], 'i')
            x = win32util.read_memory(self.game, entity_bones + constant.BONE_MATRIX_SIZE * bone_id + 0x0C, 'f')
            y = win32util.read_memory(self.game, entity_bones + constant.BONE_MATRIX_SIZE * bone_id + 0x1C, 'f')
            z = win32util.read_memory(self.game, entity_bones + constant.BONE_MATRIX_SIZE * bone_id + 0x2C, 'f')
        return (x, y, z)
    
    def get_punch(self):
        x, y = 0.0, 0.0
        if not self.player.is_in_game() or not self.is_alive():
            return (x, y)
        x = win32util.read_memory(self.game, self._get_offset() + self.offset['netvars']['m_aimPunchAngle'], 'f')
        y = win32util.read_memory(self.game, self._get_offset() + self.offset['netvars']['m_aimPunchAngle'] + constant.TYPE_FLOAT_SIZE, 'f')
        return (x, y)
    
    def get_shots_fired(self):
        if not self.player.is_in_game() or not self.is_player() or not self.is_alive():
            return 0
        return win32util.read_memory(self.game, self._get_offset() + self.offset['netvars']['m_iShotsFired'], 'i')
    
    def get_team_id(self):
        try:
            state = int(self.player.is_in_game()) and win32util.read_memory(self.game, self._get_offset() + self.offset['netvars']['m_iTeamNum'], 'i')
            return 0 if state < 0 or state > 3 else state
        except:
            return 0
    
    def get_view_angle(self):
        x, y = 0.0, 0.0
        if not self.player.is_in_game() or not self.player.is_alive():
            return (x, y)
        x = win32util.read_memory(self.game, self._get_engine_pointer() + self.offset['signatures']['dwClientState_ViewAngles'], 'f')
        y = win32util.read_memory(self.game, self._get_engine_pointer() + self.offset['signatures']['dwClientState_ViewAngles'] + constant.TYPE_FLOAT_SIZE, 'f')
        return (x, y)
    
    def get_weapon(self):
        if not self.player.is_in_game() or not self.is_player() or not self.is_alive():
            return 0
        active_weapon = win32util.read_memory(self.game, self._get_offset() + self.offset['netvars']['m_hActiveWeapon'], 'i') & 0xFFF
        entity = win32util.read_memory(self.game, self.client + self.offset['signatures']['dwEntityList'] + ((active_weapon - 1) * constant.ENTITY_SIZE), 'i')
        return win32util.read_memory(self.game, entity + self.offset['netvars']['m_iItemDefinitionIndex'], 'i')
    
    def is_alive(self):
        return self.player.is_in_game() and bool(self.player.get_health()) and not bool(win32util.read_memory(self.game, self._get_offset() + self.offset['netvars']['m_lifeState'], 'i'))
    
    def is_bspotted(self):
        if not self.player.is_in_game() or not self.is_player() or not self.is_alive():
            return False
        return win32util.read_memory(self.game, self._get_offset() + self.offset['netvars']['m_bSpotted'], 'b') == constant.STATE_SPOTTED
    
    def is_dormant(self):
        if not self.player.is_in_game() or not self.is_player() or not self.is_alive():
            return False
        return win32util.read_memory(self.game, self._get_offset() + self.offset['netvars']['m_bGunGameImmunity'], 'b') == constant.STATE_DORMANT
    
    def is_player(self):
        return self.player.is_in_game() and bool(self.get_health()) and (self.get_team_id() == constant.TEAM_ID_T or self.get_team_id() == constant.TEAM_ID_CT)
    
    def is_scoped(self):
        if not self.player.is_in_game() or not self.is_player() or not self.is_alive():
            return False
        return win32util.read_memory(self.game, self._get_offset() + self.offset['netvars']['m_bIsScoped'], 'b') == constant.STATE_SCOPED
    
    def set_bspotted(self, status = True):
        if not self.player.is_in_game() or not self.is_player() or not self.is_alive():
            return False
        win32util.write_memory(self.game, self._get_offset() + self.offset['netvars']['m_bSpotted'], constant.STATE_SPOTTED if status else constant.STATE_NOT_SPOTTED, 'b')

    def set_glow(self, color = (255, 255, 255)):
        if not self.player.is_in_game() or not self.player.is_alive() or not self.player.get_team_id():
            return
        if not len(color) == 3:
            color = (255, 255, 255)
        r, g, b = color[0] / 255, color[1] / 255, color[2] / 255
        if r > 1 or r < 0: r = 1.0
        if g > 1 or g < 0: g = 1.0
        if b > 1 or b < 0: b = 1.0
        entity_glow_index = win32util.read_memory(self.game, self._get_offset() + self.offset['netvars']['m_iGlowIndex'], 'i')
        glow_pointer = win32util.read_memory(self.game, self.client + self.offset['signatures']['dwGlowObjectManager'], 'i')
        win32util.write_memory(self.game, glow_pointer + (entity_glow_index * constant.GLOW_INDEX_SIZE) + constant.TYPE_FLOAT_SIZE, r, 'f')
        win32util.write_memory(self.game, glow_pointer + (entity_glow_index * constant.GLOW_INDEX_SIZE) + constant.TYPE_FLOAT_SIZE * 2, g, 'f')
        win32util.write_memory(self.game, glow_pointer + (entity_glow_index * constant.GLOW_INDEX_SIZE) + constant.TYPE_FLOAT_SIZE * 3, b, 'f')
        win32util.write_memory(self.game, glow_pointer + (entity_glow_index * constant.GLOW_INDEX_SIZE) + constant.TYPE_FLOAT_SIZE * 4, 1.0, 'f')
        win32util.write_memory(self.game, glow_pointer + (entity_glow_index * constant.GLOW_INDEX_SIZE) + 0x24, 1, 'i')
        win32util.write_memory(self.game, glow_pointer + (entity_glow_index * constant.GLOW_INDEX_SIZE) + 0x25, 0, 'i')

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
    
    def get_crosshair_entity(self):
        if not self.is_in_game() or not self.is_alive():
            return None
        id = win32util.read_memory(self.game, self._get_local_player() + self.offset['netvars']['m_iCrosshairId'], 'i')
        if not id:
            return None
        return Entity(self.pycsapi, self, id)
    
    def get_distance_to(self, entity, bone_id = constant.HITBOX_ID_HEAD):
        if not self.is_in_game() or not self.is_alive():
            return
        entity_pos = entity.get_position(bone_id)
        self_pos = self.get_position()
        return (entity_pos[0] - self_pos[0], entity_pos[1] - self_pos[1], entity_pos[2] - self_pos[2])
    
    def get_entity(self):
        return Entity(self.pycsapi, self, win32util.read_memory(self.game, self._get_engine_pointer() + self.offset['signatures']['dwClientState_GetLocalPlayer'], 'i') + 1)
    
    def get_health(self):
        return self.get_entity().get_health()

    def get_name(self):
        return self.get_entity().get_name()
    
    def get_position(self):
        return self.get_entity().get_position(None, True)
    
    def get_punch(self):
        return self.get_entity().get_punch()
    
    def get_shots_fired(self):
        return self.get_entity().get_shots_fired()
    
    def get_team_id(self):
        return self.get_entity().get_team_id()
    
    def get_view_angle(self):
        return self.get_entity().get_view_angle()
    
    def get_weapon(self):
        return self.get_entity().get_weapon()
    
    def is_alive(self):
        return self.get_entity().is_alive()
    
    def is_dormant(self):
        return self.get_entity().is_dormant()
    
    def is_in_game(self):
        return win32util.read_memory(self.game, self._get_engine_pointer() + self.offset['signatures']['dwClientState_State'], 'i') == constant.STATE_IN_GAME_CONNECTED
    
    def is_on_ground(self):
        return self.is_in_game() and bool(self.is_alive()) and self.get_team_id() > 1 and bool(self._get_flags() & (1 << 0))
    
    def is_scoped(self):
        return self.get_entity().is_scoped()
    
    def is_visible(self, entity):
        if not self.bsp:
            self.bsp = util.BSPParsing(self.pycsapi.get_bsp_file())
        return self.bsp.is_visible(self.get_position(), entity.get_position())
    
    def is_visible_fov(self, entity):
        if not self.is_in_game() or not self.is_alive():
            return
        mask = win32util.read_memory(self.game, entity._get_offset() + self.offset['netvars']['m_bSpottedByMask'], 'i')
        base = win32util.read_memory(self.game, self._get_local_player() + 0x64, 'i') - 1
        return (mask & (1 << base)) > 0
    
    def set_backward(self, status = True):
        if not self.is_in_game() or not self.is_alive():
            return
        win32util.write_memory(self.game, self.client + self.offset['signatures']['dwForceBackward'], constant.STATE_MOVING_ENABLE if status else constant.STATE_MOVING_DISABLE, 'i')
    
    def set_flash_alpha(self, value):
        if not self.is_in_game() or not self.is_alive():
            return
        win32util.write_memory(self.game, self._get_local_player() + self.offset['netvars']['m_flFlashMaxAlpha'], float(value), 'f')
    
    def set_forward(self, status = True):
        if not self.is_in_game() or not self.is_alive():
            return
        win32util.write_memory(self.game, self.client + self.offset['signatures']['dwForceForward'], constant.STATE_MOVING_ENABLE if status else constant.STATE_MOVING_DISABLE, 'i')
    
    def set_jump(self, status = True):
        if not self.is_in_game() or not self.is_alive():
            return
        win32util.write_memory(self.game, self.client + self.offset['signatures']['dwForceJump'], constant.STATE_JUMPING_ENABLE if status else constant.STATE_JUMPING_DISABLE, 'i')
    
    def set_left(self, status = True):
        if not self.is_in_game() or not self.is_alive():
            return
        win32util.write_memory(self.game, self.client + self.offset['signatures']['dwForceLeft'], constant.STATE_MOVING_ENABLE if status else constant.STATE_MOVING_DISABLE, 'i')
    
    def set_right(self, status = True):
        if not self.is_in_game() or not self.is_alive():
            return
        win32util.write_memory(self.game, self.client + self.offset['signatures']['dwForceRight'], constant.STATE_MOVING_ENABLE if status else constant.STATE_MOVING_DISABLE, 'i')
    
    def set_shoot(self, status = True):
        if not self.is_in_game() or not self.is_alive():
            return False
        win32util.write_memory(self.game, self.client + self.offset['signatures']['dwForceAttack'], constant.STATE_SHOOTING_ENABLE if status else constant.STATE_SHOOTING_DISABLE, 'i')
    
    def set_view_angle(self, x, y):
        if not self.is_in_game() or not self.is_alive():
            return False
        win32util.write_memory(self.game, self._get_engine_pointer() + self.offset['signatures']['dwClientState_ViewAngles'], x, 'f')
        win32util.write_memory(self.game, self._get_engine_pointer() + self.offset['signatures']['dwClientState_ViewAngles'] + constant.TYPE_FLOAT_SIZE, y, 'f')
        return True