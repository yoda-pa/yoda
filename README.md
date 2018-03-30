<div align="center" style="margin: 20px">
  <img src="https://github.com/yoda-pa/yoda/raw/master/logo.png">
</div>

<div align="center">

  <h1>yoda</h1>
  <p>Wise and powerful personal assistant, inside your terminal</p><br>
  <a href="https://travis-ci.org/yoda-pa/yoda"><img src="https://travis-ci.org/yoda-pa/yoda.png" alt="Build status"></a> 
  <a href="https://sonarcloud.io/dashboard?id=yoda"><img src="https://sonarcloud.io/api/project_badges/measure?project=yoda&metric=alert_status" alt="SonarCloud Quality Status"></a> 
  <a href="https://manparvesh.mit-license.org/"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"></a> 
  <a href="https://github.com/yoda-pa/yoda"><img src="https://img.shields.io/badge/version-0.2.0-yellow.svg" alt="Project status"></a>
  
</div>


## Install, how to


#### Requirements

- [python (both 2 and 3 are supported)](https://www.python.org/downloads/)
- [virtualenv](https://virtualenv.pypa.io/en/stable/installation/) (only for testing and development)
- Python development package:
  - `python-dev` package (if using Ubuntu)
  - `Visual C++ 9.0 for Python` (If using Windows)
  - `python-devel` package (If using MacOS/OSX: [link](https://stackoverflow.com/questions/32578106/how-to-install-python-devel-in-mac-os/32578175#32578175))

### Download and Install, how to

```
$ git clone https://github.com/yoda-pa/yoda
$ cd yoda
$ sudo python3 -m pip install -r requirements.txt
$ sudo python3 setup.py build
$ sudo python3 setup.py install
```

### Run, how to

Clone this repository and create a virtual environment using Python 2 in the cloned directory (`virtualenv -p /usr/bin/python2 venv`). Steps after that:

![](screencasts/firstsetup.gif)

Instead of `pip install --editable .` you can use `pip install .` if you don't intend to make any changes in the code.


## Use this package, how to

#### chat

This package contains a chatbot too! The `chat` command can be used to chat with it

![](screencasts/chat.gif)

You can test the chat functionality on api.ai agent website [here](https://bot.api.ai/ff4ba99e-e444-4e19-8b4e-91fb0b93e414)

#### dev

This command group contains some sub-commands that may be helpful for developers and tech-geeks.

- speedtest

![](screencasts/speedtest.gif)

- url

![](screencasts/url.gif)

- hackernews

![](screencasts/hackernews.gif)

#### diary

This command can be used to maintain a personal diary, roughly based on the concept of [Bullet Journal](http://bulletjournal.com/).

![](screencasts/diary.gif)

#### love

This command can be used to maintain a profile of someone you love.

![](screencasts/love.gif)

#### money

For tracking money, this is.

![](screencasts/money.gif)

#### Idea list

For creating list of ideas, type

```
# To add idea
$ yoda ideas add --task <task_name> --inside <project_name>

# To show list of ideas
$ yoda ideas show

# To remove a task from idea
$ yoda ideas remove --task <task_name> --inside <project_name>

# To remove an idea completely
$ yoda ideas remove --project <project_name>
```

#### learn

This command group contains commands that, helpful in learning new things, will be.  Yeesssssss.

- vocabulary: For enhancing your vocabulary and tracking your progress.

    ![](screencasts/vocab.gif)


- flashcards: for learning anything! ([inspiration](https://github.com/zergov/flashcards))

    ```
    # create new set (remember to keep the name to one word)
    $  yoda flashcards sets new english

    # modify set
    $  yoda flashcards sets modify english

    # list all sets
    $  yoda flashcards sets list

    # select a study set
    $  yoda flashcards select english

    # create new card in selected set (card name length can be more than 1 word)
    $  yoda flashcards cards new Oxford comma

    # Know which set is selected and its information
    $  yoda flashcards status

    # study the selected study set. This will show you all the cards in a study set
    # one by one.
    $  yoda flashcards study
    ```

- define: to get different meanings of a word. This definition search will be automatically saved, so that while you are working on your vocabulary, you can come through the new word as well.

    ![](screencasts/define.gif)

#### feedback

To create an issue in the github repository simple thing that shows a link.  Yeesssssss.

![](screencasts/feedback.gif)

## Packages and services used

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
- [Gravit](https://gravit.io/): for creating the logo
- Yoda's illustration SVG was taken from [here](https://www.shareicon.net/yoda-854796)

## Contribute, you must
Please refer to the [contributing guidelines](https://github.com/yoda-pa/yoda/blob/master/.github/CONTRIBUTING.md) for contributing to this project.
