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

# (list) Requirements
requirements = python3,kivy==2.3.0,pillow,urllib3,charset-normalizer,requests

# (str) Supported orientation
orientation = portrait

# (bool) Fullscreen mode
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API & Minimum API
android.api = 33
android.minapi = 21

# (str) Android NDK version
android.ndk = 25b

# (bool) Auto-accept SDK license
android.accept_sdk_license = True

# (str) Target Architectures
android.archs = arm64-v8a

# (bool) Enable AndroidX
android.enable_androidx = True

[buildozer]
log_level = 2
warn_on_root = 1
