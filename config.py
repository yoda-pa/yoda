import os.path

API_AI_TOKEN = 'caca38e8d99d4ea6bd9ffa9a8be15ff9'
API_AI_SESSION_ID = 'dd60fde7-c6ab-4f38-9487-7300c42b4916'

# gets home dir, works for all platforms
USER_HOME_DIR = os.path.expanduser('~')

config_file_paths = {
    "CONFIG_FILE_PATH": USER_HOME_DIR + '/.yoda/.yodaconfig.yml',
    "LOVE_CONFIG_FILE_PATH": USER_HOME_DIR + '/.yoda/love/.loveconfig.yml',
    "MONEY_CONFIG_FILE_PATH": os.path.expanduser('~') + '/.yoda/money/.moneyconfig.yml',
    "DIARY_CONFIG_FILE_PATH": os.path.expanduser('~') + '/.yoda/diary/.diaryconfig.yml',
    "VOCABULARY_CONFIG_FILE_PATH": os.path.expanduser('~') + '/.yoda/vocabulary/.vocabularyconfig.yml',
    "FLASHCARDS_CONFIG_FILE_PATH": os.path.expanduser('~') + '/.yoda/flashcards/.flashcardsconfig.yml'
}
