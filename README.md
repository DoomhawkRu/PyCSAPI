# PyCSAPI

## How to install:
### Installing from PyPi repository:
1. Download and install Python 3.6.6 from the [official site](https://www.python.org) ([x86-installer](https://www.python.org/ftp/python/3.6.6/python-3.6.6.exe), [x64-installer](https://www.python.org/ftp/python/3.6.6/python-3.6.6-amd64.exe))
2. Type the following command in the Windows console:
```
pip3 install pycsapi
```

### Installing manually from the source code:
1. Download and install Python 3.6.6 from the [official site](https://www.python.org) ([x86-installer](https://www.python.org/ftp/python/3.6.6/python-3.6.6.exe), [x64-installer](https://www.python.org/ftp/python/3.6.6/python-3.6.6-amd64.exe))
2. Download and install Git from the [official site](https://git-scm.com/) ([x86/x64-installer](https://git-scm.com/download/win))
3. Type the following commands in the Git Bash console:
```
git clone https://github.com/DoomhawkRu/PyCSAPI.git
cd PyCSAPI
py setup.py install
```

## Examples:

### BunnyHop:
```python
from pycsapi import constant
from pycsapi import util
import pycsapi
import time

# Make sure that you run CS:GO before running this script, otherwise you will get an error
if __name__ == '__main__':
    api = pycsapi.PyCSAPI()
    player = api.get_player()
    while True:
        if player.is_in_game() and player.is_alive():
            if player.is_on_ground() and util.is_key_pressed(constant.VK_SPACE):
                player.set_jump(True)
        time.sleep(.01)
```

### GlowESP:
```python
import pycsapi
import time

# Make sure that you run CS:GO before running this script, otherwise you will get an error
if __name__ == '__main__':
    api = pycsapi.PyCSAPI()
    player = api.get_player()
    while True:
        if player.is_in_game() and player.is_alive():
            for entity in api.get_players():
                if entity.get_team_id() != player.get_team_id():
                    health = entity.get_health()
                    r = 255 - (health * 2.55)
                    g = health * 2.55
                    b = 0
                    entity.set_glow((r, g, b))
        time.sleep(.01)
```
![GlowESP](https://raw.githubusercontent.com/DoomhawkRu/PyCSAPI/master/image/glowesp.png)

More examples coming soon

## LICENSE:
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Credits:

- [frk1](https://github.com/frk1)
- [D4stiny](https://github.com/D4stiny)
- [Kenneth Reitz](https://github.com/requests)
- [cesharp](https://www.unknowncheats.me/forum/members/1715670.html)
- [zniv](https://www.unknowncheats.me/forum/members/991627.html)
- [wep](https://www.unknowncheats.me/forum/members/2009277.html)
- [ReactiioN](https://www.unknowncheats.me/forum/members/264622.html)
- [Killstreak](https://www.unknowncheats.me/forum/members/242212.html)

If you have any questions, please feel free to contact me via email: **admin@doomhawk.org**