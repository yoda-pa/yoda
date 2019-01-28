import os.path

API_AI_TOKEN = "caca38e8d99d4ea6bd9ffa9a8be15ff9"
API_AI_SESSION_ID = "dd60fde7-c6ab-4f38-9487-7300c42b4916"
# this is where yoda's config will be stored
YODA_CONFIG_FILE_PATH = os.path.join(os.path.expanduser("~"), ".yodaconfig")

DEFAULT_CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".yoda")


def update_config_path(new_path):
    """
    Updates the path where the config files are stored.
    This is done by changing the contents of YODA_CONFIG_FILE_PATH with new_path
    of user's config.
    """
    if len(new_path) == 0:
        new_path = DEFAULT_CONFIG_PATH
    with open(YODA_CONFIG_FILE_PATH, "w") as config_file:
        config_file.write(new_path)
    return new_path


def get_config_file_paths():
    """
    Get the absolute config file paths of user
    config_path_prefix is where the config files are stored.
    """
    try:
        with open(YODA_CONFIG_FILE_PATH) as config_file:
            config_path_prefix = config_file.read().strip()
    except IOError:
        config_path_prefix = DEFAULT_CONFIG_PATH

    return {
        "USER_CONFIG_FILE_PATH": os.path.join(config_path_prefix, ".userconfig.yml"),
        "LOVE_CONFIG_FILE_PATH": os.path.join(
            config_path_prefix, "love/.loveconfig.yml"
        ),
        "MONEY_CONFIG_FILE_PATH": os.path.join(
            config_path_prefix, "money/.moneyconfig.yml"
        ),
        "DIARY_CONFIG_FILE_PATH": os.path.join(
            config_path_prefix, "diary/.diaryconfig.yml"
        ),
        "VOCABULARY_CONFIG_FILE_PATH": os.path.join(
            config_path_prefix, "vocabulary/.vocabularyconfig.yml"
        ),
        "FLASHCARDS_CONFIG_FILE_PATH": os.path.join(
            config_path_prefix, "flashcards/.flashcardsconfig.yml"
        ),
        "LIFE_CONFIG_FILE_PATH": os.path.join(
            config_path_prefix, "life/.lifeconfig.yml"
        ),
        "IDEA_CONFIG_FILE_PATH": os.path.join(
            config_path_prefix, "life/ideaconfig.txt"
        ),
        "LEASELIST_CONFIG_FILE_PATH": os.path.join(
            config_path_prefix, "life/.leaseconfig.yml"
        ),
        "ALIAS_CONFIG_FILE_PATH": os.path.join(config_path_prefix, "alias/aliases.txt"),
        "GOALS_CONFIG_FILE_PATH": os.path.join(
            config_path_prefix, "goals/.goalsconfig.yml"
        ),
        "PEOPLE_CONFIG_FILE_PATH": os.path.join(
            config_path_prefix, "people/.peopleconfig.yml"
        ),
        "KEYBINDINGS_CONFIG_FILE_PATH": os.path.join(
            config_path_prefix, "software/.softwarekeybindingsconfig.yml"
        ),
    }
