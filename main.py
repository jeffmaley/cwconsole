import boto3

def filter_logs():
    cwclient = boto3.client('logs')
    response = cwclient.filter_log_events(
        logGroupName='/aws/neptune/neptune-1-cluster/audit'
    )
    return response

def print_logs(log_entries):
    for event in log_entries['events']:
        print(f"Entry: {event}")
    return

def main():
    log_entries = filter_logs()
    print_logs(log_entries)
    #print(f"log_entries: {log_entries}")
    return

if __name__ == "__main__":
    main()