import click
import chalk
import pyspeedtest

@click.group()
def dev():
    """
        Dev command group:\n
        contains commands helpful for developers
    """

@dev.command()
#@click.argument('input', nargs=-1)
def speedtest():
    """
    run a speed test for your internet connection
    """
    speed_test = pyspeedtest.SpeedTest()

    click.echo('Speed test results:')

    ping = speed_test.ping()
    click.echo('Ping: ' + '{:.2f}'.format(ping) + ' ms')

    download_speed = speed_test.download() / (1024 * 1024)
    click.echo('Download: ' + '{:.2f}'.format(download_speed) + ' MB/s')

    upload_speed = speed_test.upload() / (1024 * 1024)
    click.echo('Upload: ' + '{:.2f}'.format(upload_speed) + ' MB/s')
