#!/usr/bin/env python
import os
from app import app
from werkzeug.contrib.cache import MemcachedCache


port = int(os.environ.get("PORT", 4000))
app.run(debug = True, host='0.0.0.0', port=port)
cache = MemcachedCache(['0.0.0.0:11211'])
