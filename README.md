# telemotion

Uses [motion](https://github.com/Motion-Project/motion) to detect any motion from a web camera and receive pics and videos on your
Telegram app.

Make sure to edit your target directory in `motion.conf`. Then place `PiNotify.sh` and `TelegramBot.py` in the target directory
you specified. Also edit the path to `PiNotify.sh` in `motion.conf` so it calls the script in the correct location when a
motion event is triggered.

This set up will automatically send you the best picture of an event to you on Telegram.

## Usage

Add your token and stuff in `PiNotify.sh` and `TelegramBot.py`. Then do

```
$ motion -c motion.conf
$ python TelegramBot.py
```

## Available commands

Precede them with a `/`.

```
ping - pong
snapshot - take and send a snapshot
motion_on - enable motion detection
motion_off - disable motion detection
motion_status - motion detection status
dir_picture - picture directory
dir_movie - movie directory
dir_snapshot - snapshot directory
dir_timelapse - timelapse directory
delete - <first_few_letters_of_filename>
deletedir - <directory_name>
```

You can also download a specific picture/video by using `dir_<directory>` command.

## License

`The MIT License`
