# telemotion

Uses [motion](https://github.com/Motion-Project/motion) to detect any motion from a web camera and receive pics and videos on your
Telegram app.

Make sure to edit your target directory in `motion.conf`. Then place `PiNotify.sh` and `TelegramBot.py` in the target directory
you specified. Also edit the path to `PiNotify.sh` in `motion.conf` so it calls the script in the correct location when a
motion event is triggered.

## Usage

Add your token and stuff in `PiNotify.sh` and `TelegramBot.py`. Then do

```
$ motion -c motion.conf
$ python TelegramBot.py
```

## License

`The MIT License`
