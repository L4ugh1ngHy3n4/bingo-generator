#!/usr/bin/env python3
"""German-language desktop interface for the bingo generator."""
from pathlib import Path
import queue
import os
import webbrowser
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from generate import generate_pdf


def main():
    root = tk.Tk()
    root.title('Bingo-Kartengenerator')
    root.minsize(660, 380)
    root.option_add('*Font', 'TkDefaultFont')
    import tkinter.font as font
    for name in ('TkDefaultFont', 'TkTextFont', 'TkHeadingFont'):
        font.nametofont(name).configure(size=14)
    style = ttk.Style(root)
    style.configure('Generate.TButton', font=(font.nametofont('TkDefaultFont').actual('family'), 16, 'bold'), padding=12)
    frame = ttk.Frame(root, padding=24)
    frame.pack(fill='both', expand=True)
    frame.columnconfigure(0, weight=1)
    count = tk.StringVar(value='10')
    output = tk.StringVar(value=str(Path.home() / 'bingo.pdf'))
    auto_open = tk.BooleanVar(value=True)
    status = tk.StringVar(value='Bereit.')
    results = queue.Queue()

    ttk.Label(frame, text='Anzahl der Bingo-Karten:').grid(row=0, column=0, columnspan=2, sticky='w')
    count_entry = ttk.Entry(frame, textvariable=count, width=12)
    count_entry.grid(row=1, column=0, sticky='w', pady=(6, 18))
    ttk.Label(frame, text='PDF speichern unter:').grid(row=2, column=0, columnspan=2, sticky='w')
    path_entry = ttk.Entry(frame, textvariable=output)
    path_entry.grid(row=3, column=0, sticky='ew', pady=(6, 18))

    def browse():
        current = Path(output.get() or 'bingo.pdf').expanduser()
        selected = filedialog.asksaveasfilename(parent=root, title='PDF speichern unter', initialdir=str(current.parent), initialfile=current.name, defaultextension='.pdf', filetypes=[('PDF-Dateien', '*.pdf')], confirmoverwrite=False)
        if selected:
            output.set(selected)

    browse_button = ttk.Button(frame, text='Durchsuchen …', command=browse)
    browse_button.grid(row=3, column=1, padx=(10, 0), pady=(6, 18))

    def busy(active):
        for widget in (count_entry, path_entry, browse_button, generate_button):
            widget.configure(state='disabled' if active else 'normal')

    def poll():
        try:
            success, result = results.get_nowait()
        except queue.Empty:
            root.after(100, poll)
            return
        busy(False)
        if success:
            status.set('PDF erfolgreich erstellt.')
            messagebox.showinfo('Fertig!', f'Die Bingo-Karten wurden gespeichert:\n{result}', parent=root)
            if auto_open.get():
                try:
                    if os.name == 'nt':
                        os.startfile(str(result))
                    else:
                        webbrowser.open(result.as_uri())
                except OSError as exc:
                    messagebox.showwarning('PDF öffnen', f'Die PDF wurde gespeichert, konnte aber nicht geöffnet werden:\n{exc}', parent=root)
        else:
            status.set('Fehler bei der Erstellung.')
            messagebox.showerror('Fehler', str(result), parent=root)

    def start():
        try:
            n = int(count.get())
            if n < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror('Ungültige Anzahl', 'Bitte eine positive ganze Zahl eingeben.', parent=root)
            return
        if not output.get().strip():
            messagebox.showerror('Ausgabedatei fehlt', 'Bitte einen Speicherort auswählen.', parent=root)
            return
        path = Path(output.get().strip()).expanduser()
        if path.suffix.lower() != '.pdf':
            path = path.with_name(path.name + '.pdf')
        if not path.parent.is_dir() or path.is_dir():
            messagebox.showerror('Ungültiger Speicherort', 'Bitte einen vorhandenen Ordner und einen Dateinamen auswählen.', parent=root)
            return
        if path.exists() and not messagebox.askyesno('Datei ersetzen?', f'Die Datei existiert bereits:\n{path}\n\nÜberschreiben?', parent=root):
            return
        output.set(str(path))
        busy(True)
        status.set(f'{n} Bingo-Karten werden erstellt …')

        def worker():
            try:
                results.put((True, generate_pdf(n, path)))
            except Exception as exc:
                results.put((False, exc))

        threading.Thread(target=worker, daemon=True).start()
        root.after(100, poll)

    generate_button = ttk.Button(frame, text='Generieren!', style='Generate.TButton', command=start)
    ttk.Checkbutton(frame, text='PDF nach dem Erstellen öffnen', variable=auto_open).grid(row=4, column=0, columnspan=2, sticky='w', pady=(0, 12))
    generate_button.grid(row=5, column=0, columnspan=2, sticky='ew')
    ttk.Label(frame, textvariable=status, wraplength=500).grid(row=6, column=0, columnspan=2, sticky='w', pady=(14, 0))
    ttk.Label(frame, text='DIN A4 · Großdruck · Eine Karte pro Seite').grid(row=7, column=0, columnspan=2, sticky='w', pady=(12, 0))
    def close():
        if generate_button.instate(['disabled']):
            messagebox.showinfo('Bitte warten', 'Die PDF-Erstellung läuft noch.', parent=root)
        else:
            root.destroy()
    root.protocol('WM_DELETE_WINDOW', close)
    count_entry.focus_set()
    root.mainloop()


if __name__ == '__main__':
    main()
