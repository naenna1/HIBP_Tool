import tkinter as tk
from tkinter import scrolledtext
from ui_format import (
    format_breach_list,
    format_paste_list,
    format_breach_summary,
    format_warning,
    format_info,
)

def show_output(text):
    output_box.delete(1.0, tk.END)
    output_box.insert(tk.END, text)

def test_gui():
    breach = {
        "Name": "Adobe Leak",
        "Domain": "adobe.com",
        "BreachDate": "2019-10-04",
        "Description": "Passwort-Leak durch Sicherheitslücke."
    }

    summary = {
        "total_breaches": 5,
        "risk_score": 78
    }

    text = format_breach_list([breach])
    text += "\n\n" + format_breach_summary(summary)

    show_output(text)

# GUI Fenster
window = tk.Tk()
window.title("Datenleck GUI Tester")
window.geometry("700x600")

# Knopf zum Testen
button = tk.Button(window, text="Test anzeigen", command=test_gui)
button.pack(pady=10)

# Textbox für Ausgabe
output_box = scrolledtext.ScrolledText(window, width=80, height=30)
output_box.pack()

window.mainloop()