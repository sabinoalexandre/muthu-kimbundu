[app]
title = MUTHU
package.name = muthu
package.domain = org.muthu
source.dir = .
source.include_exts = py,kv,json,png,jpg,jpeg,atlas,ttf
source.exclude_dirs = tests,bin,.buildozer,.pytest_cache
version = 1.0.0
requirements = python3,kivy==2.3.1,kivymd,python-dotenv
orientation = portrait
fullscreen = 0
android.minapi = 23
android.archs = arm64-v8a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
