#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
mkdir -p build-deps/AppDir
v=0.15.1
curl -fL --retry 3 "https://github.com/typst/typst/releases/download/v$v/typst-x86_64-unknown-linux-musl.tar.xz" -o build-deps/typst.tar.xz
tar -xJf build-deps/typst.tar.xz -C build-deps
python3 -m venv build-deps/venv
p=build-deps/venv/bin/python
"$p" -m pip install 'pyinstaller==6.22.0'
"$p" -m PyInstaller --noconfirm --clean --onefile --name Bingo-Kartengenerator --add-data 'bingo.typ:.' --add-binary 'build-deps/typst-x86_64-unknown-linux-musl/typst:.' gui.py
cp dist/Bingo-Kartengenerator build-deps/AppDir/AppRun
cat > build-deps/AppDir/bingo.desktop <<'DESKTOP'
[Desktop Entry]
Name=Bingo-Kartengenerator
Exec=Bingo-Kartengenerator
Icon=bingo
Type=Application
Categories=Utility;
DESKTOP
cat > build-deps/AppDir/bingo.svg <<'SVG'
<svg xmlns="http://www.w3.org/2000/svg" width="128" height="128"><rect width="128" height="128" rx="16" fill="#245a94"/><text x="64" y="86" font-size="72" text-anchor="middle" font-family="sans-serif" font-weight="bold" fill="white">B</text></svg>
SVG
curl -fL --retry 3 https://github.com/AppImage/appimagetool/releases/download/continuous/appimagetool-x86_64.AppImage -o build-deps/appimagetool
chmod +x build-deps/appimagetool
ARCH=x86_64 APPIMAGE_EXTRACT_AND_RUN=1 build-deps/appimagetool build-deps/AppDir dist/Bingo-Kartengenerator.AppImage
