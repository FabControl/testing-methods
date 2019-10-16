#!/usr/bin/python
import sys
import logging
import os

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,os.path.dirname(os.path.realpath(__file__)))

from app import app as application
application.secret_key = 'NZvzwzpqb%AKsnqtF8o*'
