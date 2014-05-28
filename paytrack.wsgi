import sys

activate_this = '/var/www/dev/paytrack/venv/paytrack-v1/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
sys.path.insert(0, '/var/www/dev/payTrack/paytrack')

from paytrack import app as application
