Moonton Safe Checker (APK) - Project Skeleton
---------------------------------------------
This Android app validates combo list file format locally (email:password per line).
It DOES NOT perform any login, checking, or network requests to any service.
Designed as a safe template you can build with Buildozer on Linux.

How to build (on Linux machine with Buildozer):
1. Install dependencies:
   sudo apt update && sudo apt install -y build-essential git python3-pip python3-venv        libssl-dev libffi-dev libjpeg-dev zlib1g-dev
   pip install --user buildozer
2. Initialize Buildozer inside project folder and build:
   cd MoontonChecker_SafeApp
   buildozer android debug
3. The generated APK will be in bin/ after build.

How to use on Android (without building):
1. Place your combo file at /sdcard/Download/combo.txt with format email:password per line
2. Optionally place proxy list at /sdcard/Download/proxy.txt (not used for network in this safe app)
3. Install the generated APK, open app, press 'Load combo.txt' then 'Validate' then 'Save results'

Security & Ethics:
- This app intentionally avoids any network calls or account checking to prevent misuse.
- Use it only for formatting and local data management.