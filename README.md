## The Story

I wanted to get KLACK because my friend had it and found out it was 5 usd. My dad then said why not make it on your own. So I did.

## How to use

Run soundy.py with the required packages installed. Tested on Python 3.14.2, however should work on older python3 versions. You will need to enable key tracking for vscode / terminal

### Needed packages

Pynput - python -m pip install pynput

### Slight problem

It only supports MacOS. To get it to work on windows you will have to change the method of playing the sounds to something like WinSound (windows only), just change this line with your sound player and put file_path in the file path area.

```
try:
        subprocess.Popen(["afplay", file_path])
```

*You will also need to convert all of the sound files (m4a) to mp3. I think, because m4a is a MacOS thing. (Don't quote me) 

## Credits

Me - for everything
KLACK Devs - for the sounds + me for recording them from their website and then spending ages splicing the separate keys. (They did not make it easy)
Github Copilot - for researching about ways to play sounds