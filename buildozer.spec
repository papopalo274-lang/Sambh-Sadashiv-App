[app]
title = Sambh Sadashiv
package.name = sambhsadashiv
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf

requirements = python3,kivy,pyjnius,sqlite3,requests,urllib3

version = 0.1
icon.filename = %(source.dir)s/icon.png

# App Orientation: 'portrait' सेट करने से ऐप डिफ़ॉल्ट पोर्ट्रेट में खुलेगी
orientation = portrait

# Permissions for File Storage & Gallery Read
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, READ_MEDIA_IMAGES

android.api = 34
android.minapi = 24
android.accept_sdk_license = True
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
