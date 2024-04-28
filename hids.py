import time
import json
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Load configuration
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Setup logging
logging.basicConfig(filename=config['log_file'], level=logging.INFO, format='%(asctime)s - %(message)s')

class ChangeHandler(FileSystemEventHandler):
    """Handles file system events."""
    def on_modified(self, event):
        super(ChangeHandler, self).on_modified(event)
        if event.is_directory:
            return
        logging.info(f'Modified file: {event.src_path}')

    def on_created(self, event):
        super(ChangeHandler, self).on_created(event)
        logging.info(f'Created file: {event.src_path}')

    def on_deleted(self, event):
        super(ChangeHandler, self).on_deleted(event)
        logging.info(f'Deleted file: {event.src_path}')

    def on_moved(self, event):
        super(ChangeHandler, self).on_moved(event)
        logging.info(f'Moved file: from {event.src_path} to {event.dest_path}')

# Monitor the filesystem
observer = Observer()
event_handler = ChangeHandler()
paths = config['paths_to_monitor']
for path in paths:
    observer.schedule(event_handler, path, recursive=True)

observer.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
