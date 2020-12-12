import sys
import boto3
import datetime

epoch = datetime.datetime(1970, 1, 1, 0, 0, 0, 0)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

def filter_logs(log_group):
    base_delta = datetime.datetime.now() - epoch
    ms_from_epoch = int(base_delta.total_seconds()) * 1000
    five_seconds_ago = ms_from_epoch - 5000
    cwclient = boto3.client('logs')
    response = cwclient.filter_log_events(
        logGroupName=log_group,
        startTime=five_seconds_ago,
        endTime=ms_from_epoch
    )
    return response

def print_logs(log_entries):
    for event in log_entries['events']:
        for key in event.keys():
            if key == 'logStreamName':
                print(f"{bcolors.UNDERLINE}{bcolors.BOLD}{event[key]}{bcolors.RESET}")
            else:
                print(f"{bcolors.HEADER}{key}: {bcolors.OKGREEN}{event[key]}")
    print(f"{bcolors.RESET}End of output")
    return

def main():
    while 1:
        log_entries = filter_logs(sys.argv[1])
        print_logs(log_entries)
    return

if __name__ == "__main__":
    main()