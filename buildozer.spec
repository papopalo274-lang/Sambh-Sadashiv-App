[app]

# (str) Title of your application
title = Sambh Sadashiv

# (str) Application version
version = 1.0.0

# (str) Package name
package.name = sambhsadashiv

# (str) Package domain (needed for android/ios packaging)
package.domain = org.devotional

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (include Hindi font & images)
source.include_exts = py,png,jpg,jpeg,ttf,kv

# (list) Application requirements
# Unpinned python3 auto-matches the runner's hostpython version
requirements = python3,kivy==2.3.0,pillow,urllib3==2.1.0,charset-normalizer==3.3.2,requests==2.31.0

# (str) Supported orientation (landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

# (int) Target Android API
android.api = 34

# (int) Minimum API your APK will support
android.minapi = 24

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Accept SDK license automatically
android.accept_sdk_license = True

# (str) The Android arch to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) Enable AndroidX support
android.enable_androidx = True

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1
