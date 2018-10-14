from __future__ import absolute_import
from builtins import str
from builtins import input
import datetime
from .config import get_config_file_paths
from .util import *
import subprocess as sp

# config file path
PEOPLE_CONFIG_FILE_PATH = get_config_file_paths()["PEOPLE_CONFIG_FILE_PATH"]
PEOPLE_CONFIG_FOLDER_PATH = get_folder_path_from_file_path(PEOPLE_CONFIG_FILE_PATH)

def get_friends_file_path(friend_name):
    """
    get file path for friend's entry file
    :return:
    """
    return PEOPLE_CONFIG_FOLDER_PATH + '/' + friend_name + ".yaml"


def friend_name_exists(friend_name):
    file_name = get_friends_file_path(friend_name)
    return os.path.isfile(file_name)


def append_data_into_file(data, file_path):
    """
    append data into existing file
    :param data:
    :param file_path:
    """
    with open(file_path) as todays_tasks_entry:
        # read contents
        contents = yaml.load(todays_tasks_entry)
        contents['entries'].append(
            data
        )
        # enter data
        with open(file_path, "w") as todays_tasks_entry:
            yaml.dump(contents, todays_tasks_entry, default_flow_style=False)


def status():
    """
    check status
    """
    if os.path.isfile(PEOPLE_CONFIG_FILE_PATH):
        with open(PEOPLE_CONFIG_FILE_PATH) as config_file:
            contents = yaml.load(config_file)
            entries = contents['entries']
            click.echo('People:')
            click.echo("--------------------------------------")
            click.echo("     Mob    |     DOB    |   Name     ")
            click.echo("------------|------------|------------")
            for i, entry in enumerate(entries):
                s_no = str(i)
                name = entry['name']
                dob = entry['dob']
                mob = entry['mobile']
                click.echo(' ' + mob + ' | ' + dob +' | ' + name)
    else:
        click.echo(chalk.red(
            'The configuration file for this module does not exist. Please type "yoda people setup" to create a new one'))


def setup():
    """
    create new setup
    :return:
    """
    create_folder(PEOPLE_CONFIG_FOLDER_PATH)

    click.echo(chalk.blue('Enter their name:'))
    name = (input().strip().lower())

    if friend_name_exists(name):
        click.echo(chalk.red(
            'A configuration with this friend name already exists.Please type "yoda people --help"'))

    click.echo(chalk.blue('Input their DOB (YYYY-MM-DD):'))
    incorrect_date_format = True
    while incorrect_date_format:
        dob = input().strip()
        try:
            date_str = datetime.datetime.strptime(dob, '%Y-%m-%d').strftime('%Y-%m-%d')
            if date_str != dob:
                raise ValueError
            incorrect_date_format = False
        except ValueError:
            click.echo(chalk.red("Incorrect data format, should be YYYY-MM-DD. Please repeat:"))

    click.echo(chalk.blue('Enter their Mobile Number:'))
    mobile = (input().strip())

    if os.path.isfile(PEOPLE_CONFIG_FILE_PATH):
        setup_data = dict(
            name=name,
            mobile=mobile,
            dob=dob
        )
        append_data_into_file(setup_data, PEOPLE_CONFIG_FILE_PATH)
    else:
        setup_data = dict(
            entries=[
                dict(
                    name=name,
                    mobile=mobile,
                    dob=dob
                    )
                ]
            )
        input_data(setup_data, PEOPLE_CONFIG_FILE_PATH)

    input_data(dict(entries=[]), get_friends_file_path(name))


def like():
    '''
    Adds likes
    '''
    click.echo(chalk.blue('For whom you want to add like for'))
    friend_name = input().strip().lower()

    FRIENDS_FILE_PATH = get_friends_file_path(friend_name)
    
    if os.path.isfile(FRIENDS_FILE_PATH):
        hashtags = []
        with open(FRIENDS_FILE_PATH) as fin:
            contents = yaml.load(fin)
            entries = contents['entries']
        if 'likes' in entries:
            notes = entries['likes']
            del entries['likes']
        continue_adding_hashtags = True
        while continue_adding_hashtags:
            click.echo(chalk.blue(
                'Enter what they like or -'))
            hashtag = input().strip()
            if hashtag == '-':
                continue_adding_hashtags = False
            else:
                hashtags.append('#'+hashtag)

        setup_data = dict(
            likes=hashtags
        )
        append_data_into_file(setup_data,FRIENDS_FILE_PATH)
    else:
        click.echo(chalk.red(
            "Friend's config file doesn't exist. Type 'yoda people setup' to setup a friend"))

def note():
    '''
    Adds notes
    '''
    click.echo(chalk.blue('For whom you want to add a note for'))
    friend_name = input().strip().lower()

    FRIENDS_FILE_PATH = get_friends_file_path(friend_name)
    
    if os.path.isfile(FRIENDS_FILE_PATH):
        notes = []
        with open(FRIENDS_FILE_PATH) as fin:
            contents = yaml.load(fin)
            entries = contents['entries']
        if 'notes' in entries:
            notes = entries['notes']
            del entries['notes']
        continue_adding_notes = True
        while continue_adding_notes:
            click.echo(chalk.blue(
                'Enter note or press -'))
            note = input().strip()
            if note == '-':
                continue_adding_notes = False
            else:
                notes.append(note)

        setup_data = dict(
            notes=notes
        )
        append_data_into_file(setup_data,FRIENDS_FILE_PATH)
    else:
        click.echo(chalk.red(
            "Friend's config file doesn't exist. Type 'yoda people setup' to setup a friend"))

def likes():
    """
    view the things they like
    """
    click.echo(chalk.blue('For whom you want to view likes for'))
    friend_name = input().strip().lower()
    FRIENDS_FILE_PATH = get_friends_file_path(friend_name)

    if os.path.isfile(FRIENDS_FILE_PATH):
        with open(FRIENDS_FILE_PATH) as fin:
            contents = yaml.load(fin)
            entries = contents['entries']
            likes = []
            for entry in entries:
                if 'likes' in entry:
                    likes.extend(entry['likes'])
            i = 0
            click.echo('Likes:')
            for n in likes:
                i += 1
                click.echo(str(i) + ": " + n)
    else:
        click.echo(chalk.red(
            'The Likes file path for this module does not exist. Please type "yoda people like" to create a new one'))


def notes():
    """
    view notes
    """
    click.echo(chalk.blue('For whom you want to view notes for'))
    friend_name = input().strip().lower()
    FRIENDS_FILE_PATH = get_friends_file_path(friend_name)
    
    if os.path.isfile(FRIENDS_FILE_PATH):
        with open(FRIENDS_FILE_PATH) as fin:
            contents = yaml.load(fin)
            entries = contents['entries']
            notes = []
            for entry in entries:
                if 'notes' in entry:
                    notes.extend(entry['notes'])
            #TODO: use enumerate function for this stuff
            i = 0
            click.echo('Notes:')
            for n in notes:
                i += 1
                click.echo(str(i) + ": " + n)
    else:
        click.echo(chalk.red(
            'The Notes file path for this module does not exist. Please type "yoda people note" to create a new one'))

def sms():
    """
    send an sms to a friend using kdeconnect
    """
    def send_sms(number, message):
            devices = sp.run(['kdeconnect-cli','-l','--id-name-only'],stdout=sp.PIPE)
            return_code = devices.returncode
            if(return_code is not 0):
                click.echo(chalk.red('Not found kdeconnect-cli, return code: ' + str(return_code)))
                return
            devices = str(devices.stdout).splitlines()
            device_id_name_pairs = dict()
            for device in devices:
                if('0 devices' in device):
                    click.echo(chalk.red('Devices found not.'))
                    return
            for device in devices:
                device = device.strip('b\'\\n').split(' ', 1)
                device_id_name_pairs[device[1]] = device[0]
            if(len(devices) is 1):
                the_chosen_device = devices[0].strip('b\'\\n').split(' ', 1)[1]
                click.echo(chalk.yellow('Device using: ' + the_chosen_device))
                os.system('kdeconnect-cli -d ' + device_id_name_pairs[the_chosen_device] + ' --send-sms "' + message +'" --destination ' + number)
            else:
                choice_map = dict()
                for idx, device in enumerate(device_id_name_pairs, start=1):
                    click.echo(chalk.green(str(idx) + ': ' + device))
                    choice_map[str(idx)] = device
                the_chosen_device = click.prompt(chalk.blue('Device, you must select: '), default='1', type=click.Choice(choice_map.keys()))
                #click.echo('you chose: ' + choice_map[the_chosen_device] + ' with id: ' + device_id_name_pairs[choice_map[the_chosen_device]])
                os.system('kdeconnect-cli -d ' + device_id_name_pairs[choice_map[the_chosen_device]] + ' --send-sms "' + message +'" --destination ' + number)
            return

    click.echo(chalk.blue('For whom you want to send an sms'))
    friend_name = input().strip().lower()
    if os.path.isfile(PEOPLE_CONFIG_FILE_PATH):
        with open(PEOPLE_CONFIG_FILE_PATH) as fin:
            contents = yaml.load(fin)
            entries = contents['entries']
            for entry in entries:
                if(friend_name == entry['name']):
                    number = entry['mobile']
                    break
            if('number' not in locals()):
                click.echo(chalk.red('Friend not found.'))
            else:
                if(len(number) is not 0):
                    click.echo(chalk.blue('Message, you must enter: '))
                    message = input(':')
                    click.echo(chalk.yellow('Device to send sms to looking for: ' + number))
                    send_sms(number, message)
                else:
                    click.echo(chalk.red('Friends number not in people file, run `yoda people setup` to add it.'))
    else:
        click.echo(chalk.red('The People file does not exist, run `yoda people setup` to create an entry.'))


def check_sub_command(c):
    """
    command checker
    :param c:
    :return:
    """
    sub_commands = {
        'setup': setup,
        'status': status,
        'note': note,
        'notes': notes,
        'likes': likes,
        'like': like,
        'sms': sms
        # 'addbirth': addbirth,
        # 'showbirth': showbirth
    }
    try:
        return sub_commands[c]()
    except KeyError:
        click.echo(chalk.red('Command does not exist!'))
        click.echo('Try "yoda love --help" for more info')


def process(input):
    """
    the main process
    :param input:
    """
    _input = input.lower().strip()
    check_sub_command(_input)
