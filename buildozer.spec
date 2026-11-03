[app]
title = MUTHU
package.name = muthu
package.domain = ao.muthu
source.dir = .
source.include_exts = py,kv,png,jpg,jpeg,ttf,txt,json
source.exclude_dirs = .git,.venv,.kivy,.buildozer,bin,tests,__pycache__
version = 1.0.0
requirements = python3,kivy,kivymd,python-dotenv
orientation = portrait
fullscreen = 0
android.api = 35
android.minapi = 24
android.ndk_api = 24
android.ndk = 28c
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
