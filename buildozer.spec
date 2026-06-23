[app]
title = HoloLock Launcher
package.name = hololock
package.domain = org.cybercore
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3, kivy==2.3.0, pillow, pyjnius
orientation = portrait
fullscreen = 1
android.api = 31
android.minapi = 21
android.ndk_api = 21
android.archs = arm64-v8a
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 0
