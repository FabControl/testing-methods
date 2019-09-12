#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/fc-testing-methods/")

from app import app as application
application.secret_key = 'NZvzwzpqb%AKsnqtF8o*'
