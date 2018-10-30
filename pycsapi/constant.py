'''
Copyright (c) 2018 Doomhawk

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

CLIENT_DLL = 'client_panorama.dll'
ENGINE_DLL = 'engine.dll'
PROCESS_NAME = 'csgo.exe'
PROCESS_TITLE = 'Counter-Strike: Global Offensive'
URL_OFFSETS = 'https://raw.githubusercontent.com/frk1/hazedumper/master/csgo.json'

PATTERN_DWCLIENTCMD = [0x55, 0x8B, 0xEC, 0x8B, 0x0D, -0x01, -0x01, -0x01, -0x01, 0x81, 0xF9, -0x01, -0x01, -0x01, -0x01, 0x75, 0x0C, 0xA1, -0x01, -0x01, -0x01, -0x01, 0x35, -0x01, -0x01, -0x01, -0x01, 0xEB, 0x05, 0x8B, 0x01, 0xFF, 0x50, 0x34, 0x50, 0xA1]

INTERVAL_PER_TICK = 1 / 64

TEAM_ID_INVALID = 0
TEAM_ID_SPECTATOR = 1
TEAM_ID_T = 2
TEAM_ID_CT = 3

TYPE_BYTE_SIZE = 1
TYPE_CHAR_SIZE = 1
TYPE_FLOAT_SIZE = 4
TYPE_INT_SIZE = 4

STATE_DORMANT = 1
STATE_NOT_DORMANT = 0

STATE_JUMPING_DISABLE = 5
STATE_JUMPING_ENABLE = 6

STATE_IN_GAME_CONNECTED = 6

STATE_MOVING_DISABLE = 0
STATE_MOVING_ENABLE = 1

STATE_SCOPED = 1
STATE_NOT_SCOPED = 0

STATE_SENDING_PACKETS_DISABLE = 0
STATE_SENDING_PACKETS_ENABLE = 1

STATE_SHOOTING_DISABLE = 4
STATE_SHOOTING_ENABLE = 6

STATE_SPOTTED = 1
STATE_NOT_SPOTTED = 0

HITBOX_ID_BODY = 6
HITBOX_ID_HEAD = 8
HITBOX_ID_LEFT_HAND = 13
HITBOX_ID_RIGHT_HAND = 39
HITBOX_ID_LEFT_LEG = 66
HITBOX_ID_LEFT_FOOT = 67
HITBOX_ID_RIGHT_LEG = 73
HITBOX_ID_RIGHT_FOOT = 74

HITBOX_PELVIS = (-6.42, -5.7459, -6.8587), (4.5796, 4.5796, 6.8373)
HITBOX_L_THIGH = (1.819, -3.959, -2.14), (22.149002, 3.424, 4.5796)
HITBOX_L_CALF = (2.0758, -3.21, -2.1507), (19.26, 2.675, 3.0495)
HITBOX_L_FOOT = (1.8725, -2.675, -2.4075), (5.6175, 9.694201, 2.4075)
HITBOX_R_THIGH = (1.819, -3.7557, -4.5796), (22.149002, 3.424, 2.14)
HITBOX_R_CALF = (2.0758, -3.21, -2.8462), (19.26, 2.675, 2.247)
HITBOX_R_FOOT = (1.8725, -2.675, -2.4075), (5.6175, 9.694201, 2.4075)
HITBOX_SPINE2 = (-4.28, -4.5796, -6.3879), (3.21, 5.885, 6.2809)
HITBOX_SPINE3 = (-4.28, -5.029, -6.0883), (3.21, 5.885, 5.9813)
HITBOX_SPINE4 = (-4.28, -5.35, -5.885), (2.9211, 5.1467, 5.885)
HITBOX_NECK = (0.3317, -3.0174, -2.4503), (3.4026, 2.4182, 2.354)
HITBOX_HEAD = (-2.7713, -2.8783, -3.103), (6.955, 3.5203, 3.0067)
HITBOX_L_UPPER_ARM = (-2.675, -3.21, -2.14), (12.84, 3.21, 2.14)
HITBOX_L_FOREARM = (0, -2.14, -2.14), (9.63, 2.14, 2.14)
HITBOX_L_HAND = (-1.7227, -1.2198, -1.3803), (4.4726, 1.2198, 1.3803)
HITBOX_R_UPPER_ARM = (-2.675, -3.21, -2.14), (12.84, 3.21, 2.14)
HITBOX_R_FOREARM = (0, -2.14, -2.14), (9.63, 2.14, 2.14)
HITBOX_R_HAND = (-1.7227, -1.2198, -1.3803), (4.4726, 1.2198, 1.3803)
HITBOX_L_CLAVICLE = (0, -3.21, -5.35), (7.49, 4.28, 3.21)
HITBOX_R_CLAVICLE = (0, -3.21, -3.21), (7.49, 4.28, 5.35)
HITBOX_HEAD_2 = (-2.5038, 2.009, -1.1021), (6.3023, 5.2965, 0.9951)
HITBOX_SPINE4_2 = (-0.2996, -6.0027, -4.996901), (5.4998, 2.5038, 5.1039)

BONE_MATRIX_SIZE = 0x30
ENTITY_SIZE = 0x10
GAME_DIR_SIZE = 0x60
GLOW_INDEX_SIZE = 0x38
MAP_DIRECTORY_SIZE = 0x100
MAP_NAME_SIZE = 0x20
NAME_SIZE = 0x40
RADAR_NAME_OFFSET = 0x18
RADAR_POINTER_OFFSET = 0x6C
RADAR_SIZE = 0x168
VEC_MAX = 0x1C
VEC_MIN = 0x10

CLASS_NEXTBOTCOMBATCHARACTER = 0
CLASS_CAK47 = 1
CLASS_CBASEANIMATING = 2
CLASS_CBASEANIMATINGOVERLAY = 3
CLASS_CBASEATTRIBUTABLEITEM = 4
CLASS_CBASEBUTTON = 5
CLASS_CBASECOMBATCHARACTER = 6
CLASS_CBASECOMBATWEAPON = 7
CLASS_CBASECSGRENADE = 8
CLASS_CBASECSGRENADEPROJECTILE = 9
CLASS_CBASEDOOR = 10
CLASS_CBASEENTITY = 11
CLASS_CBASEFLEX = 12
CLASS_CBASEGRENADE = 13
CLASS_CBASEPARTICLEENTITY = 14
CLASS_CBASEPLAYER = 15
CLASS_CBASEPROPDOOR = 16
CLASS_CBASETEAMOBJECTIVERESOURCE = 17
CLASS_CBASETEMPENTITY = 18
CLASS_CBASETOGGLE = 19
CLASS_CBASETRIGGER = 20
CLASS_CBASEVIEWMODEL = 21
CLASS_CBASEVPHYSICSTRIGGER = 22
CLASS_CBASEWEAPONWORLDMODEL = 23
CLASS_CBEAM = 24
CLASS_CBEAMSPOTLIGHT = 25
CLASS_CBONEFOLLOWER = 26
CLASS_CBREAKABLEPROP = 27
CLASS_CBREAKABLESURFACE = 28
CLASS_CC4 = 29
CLASS_CCASCADELIGHT = 30
CLASS_CCHICKEN = 31
CLASS_CCOLORCORRECTION = 32
CLASS_CCOLORCORRECTIONVOLUME = 33
CLASS_CCSGAMERULESPROXY = 34
CLASS_CCSPLAYER = 35
CLASS_CCSPLAYERRESOURCE = 36
CLASS_CCSRAGDOLL = 37
CLASS_CCSTEAM = 38
CLASS_CDEAGLE = 39
CLASS_CDECOYGRENADE = 40
CLASS_CDECOYPROJECTILE = 41
CLASS_CDYNAMICLIGHT = 42
CLASS_CDYNAMICPROP = 43
CLASS_CECONENTITY = 44
CLASS_CEMBERS = 45
CLASS_CENTITYDISSOLVE = 46
CLASS_CENTITYFLAME = 47
CLASS_CENTITYFREEZING = 48
CLASS_CENTITYPARTICLETRAIL = 49
CLASS_CENVAMBIENTLIGHT = 50
CLASS_CENVDETAILCONTROLLER = 51
CLASS_CENVDOFCONTROLLER = 52
CLASS_CENVPARTICLESCRIPT = 53
CLASS_CENVPROJECTEDTEXTURE = 54
CLASS_CENVQUADRATICBEAM = 55
CLASS_CENVSCREENEFFECT = 56
CLASS_CENVSCREENOVERLAY = 57
CLASS_CENVTONEMAPCONTROLLER = 58
CLASS_CENVWIND = 59
CLASS_CFIRECRACKERBLAST = 60
CLASS_CFIRESMOKE = 61
CLASS_CFIRETRAIL = 62
CLASS_CFISH = 63
CLASS_CFLASHBANG = 64
CLASS_CFOGCONTROLLER = 65
CLASS_CFOOTSTEPCONTROL = 66
CLASS_CFUNC_DUST = 67
CLASS_CFUNC_LOD = 68
CLASS_CFUNCAREAPORTALWINDOW = 69
CLASS_CFUNCBRUSH = 70
CLASS_CFUNCCONVEYOR = 71
CLASS_CFUNCLADDER = 72
CLASS_CFUNCMONITOR = 73
CLASS_CFUNCMOVELINEAR = 74
CLASS_CFUNCOCCLUDER = 75
CLASS_CFUNCREFLECTIVEGLASS = 76
CLASS_CFUNCROTATING = 77
CLASS_CFUNCSMOKEVOLUME = 78
CLASS_CFUNCTRACKTRAIN = 79
CLASS_CGAMERULESPROXY = 80
CLASS_CHANDLETEST = 81
CLASS_CHEGRENADE = 82
CLASS_CHOSTAGE = 83
CLASS_CHOSTAGECARRIABLEPROP = 84
CLASS_CINCENDIARYGRENADE = 85
CLASS_CINFERNO = 86
CLASS_CINFOLADDERDISMOUNT = 87
CLASS_CINFOOVERLAYACCESSOR = 88
CLASS_CKNIFE = 89
CLASS_CKNIFEGG = 90
CLASS_CLIGHTGLOW = 91
CLASS_CMATERIALMODIFYCONTROL = 92
CLASS_CMOLOTOVGRENADE = 93
CLASS_CMOLOTOVPROJECTILE = 94
CLASS_CMOVIEDISPLAY = 95
CLASS_CPARTICLEFIRE = 96
CLASS_CPARTICLEPERFORMANCEMONITOR = 97
CLASS_CPARTICLESYSTEM = 98
CLASS_CPHYSBOX = 99
CLASS_CPHYSBOXMULTIPLAYER = 100
CLASS_CPHYSICSPROP = 101
CLASS_CPHYSICSPROPMULTIPLAYER = 102
CLASS_CPHYSMAGNET = 103
CLASS_CPLANTEDC4 = 104
CLASS_CPLASMA = 105
CLASS_CPLAYERRESOURCE = 106
CLASS_CPOINTCAMERA = 107
CLASS_CPOINTCOMMENTARYNODE = 108
CLASS_CPOSECONTROLLER = 109
CLASS_CPOSTPROCESSCONTROLLER = 110
CLASS_CPRECIPITATION = 111
CLASS_CPRECIPITATIONBLOCKER = 112
CLASS_CPREDICTEDVIEWMODEL = 113
CLASS_CPROP_HALLUCINATION = 114
CLASS_CPROPDOORROTATING = 115
CLASS_CPROPJEEP = 116
CLASS_CPROPVEHICLEDRIVEABLE = 117
CLASS_CRAGDOLLMANAGER = 118
CLASS_CRAGDOLLPROP = 119
CLASS_CRAGDOLLPROPATTACHED = 120
CLASS_CROPEKEYFRAME = 121
CLASS_CSCAR17 = 122
CLASS_CSCENEENTITY = 123
CLASS_CSHADOWCONTROL = 124
CLASS_CSLIDESHOWDISPLAY = 125
CLASS_CSMOKEGRENADE = 126
CLASS_CSMOKEGRENADEPROJECTILE = 127
CLASS_CSMOKESTACK = 128
CLASS_CSPATIALENTITY = 129
CLASS_CSPOTLIGHTEND = 130
CLASS_CSPRITE = 131
CLASS_CSPRITEORIENTED = 132
CLASS_CSPRITETRAIL = 133
CLASS_CSTATUEPROP = 134
CLASS_CSTEAMJET = 135
CLASS_CSUN = 136
CLASS_CSUNLIGHTSHADOWCONTROL = 137
CLASS_CTEAM = 138
CLASS_CTEAMPLAYROUNDBASEDRULESPROXY = 139
CLASS_CTEARMORRICOCHET = 140
CLASS_CTEBASEBEAM = 141
CLASS_CTEBEAMENTPOINT = 142
CLASS_CTEBEAMENTS = 143
CLASS_CTEBEAMFOLLOW = 144
CLASS_CTEBEAMLASER = 145
CLASS_CTEBEAMPOINTS = 146
CLASS_CTEBEAMRING = 147
CLASS_CTEBEAMRINGPOINT = 148
CLASS_CTEBEAMSPLINE = 149
CLASS_CTEBLOODSPRITE = 150
CLASS_CTEBLOODSTREAM = 151
CLASS_CTEBREAKMODEL = 152
CLASS_CTEBSPDECAL = 153
CLASS_CTEBUBBLES = 154
CLASS_CTEBUBBLETRAIL = 155
CLASS_CTECLIENTPROJECTILE = 156
CLASS_CTEDECAL = 157
CLASS_CTEDUST = 158
CLASS_CTEDYNAMICLIGHT = 159
CLASS_CTEEFFECTDISPATCH = 160
CLASS_CTEENERGYSPLASH = 161
CLASS_CTEEXPLOSION = 162
CLASS_CTEFIREBULLETS = 163
CLASS_CTEFIZZ = 164
CLASS_CTEFOOTPRINTDECAL = 165
CLASS_CTEFOUNDRYHELPERS = 166
CLASS_CTEGAUSSEXPLOSION = 167
CLASS_CTEGLOWSPRITE = 168
CLASS_CTEIMPACT = 169
CLASS_CTEKILLPLAYERATTACHMENTS = 170
CLASS_CTELARGEFUNNEL = 171
CLASS_CTEMETALSPARKS = 172
CLASS_CTEMUZZLEFLASH = 173
CLASS_CTEPARTICLESYSTEM = 174
CLASS_CTEPHYSICSPROP = 175
CLASS_CTEPLANTBOMB = 176
CLASS_CTEPLAYERANIMEVENT = 177
CLASS_CTEPLAYERDECAL = 178
CLASS_CTEPROJECTEDDECAL = 179
CLASS_CTERADIOICON = 180
CLASS_CTESHATTERSURFACE = 181
CLASS_CTESHOWLINE = 182
CLASS_CTESLA = 183
CLASS_CTESMOKE = 184
CLASS_CTESPARKS = 185
CLASS_CTESPRITE = 186
CLASS_CTESPRITESPRAY = 187
CLASS_CTEST_PROXYTOGGLE_NETWORKABLE = 188
CLASS_CTESTTRACELINE = 189
CLASS_CTEWORLDDECAL = 190
CLASS_CTRIGGERPLAYERMOVEMENT = 191
CLASS_CTRIGGERSOUNDOPERATOR = 192
CLASS_CVGUISCREEN = 193
CLASS_CVOTECONTROLLER = 194
CLASS_CWATERBULLET = 195
CLASS_CWATERLODCONTROL = 196
CLASS_CWEAPONAUG = 197
CLASS_CWEAPONAWP = 198
CLASS_CWEAPONBIZON = 199
CLASS_CWEAPONCSBASE = 200
CLASS_CWEAPONCSBASEGUN = 201
CLASS_CWEAPONCYCLER = 202
CLASS_CWEAPONELITE = 203
CLASS_CWEAPONFAMAS = 204
CLASS_CWEAPONFIVESEVEN = 205
CLASS_CWEAPONG3SG1 = 206
CLASS_CWEAPONGALIL = 207
CLASS_CWEAPONGALILAR = 208
CLASS_CWEAPONGLOCK = 209
CLASS_CWEAPONHKP2000 = 210
CLASS_CWEAPONM249 = 211
CLASS_CWEAPONM3 = 212
CLASS_CWEAPONM4A1 = 213
CLASS_CWEAPONMAC10 = 214
CLASS_CWEAPONMAG7 = 215
CLASS_CWEAPONMP5NAVY = 216
CLASS_CWEAPONMP7 = 217
CLASS_CWEAPONMP9 = 218
CLASS_CWEAPONNEGEV = 219
CLASS_CWEAPONNOVA = 220
CLASS_CWEAPONP228 = 221
CLASS_CWEAPONP250 = 222
CLASS_CWEAPONP90 = 223
CLASS_CWEAPONSAWEDOFF = 224
CLASS_CWEAPONSCAR20 = 225
CLASS_CWEAPONSCOUT = 226
CLASS_CWEAPONSG550 = 227
CLASS_CWEAPONSG552 = 228
CLASS_CWEAPONSG556 = 229
CLASS_CWEAPONSSG08 = 230
CLASS_CWEAPONTASER = 231
CLASS_CWEAPONTEC9 = 232
CLASS_CWEAPONTMP = 233
CLASS_CWEAPONUMP45 = 234
CLASS_CWEAPONUSP = 235
CLASS_CWEAPONXM1014 = 236
CLASS_CWORLD = 237
CLASS_DUSTTRAIL = 238
CLASS_MOVIEEXPLOSION = 239
CLASS_PARTICLESMOKEGRENADE = 240
CLASS_ROCKETTRAIL = 241
CLASS_SMOKETRAIL = 242
CLASS_SPOREEXPLOSION = 243
CLASS_SPORETRAIL = 244

WEAPON_INVALID = 0
WEAPON_DEAGLE = 1
WEAPON_ELITE = 2
WEAPON_FIVESEVEN = 3
WEAPON_GLOCK = 4
WEAPON_AK47 = 7
WEAPON_AUG = 8
WEAPON_AWP = 9
WEAPON_FAMAS = 10
WEAPON_G3SG1 = 11
WEAPON_GALILAR = 13
WEAPON_M249 = 14
WEAPON_M4A1 = 16
WEAPON_MAC10 = 17
WEAPON_P90 = 19
WEAPON_UMP45 = 24
WEAPON_XM1014 = 25
WEAPON_BIZON = 26
WEAPON_MAG7 = 27
WEAPON_NEGEV = 28
WEAPON_SAWEDOFF = 29
WEAPON_TEC9 = 30
WEAPON_TASER = 31
WEAPON_HKP2000 = 32
WEAPON_MP7 = 33
WEAPON_MP9 = 34
WEAPON_NOVA = 35
WEAPON_P250 = 36
WEAPON_SCAR20 = 38
WEAPON_SG556 = 39
WEAPON_SSG08 = 40
WEAPON_KNIFE = 42
WEAPON_FLASHBANG = 43
WEAPON_HEGRENADE = 44
WEAPON_SMOKEGRENADE = 45
WEAPON_MOLOTOV = 46
WEAPON_DECOY = 47
WEAPON_INCGRENADE = 48
WEAPON_C4 = 49
WEAPON_KNIFE_T = 59
WEAPON_M4A1_SILENCER = 60
WEAPON_USP_SILENCER = 61
WEAPON_CZ75A = 63
WEAPON_REVOLVER = 262208
WEAPON_KNIFE_BAYONET = 500
WEAPON_KNIFE_FLIP = 505
WEAPON_KNIFE_GUT = 506
WEAPON_KNIFE_KARAMBIT = 507
WEAPON_KNIFE_M9_BAYONET = 508
WEAPON_KNIFE_TACTICAL = 509
WEAPON_KNIFE_FALCHION = 512
WEAPON_KNIFE_SURVIVAL_BOWIE = 514
WEAPON_KNIFE_BUTTERFLY = 515
WEAPON_KNIFE_PUSH = 516

VK_LBUTTON = 0x01 # Left mouse button
VK_RBUTTON = 0x02 # Right mouse button
VK_CANCEL = 0x03 # Control-break processing
VK_MBUTTON = 0x04 # Middle mouse button (three-button mouse)
VK_XBUTTON1 = 0x05 # X1 mouse button
VK_XBUTTON2 = 0x06 # X2 mouse button
VK_BACK = 0x08 # BACKSPACE key
VK_TAB = 0x09 # TAB key
VK_CLEAR = 0x0C # CLEAR key
VK_RETURN = 0x0D # ENTER key
VK_SHIFT = 0x10 # SHIFT key
VK_CONTROL = 0x11 # CTRL key
VK_MENU = 0x12 # ALT key
VK_PAUSE = 0x13 # PAUSE key
VK_CAPITAL = 0x14 # CAPS LOCK key
VK_KANA = 0x15 # IME Kana mode
VK_HANGUEL = 0x15 # IME Hanguel mode (maintained for compatibility; use VK_HANGUL)
VK_HANGUL = 0x15 # IME Hangul mode
VK_JUNJA = 0x17 # IME Junja mode
VK_FINAL = 0x18 # IME final mode
VK_HANJA = 0x19 # IME Hanja mode
VK_KANJI = 0x19 # IME Kanji mode
VK_ESCAPE = 0x1B # ESC key
VK_CONVERT = 0x1C # IME convert
VK_NONCONVERT = 0x1D # IME nonconvert
VK_ACCEPT = 0x1E # IME accept
VK_MODECHANGE = 0x1F # IME mode change request
VK_SPACE = 0x20 # SPACEBAR
VK_PRIOR = 0x21 # PAGE UP key
VK_NEXT = 0x22 # PAGE DOWN key
VK_END = 0x23 # END key
VK_HOME = 0x24 # HOME key
VK_LEFT = 0x25 # LEFT ARROW key
VK_UP = 0x26 # UP ARROW key
VK_RIGHT = 0x27 # RIGHT ARROW key
VK_DOWN = 0x28 # DOWN ARROW key
VK_SELECT = 0x29 # SELECT key
VK_PRINT = 0x2A # PRINT key
VK_EXECUTE = 0x2B # EXECUTE key
VK_SNAPSHOT = 0x2C # PRINT SCREEN key
VK_INSERT = 0x2D # INS key
VK_DELETE = 0x2E # DEL key
VK_HELP = 0x2F # HELP key
VK_0_KEY = 0x30
VK_1_KEY = 0x31
VK_2_KEY = 0x32
VK_3_KEY = 0x33
VK_4_KEY = 0x34
VK_5_KEY = 0x35
VK_6_KEY = 0x36
VK_7_KEY = 0x37
VK_8_KEY = 0x38
VK_9_KEY = 0x39
VK_A_KEY = 0x41
VK_B_KEY = 0x42
VK_C_KEY = 0x43
VK_D_KEY = 0x44
VK_E_KEY = 0x45
VK_F_KEY = 0x46
VK_G_KEY = 0x47
VK_H_KEY = 0x48
VK_I_KEY = 0x49
VK_J_KEY = 0x4A
VK_K_KEY = 0x4B
VK_L_KEY = 0x4C
VK_M_KEY = 0x4D
VK_N_KEY = 0x4E
VK_O_KEY = 0x4F
VK_P_KEY = 0x50
VK_Q_KEY = 0x51
VK_R_KEY = 0x52
VK_S_KEY = 0x53
VK_T_KEY = 0x54
VK_U_KEY = 0x55
VK_V_KEY = 0x56
VK_W_KEY = 0x57
VK_X_KEY = 0x58
VK_Y_KEY = 0x59
VK_Z_KEY = 0x5A
VK_LWIN = 0x5B # Left Windows key (Natural keyboard) 
VK_RWIN = 0x5C # Right Windows key (Natural keyboard)
VK_APPS = 0x5D # Applications key (Natural keyboard)
VK_SLEEP = 0x5F # Computer Sleep key
VK_NUMPAD0 = 0x60 # Numeric keypad 0 key
VK_NUMPAD1 = 0x61 # Numeric keypad 1 key
VK_NUMPAD2 = 0x62 # Numeric keypad 2 key
VK_NUMPAD3 = 0x63 # Numeric keypad 3 key
VK_NUMPAD4 = 0x64 # Numeric keypad 4 key
VK_NUMPAD5 = 0x65 # Numeric keypad 5 key
VK_NUMPAD6 = 0x66 # Numeric keypad 6 key
VK_NUMPAD7 = 0x67 # Numeric keypad 7 key
VK_NUMPAD8 = 0x68 # Numeric keypad 8 key
VK_NUMPAD9 = 0x69 # Numeric keypad 9 key
VK_MULTIPLY = 0x6A # Multiply key
VK_ADD = 0x6B # Add key
VK_SEPARATOR = 0x6C # Separator key
VK_SUBTRACT = 0x6D # Subtract key
VK_DECIMAL = 0x6E # Decimal key
VK_DIVIDE = 0x6F # Divide key
VK_F1 = 0x70 # F1 key
VK_F2 = 0x71 # F2 key
VK_F3 = 0x72 # F3 key
VK_F4 = 0x73 # F4 key
VK_F5 = 0x74 # F5 key
VK_F6 = 0x75 # F6 key
VK_F7 = 0x76 # F7 key
VK_F8 = 0x77 # F8 key
VK_F9 = 0x78 # F9 key
VK_F10 = 0x79 # F10 key
VK_F11 = 0x7A # F11 key
VK_F12 = 0x7B # F12 key
VK_F13 = 0x7C # F13 key
VK_F14 = 0x7D # F14 key
VK_F15 = 0x7E # F15 key
VK_F16 = 0x7F # F16 key
VK_F17 = 0x80 # F17 key
VK_F18 = 0x81 # F18 key
VK_F19 = 0x82 # F19 key
VK_F20 = 0x83 # F20 key
VK_F21 = 0x84 # F21 key
VK_F22 = 0x85 # F22 key
VK_F23 = 0x86 # F23 key
VK_F24 = 0x87 # F24 key
VK_NUMLOCK = 0x90 # NUM LOCK key
VK_SCROLL = 0x91
VK_LSHIFT = 0xA0 # Left SHIFT key
VK_RSHIFT = 0xA1 # Right SHIFT key
VK_LCONTROL = 0xA2 # Left CONTROL key
VK_RCONTROL = 0xA3 # Right CONTROL key
VK_LMENU = 0xA4 # Left MENU key
VK_RMENU = 0xA5 # Right MENU key
VK_BROWSER_BACK = 0xA6 # Browser Back key
VK_BROWSER_FORWARD = 0xA7 # Browser Forward key
VK_BROWSER_REFRESH = 0xA8 # Browser Refresh key
VK_BROWSER_STOP = 0xA9 # Browser Stop key
VK_BROWSER_SEARCH = 0xAA # Browser Search key 
VK_BROWSER_FAVORITES = 0xAB # Browser Favorites key
VK_BROWSER_HOME = 0xAC # Browser Start and Home key
VK_VOLUME_MUTE = 0xAD # Volume Mute key
VK_VOLUME_DOWN = 0xAE # Volume Down key
VK_VOLUME_UP = 0xAF # Volume Up key
VK_MEDIA_NEXT_TRACK = 0xB0 # Next Track key
VK_MEDIA_PREV_TRACK = 0xB1 # Previous Track key
VK_MEDIA_STOP = 0xB2 # Stop Media key
VK_MEDIA_PLAY_PAUSE = 0xB3 # Play/Pause Media key
VK_LAUNCH_MAIL = 0xB4 # Start Mail key
VK_LAUNCH_MEDIA_SELECT = 0xB5 # Select Media key
VK_LAUNCH_APP1 = 0xB6 # Start Application 1 key
VK_LAUNCH_APP2 = 0xB7 # Start Application 2 key
VK_OEM_1 = 0xBA # Used for miscellaneous characters; it can vary by keyboard. For the US standard keyboard, the ';:' key 
VK_OEM_PLUS = 0xBB # For any country/region, the '+' key
VK_OEM_COMMA = 0xBC # For any country/region, the ',' key
VK_OEM_MINUS = 0xBD # For any country/region, the '-' key
VK_OEM_PERIOD = 0xBE # For any country/region, the '.' key
VK_OEM_2 = 0xBF # Used for miscellaneous characters; it can vary by keyboard. For the US standard keyboard, the '/?' key 
VK_OEM_3 = 0xC0 # Used for miscellaneous characters; it can vary by keyboard. For the US standard keyboard, the '`~' key 
VK_OEM_4 = 0xDB # Used for miscellaneous characters; it can vary by keyboard. For the US standard keyboard, the '[{' key
VK_OEM_5 = 0xDC # Used for miscellaneous characters; it can vary by keyboard. For the US standard keyboard, the '\|' key
VK_OEM_6 = 0xDD # Used for miscellaneous characters; it can vary by keyboard. For the US standard keyboard, the ']}' key
VK_OEM_7 = 0xDE # Used for miscellaneous characters; it can vary by keyboard. For the US standard keyboard, the 'single-quote/double-quote' key
VK_OEM_8 = 0xDF # Used for miscellaneous characters; it can vary by keyboard.
VK_OEM_102 = 0xE2 # Either the angle bracket key or the backslash key on the RT 102-key keyboard = 0xE3-E4
VK_PROCESS_KEY = 0xE5
IME_PROCESS_KEY = 0xE6
VK_PACKET = 0xE7 # Used to pass Unicode characters as if they were keystrokes. The VK_PACKET key is the low word of a 32-bit Virtual Key value used for non-keyboard input methods. For more information, see Remark in KEYBDINPUT, SendInput, WM_KEYDOWN, and WM_KEYUP
VK_ATTN = 0xF6 # Attn key
VK_CRSEL = 0xF7 # CrSel key
VK_EXSEL = 0xF8 # ExSel key
VK_EREOF = 0xF9 # Erase EOF key
VK_PLAY = 0xFA # Play key
VK_ZOOM = 0xFB # Zoom key
VK_PA1 = 0xFD # PA1 key
VK_OEM_CLEAR = 0xFE