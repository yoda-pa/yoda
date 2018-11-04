from __future__ import absolute_import
from builtins import str
from builtins import input
import datetime
from .config import get_config_file_paths
from .util import *
import dbus
import xml.etree.ElementTree as ET

# config file path
PEOPLE_CONFIG_FILE_PATH = get_config_file_paths()["PEOPLE_CONFIG_FILE_PATH"]
PEOPLE_CONFIG_FOLDER_PATH = get_folder_path_from_file_path(PEOPLE_CONFIG_FILE_PATH)


def get_friends_file_path(friend_name):
    """
    get file path for friend's entry file
    :return:
    """
    return PEOPLE_CONFIG_FOLDER_PATH + "/" + friend_name + ".yaml"


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
        contents["entries"].append(data)
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
            entries = contents["entries"]
            click.echo("People:")
            click.echo("--------------------------------------")
            click.echo("     Mob    |     DOB    |   Name     ")
            click.echo("------------|------------|------------")
            for i, entry in enumerate(entries):
                s_no = str(i)
                name = entry["name"]
                dob = entry["dob"]
                mob = entry["mobile"]
                click.echo(" " + mob + " | " + dob + " | " + name)
    else:
        click.echo(
            chalk.red(
                'The configuration file for this module does not exist. Please type "yoda people setup" to create a new one'
            )
        )


def setup():
    """
    create new setup
    :return:
    """
    create_folder(PEOPLE_CONFIG_FOLDER_PATH)

    click.echo(chalk.blue("Enter their name:"))
    name = input().strip().lower()

    if friend_name_exists(name):
        click.echo(
            chalk.red(
                'A configuration with this friend name already exists.Please type "yoda people --help"'
            )
        )

    click.echo(chalk.blue("Input their DOB (YYYY-MM-DD):"))
    incorrect_date_format = True
    while incorrect_date_format:
        dob = input().strip()
        try:
            date_str = datetime.datetime.strptime(dob, "%Y-%m-%d").strftime("%Y-%m-%d")
            if date_str != dob:
                raise ValueError
            incorrect_date_format = False
        except ValueError:
            click.echo(
                chalk.red("Incorrect data format, should be YYYY-MM-DD. Please repeat:")
            )

    click.echo(chalk.blue("Enter their Mobile Number:"))
    mobile = input().strip()

    if os.path.isfile(PEOPLE_CONFIG_FILE_PATH):
        setup_data = dict(name=name, mobile=mobile, dob=dob)
        append_data_into_file(setup_data, PEOPLE_CONFIG_FILE_PATH)
    else:
        setup_data = dict(entries=[dict(name=name, mobile=mobile, dob=dob)])
        input_data(setup_data, PEOPLE_CONFIG_FILE_PATH)

    input_data(dict(entries=[]), get_friends_file_path(name))


def like():
    """
    Adds likes
    """
    click.echo(chalk.blue("For whom you want to add like for"))
    friend_name = input().strip().lower()

    FRIENDS_FILE_PATH = get_friends_file_path(friend_name)

    if os.path.isfile(FRIENDS_FILE_PATH):
        hashtags = []
        with open(FRIENDS_FILE_PATH) as fin:
            contents = yaml.load(fin)
            entries = contents["entries"]
        if "likes" in entries:
            notes = entries["likes"]
            del entries["likes"]
        continue_adding_hashtags = True
        while continue_adding_hashtags:
            click.echo(chalk.blue("Enter what they like or -"))
            hashtag = input().strip()
            if hashtag == "-":
                continue_adding_hashtags = False
            else:
                hashtags.append("#" + hashtag)

        setup_data = dict(likes=hashtags)
        append_data_into_file(setup_data, FRIENDS_FILE_PATH)
    else:
        click.echo(
            chalk.red(
                "Friend's config file doesn't exist. Type 'yoda people setup' to setup a friend"
            )
        )


def note():
    """
    Adds notes
    """
    click.echo(chalk.blue("For whom you want to add a note for"))
    friend_name = input().strip().lower()

    FRIENDS_FILE_PATH = get_friends_file_path(friend_name)

    if os.path.isfile(FRIENDS_FILE_PATH):
        notes = []
        with open(FRIENDS_FILE_PATH) as fin:
            contents = yaml.load(fin)
            entries = contents["entries"]
        if "notes" in entries:
            notes = entries["notes"]
            del entries["notes"]
        continue_adding_notes = True
        while continue_adding_notes:
            click.echo(chalk.blue("Enter note or press -"))
            note = input().strip()
            if note == "-":
                continue_adding_notes = False
            else:
                notes.append(note)

        setup_data = dict(notes=notes)
        append_data_into_file(setup_data, FRIENDS_FILE_PATH)
    else:
        click.echo(
            chalk.red(
                "Friend's config file doesn't exist. Type 'yoda people setup' to setup a friend"
            )
        )


def likes():
    """
    view the things they like
    """
    click.echo(chalk.blue("For whom you want to view likes for"))
    friend_name = input().strip().lower()
    FRIENDS_FILE_PATH = get_friends_file_path(friend_name)

    if os.path.isfile(FRIENDS_FILE_PATH):
        with open(FRIENDS_FILE_PATH) as fin:
            contents = yaml.load(fin)
            entries = contents["entries"]
            likes = []
            for entry in entries:
                if "likes" in entry:
                    likes.extend(entry["likes"])
            click.echo("Likes:")
            for i, n in enumerate(likes):
                click.echo(str(i) + ": " + n)
    else:
        click.echo(
            chalk.red(
                'The Likes file path for this module does not exist. Please type "yoda people like" to create a new one'
            )
        )


def notes():
    """
    view notes
    """
    click.echo(chalk.blue("For whom you want to view notes for"))
    friend_name = input().strip().lower()
    FRIENDS_FILE_PATH = get_friends_file_path(friend_name)

    if os.path.isfile(FRIENDS_FILE_PATH):
        with open(FRIENDS_FILE_PATH) as fin:
            contents = yaml.load(fin)
            entries = contents["entries"]
            notes = []
            for entry in entries:
                if "notes" in entry:
                    notes.extend(entry["notes"])
            click.echo("Notes:")
            for i, n in enumerate(notes):
                click.echo(str(i) + ": " + n)
    else:
        click.echo(
            chalk.red(
                'The Notes file path for this module does not exist. Please type "yoda people note" to create a new one'
            )
        )

def sms():
    """
    send an sms to a friend using kdeconnect
    """
    def send_sms(number, message):
            #get session bus
            try:
                session_bus = dbus.SessionBus()
            except dbus.exceptions.DBusException:
                click.echo(chalk.red('Have a display you must'))
                return

            #check for kdeconnect
            try:
                devices_dbus_obj = session_bus.get_object('org.kde.kdeconnect','/modules/kdeconnect/devices')
            except dbus.exceptions.DBusException:
                click.echo(chalk.red('kdeconnect not installed it appears'))
                return

            #get devices ids
            devices_xml = devices_dbus_obj.Introspect(dbus_interface='org.freedesktop.DBus.Introspectable')
            devices_xml = ET.fromstring(devices_xml)
            nodes = devices_xml.findall('node')
            if(len(nodes) is 0):
                click.echo(chalk.red('Devices there are not'))
                return
            deviceIDs = list()
            for node in nodes:
                deviceIDs.append(node.get('name'))

            #get devices properties
            deviceID_Props = dict()
            for ID in deviceIDs:
                try:
                    device = session_bus.get_object('org.kde.kdeconnect', '/modules/kdeconnect/devices/' + ID)
                    deviceProps = device.GetAll('', dbus_interface='org.freedesktop.DBus.Properties')
                    deviceID_Props[ID] = deviceProps
                except dbus.exceptions.DBusException:
                    #don't create an entry in the dictionary if the object, or a GetAll method does not exist
                    pass
            if(len(deviceID_Props) is 0):
                click.echo(chalk.red('Devices there are not'))
                return

            #eliminate non sms devices
            devices_no_sms = list()
            for device in deviceID_Props:
                keeping = False
                for plugin in deviceID_Props[device]['supportedPlugins']:
                    if('sms' in plugin):
                        keeping = True
                if(not keeping):
                    devices_no_sms.append(device)
            for device in devices_no_sms:
                del deviceID_Props[device]

            #if there are no devices that support sms
            if(len(deviceID_Props) is 0):
                click.echo(chalk.red('Devices that support sms there are not'))
                return
            #elif only one device was found that supports sms
            elif(len(deviceID_Props) is 1):
                click.echo(chalk.yellow('Device using: ' + str(list(deviceID_Props.values())[0]['name'])))
                sendMessage = session_bus.get_object('org.kde.kdeconnect', '/modules/kdeconnect/devices/' + str(list(deviceID_Props.keys())[0]) + '/sms')
                sendMessage.sendSms(number, message, dbus_interface='org.kde.kdeconnect.device.sms')
                return
            #otherwise get user to choose device
            else:
                choice_map = dict()
                for idx, device in enumerate(deviceID_Props, start=1):
                    click.echo(chalk.green(str(idx) + ': ' + deviceID_Props[device]['name']))
                    choice_map[str(idx)] = device
                choice = click.prompt(chalk.blue('Device, you must select: '), default='1', type=click.Choice(choice_map.keys()))
                #click.echo('you chose: ' + choice_map[the_chosen_device] + ' with id: ' + deviceNames_IDs[choice_map[the_chosen_device]])
                sendMessage = session_bus.get_object('org.kde.kdeconnect', '/modules/kdeconnect/devices/' + choice_map[choice] + '/sms')
                sendMessage.sendSms(number, message, dbus_interface='org.kde.kdeconnect.device.sms')
                return

    click.echo(chalk.blue('For whom you want to send an sms'))
    friend_name = input().strip()
    friend_name_lower = friend_name.lower()
    if os.path.isfile(PEOPLE_CONFIG_FILE_PATH):
        with open(PEOPLE_CONFIG_FILE_PATH) as fin:
            contents = yaml.load(fin)
            entries = contents['entries']
            for entry in entries:
                if(friend_name == entry['name'] or friend_name_lower == entry['name']):
                    number = entry['mobile']
                    break
            if('number' not in locals()):
                click.echo(chalk.red('Friend not found.'))
            else:
                if(len(number) is not 0):
                    click.echo(chalk.blue('Message, you must enter: '))
                    message = input(':')
                    click.echo(chalk.yellow('Device to send sms to ' + number + ' looking for: '))
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
        'sms' : sms
        # 'addbirth': addbirth,
        # 'showbirth': showbirth
    }
    try:
        return sub_commands[c]()
    except KeyError:
        click.echo(chalk.red("Command does not exist!"))
        click.echo('Try "yoda love --help" for more info')


def process(input):
    """
    the main process
    :param input:
    """
    _input = input.lower().strip()
    check_sub_command(_input)
