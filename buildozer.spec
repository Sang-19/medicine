[app]
title = Medicine Tracker
package.name = medicinetracker
package.domain = org.medicinetracker
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 0.1
requirements = python3,kivy==2.2.1,kivymd==1.1.1,pillow,python-dateutil
orientation = portrait
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 30
android.minapi = 21
android.sdk = 30
android.ndk = 23b
android.sdk_path = ~/.buildozer/android/platform/android-sdk
android.build_tools = 30.0.3
android.archs = armeabi-v7a
android.allow_backup = True
android.enable_androidx = True

[buildozer]
log_level = 2
warn_on_root = 0
