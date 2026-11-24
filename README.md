Bingo-Kartengenerator – Windows und Linux (x86-64)

AI SLOP

Für Anwender:
Windows: Bingo-Kartengenerator.exe doppelklicken.
Linux: Bingo-Kartengenerator.AppImage in den Dateieigenschaften als
 ausführbar markieren, dann doppelklicken. Alternativ die mitgelieferte
 native Linux-Datei Bingo-Kartengenerator ausführbar machen und starten.
 Die AppImage kann FUSE benötigen; die native Datei benötigt kein FUSE.
Anzahl und PDF-Speicherort auswählen, Generieren! anklicken.
Keine separate Python- oder Typst-Installation notwendig.
Linux benötigt eine grafische Desktop-Umgebung und kompatible Systembibliotheken.

Für Entwickler:
Windows: Python 3 installieren, Build.bat starten.
Linux (empfohlen Ubuntu 22.04):
 sudo apt install python3 python3-venv python3-tk curl binutils libfuse2
 bash Build.sh
Die Ergebnisse liegen unter dist/.
Alternativ alle Dateien inklusive .github in ein GitHub-Repository kopieren,
 unter Actions den Workflow Build portable applications manuell starten und
 die beiden Artefakte herunterladen.
Build benötigt Internetzugang. Die Anwendungen benötigen keinen Internetzugang.
Die Windows-Datei ist nicht signiert. Die Linux-Datei ist für glibc-basierte
 x86-64-Distributionen ab der Build-Systemversion vorgesehen; keine Garantie
 für alle Distributionen oder ARM-Geräte.
