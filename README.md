<div align="center" style="margin: 20px">
  <img src="https://github.com/yoda-pa/yoda/raw/master/logo.png">
</div>

<div align="center">

  <h1>yoda</h1>

<a href="https://app.travis-ci.com/yoda-pa/yoda"><img src="https://app.travis-ci.com/yoda-pa/yoda.svg?branch=master" alt="Build status"></a>
  <a href="https://sonarcloud.io/dashboard?id=yoda"><img src="https://sonarcloud.io/api/project_badges/measure?project=yoda&metric=alert_status&template=FLAT" alt="SonarCloud Quality Status"></a>
  <a href="https://manparvesh.mit-license.org/"><img src="https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square" alt="License"></a>
  <a href="https://github.com/yoda-pa/yoda"><img src="https://img.shields.io/badge/version-1.0.0-blue.svg?style=flat-square" alt="Project status"></a>
  <a href="https://github.com/ambv/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style: black"></a>

  <p>Wise and powerful personal assistant, available in your nearest terminal</p><br>

</div>


## Install, how to

#### Requirements

- [python (both 2 and 3 are supported)](https://www.python.org/downloads/)
- [virtualenv](https://virtualenv.pypa.io/en/stable/installation/) (only for testing and development)
- Python development package:
  - Ubuntu: `sudo apt-get install -y libxml2-dev libxslt-dev python-dev libav-tools`
  - `Visual C++ 9.0 for Python` (If using Windows)
  - `python-devel` package (If using MacOS/OSX: [link](https://stackoverflow.com/questions/32578106/how-to-install-python-devel-in-mac-os/32578175#32578175))

### Run, how to

#### 1. Docker

1. [Install docker](https://docs.docker.com/install/)
2. Run `docker run --rm -it yodapa/yoda:latest yoda chat Hi`

#### 2. Using pip, without cloning

You can install yoda directly from the github repository using the following commands in shell.
`virtualenv yodaenv`
`./yodaenv/bin/pip install git+https://github.com/yoda-pa/yoda`

#### 3. Using pip, with cloning
Clone this repository and create a virtual environment using Python 2 in the cloned directory (`virtualenv -p /usr/bin/python2 venv`). Steps after that:

![](https://raw.githubusercontent.com/yoda-pa/yoda/master/screencasts/firstsetup.gif)

Instead of `pip install --editable .` you can use `pip install .` if you don't intend to make any changes in the code.

## Use this package, how to

#### chat

Use the `chat` command to talk to the inbuilt chatbot for this project.

![](https://raw.githubusercontent.com/yoda-pa/yoda/master/screencasts/chat.gif)

You can test the chat functionality on api.ai agent website [here](https://bot.api.ai/ff4ba99e-e444-4e19-8b4e-91fb0b93e414)

#### dev

This command group contains some sub-commands that may be helpful for developers and tech-geeks.

- **speedtest**: check your internet speed
  ![](https://raw.githubusercontent.com/yoda-pa/yoda/master/screencasts/speedtest.gif)

- **url**: URL shortener
  ![](https://raw.githubusercontent.com/yoda-pa/yoda/master/screencasts/url.gif)

- **hackernews**: read hackernews articles
  ![](https://raw.githubusercontent.com/yoda-pa/yoda/master/screencasts/hackernews.gif)

- **sitechecker**: check if a site is up

    Usage:

    ~~~
    $ yoda checksite https://manparvesh.com

    $ yoda checksite https://manparveshs.com
    ~~~

    ![](https://raw.githubusercontent.com/yoda-pa/yoda/master/screencasts/sitechecker.gif)

- **whois**: get whois records

    Usage:
    ~~~
    $ yoda dev whois google.com
    ~~~

    ![](https://raw.githubusercontent.com/yoda-pa/yoda/master/screencasts/whois.gif)

- **grep**: grep implementation
 
    ~~~
    $ yoda dev grep PATTERN FILE|FOLDER -r [True] -i [True]
    -r is the flag for recursive search. -i enables case insensitive search.
    Both are optional parameter and the flags are off if they are not provided.

    $ yoda dev grep \d+ modules/ -r True
    Will recursively search all files in modules directory for any line containing 1 or more digits.

    $ yoda dev grep yOdA modules/ -i True
    Will recursively search all files in modules directory for any line containing the word yoda.
    This search is case insensitive.

    $ yoda dev grep yOdA yoda.py -i True
    Will recursively search the file yoda.py for any line containing the word yoda.
    This search is case insensitive.
    ~~~

- **gif**: Create gif from images

    ~~~
    $ yoda gif from_images --source SOURCE_DIR --output OUTPUT_FILE
    Will scan the source directory and generate a gif. File will be located at OUTPUT_FILE.
    e.g.
    yoda gif from-images --source tests/resources/gif_frames/ --output test.gif

    $ yoda gif from_images --source SOURCE_DIR --output OUTPUT_FILE --<param> <value>
    Will scan the source directory and generate a gif. File will be located at OUTPUT_FILE.
    <param> and <value> can be any keyword argument that imageio's mimsave function takes.
    e.g.
    yoda gif from-images --source tests/resources/gif_frames/ --output test.gif --fps 9
    will create a gif with 9 fps.
    ~~~

- **gitsummary**: gets the summary of your github account

    ~~~
    $ yoda gitsummary GITHUB_LOGIN GITHUB_PASSWORD
    Uses the GIthub v3 API to get number of repos, commits (last 24hr), open pull requests (last 24hr) and open issues (last 24hr).

    e.g.
    $ yoda gitsummary SomeUsername MySuperS3cr3tP4ssw0rd!
    Fetching data. Patience you must have, my young padawan.

    SomeUsername, ready your GitHub statistics are.
    6 repositories you have.
    In last 24 hours 10 commit(s), 2 pull requests(s) and 3 issue(s) you made.
    ~~~

- **run**: compile and run source codes written in different programming languages!

    ~~~
    $ yoda run tests/resources/test_code.py
    ~~~

    ![](https://raw.githubusercontent.com/yoda-pa/yoda/master/screencasts/runcode.gif)


- **fileshare**: share files that are accessible only once

    ~~~
    $ yoda fileshare transport.png
    ~~~

    ![](https://raw.githubusercontent.com/yoda-pa/yoda/master/screencasts/fileshare.gif)

- **keybindings**: save key bindings

    ~~~
    # To add(or import) a keybindings file
    $ yoda dev keybindings add vim /absolute/path/to/keybinding/file.csv

    # To search keybinding action for a software
    $ yoda dev keybindings search vim move cusror
    Key Bindings:
    ---------------------------------------
        key       |          action
    ---------------|-----------------------
          h       |       move cursor left
          j       |       move cursor down
          k       |       move cursor up
          l       |       move cursor right
    ~~~

- **IP lookup:** Get the geographical location of an IP address.

    ```
    $ yoda iplookup 23.20.227.213
    Virginia, United States
    ```

#### horoscope
See your horoscope

![](https://raw.githubusercontent.com/yoda-pa/yoda/master/screencasts/horoscope.gif)

- command keep
~~~
# To add a command to your keep
$ yoda keep save -k find -k text -k name 'find . -name "*.txt"' command used to find textfiles by name
# To show all commands
$ yoda keep findall
# To show commands by keywords
$ yoda keep find -k text
# To remove a command
$ yoda keep remove -i ##command index, showed when running find or findall##
~~~

#### goals

Create and complete goals, add tasks and analyze your progress.

```
# To set a goal (name, description, deadline)
$ yoda goals new

# To show list of ideas
$ yoda goals view

# To set a goal as completed
$ yoda goals complete

# To see number of completed/incomplete goals, missed deadlines etc.
$ yoda goals analyze

# To view tasks assigned to the goal
$ yoda goals tasks

```

![](https://raw.githubusercontent.com/yoda-pa/yoda/master/screencasts/goals.gif)

**Note:** Use this module with ```diary``` module and assign new tasks to the goals by typing

```
$ yoda diary nt
```
and adding the goal names to the task when prompted to do so.

#### diary

This command can be used to maintain a personal diary, roughly based on the concept of [Bullet Journal](http://bulletjournal.com/).

![](https://raw.githubusercontent.com/yoda-pa/yoda/master/screencasts/diary.gif)

For creating and writing new note type

```
# For writing new note
$ yoda diary nn

# First give the title of the note.
# Second give the text of the note

# Viewing all notes.
$ yoda diary notes

# Updating note
# Choose the date and then the note to update
$ yoda diary un

# Deleting Note
# Choose the date and then the note to delete
$ yoda diary dn
```
For writing and viewing tasks.

```
# Writing new task
$ yoda diary nt

# Viewing all tasks
$ yoda diary tasks

# Change the status of task to completed
$ yoda diary ct

# Update task
# Choose the date and then the task to update
$ yoda diary ut

# Delete Task
# Choose the date and then the task to delete
$ yoda diary dt

# Delete all completed tasks for today
$ yoda diary dct
# type c to confirm the deletion
```

#### love

This command can be used to maintain a profile of someone you love, take notes and remember what they like.

![](https://raw.githubusercontent.com/yoda-pa/yoda/master/screencasts/love.gif)

#### money

For tracking money, this is.

![](https://raw.githubusercontent.com/yoda-pa/yoda/master/screencasts/money.gif)

Get your expenses per month
```
$ yoda money exps_month
$ Sep: spent 75 USD
$ Nov: spent 15 USD
$ Dec: spent 125 USD
```

Convert currency
```
$ yoda money convert
Enter currency codes seperated by space:
INR USD
₹ 1 = US$ 0.0136
Enter the amount in INR to be converted to USD
100
100 INR = 1.36 USD
```
#### leaselist

Keep a record of things people have taken from you, and the things you have taken from them - to remind them / yourself to return

```
# To add an item
$ yoda leaselist add

# To show list of items lent/borrowed
$ yoda leaselist show

# To remove an item from the list
$ yoda leaselist remove

```

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

#### IP lookup

Get the geographical location of an IP address.

```
$ yoda iplookup 23.20.227.213
Virginia, United States
```

#### Custom cummands

Set a custom command.

```
$ yoda cc pwd
$ yoda pwd
/home/alex/git-clones/yoda
```

#### learn

This command group contains commands that, helpful in learning new things, will be.

- **vocabulary**: For enhancing your vocabulary and tracking your progress.

    ![](https://raw.githubusercontent.com/yoda-pa/yoda/master/screencasts/vocab.gif)


- **flashcards**: for learning anything! ([inspiration](https://github.com/zergov/flashcards))

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

- **dictionary:** to get definition, synonym, antonym and example of a word. This definition or synonym search will be automatically saved, so that while you are working on your vocabulary, you can come through the new word as well.

    ```
    $ yoda dictionary define car
    A few definitions of the word "car" with their parts of speech are given below:
    ---------------------------------
    noun: a motor vehicle with four wheels; usually propelled by an internal combustion engine
    noun: the compartment that is suspended from an airship and that carries personnel and the cargo and the power plant
    noun: where passengers ride up and down
    noun: a wheeled vehicle adapted to the rails of railroad
    noun: a conveyance for passengers or freight on a cable railway
    This word already exists in the vocabulary set, so you can practice it while using that

    $ yoda dictionary synonym car
    A few synonyms of the word "car" are given below:
    ---------------------------------
    auto
    automobile
    machine
    motorcar
    gondola
    elevator car
    railcar
    railroad car
    railway car
    cable car
    This word already exists in the vocabulary set, so you can practice it while using that

    $ yoda dictionary antonym car
    Sorry, no antonyms were found for this word

    $ yoda dictionary example good
    A few examples of the word "good" are given below:
    ---------------------------------
    weigh the good against the bad
    among the highest goods of all are happiness and self-realization
    a good friend

    ```

#### Aliasing

This command allows you to alias cumbersome commands.

  ```
  # before: shortening a url
  $ yoda url shorten google.com

  # alias shorten to be s
  $ yoda alias new "shorten" "s"

  # can now use s in place of shorten
  $ yoda url s google.com

  # or alias the whole command as us
  $ yoda alias new "url shorten" "us"
  $ yoda us google.com

  # show your current aliases
  $ yoda alias show

  # delete aliases
  $ yoda alias delete "us"
  $ yoda alias delete "s"

  ```



#### ascii_transfrom

This command outputs transformed ascii version of a given image.

```
    # give the path of the image you want to transform
    $ yoda ascii_transform logo.png

    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%.%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%..S%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%..+.?%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%..SSS%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%.+..+..+?%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%..SSSSS%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%..+..+..+..%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%SSSSS++%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%...+.....+...%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%SSS++++%%%%%%%%%%%%%%%%%%%%%%%%%%%..............S%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%S+++++.%%%%%%%%%%..........?%%%................%%%%..........%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%++++...%%%%%%%%%%SSS............+++....+++.............SSS%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%++.....%%%%%%%%%SSSS.........+....+.+....+..+......SSS%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%.....**%%%%%%%%SSSSS...+..+......+.............SSSS%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%...****%%%%%%%SSSSSS...........+......+..+.SSSSS%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%.******%%%%%%SSSSSS......@@.....@@......SSSSS%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%*****%%%%%%SSSS.......@......@.......SSSS%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%******%%%%%%%%SS..........SSS.........%S%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%..******%%%%%%%%%%%......................%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%....****%%%%%%%%%%%%%%.......S.............%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%++.....*%%%%%%%%%%%%%%%%%%.....%%%.S.........%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%++++....%%%%%%%%%%%%%%%%%%%%%?......%%%%%%...%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%S+++++..%%%%%%%%%%%%%%%%%%%%%%%%%............?%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%SSSS++++%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%.........%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%.SSSSS++%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%......?%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%..SSSSS%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%..SSS%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%..%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%.SSSSS++++++......*****%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%.SSSSS++++++......*****%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%.SSSSS++++++......*****%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


```



#### Weather

This command obtains the weather information of a specified location using
[wttr](http://wttr.in) as the weather service.

![](https://raw.githubusercontent.com/yoda-pa/yoda/master/screencasts/weather.gif)

#### people

This is an inbuilt people manager that can be used to save profiles of people and related information, like their birthdays, likes, and some personalized notes for them.

```
# To add people(or a friend)
$ yoda people setup

# To show added friends
$ yoda people status
--------------------------------------
     Mob    |     DOB    |   Name
------------|------------|------------
 7503160111 | 1994-06-26 | Joy
 7503160112 | 1994-05-26 | Lobo

# To add what people like(or a friend likes)
$ yoda people like

# To add personalized notes for people(or friend)
$ yoda people note

# To view likes of your added people
$ yoda people likes
Joy
Likes:
1: #petry
2: #acting

# To view personalized notes for added people(or friend)
$ yoda people notes
Lobo
Notes:
1: stop saying start doing
2: keep chin up

```

#### lyrics

This command can be used to get the lyrics of a song.

```
$ yoda lyrics
Enter the artist name:
imagine dragons
Enter the title name:
thunder
--------Lyrics--------
Just a young gun with a quick fuse
I was uptight, wanna let loose
I was dreaming of bigger things in
```

#### food

Use this command to get suggestions related to food.

```
# To get a restaurant suggestion in your city:
$ yoda food suggest_restaurant
What city are you in? Berlin
What type of food are you interested in? Chinese

Why don't you try THIS restaurant tonight!

Shaniu's House of Noodles on Pariser Str. 58
Book a table at +493091552605


# To get a drink suggestion
$ yoda food suggest_drinks
Like you need a drink you look.  Hmmmmmm.
---------------------Jello shots---------------------
Ingredients:
Vodka x 2 cups
Jello x 3 packages
Water x 3 cups
Instructions: Boil 3 cups of water then add jello. Mix jello and water until jello is completely disolved. Add the two cups of vodka and mix together. Pour mixture into plastic shot glasses and chill until firm. Then, eat away...


# To get a recipe suggestion
$ yoda food suggest_recipes
Categories: American, British, Canadian, Chinese, Dutch, Egyptian, French, Greek, Indian, Irish, Italian, Jamaican, Japanese, Kenyan, Malaysian, Mexican, Moroccan, Russian, Spanish, Thai, Unknown, Vietnamese

Choose a category above or type 'Random' for a random recipe suggestion: Random

---------------------Spicy Arrabiata Penne---------------------

Ingredients:
penne rigate x 1 pound
olive oil x 1/4 cup
garlic x 3 cloves
chopped tomatoes x 1 tin
red chile flakes x 1/2 teaspoon
italian seasoning x 1/2 teaspoon
basil x 6 leaves
Parmigiano-Reggiano x spinkling

Instructions: Bring a large pot of water to a boil. Add kosher salt to the boiling water, then add the pasta. Cook according to the package instructions, about 9 minutes.
In a large skillet over medium-high heat, add the olive oil and heat until the oil starts to shimmer. Add the garlic and cook, stirring, until fragrant, 1 to 2 minutes. Add the chopped tomatoes, red chile flakes, Italian seasoning and salt and pepper to taste. Bring to a boil and cook for 5 minutes. Remove from the heat and add the chopped basil.
Drain the pasta and add it to the sauce. Garnish with Parmigiano-Reggiano flakes and more basil and serve warm.

```

#### feedback

To create an issue in the github repository simple thing that shows a link.  Yeesssssss.

![](https://raw.githubusercontent.com/yoda-pa/yoda/master/screencasts/feedback.gif)

#### ciphers

Use this command to encrypt or decrypt text using various classical ciphers

```
$ yoda ciphers encrypt
0: Atbash
1: Caesar
2: ROT13
3: Vigenere
Choose a cipher: 3
The text you want to encrypt: Mary had a litle lamb
The encryption keyword: mango
ZBFF WNE O SXGUZL ANNP

$ yoda ciphers decrypt
0: Atbash
1: Caesar
2: ROT13
3: Vigenere
Choose a cipher: 3
The text you want to decrypt: ZBFF WNE O SXGUZL ANNP
The encryption keyword: mango
MARY HAD A LITTLE LAMB
```

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
- [chardet](https://github.com/chardet/chardet): universal character encoding detector
- [Codecov](https://codecov.io/): code coverage dashboard
- [coverage](https://pypi.org/project/coverage/): For code coverage testing
- [requests](http://docs.python-requests.org/en/latest/): For HTTP requests
- [nose](https://github.com/nose-devs/nose): For unit testing
- [urllib3](https://github.com/urllib3/urllib3): HTTP client
- [Certifi](https://github.com/certifi/python-certifi): Python SSL Certificates
- [idna](https://github.com/kjd/idna): For the domain name
- [GeoIP2-database](https://www.maxmind.com/en/geoip2-city): For geographical IP lookups
- [future](https://pypi.org/project/future/): the layer of compatability for Python 2/3
- [Google URL Shortener](https://developers.google.com/url-shortener/): URL shortener
- [News API](https://newsapi.org/): Used to get the top headlines from Hacker News
- [Forismatic API](https://forismatic.com/en/api/): Get random quotes that are used in the chat module
- [Cocktail DB](https://www.thecocktaildb.com/api.php): Used to search for a drink and to get a random drink
- [Words API](https://www.wordsapi.com/): Used to get the definition of a word
- [Requests](https://wwww.docs.python-requests.org): Used for online http requests/services
- [wttr](http://wttr.in): Used for getting weather information
- [file.io](https://file.io/): Used for fileshare
- [HackerEarthAPI](https://www.hackerearth.com/docs/wiki/developers/v3/): Used to run code
- [lyrics.ovh](https://lyricsovh.docs.apiary.io/#): Used for lyrics
- Yoda's illustration SVG was taken from [here](https://www.shareicon.net/yoda-854796)
- [WhoIs](https://www.whois.com): Used for getting information about domains.

## Contribute, you must
Please refer to the [contributing guidelines](https://github.com/yoda-pa/yoda/blob/master/.github/CONTRIBUTING.md) for contributing to this project. This project was made possible by contributions from [many awesome people](https://github.com/yoda-pa/yoda/graphs/contributors).

## In the news
- [ostechnix](https://www.ostechnix.com/yoda-the-command-line-personal-assistant-for-your-linux-system/)
- [sdtimes](https://sdtimes.com/os/sd-times-github-project-week-yoda-2/)

## Changelog

### v1.0.0
Related milestone: [v1.0.0](https://github.com/yoda-pa/yoda/milestone/5)

Changes in this version:
- Docker setup
- Load modules on demand
- Mock external services in tests
- Support for custom commands
- Currency conversion
- Weather functionality
- Money Manager: monthly expenses
- Gif creator
- Site checker
- IP Lookup
- Grep
- Horoscope
- Suggest drinks
- Suggest recipes
- Small bug fixes and improvements

### v0.4.0
Related milestone: [v0.4.0](https://github.com/yoda-pa/yoda/milestone/2)

Changes in this version:
- Added goals and analysis
- Added reading list
- Enhancements to diary
- Better documentation and code quality than before
- Added more tests
- Security alert fixes
- Various bug fixes

### v0.3.0
Related milestone: [v0.3.0](https://github.com/yoda-pa/yoda/milestone/3)

Changes in this version:
- Support for both Python 2 and Python 3
- Command aliasing
- Port scanning
- More features in love module
- Hackernews
- yoda inspire
- Increased test coverage
- Bug fixes

### v0.2.0
Related milestone: [v0.2.0](https://github.com/yoda-pa/yoda/milestone/1)

Changes in this version:
- Idea list
- Reading list
- Automated tests
- Test coverage
- Custom config directory location
- Minor bug fixes

### v0.1.0
Initial release.
