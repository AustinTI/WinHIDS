import win32evtlog  # Imports the win32evtlog module

def monitor_event_logs():
    server = 'localhost'  # Use your server name here
    logtype = 'System'  # Can be 'Application', 'System', 'Security', etc.
    hand = win32evtlog.OpenEventLog(server, logtype)
    
    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    total = 0  # Count of events handled
    try:
        while True:
            events = win32evtlog.ReadEventLog(hand, flags, 0)
            if not events:
                break
            for event in events:
                if event.EventID in [4625]:  # Example: Failed login attempt
                    print('Failed login detected!')
                    print(f'Event ID: {event.EventID}')
                    print(f'Source: {event.SourceName}')
                    print(f'Time Generated: {event.TimeGenerated}')
                    print(f'Message: {event.StringInserts}')
                total += 1
    finally:
        win32evtlog.CloseEventLog(hand)
    return total

monitor_event_logs()
