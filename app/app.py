#!/usr/bin/env python
import os
from app import app
port = int(os.environ.get("PORT", 4000))
app.run(debug = True, host='0.0.0.0', port=port)
