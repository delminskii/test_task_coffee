# CoffeeLike test task for junior position
## requirements
----
* python 2.7 (written on that)
* virtualenv 15.0.3 (written for that)
* pip package manager 1.5.4
## usage
----
1. You need to get a [client access token](https://docs.genius.com/#/getting-started-h1). Just register there and you'll find it in your profile settings.
2. Install all the necessary 3rd party libraries using pip:
```bash
    pip install -r requirements.txt
```
3. After that, simply run this script with a predefined `GENIUS_ACCESS_TOKEN` environment variable like this:
```bash
GENIUS_ACCESS_TOKEN="%YOUR_TOKEN_HERE%" python get_lyrics.py -h
```
4. Don't forget about 1 mandatory argument - `song` and 1 optional argument - `an output file`. If you omit an optional one you are able getting an access to the output somewhere here: `/tmp/get_lyrics.py_%timestamp%.txt`, otherwise define your own one: `-o path/to/your/file`

## example run
```bash
GENIUS_ACCESS_TOKEN="%YOUR_TOKEN_HERE%" python get_lyrics.py "Madonna Girl gone wild" -o $HOME/madonna-girl_gone_wild.txt
```
