import sys
import boto3
import datetime
import time

epoch = datetime.datetime(1970, 1, 1, 0, 0, 0, 0)

class bcolors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

class bgcolors:
    GRAY = '\033[47m'
    DARKGRAY = '\033[100m'
   

def filter_logs(log_group, search_strings):
    base_delta = datetime.datetime.now() - epoch
    ms_from_epoch = int(base_delta.total_seconds()) * 1000
    five_seconds_ago = ms_from_epoch - 5000
    cwclient = boto3.client('logs')
    response = ''
    try:
        response = cwclient.filter_log_events(
            logGroupName=log_group,
            startTime=five_seconds_ago,
            endTime=ms_from_epoch,
            filterPattern=f"{search_strings}"
        )
    except Exception as e:
        print(f"Error with: {log_group}. {e}")
    return response

def print_logs(log_entries, log_group):
    print(f"{bcolors.YELLOW}{bcolors.BOLD}{log_group}{bcolors.RESET}")
    for event in log_entries['events']:
        for key in event.keys():
            if key == 'logStreamName':
                print(f"{bcolors.YELLOW}{bcolors.BOLD}{event[key]}{bcolors.RESET}")
            elif key == 'message':
                print(f"{bcolors.CYAN}{key}: {bcolors.GREEN}{event[key]}{bcolors.RESET}")
    print(f"{bcolors.YELLOW}{bcolors.BOLD}================================================================================================================{bcolors.RESET}")            
    return

def main():
    # TODO: remove bad entries from list
    log_groups = input("Enter log groups: ").split(',')
    # TODO: accept more than one search string
    search_strings_raw = input("Enter search strings: ").split(' ')
    search_strings = ''
    for string in search_strings_raw:
        search_strings = f"{search_strings} {string}"
    print(f"Log groups: {log_groups}")
    print(f"Search strings: {search_strings}")
    while 1:
        for log_group in log_groups:
            log_entries = filter_logs(log_group.rstrip().lstrip(), search_strings[0].rstrip().lstrip())
            if log_entries: 
                print_logs(log_entries, log_group)
        time.sleep(5)
    return

if __name__ == "__main__":
    main()