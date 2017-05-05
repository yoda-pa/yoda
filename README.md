# dude
[![Build Status](https://travis-ci.org/dude-pa/dude.png)](https://travis-ci.org/dude-pa/dude)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/dude-pa/dude/master/LICENSE)
[![Project status](https://img.shields.io/badge/version-0.0.1-yellow.svg)](https://github.com/dude-pa/dude)

Dudely Command line interface to help with daily tasks

## Installation
#### Requirements
- [python](https://www.python.org/downloads/)
- [virtualenv](https://virtualenv.pypa.io/en/stable/installation/) (only for testing and development)  

### How to run
```bash
# clone this repo
$ git clone https://github.com/dude-pa/dude

# create a virtualenv
$ virtualenv venv  

# activate the virtualenv
$ . venv/bin/activate

# Install the package! In case you want to edit the source code
# use 'pip install --editable .' so that you don't need to install again and again
$ pip install

# run it!
$ dude
# to exit the virtualenv, just type 'deactivate' without quotes
```

## How to use this package
#### setup
This command helps to create a setup configuration for you to save some information locally. You can also save this in a github repository. Your password is saved in the config file after encrypting, so you need not worry about it.
```bash
# To create a configuration
$ dude setup new

# To delete a configuration
$ dude setup delete

# To check current configuration
$ dude setup check
```
#### chat
This package contains a simple chatbot as well! The `chat` command can be used to chat with it
```bash
$ dude chat hi!
Dude says: Howdy.

# Simply write messages with more than one word
$ dude chat how are you?
Dude says: Lovely, thanks.
```
You can test the chat functionality on api.ai agent website [here](https://bot.api.ai/ff4ba99e-e444-4e19-8b4e-91fb0b93e414)
#### dev
This command group contains some sub-commands that may be helpful for developers and tech-geeks.
- speedtest
```bash
# run a speed test for your internet connection
$ dude speedtest
Speed test results:
Ping: 3.04 ms
Download: 144.90 MB/s
Upload: 203.13 MB/s
```
- url
```bash
# URL shortener and expander
$ dude url shorten manparvesh.com
Here\'s your shortened URL:
https://goo.gl/EVVPzK
$ dude url expand https://goo.gl/EVVPzK
Here\'s your original URL:
http://manparvesh.com/
```
#### diary
This command can be used to maintain a personal diary, roughly based on the concept of [Bullet Journal](http://bulletjournal.com/).
```bash
# new note
$ dude diary nn
Input your entry for note:
hey there

# view notes
$ dude diary notes
Today\'s notes:
----------------
  Time  | Note
--------|-----
12:54:22| hey there
12:54:45| hi, this is the dude

# new task
$ dude diary nt
Input your entry for task:
go office

# view tasks
$ dude diary tasks
Today\'s agenda:
----------------
Status |  Time   | Text
-------|---------|-----
   O   | 15:50:48: go office
----------------

Summary:
----------------
Incomplete tasks: 1
Completed tasks: 0

# view tasks
$ dude diary ct
Today\'s agenda:                                                
----------------                                               
Number |  Time   | Task                                        
-------|---------|-----                                        
   1   | 15:50:48: go office                                   
Enter the task number that you would like to set as completed  
1                                                              
```
#### love
This command can be used to maintain a profile of someone.
```bash
# create configuration
$ dude love setup

# view config
$ dude love status

# write a note for them
$ dude love note

# view notes
$ dude love notes
```
#### money
This is for tracking money.
```bash
# create configuration
$ dude money setup

# view config
$ dude money status

# add an expense using natural language
$ dude money exp
spent 30 dollars on shoes

# view expenses
$ dude money exps
2017-05-04 16:06:00 SGD 30 shoes
```
#### vocabulary
For enhancing your vocabulary and tracking your progress.
```bash
# get a random word
$  dude vocabulary word
sinecure:
<Enter> to show meaning
a job that pays a salary but requires little work
Did you know / remember the meaning?
no

# view your progress
$  dude vocabulary accuracy
Words asked in the past:
sinecure-- times used: 8 accuracy: 50.0
squalid-- times used: 6 accuracy: 66.0
```
## Packages used
- [Click](http://click.pocoo.org/5/): for building command line application
- [pychalk](https://github.com/anthonyalmarza/chalk): Colors in terminal
- [apiai](https://github.com/api-ai/apiai-python-client): api-ai for natural language understanding
- [pyyaml](https://pypi.python.org/pypi/PyYAML): for parsing yaml files
- [emoji](https://pypi.python.org/pypi/emoji/): emojis!
- [lepl](https://pypi.python.org/pypi/LEPL/): for formatted parsing
- [pycrypto](https://pypi.python.org/pypi/pycrypto): To encrypt / decrypt your password
- [pyspeedtest](https://pypi.python.org/pypi/pyspeedtest): To test network bandwidth
- [forex-python](https://pypi.python.org/pypi/forex-python): Foreign exchange rates and currency conversion
- [dulwich](https://github.com/jelmer/dulwich): for git
- [PyGithub](https://github.com/PyGithub/PyGithub): for using Github API v3

## Contributing
#### Feature suggestions / bug reports
You can contribute to this project by suggesting features or filing bugs by creating an issue [here](https://github.com/dude-pa/dude/issues/new).
#### Writing code
If you are interested in contributing by writing code, you can do so by implementing the features listed in [the TODO file](TODO.md).  
