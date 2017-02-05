import click
import chalk
import pyspeedtest

def speedtest():
    speed_test = pyspeedtest.SpeedTest()

    click.echo('Speed test results:')

    ping = speed_test.ping()
    click.echo('Ping: ' + '{:.2f}'.format(ping) + ' ms')

    download_speed = speed_test.download() / (1024 * 1024)
    click.echo('Download: ' + '{:.2f}'.format(download_speed) + ' MB/s')

    upload_speed = speed_test.upload() / (1024 * 1024)
    click.echo('Upload: ' + '{:.2f}'.format(upload_speed) + ' MB/s')

def check_sub_command(c):
    sub_commands = {
        'speedtest' : speedtest
    }
    return sub_commands[c]()

def process(input):
    input = input.lower().strip()
    check_sub_command(input)
