import tkinter as tk
from tkinter import filedialog, messagebox
import json
import datetime
import requests
import base64
import os
import sys
import time
import threading
import ctypes

# -------- UTILITAIRE POUR CHEMIN VERS ICÔNE (compatible PyInstaller) -------- #
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    full_path = os.path.join(base_path, relative_path)
    if not os.path.exists(full_path):
        print(f"⚠️ Attention : Le fichier {full_path} n'existe pas.")
    return full_path

# -------- FORCER ICÔNE DANS LA BARRE DES TÂCHES -------- #
def forcer_actualisation_icone(window, delai=0.5):
    icon_path = resource_path(r"C:\Users\Utilisateur\Documents\Logo_Umbro.ico")
    deja_applique = [False]

    def _forcer():
        while not deja_applique[0]:
            try:
                window.withdraw()
                time.sleep(0.1)
                window.iconbitmap(icon_path)
                window.deiconify()
                deja_applique[0] = True
                print("✅ Icône appliquée avec succès.")
            except Exception as e:
                print(f"Erreur lors de l'application de l'icône -> {e}")
                time.sleep(delai)

    threading.Thread(target=_forcer, daemon=True).start()

# -------- DONNÉES -------- #
monnaie = [1, 2, 5, 10, 20, 50, 100]
historique = []

# -------- ALGORITHME GLOUTON -------- #
def glouton(a_rendre, dispo):
    tab = []
    dispo = sorted([m for m, var in dispo.items() if var.get() == 1], reverse=True)
    i = 0
    while a_rendre > 0 and i < len(dispo):
        if a_rendre >= dispo[i]:
            tab.append(dispo[i])
            a_rendre -= dispo[i]
        else:
            i += 1
    if a_rendre != 0:
        return ["Impossible"]
    return tab

# -------- ACTIONS -------- #
def calculer():
    try:
        montant = int(entry.get())
        result = glouton(montant, check_vars)
        rendu_str = f"Montant : {montant} -> Rendu : {result}\n"
        output_text.insert(tk.END, rendu_str)
        output_text.see(tk.END)
        historique.append({
            "timestamp": datetime.datetime.now().isoformat(),
            "montant": montant,
            "resultat": result
        })
    except ValueError:
        output_text.insert(tk.END, "❌ Erreur : Entrez un nombre entier.\n")
        output_text.see(tk.END)
    except Exception as e:
        output_text.insert(tk.END, f"❌ Erreur inattendue : {e}\n")
        output_text.see(tk.END)

def reset():
    try:
        entry.delete(0, tk.END)
        output_text.delete(1.0, tk.END)
        for var in check_vars.values():
            var.set(1)
        historique.clear()
        messagebox.showinfo("Réinitialisé", "Champs et historique réinitialisés.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors du reset : {e}")

def sauvegarder():
    try:
        if not historique:
            messagebox.showinfo("Sauvegarde", "Aucune donnée à sauvegarder.")
            return

        filepath = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("Fichiers JSON", "*.json")],
            title="Enregistrer l'historique"
        )
        if filepath:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(historique, f, indent=4)
            messagebox.showinfo("Succès", f"Données enregistrées dans {filepath}")
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde : {e}")

def upload_to_github():
    try:
        token = token_entry.get().strip()
        repo = repo_entry.get().strip()
        nom_fichier = fichier_entry.get().strip()

        if not all([token, repo, nom_fichier]):
            messagebox.showerror("Erreur", "Tous les champs GitHub doivent être remplis.")
            return

        if not historique:
            messagebox.showinfo("Info", "Aucune donnée à envoyer.")
            return

        json_data = json.dumps(historique, indent=4)
        b64_data = base64.b64encode(json_data.encode("utf-8")).decode("utf-8")

        url = f"https://api.github.com/repos/{repo}/contents/{nom_fichier}"
        headers = {"Authorization": f"token {token}"}
        data = {
            "message": "Upload automatique du rendu de monnaie",
            "content": b64_data,
            "branch": "main"
        }

        response = requests.put(url, headers=headers, json=data)
        if response.status_code in [200, 201]:
            messagebox.showinfo("Succès", "✅ Fichier publié sur GitHub.")
        else:
            messagebox.showerror("Erreur", f"Erreur GitHub : {response.status_code}\n{response.text}")
    except Exception as e:
        messagebox.showerror("Erreur", f"Échec de l'envoi GitHub : {e}")

def telecharger_fichier():
    url = "https://raw.githubusercontent.com/thesevendeadlysinsds/thesevendeadlysinsds.github.io/main/download-python-file.com/app/exe/RenduMonnaie.py"  # ← À adapter
    try:
        r = requests.get(url)
        r.raise_for_status()
        chemin = filedialog.asksaveasfilename(
            defaultextension=".py",
            filetypes=[("Fichiers Python", "*.py")],
            title="Enregistrer tifsec.py"
        )
        if chemin:
            with open(chemin, "w", encoding="utf-8") as f:
                f.write(r.text)
            messagebox.showinfo("Succès", f"✅ Fichier enregistré dans {chemin}")
    except Exception as e:
        messagebox.showerror("Erreur", f"❌ Téléchargement échoué : {e}")

# -------- INTERFACE -------- #
def lancer_app():
    try:
        global entry, output_text, check_vars
        global token_entry, repo_entry, fichier_entry

        root = tk.Tk()
        root.title("💰 Rendu de Monnaie")

        # Style police agrandie
        font_style = ("*font", 16)

        # Windows : set AppUserModelID
        if sys.platform == "win32":
            try:
                app_id = "Umbro.RenduMonnaie.2025"
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
            except Exception as e:
                print(f"Erreur AppUserModelID : {e}")

        # Appliquer l'icône
        try:
            icon_path = resource_path("Library/Logo_Umbro.ico")
            root.iconbitmap(icon_path)
            print(f"Icône appliquée : {icon_path}")
        except Exception as e:
            print(f"Erreur lors de l'application de l'icône : {e}")

        forcer_actualisation_icone(root)

        # Maximiser la fenêtre
        if sys.platform == "win32":
            root.state('zoomed')
        else:
            root.geometry("1200x900")

        # Widgets avec police agrandie
        tk.Label(root, text="Montant à rendre :", font=font_style).pack(pady=5)
        entry = tk.Entry(root, font=font_style)
        entry.pack(pady=5, fill='x', padx=20)

        tk.Label(root, text="Pièces disponibles :", font=font_style).pack(pady=5)
        check_vars = {}
        for m in monnaie:
            var = tk.IntVar(value=1)
            chk = tk.Checkbutton(root, text=f"{m}", variable=var, font=font_style)
            chk.pack(anchor='w', padx=40)
            check_vars[m] = var

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Calculer", font=font_style, command=calculer).pack(side="left", padx=15)
        tk.Button(btn_frame, text="Reset", font=font_style, command=reset).pack(side="left", padx=15)
        tk.Button(btn_frame, text="Sauvegarder en JSON", font=font_style, command=sauvegarder).pack(side="left", padx=15)
        tk.Button(root, text="⬇️ Télécharger tifsec.py", font=font_style, command=telecharger_fichier).pack(pady=5)

        tk.Label(root, text="Console :", font=font_style).pack(pady=5)
        output_text = tk.Text(root, height=12, font=font_style)
        output_text.pack(padx=20, pady=5, fill='both', expand=True)

        tk.Label(root, text="--- Publier sur GitHub (optionnel) ---", font=font_style).pack(pady=10)
        github_frame = tk.Frame(root)
        github_frame.pack(padx=20, pady=5, fill='x')

        tk.Label(github_frame, text="Token GitHub :", font=font_style).grid(row=0, column=0, sticky="e", pady=5)
        token_entry = tk.Entry(github_frame, show="*", font=font_style, width=40)
        token_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(github_frame, text="Repo (ex: user/repo) :", font=font_style).grid(row=1, column=0, sticky="e", pady=5)
        repo_entry = tk.Entry(github_frame, font=font_style, width=40)
        repo_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(github_frame, text="Nom du fichier (ex: rendu.json) :", font=font_style).grid(row=2, column=0, sticky="e", pady=5)
        fichier_entry = tk.Entry(github_frame, font=font_style, width=40)
        fichier_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Button(root, text="Publier sur GitHub", font=font_style, command=upload_to_github).pack(pady=20)

        root.mainloop()

    except Exception as e:
        with open("erreur_log.txt", "w", encoding="utf-8") as f:
            f.write(str(e))
        messagebox.showerror("Erreur critique", f"Erreur critique : {e}")

# -------- POINT D'ENTRÉE -------- #
if __name__ == "__main__":
    try:
        lancer_app()
    except Exception as e:
        import traceback
        erreur = traceback.format_exc()
        with open("erreur_log.txt", "w", encoding="utf-8") as f:
            f.write(erreur)
        tk.Tk().withdraw()
        messagebox.showerror("Erreur critique", f"Une erreur est survenue :\n\n{e}")