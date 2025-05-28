import time
import datetime
import subprocess

source_path = "/home/lab/tcam/tjsn_collection"  # Raspi side
dest_path = "/home/lab/clonesync"  # OneDrive side

def rclone_copy(folder_date):
    '''
    folder_date: 20250522
                 20250523
                 20250523
                 ...

    This function is used to upload the entire folder of current date
    '''
    source_folder = f"{source_path}/{folder_date}"   # Raspi
    dest_folder = f"{dest_path}/{folder_date}"   # OneDrive

    print(f"Running rclone copy from {source_folder} to {dest_folder}")
    subprocess.run(["rclone", "copy", source_folder, dest_folder])

def wait_until_next_hour_plus_one_minute():
    now = datetime.datetime.now()  # e.g 2025-05-22 13:45:27.123456
    next_hour = (now + datetime.timedelta(hours=1)).replace(minute=1, second=0, microsecond=0)  # e.g 2025-05-22 14:45:27.123456  --> 2025-05-22 14:01:27.123456
    wait_seconds = (next_hour - now).total_seconds()
    print(f"[{now}] Sleeping {wait_seconds:.2f} seconds until {next_hour}")
    time.sleep(wait_seconds)


def main():
    '''
    Main scrip aims to check the folder status houly past 1 minutes
    e.g:
            00:01
            01:01
            ...
            23:01

    '''
    last_date = datetime.date.today()  # e.g 2025-05-22

    while True:
        wait_until_next_hour_plus_one_minute()  # waiting

        current_date = datetime.date.today()  

        if current_date != last_date:  # move to next day
            # Date changed — copy previous day's folder one last time
            rclone_copy(last_date.strftime("%Y%m%d"))
            last_date = current_date

        # Copy current day's folder
        rclone_copy(current_date.strftime("%Y%m%d"))

if __name__ == "__main__":
    main()