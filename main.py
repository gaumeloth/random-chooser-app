#!/usr/bin/env python3

import json
import os
import random
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

FILE_NAME = 'sets.json'

class RandomChooserApp:
    def __init__(self, master):
        self.master = master
        master.title("Random Chooser App")
        master.geometry("600x450")

        # Carichiamo i set e il tema dal file JSON
        self.sets_data = {}
        self.current_set_name = None
        self.load_sets()

        # Creiamo lo Style e i due temi (chiaro e scuro) PRIMA di creare i widget
        self.style = ttk.Style(master)
        self.create_light_theme()
        self.create_dark_theme()

        # Decidiamo quale tema usare inizialmente (letto da sets_data, default: 'my_light')
        self.current_theme = self.sets_data.get("last_theme", "my_light")

        # FRAME per selezione e creazione set
        self.frame_sets = ttk.Frame(master, padding=10)
        self.frame_sets.pack(fill=tk.X)

        ttk.Label(self.frame_sets, text="Seleziona il set:").pack(side=tk.LEFT, padx=5)

        self.combo_set_names = ttk.Combobox(self.frame_sets, state="readonly")
        self.combo_set_names.pack(side=tk.LEFT)
        self.combo_set_names.bind("<<ComboboxSelected>>", self.on_set_selected)

        btn_new_set = ttk.Button(self.frame_sets, text="Crea nuovo set", command=self.create_new_set)
        btn_new_set.pack(side=tk.LEFT, padx=5)

        btn_delete_set = ttk.Button(self.frame_sets, text="Elimina set", command=self.delete_set)
        btn_delete_set.pack(side=tk.LEFT, padx=5)

        # Aggiungiamo un Checkbutton per il tema scuro, a fianco al pulsante "Elimina set"
        self.dark_var = tk.BooleanVar()
        # Impostiamo il valore iniziale della spunta in base a self.current_theme
        self.dark_var.set(True if self.current_theme == "my_dark" else False)
        self.chbtn_dark = ttk.Checkbutton(
            self.frame_sets,
            text="Tema scuro",
            variable=self.dark_var,
            command=self.on_dark_toggled
        )
        # Lo posizioniamo a destra nella stessa riga
        self.chbtn_dark.pack(side=tk.RIGHT, padx=5)

        # FRAME principale con listbox e pulsanti
        self.frame_main = ttk.Frame(master, padding=10)
        self.frame_main.pack(fill=tk.BOTH, expand=True)

        # Listbox (widget classico di tk) per le opzioni
        self.listbox_options = tk.Listbox(self.frame_main, height=10)
        self.listbox_options.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar
        self.scrollbar_options = ttk.Scrollbar(self.frame_main, orient=tk.VERTICAL, command=self.listbox_options.yview)
        self.scrollbar_options.pack(side=tk.LEFT, fill=tk.Y)
        self.listbox_options.config(yscrollcommand=self.scrollbar_options.set)

        # FRAME laterale per i pulsanti
        self.frame_buttons = ttk.Frame(self.frame_main, padding=5)
        self.frame_buttons.pack(side=tk.LEFT, fill=tk.Y)

        ttk.Label(self.frame_buttons, text="Opzione:").pack(anchor="w")
        self.entry_option = ttk.Entry(self.frame_buttons)
        self.entry_option.pack(anchor="w", fill=tk.X, pady=5)

        btn_add_option = ttk.Button(self.frame_buttons, text="Aggiungi opzione", command=self.add_option)
        btn_add_option.pack(anchor="w", fill=tk.X, pady=5)

        btn_remove_option = ttk.Button(self.frame_buttons, text="Rimuovi selezionata", command=self.remove_option)
        btn_remove_option.pack(anchor="w", fill=tk.X, pady=5)

        btn_random_choice = ttk.Button(self.frame_buttons, text="Estrai casuale", command=self.choose_random)
        btn_random_choice.pack(anchor="w", fill=tk.X, pady=5)

        # Ora che i widget sono creati, possiamo applicare il tema
        self.set_theme(self.current_theme)

        # Popoliamo la combobox dei set
        self.refresh_combo()

    def on_dark_toggled(self):
        """Callback quando si clicca sul checkbutton Tema scuro."""
        if self.dark_var.get():
            self.set_theme("my_dark")
        else:
            self.set_theme("my_light")

    def load_sets(self):
        """Carica il dizionario set->opzioni e l'ultimo tema da FILE_NAME, se esiste."""
        if os.path.exists(FILE_NAME):
            try:
                with open(FILE_NAME, 'r', encoding='utf-8') as f:
                    self.sets_data = json.load(f)
            except json.JSONDecodeError:
                # File corrotto o vuoto
                self.sets_data = {}
        else:
            self.sets_data = {}

    def save_sets(self):
        """Salva il dizionario set->opzioni e l'ultimo tema su FILE_NAME."""
        with open(FILE_NAME, 'w', encoding='utf-8') as f:
            json.dump(self.sets_data, f, indent=4, ensure_ascii=False)

    def create_light_theme(self):
        """Crea un tema chiaro personalizzato."""
        self.style.theme_create(
            "my_light", parent="clam",
            settings={
                "TFrame": {
                    "configure": {
                        "background": "#efefef"
                    }
                },
                "TLabel": {
                    "configure": {
                        "background": "#efefef",
                        "foreground": "#000000"
                    }
                },
                "TButton": {
                    "configure": {
                        "background": "#ddd",
                        "foreground": "#000000",
                        "padding": 6,
                        "relief": "flat"
                    },
                    "map": {
                        "background": [
                            ("active", "#ccc"),
                            ("pressed", "#ccc")
                        ],
                        "foreground": [
                            ("disabled", "#777777")
                        ]
                    }
                },
                "TCombobox": {
                    "configure": {
                        "background": "#ffffff",
                        "foreground": "#000000",
                        "fieldbackground": "#ffffff"
                    }
                },
                "TEntry": {
                    "configure": {
                        "foreground": "#000000",
                        "fieldbackground": "#ffffff",
                        "background": "#ffffff"
                    }
                },
                "TScrollbar": {
                    "configure": {
                        "troughcolor": "#f0f0f0",
                        "background": "#d0d0d0"
                    }
                }
            }
        )

    def create_dark_theme(self):
        """Crea un tema scuro personalizzato."""
        self.style.theme_create(
            "my_dark", parent="clam",
            settings={
                "TFrame": {
                    "configure": {
                        "background": "#2b2b2b"
                    }
                },
                "TLabel": {
                    "configure": {
                        "background": "#2b2b2b",
                        "foreground": "#ffffff"
                    }
                },
                "TButton": {
                    "configure": {
                        "background": "#3c3f41",
                        "foreground": "#ffffff",
                        "padding": 6,
                        "relief": "flat"
                    },
                    "map": {
                        "background": [
                            ("active", "#505354"),
                            ("pressed", "#505354")
                        ],
                        "foreground": [
                            ("disabled", "#777777")
                        ]
                    }
                },
                "TCombobox": {
                    "configure": {
                        "background": "#3c3f41",
                        "foreground": "#ffffff",
                        "fieldbackground": "#3c3f41"
                    }
                },
                "TEntry": {
                    "configure": {
                        "foreground": "#ffffff",
                        "fieldbackground": "#3c3f41",
                        "background": "#3c3f41"
                    }
                },
                "TScrollbar": {
                    "configure": {
                        "troughcolor": "#3c3f41",
                        "background": "#4a4e4f"
                    }
                }
            }
        )

    def set_theme(self, theme_name):
        """
        Applica il tema specificato (my_light o my_dark) e imposta
        anche il colore di sfondo della finestra radice in modo coerente.
        """
        self.style.theme_use(theme_name)
        if theme_name == "my_dark":
            self.master.configure(bg="#2b2b2b")
            # Modifichiamo anche la Listbox manualmente
            self.listbox_options.configure(
                bg="#3c3f41", 
                fg="#ffffff", 
                selectbackground="#505354"
            )
        else:
            # Tema chiaro
            self.master.configure(bg="#efefef")
            self.listbox_options.configure(
                bg="#ffffff", 
                fg="#000000", 
                selectbackground="#c0c0c0"
            )
        # Salviamo il tema scelto in sets_data
        self.sets_data["last_theme"] = theme_name
        self.save_sets()

    def refresh_combo(self):
        """Aggiorna la combobox dei set disponibili."""
        set_names = sorted(list(self.sets_data.keys()))
        # Rimuoviamo eventuale chiave 'last_theme' dal set se presente
        if "last_theme" in set_names:
            set_names.remove("last_theme")

        self.combo_set_names['values'] = set_names
        if set_names:
            if self.current_set_name and self.current_set_name in set_names:
                self.combo_set_names.set(self.current_set_name)
            else:
                self.combo_set_names.current(0)
                self.current_set_name = self.combo_set_names.get()
            self.load_listbox_options()
        else:
            # Nessun set disponibile
            self.combo_set_names.set('')
            self.current_set_name = None
            self.listbox_options.delete(0, tk.END)

    def on_set_selected(self, event=None):
        """Callback quando l'utente seleziona un set dalla combobox."""
        self.current_set_name = self.combo_set_names.get()
        self.load_listbox_options()

    def load_listbox_options(self):
        """Carica le opzioni del set selezionato nella listbox."""
        self.listbox_options.delete(0, tk.END)
        if self.current_set_name:
            options = self.sets_data.get(self.current_set_name, [])
            # Evitiamo di caricare eventuali chiavi extra (es. last_theme)
            if isinstance(options, list):
                for opt in options:
                    self.listbox_options.insert(tk.END, opt)

    def create_new_set(self):
        """Crea un nuovo set, chiedendo all'utente il nome con un dialogo."""
        new_set_name = simpledialog.askstring("Nuovo Set", "Inserisci il nome del nuovo set:")
        if new_set_name:
            new_set_name = new_set_name.strip()
            if not new_set_name:
                messagebox.showerror("Errore", "Nome del set vuoto.")
                return
            if new_set_name in self.sets_data:
                messagebox.showerror("Errore", f"Il set '{new_set_name}' esiste già.")
                return
            self.sets_data[new_set_name] = []
            self.save_sets()
            self.current_set_name = new_set_name
            self.refresh_combo()

    def delete_set(self):
        """Elimina il set selezionato (chiede conferma)."""
        if not self.current_set_name:
            return
        answer = messagebox.askyesno("Elimina Set", f"Sei sicuro di voler eliminare il set '{self.current_set_name}'?")
        if answer:
            del self.sets_data[self.current_set_name]
            self.save_sets()
            self.current_set_name = None
            self.refresh_combo()

    def add_option(self):
        """Aggiunge l'opzione digitata all'elenco del set corrente."""
        if not self.current_set_name:
            messagebox.showinfo("Nessun Set Selezionato", "Crea o seleziona un set prima di aggiungere opzioni.")
            return
        new_option = self.entry_option.get().strip()
        if not new_option:
            messagebox.showwarning("Valore Vuoto", "Inserisci un testo per l'opzione.")
            return
        if new_option in self.sets_data[self.current_set_name]:
            messagebox.showinfo("Duplicato", f"L'opzione '{new_option}' è già presente nel set.")
            return
        self.sets_data[self.current_set_name].append(new_option)
        self.save_sets()
        self.entry_option.delete(0, tk.END)
        self.load_listbox_options()

    def remove_option(self):
        """Rimuove l'opzione selezionata nella listbox dal set corrente."""
        if not self.current_set_name:
            return
        selection = self.listbox_options.curselection()
        if not selection:
            return
        index = selection[0]
        to_remove = self.listbox_options.get(index)
        self.sets_data[self.current_set_name].remove(to_remove)
        self.save_sets()
        self.load_listbox_options()

    def choose_random(self):
        """Estrae un'opzione casuale dal set corrente."""
        if not self.current_set_name:
            messagebox.showinfo("Nessun Set Selezionato", "Nessun set disponibile.")
            return
        options = self.sets_data.get(self.current_set_name, [])
        if not options:
            messagebox.showinfo("Set Vuoto", "Il set selezionato non contiene opzioni.")
            return
        chosen = random.choice(options)
        messagebox.showinfo("Opzione Estratta", f"{chosen}")


def main():
    root = tk.Tk()
    app = RandomChooserApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
