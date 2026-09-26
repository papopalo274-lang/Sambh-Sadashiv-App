[app]

# (str) Title of your application
title = Sambh Sadashiv

# (str) Application version
version = 1.0.0

# (str) Package name
package.name = sambhsadashiv

# (str) Package domain
package.domain = org.devotional

# (str) Source code directory
source.dir = .

# (list) Source files extensions
source.include_exts = py,png,jpg,jpeg,ttf,kv

# (list) Requirements: Fix versions to work cleanly with Python 3.10
requirements = python3,kivy==2.3.0,pillow,urllib3,charset-normalizer,requests

# (str) Supported orientation
orientation = portrait

# (bool) Fullscreen mode
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

# (int) Target Android API & Minimum API
android.api = 33
android.minapi = 21

# (str) Android NDK version
android.ndk = 25b

# (bool) Auto-accept SDK license
android.accept_sdk_license = True

# (str) Target Architectures (arm64-v8a build setup)
android.archs = arm64-v8a

# (bool) Enable AndroidX
android.enable_androidx = True

[buildozer]
log_level = 2
warn_on_root = 1
