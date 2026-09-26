[app]

# (str) Title of your application
title = Sambh Sadashiv

# (str) Package name
package.name = sambhsadashiv

# (str) Package domain (needed for android packaging)
package.domain = org.test

# (str) Source code where the main.py is located
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas

# (list) Application requirements
requirements = python3,kivy,pyjnius,sqlite3

# (str) Application version
version = 0.1

# (str) Icon of the application (आपकी फोटो का नाम icon.png होना चाहिए)
icon.filename = %(source.dir)s/icon.png

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API
android.api = 33

# (int) Minimum API supported
android.minapi = 21

# (bool) Accept SDK license automatically
android.accept_sdk_license = True

# (str) The Android arch to build for
android.archs = arm64-v8a

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1
