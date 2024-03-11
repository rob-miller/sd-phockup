# sd-photostore

Written for Debian Linux 12 running on a Mac Mini.

Python 3 and systemd scripts to monitor the SD card slot and run [phockup](https://github.com/ivandokov/phockup)
when a card is inserted.  Phockup copies and organizes photos by year, month, day.  

_You will need to edit the script to configure your own source, destination and log directories._

I had to add root to the `pulse` group to enable root to use the `speaker-test` command (and thus make the beeps).

While phockup is running, beeps every two seconds.

When phockup is finished, the SD card is unmounted.

The intent is to support a headless device for backing up photos from SD cards.  Consider [PhotoPrism](https://www.photoprism.app/)
for viewing the library.


_Beep codes:_

- low beep :  SD card inserted or removed
- medium beep : SD card successfully mounted
- high beep : copying photos, repeats every two seconds while card is mounted.

- 3 very high beeps : error mounting SD card; will retry twice (nine beeps total)


