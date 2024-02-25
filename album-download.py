#!/usr/bin/python3

from dotenv import load_dotenv
import subprocess
import os
import time
import sys

load_dotenv()

# Configuration
icloudpd_path = "/usr/local/bin/icloudpd"

username = None  # os.getenv('JANE_APPLE_ID')
password = None  # os.getenv('JANE_APPLE_PASSWD')

base_output_dir = None  # "/media/nvm1/photos/albums/jane"


smtp_username = os.getenv('ROB_GOOGLE_ID')
smtp_password = os.getenv('ROB_GOOGLE_APP_PASSWD')

smtp_sendto = "robjane@gmail.com"

main_delay = 190

ignore_albums = [
    "All Photos",
    "Time-lapse",
    "Videos",
    "Slo-mo",
    "Bursts",
    "Favorites",
    "Panoramas",
    "Screenshots",
    "Live",
    "Recently Deleted",
    "Hidden",
    # Jane
    "Instagram",
    "Twitter",
    # rob
    "You Doodle Pro",
    "WhatsApp",
    "Scannable",
    "Dropbox",
    "RAW",
    "Fjorden",
    "Canon EOS R7"
]


def list_albums():
    command = [
        icloudpd_path,
        "-u", username,
        "--smtp-username", smtp_username,
        "-l",
        "--notification-email", smtp_sendto,
        "-p", password,
        "--smtp-password", smtp_password,
        "--cookie-directory", "/root/.pyicloud",
        "--log-level", "error"
    ]
    # print(command)
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout
    else:
        print(result.stdout)
        print(result.stderr)
        raise Exception("Failed to list albums")


def download_album(album_name):
    album_dir = os.path.join(base_output_dir, album_name)
    if not os.path.exists(album_dir):
        os.makedirs(album_dir)
    command = [
        icloudpd_path,
        "-u", username,
        "--smtp-username", smtp_username,
        "--notification-email", smtp_sendto,
        "-p", password,
        "--smtp-password", smtp_password,
        "--log-level", "error",
        "--no-progress-bar",
        "--cookie-directory", "/root/.pyicloud",
        # "--only-print-filenames",
        "--folder-structure", "none",
        "-a", album_name,
        "-d", album_dir
    ]
    subprocess.run(command)


def main():
    for targ in ["jane", "rob"]:
        global username, password, base_output_dir

        if targ == "jane":
            username = os.getenv('JANE_APPLE_ID')
            password = os.getenv('JANE_APPLE_PASSWD')

            base_output_dir = "/media/nvm1/photos/albums/jane"
        elif targ == "rob":
            username = os.getenv('ROB_APPLE_ID')
            password = os.getenv('ROB_APPLE_PASSWD')

            base_output_dir = "/media/nvm1/photos/albums/rob"           

        print(f"downloading iphoto albums for user {targ}")
        albums_output = list_albums()
        time.sleep(10)
        albums = [line.strip() for line in albums_output.split("\n") if line.strip() and "Albums:" not in line]
        for album in albums:
            if album not in ignore_albums:
                print(f"Downloading album: {album} for user {targ}")
                try:
                    download_album(album)
                except Exception as e:
                    print(f"error downloading album {album} for user {targ}:")
                    print(e)
                    print(f"exit in {main_delay} seconds")
                    time.sleep(main_delay)
                    sys.exit(1)
                time.sleep(main_delay)
            else:
                print(f"Ignoring album: {album}")


if __name__ == "__main__":
    main()


# Jane albums feb 2024

# "Judy and Jane",
# "Falklands, South Georgia, Antarctic",
# "Antarctic friends",
# "Bill",
# "Hondius share",
# "Hondius social media",
# "Loreen",
# "Antarctica",
# "Jamaica - Port Antonio & Kingston",
# "Ian and Lizzie trip October 2023",
# "Nikki and Mike Gerrard August 2023",
# "Kaieteur falls",
# "SMART Hospital Initiative",
# "Explore Guyana 2023",
# "Rob",
# "Jon, Sue and Tom Visit",
# "Trade Guyana",
# "Mexico, Guatemala and Honduras",
# "Rob and Jane",
# "Zac Goldsmith visit",
# "Rebecca Fabrizi visit, Falls and Limden",
# "Diving Barbados Feb 2023",
# "Death of Her Majesty the Queen",
# "For printing",
# "Sim and Rog December 2022",
# "Whicabai, Rupununi and Kanuku Mountains",
# "Iceland 2022",
# "Hurakabra Essequibo August 2022",
# "Pandama Aug 2022",
# "CARICOM heads Suriname 2022",
# "Dive Barbados with Sam",
# "Barbados",
# "Queens Birthday Party and Platinum Jubilee 2022",
# "EnGenDER Visit to Suriname",
# "Royal Garden Party",
# "Zoe",
# "Gone Fishing - Jane and Yonnick on the Essequibo",
# "Queens Baton Relay",
# "Belize 2022",
# "Uk lockdown 2020",
# "Iwokrama and Rupununi Nov 2021",
# "Explore Guyana",
# "Georgetown trip with Mayor",
# "Rupununi with First Lady",
# "Linden to Madura Hills",
# "Moraikobai",
# "Arrow point with Captain",
# "UK Covid vaccine arrival",
# "Mnemba with Sam and Iwan",
# "Jane work",
# "Ethiopia May 2021",
# "Gombe chimps and dive",
# "Gombe with Antonio and Daniela",
# "Gombe Chimps May 2021",
# "Uganda March 2021",
# "Mafia 2021",
# "Christmas 2020",
# "Overhang, South Beach December 2020",
# "New Year 2021 Zanzibar",
# "Tanga Yacht Race",
# "Mnemba October 2020",
# "Sim and Rog et al March 2020",
# "Mount Meru",
# "Sauti za Busara 2020",
# "Ngorongoro Jan 2020",
# "Pemba Jan 2020",
# "Zanzibar caves",
# "Mikumi Oct 2019",
# "Red Sea diving",
# "Mnemba Atol, Zanzibar",
# "Idaho Circle Drive",
# "Pic Collage"


# rob albums feb 2024

# "not iphone",
# "eos r7",
# "Prescriptions",
# "Herbie Marshall",
# "Keep",
# "Receipts",
# "Moscow Asante",
# "Devices",
# "Drawing lessons",
# "GY stores & hardware",
# "3d printing",
# "GY",
# "Covid",
#  "GY menus",
# "Packing",
# "Nala docs",
# "House",
# "Diving",
#  "Best photos",
# "Mnemba",
# "4 woodlands",
# "Delta",
# "Cartesian i3",
# "Inventory",
# "WaterRower",
# "Dive",
# "DYC",
# "Card skimmer",
# "Filament dryer",
# "Run routes",
# "Recipes",
# "Projects",
# "Shopping",
# "Wine",
# "Navionics",
