# -*- coding: utf-8 -*-
import logging
import sys

logger = logging.getLogger(__name__)

from .base import *


try:
    from .local import *
except ImportError:
    logger.info('No local settings')

if 'test' in sys.argv:
    from .test import *

TEMPLATE_DEBUG = DEBUG
THUMBNAIL_DEBUG = DEBUG
