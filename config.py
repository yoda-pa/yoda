import os.path

API_AI_TOKEN = 'caca38e8d99d4ea6bd9ffa9a8be15ff9'
API_AI_SESSION_ID = 'dd60fde7-c6ab-4f38-9487-7300c42b4916'

# gets home dir, works for all platforms
USER_HOME_DIR = raw_input("Enter the path to store config folder (eg../home/user_name): ")
while(not os.path.exists(USER_HOME_DIR)):
   print "Sorry! No such directory exist."
   USER_HOME_DIR = raw_input("Enter the path to store config folder (eg../home/user_name): ")

config_file_paths = {
    "CONFIG_FILE_PATH": USER_HOME_DIR + '/.dude/.dudeconfig.yml',
    "LOVE_CONFIG_FILE_PATH": USER_HOME_DIR + '/.dude/love/.loveconfig.yml',
    "MONEY_CONFIG_FILE_PATH": USER_HOME_DIR + '/.dude/money/.moneyconfig.yml',
    "DIARY_CONFIG_FILE_PATH": USER_HOME_DIR + '/.dude/diary/.diaryconfig.yml',
    "VOCABULARY_CONFIG_FILE_PATH": USER_HOME_DIR + '/.dude/vocabulary/.vocabularyconfig.yml',
    "FLASHCARDS_CONFIG_FILE_PATH": USER_HOME_DIR + '/.dude/flashcards/.flashcardsconfig.yml'
}
