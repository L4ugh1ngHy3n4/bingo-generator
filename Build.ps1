$ErrorActionPreference = 'Stop'
Set-Location $PSScriptRoot
$version = '0.15.1'
$url = "https://github.com/typst/typst/releases/download/v$version/typst-x86_64-pc-windows-msvc.zip"
$work = Join-Path $PSScriptRoot 'build-deps'
New-Item -ItemType Directory -Force $work | Out-Null
Invoke-WebRequest -Uri $url -OutFile "$work/typst.zip"
Expand-Archive "$work/typst.zip" "$work/typst" -Force
$compiler = Get-ChildItem "$work/typst" -Filter typst.exe -Recurse | Select-Object -First 1
if (-not $compiler) { throw 'Typst executable not found' }
Copy-Item $compiler.FullName "$work/typst.exe" -Force
py -3 -m venv "$work/venv"
if ($LASTEXITCODE -ne 0) { throw 'Python venv failed' }
$python = "$work/venv/Scripts/python.exe"
& $python -m pip install 'pyinstaller==6.22.0'
if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed' }
& $python -m PyInstaller --noconfirm --clean --onefile --windowed --name Bingo-Kartengenerator --add-data 'bingo.typ:.' --add-binary "$work/typst.exe:." gui.py
if ($LASTEXITCODE -ne 0) { throw 'Build failed' }
Write-Host 'Fertig: dist/Bingo-Kartengenerator.exe'
