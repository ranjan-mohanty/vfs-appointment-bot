import sys
import logging
import signal

from logging.config import fileConfig
from _Timer import countdown
from _ConfigReader import _ConfigReader
from _VfsClient import _VfsClient

def _input():
    centres = {
        "Portugal":
        ("https://visa.vfsglobal.com/gbr/en/prt/login",
         [ ("Portugal Visa application centre Edinburgh", "GENERAL", "Business Visa"),
          ("Portugal Visa application centre Edinburgh", "GENERAL", "Tourist visa")
         ]),
        "Netherlands":
        ("https://visa.vfsglobal.com/gbr/en/nld/login",
         [("Netherlands Visa application center- Edinburgh", "Default Netherlands United Kingdom", "Tourism")]),
        "Slovenia" :
        ("https://visa.vfsglobal.com/gbr/en/svn/login",
         [("Slovenia Visa Application Center - Edinburgh", "Visa", "All Visa Categories")]),
        "Italy" :
        ("https://visa.vfsglobal.com/gbr/en/ita/login",
         [("Italy Visa Application Centre Edinburgh", "Italy UK VisaCategory", "Tourist")]),
        "Norway" :
        ("https://visa.vfsglobal.com/gbr/en/nor/login",
         [("Norway Visa Application Centre, Edinburgh", "Default_Norway_United Kingdom", "Tourist Visa")]),
        "Malta":
        ("https://visa.vfsglobal.com/gbr/en/mlt/login",
         [("Malta Visa application center- Edinburgh", "Short Stay Schengen Visa", "Short Stay Visa")]),
    }

#    print("Enter the visa centre: ")
#    #visa_centre = input()
#    visa_centre = "Portugal Visa application centre Edinburgh"
#
#    print("Enter the category: ")
#    #category = input()
#    category = "GENERAL"
#
#    print("Enter the sub category: ")
#    sub_category = "Tourist visa"
#    #sub_category = input()

    logging.info("Processing countries: ")
    for key in centres:
        logging.info("  {}, URL: {}".format(key, centres[key][0]))
        for r in centres[key][1]:
            logging.info("    Centre: {}, Category: {}, Sub-Category: {}".format(r[0],r[1],r[2]))
        logging.info("")

    return centres

def _read_command_line_args():
    if len(sys.argv) != 4:
        return _input()
    return sys.argv[1], sys.argv[2], sys.argv[3]


if __name__ == "__main__":
    count = 1
    fileConfig('config/logging.ini')
    logging = logging.getLogger(__name__);

    _vfs_client = _VfsClient()

    def handler(signum, frame):
        logging.info("Ctrl-c was pressed. Closing browser")
        try:
            _vfs_client.close()
            logging.info("Browser closed")
        except Exception as e:
            logging.info("Couldn't close the browser")

        sys.exit(0)

    signal.signal(signal.SIGINT, handler)

    _config_reader = _ConfigReader()
    _interval = _config_reader.read_prop("DEFAULT", "interval")
    logging.debug("Interval: {}".format(_interval))

    centres = _read_command_line_args()
    #visa_centre, category, sub_category = _read_command_line_args()

    logging.info("Starting VFS Appointment Bot")
    while True:
        for country in centres:
            logging.info("Running, country {}, iteration#{}".format(country,count))
            try:
                _vfs_client.check_slot(country,centres[country][0],centres[country][1])
                logging.debug("Sleeping for {} seconds".format(_interval))
                countdown(int(_interval))
            except Exception as e:
                logging.info(e.args[0] + ". Please check the logs for more details")
                logging.debug(e, exc_info=True, stack_info=True)
                countdown(int(_interval))
                pass
            print("\n")
            count += 1
