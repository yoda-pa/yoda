
# Contributing

Firstly, thanks for taking the time to contribute! :grin:

## What should I know before getting started?
- git
- python (reading and understanding code)

## How Can I Contribute?
### Feature suggestions / bug reports
You can contribute to this project by suggesting features or filing bugs by creating an issue [here](https://github.com/dude-pa/dude/issues/new).
### Writing code
If you are interested in contributing by writing code, you can do so by implementing the features listed in [the TODO file](TODO.md).  
#### Structure
```sh
├── modules/         # home for various features
├── resources/       # home for resources required in modules
├── config.py        # contains configuration
├── util.py          # contains utility functions
├── setup.py         # the setup script
└── dude.py          # the main script
```
#### Setup
```bash
# Fork, then clone the repo
$ git clone git@github.com:<your-username>/dude.git

# create a virtualenv
$ virtualenv venv  

# activate the virtualenv
$ . venv/bin/activate

# Install the package in editable mode
$ pip install --editable .

# run it!
$ dude
# to exit the virtualenv, just type 'deactivate' without quotes
```
#### First contribution
In case you are unsure about where to start, you can look at the `easy` and `up-for-grabs` issues. 
- [easy issues](https://github.com/dude-pa/dude/issues?q=is%3Aopen+is%3Aissue+label%3A%22difficulty%3A+easy%22) - do not require much work
- [up for grabs issues](https://github.com/dude-pa/dude/issues?q=is%3Aopen+is%3Aissue+label%3Aup-for-grabs) - should be a bit more involved than `easy` issues.

#### Sending a pull request
Push to your fork and [submit a pull request](https://github.com/dude-pa/dude/compare/). Follow the [pull request template](https://github.com/dude-pa/dude/blob/master/.github/PULL_REQUEST_TEMPLATE.md)  
