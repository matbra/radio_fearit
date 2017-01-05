import sys
sys.path.insert(0, '/var/www/vhosts/lvps83-169-2-231.dedicated.hosteurope.de/src/radio_fearit/radio_fearit')

activate_this = '/var/www/vhosts/lvps83-169-2-231.dedicated.hosteurope.de/src/radio_fearit/rfi/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

from app import app as application