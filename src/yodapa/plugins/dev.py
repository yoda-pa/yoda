import os
import string
from typing import List

import typer
from rich import print

app = typer.Typer()


@app.command()
def speedtest():
    """Test your internet connection"""
    os.system("speedtest-cli")


@app.command()
def coinflip():
    """Flip a coin!"""
    import random
    value = random.randint(0, 1)
    if value == 1:
        print("[green]Heads! :speaking_head:[/]")
    else:
        print("[magenta]Tails![/]")


@app.command()
def checksite(url: str):
    """Check if a site is up and running"""
    import urllib.request
    try:
        code = urllib.request.urlopen(url).getcode()
        if code != 200:
            print(f"[bold red] Site is DOWN![/] HTTP code received: {code}")
        else:
            print("[bold green] Site is UP![/]")
    except Exception as e:
        print(e)
        print("[bold red] Site is DOWN![/]")


@app.command()
def whois(domain: str):
    """Check whois info for a domain name"""
    import whois
    whois_data = whois.whois(domain)
    print(whois_data.text)


@app.command()
def generatepassword():
    """Generates a secure password"""
    import random
    length = random.randint(16, 25)
    characters = string.ascii_letters + string.digits + string.punctuation
    result: List[str] = list()
    for _ in range(length):
        result.append(random.choice(characters))
    print(''.join(result))
