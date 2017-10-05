
# Contributing

Firstly, thanks for taking the time to contribute! :grin:

## What should I know before getting started?
- git
- python (reading and understanding code)

## How Can I Contribute?
### Feature suggestions / bug reports
You can contribute to this project by suggesting features or filing bugs by creating an issue [here](https://github.com/yoda-pa/yoda/issues/new).
### Writing code
If you are interested in contributing by writing code, you can do so by implementing the features listed in [the TODO file](../TODO.md).  
#### Structure
```sh
├── modules/         # home for various features
├── resources/       # home for resources required in modules
├── config.py        # contains configuration
├── util.py          # contains utility functions
├── setup.py         # the setup script
└── yoda.py          # the main script
```
#### Setup
```bash
# Fork, then clone the repo
$ git clone git@github.com:<your-username>/yoda.git

# create a virtualenv
$ virtualenv venv  

# activate the virtualenv
$ . venv/bin/activate

# Install the package in editable mode
$ pip install --editable .

# run it!
$ yoda
# to exit the virtualenv, just type 'deactivate' without quotes
```
#### First contribution
In case you are unsure about where to start, you can look at the `easy` and `medium` issues.
- [easy issues](https://github.com/yoda-pa/yoda/issues?q=is%3Aopen+is%3Aissue+label%3A%22difficulty%3A+easy%22) - do not require much work
- [medium issues](https://github.com/yoda-pa/yoda/issues?q=is%3Aissue+is%3Aopen+label%3A%22difficulty%3A+medium%22) - should be a bit more involved than `easy` issues.

#### Sending a pull request
Push to your fork and [submit a pull request](https://github.com/yoda-pa/yoda/compare/). Follow the [pull request template](https://github.com/yoda-pa/yoda/blob/master/.github/PULL_REQUEST_TEMPLATE.md)  

## Github labels
### Issue labels
- Labels starting with `module: `: these specify the modules in which the changes / enhancements are to be made.
- `bug`: it's a bug
- `enhancement`: hacking on the existing code
- Labels starting with `difficulty: `: specify the difficulty levels of the issue, depending on the work to be done to complete it.
- `new feature`: new feature introduced
