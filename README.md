# red-installer

This is a simple installer for Red-DiscordBot, in use until discord.py is uploaded to
the Python Package Index.

It is roughly equivalent to doing the following command on pip versions prior to 19.0:
```bash
pip install -U --process-dependency-links Red-DiscordBot[voice]
```

As such, installing pre-requirements and creating virtual environments is not handled by
this script.

Unlike the original `pip` command, this script will ensure that the correct version of
discord.py is installed when updating an existing installation, *without* bypassing the
cache and force reinstalling all dependencies.

## Usage
Please execute the following command whilst activated in your virtual environment.

### Linux and Mac
In bash/Terminal:
```
wget https://raw.githubusercontent.com/Tobotimus/red-installer/master/red-installer.py | python -
```

### Windows
In PowerShell:
```powershell
wget -UseBasicParsing https://raw.githubusercontent.com/Tobotimus/red-installer/master/red-installer.py | python -
```


