# poe2-item-search
Price check items ingame against PoE2 trading website
Press Ctrl-D while your cursor is on an item to open up the trade website with filters pre-populated.

# Installation

This project requires [Python](https://www.python.org/downloads/) to be installed locally. 

## (Optional) Set up a virtual Python environment for this project

Navigate to the directory containing the project:
```commandline
# for example on Windows
cd %USERPROFILE%\Downloads\poe2-item-search
# for example on Linux/etc
cd ~/Downloads/poe2-item-search
```

Create a Python virtual environment:
```commandline
python -m venv .venv
```

Then tell your shell to use the virtual environment (must be repeated any time you run):
```commandline
# Windows
.venv\Scripts\activate
# Linux/etc
source .venv/bin/activate
```

## Install requirements

Finally, install packages:
```
pip install -r requirements.txt
```

# Running

If choosing to use venv, activate it as above; `.venv\Scripts\activate`, then:
```
python project.py
```

Use `Ctrl+Break` to stop the app.
