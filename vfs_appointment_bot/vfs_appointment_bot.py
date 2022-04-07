import sys
import logging

from logging.config import fileConfig
from _Timer import countdown
from _ConfigReader import _ConfigReader
from _VfsClient import _VfsClient

def _input():
    print("Enter the visa centre: ")
    visa_centre = input()

    print("Enter the category: ")
    category = input()

    print("Enter the sub category: ")
    sub_category = input()

    logging.debug("Visa centre: {}, Category: {}, Sub-Category: {}".format(visa_centre, category, sub_category))

    return visa_centre, category, sub_category

def _read_command_line_args():
    if len(sys.argv) != 4:
        return _input()
    return sys.argv[1], sys.argv[2], sys.argv[3]
    

if __name__ == "__main__":
    count = 1
    fileConfig('config/logging.ini')
    logging = logging.getLogger(__name__);

    _vfs_client = _VfsClient()
    _config_reader = _ConfigReader()
    _interval = _config_reader.read_prop("DEFAULT", "interval");
    logging.debug("Interval: {}".format(_interval))
    
    visa_centre, category, sub_category = _read_command_line_args()

    logging.info("Starting VFS Appointment Bot")
    while True:
        try:
            logging.info("Running VFS Appointment Bot: Attempt#{}".format(count))
            _vfs_client.check_slot(visa_centre=visa_centre, category=category, sub_category=sub_category)
            logging.debug("Sleeping for {} seconds".format(_interval))
            countdown(int(_interval))
        except Exception as e:
            logging.info(e.args[0] + ". Please check the logs for more details")
            logging.debug(e, exc_info=True, stack_info=True)
            countdown(int(60))
            pass
        print("\n")
        count += 1
 
