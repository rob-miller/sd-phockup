#!/usr/bin/python3

import pyudev
import threading
# import subprocess
import os
import time

# Configuration parameters
BEEP_DURATION = 0.2  # duration for beep
CONTINUOUS_BEEP_INTERVAL = 2  # seconds
MOUNT_POINT = "/mnt/sdcard"  # SD card mount point
#PHOTO_DEST = "/home/rob/foo"
#PHOCKUP_LOG = "/home/rob/p.log"
PHOTO_DEST = "/media/nvm1/photos"
PHOCKUP_LOG = "/home/rob/phock.log"
#PHOCKUP_COMMAND = "sleep 10"
PHOCKUP_COMMAND = f"phockup -o -c 1 --log {PHOCKUP_LOG} {MOUNT_POINT} {PHOTO_DEST}"
# for moving and clearing old photos from drive
#PHOCKUP_COMMAND = "phockup -m -o -c 1 --rmdirs --skip-unknown --movedel --log /home/rob/phock.log {} /media/nvm1/photos"

LOW = 800
MEDIUM = 1000
HIGH = 2000
VHIGH = 4000

#SDDEVNUM = 0
#SDPARTITION = 1

def beep(freq):
    if freq == VHIGH:
        os.system("speaker-test -t sine -f {} -l 1 >/dev/null & sleep {} && kill -9 $!".format(freq, BEEP_DURATION/2))
    else:
        os.system("speaker-test -t sine -f {} -l 1 >/dev/null & sleep {} && kill -9 $!".format(freq, BEEP_DURATION))

def mount_sd_card(context, device):
    for _ in range(3):
        for dev2 in context.list_devices(subsystem='block', DEVTYPE='partition'):
            if device.driver in dev2.device_node and dev2.get('ID_FS_TYPE') is not None:
                print('{0} ({1})'.format(dev2.device_node, dev2.get('ID_FS_TYPE')))
                os.system("mount {} {}".format(dev2.device_node, MOUNT_POINT))
                # os.system(f'ls {MOUNT_POINT}')
                beep(MEDIUM)  # Different beep to indicate mounting
                return True
        # mount fail, beep more and retry
        beep(VHIGH)
        beep(VHIGH)
        beep(VHIGH)
        time.sleep(2)
    print("failed to mount sd card")
    return False

stop_beeping_event = threading.Event()

def continuous_beep():
    while not stop_beeping_event.is_set():
        time.sleep(CONTINUOUS_BEEP_INTERVAL)
        beep(HIGH)

def run_command():
    os.system(PHOCKUP_COMMAND)

def unmount_sd_card():
    os.system("umount {}".format(MOUNT_POINT))

def monitor_sd_card():
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by(subsystem='mmc')
    for device in iter(monitor.poll, None):
        print(f"detected {device} action {device.action}")
        """
        for dev2 in context.list_devices(subsystem='block', DEVTYPE='partition'):
            print('{0} ({1})'.format(dev2.device_node, dev2.get('ID_FS_TYPE')))
        print()
        """
        if 'SD' in device.properties["MMC_TYPE"] and 'bind' == device.action:
            # time.sleep(1)
            beep(LOW)  # Beep to indicate SD card detection
            if mount_sd_card(context, device):
                print("mounted sdcard")
                beep_thread = threading.Thread(target=continuous_beep)
                beep_thread.start()
                #run_command()
                #unmount_sd_card()
        elif 'SD' in device.properties["MMC_TYPE"] and 'remove' == device.action:
            try:
                stop_beeping_event.set()  # Signal the thread to stop beeping
                beep_thread.join()  # Wait for the beep thread to finish
                stop_beeping_event.clear()  # ready for next time
            except UnboundLocalError as e:
                print("remove but not beeping")
            #beep(LOW)
            beep(LOW)
        # else:
        #    beep(VHIGH)

if __name__ == "__main__":
    monitor_sd_card()
