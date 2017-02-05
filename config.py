import os.path
import platform

API_AI_TOKEN = 'caca38e8d99d4ea6bd9ffa9a8be15ff9'
API_AI_SESSION_ID = 'dd60fde7-c6ab-4f38-9487-7300c42b4916'

# platform specific constants
PLATFORM = platform.system().lower()
if PLATFORM == 'linux':
    CONFIG_FILE_PATH = os.path.expanduser('~') + '/.dude/.dudeconfig.yml'
    MONEY_CONFIG_FILE_PATH = os.path.expanduser('~') + '/.dude/money/.moneyconfig.yml'
