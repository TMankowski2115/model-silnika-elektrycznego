import math
import tkinter as okno
from PIL import ImageTk, Image
from tkinter import font
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def on_button_click(button):
    global napiecie
    global button_selected
    
    button_selected = button
    napiecie = wybor_funkcji(button_selected)
    update_window()

def wybor_funkcji(button):
    global os_czasu
    global x1 # i
    global x2 # w
    x1 = []
    x2 = []
    napiecie = []
    os_czasu = []
    R = float(wprowadz_rezystancje.get())
    L = float(wprowadz_indukcyjnosc.get())
    J = float(wprowadz_moment_bezwladnosci.get())
    B = float(wprowadz_wspolczynnik_tarcia_lepkiego.get())
    Ke = float(wprowadz_Ke.get())
    Km = float(wprowadz_Km.get())
    x=0
    while x < float(wprowadz_czas_trwania.get()) and x < float(wprowadz_czas_symulacji.get()):
        os_czasu.append(x)
        if button == "sinus":
            napiecie.append(sinus(x, float(wprowadz_okres.get()), float(wprowadz_napiecie.get())))
        elif button == "trojkat":
            napiecie.append(trojkat(x+float(wprowadz_okres.get())*1/4, float(wprowadz_okres.get()), float(wprowadz_napiecie.get())))
        elif button == "prostokat":
            napiecie.append(prostokat(x, float(wprowadz_okres.get()), float(wprowadz_napiecie.get())))
        x+=0.001
    j=0
    while j < float(wprowadz_czas_symulacji.get())-float(wprowadz_czas_trwania.get()):
        os_czasu.append(x)
        napiecie.append(0)
        x+=0.001
        j+=0.001
    i=0
    x1p = napiecie[i]/L
    x2p = 0
    x1.append(0 + x1p * 0.001)
    x2.append(0 + x2p * 0.001)
    for i in range(len(os_czasu)-1):
        x1p = -(R * x1[i])/L - (Ke * x2[i])/L + napiecie[i]/L
        x2p = (Km * x1[i])/J - (B * x2[i])/J
        x1.append(x1[i] + x1p * 0.001)
        x2.append(x2[i] + x2p * 0.001)
    
    return napiecie

def sinus(x, okres, amplituda):
    return amplituda * math.sin(2 * math.pi * x / okres)

def trojkat(x, okres, amplituda):
    temp = (x / okres) % 1
    if temp < 0.5:
        return 4 * amplituda * temp - amplituda
    else:
        return -4 * amplituda *temp + 3* amplituda
    
def prostokat(x, okres, amplituda):
    if (x / okres) % 1 < 0.5:
        return amplituda
    else:
        return -amplituda

def rysuj_funkcje(frame, wsp_x, wsp_y):
    
    fig = plt.figure(figsize=(6, 4), dpi=100)
    plt.plot(wsp_x, wsp_y)
    plt.xlabel('t [s]')
    if frame == wykres:
        plt.ylabel('u [V]')
    elif frame == wykres2:
        plt.ylabel('i [A]')
    elif frame == wykres3:
        plt.ylabel('ω [rad/s]')
    
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=okno.TOP, fill=okno.BOTH, expand=1)

def update_window():
    global wykres
    global wykres2
    global wykres3
    plt.close()
    wykres.destroy()
    wykres = okno.Frame(okno_funkcje_wejsciowe)
    wykres.pack(side=okno.RIGHT, expand=1)
    rysuj_funkcje(wykres, os_czasu, napiecie)
    wykres2.destroy()
    wykres2 = okno.Frame(okno_natezenie)
    wykres2.pack(side=okno.RIGHT, expand=1)
    rysuj_funkcje(wykres2, os_czasu, x1)
    wykres3.destroy()
    wykres3 = okno.Frame(okno_funkcje_predkosc_katowa)
    wykres3.pack(side=okno.RIGHT, expand=1)
    rysuj_funkcje(wykres3, os_czasu, x2)
    window.update()

napiecie = []
button_selected = None

window = okno.Tk()
window.title("Projekt MMM")
window.geometry("1800x1000")
Tytuly = font.Font(family='Helvetica', size=20, weight='bold')
Podtytuly = font.Font(family='Arial', size=12, weight='bold')
tresc = font.Font(family='Arial', size=9, weight='normal')

#schemat
dane_ukladu = okno.Frame(master=window, width=700, height=200)
dane_ukladu.place(x=100, y=100)
podpis1 = okno.Label(master=dane_ukladu, text="Schemat Obrazujący działanie układu", font=Tytuly)
podpis1.pack()
zdjecie_ukladu = ImageTk.PhotoImage(Image.open("uklad.png"))
ukladzik = okno.Label(master=dane_ukladu, image=zdjecie_ukladu)
ukladzik.pack()

#wykres funkcji wejściowej
okno_funkcje_wejsciowe = okno.Frame(master=window, borderwidth=1, width=700)
okno_funkcje_wejsciowe.place(x=900, y=10)
podpis2 = okno.Label(master=okno_funkcje_wejsciowe, text="Wykres funkcji wejściowej", font=Tytuly)
podpis2.pack()

okno_natezenie = okno.Frame(master=window, borderwidth=1, width=700)
okno_natezenie.place(x=200, y=520)
podpis4 = okno.Label(master=okno_natezenie, text="Wykres natężenia", font=Tytuly)
podpis4.pack()

okno_funkcje_predkosc_katowa = okno.Frame(master=window, borderwidth=1, width=700)
okno_funkcje_predkosc_katowa.place(x=900, y=520)
podpis5 = okno.Label(master=okno_funkcje_predkosc_katowa, text="Wykres prędkości kątowej", font=Tytuly)
podpis5.pack()

zmiany_funkcji = okno.Frame(master=okno_funkcje_wejsciowe, width=400, height=50)
zmiany_funkcji.pack()

#zmiany parametrów układu
zmiany_parametrow_ukladu = okno.Frame(master=window, width=100, height=600, background="lightgray", borderwidth=3) 
zmiany_parametrow_ukladu.pack(anchor=okno.E)

podpis3 = okno.Label(master=zmiany_parametrow_ukladu, text="Parametry układu", font=Podtytuly,  background="lightgray")
wprowadz_napiecie = okno.Entry(master=zmiany_parametrow_ukladu)
wprowadz_napiecie_podpis = okno.Label(master=zmiany_parametrow_ukladu, text="\nNapiecie [V]", font=tresc,  background="lightgray")

wprowadz_okres = okno.Entry(master=zmiany_parametrow_ukladu)
wprowadz_okres_podpis = okno.Label(master=zmiany_parametrow_ukladu, text="\nOkres [s]", font=tresc,  background="lightgray")

wprowadz_czas_trwania = okno.Entry(master=zmiany_parametrow_ukladu)
wprowadz_czas_trwania_podpis = okno.Label(master=zmiany_parametrow_ukladu, text="\nCzas trwania sygnału [s]", font=tresc,  background="lightgray")

wprowadz_czas_symulacji = okno.Entry(master=zmiany_parametrow_ukladu)
wprowadz_czas_symulacji_podpis = okno.Label(master=zmiany_parametrow_ukladu, text="\nCzas trwania symulacji [s]", font=tresc,  background="lightgray")

wprowadz_rezystancje = okno.Entry(master=zmiany_parametrow_ukladu)
wprowadz_rezystancje_podpis = okno.Label(master=zmiany_parametrow_ukladu, text="\nRezystancja", font=tresc,  background="lightgray")

wprowadz_indukcyjnosc = okno.Entry(master=zmiany_parametrow_ukladu)
wprowadz_indukcyjnosc_podpis = okno.Label(master=zmiany_parametrow_ukladu, text="\nIndukcyjność", font=tresc,  background="lightgray")

wprowadz_moment_bezwladnosci = okno.Entry(master=zmiany_parametrow_ukladu)
wprowadz_moment_bezwladnosci_podpis = okno.Label(master=zmiany_parametrow_ukladu, text="\nMoment bezwładności ( J ) [kg*m^2]", font=tresc,  background="lightgray")

wprowadz_wspolczynnik_tarcia_lepkiego = okno.Entry(master=zmiany_parametrow_ukladu)
wprowadz_wspolczynnik_tarcia_lepkiego_podpis = okno.Label(master=zmiany_parametrow_ukladu, text="\nWspółczynnik tarcia lepkiego ( b ) [Pa * s]", font=tresc,  background="lightgray")

wprowadz_Ke = okno.Entry(master=zmiany_parametrow_ukladu)
wprowadz_Ke_podpis = okno.Label(master=zmiany_parametrow_ukladu, text="\nKe [V * s/rad]", font=tresc,  background="lightgray")

wprowadz_Km = okno.Entry(master=zmiany_parametrow_ukladu)
wprowadz_Km_podpis = okno.Label(master=zmiany_parametrow_ukladu, text="\nKm [N *m/A]", font=tresc,  background="lightgray")

podpis3.pack()
wprowadz_napiecie_podpis.pack()
wprowadz_napiecie.pack()
wprowadz_okres_podpis.pack()
wprowadz_okres.pack()
wprowadz_czas_trwania_podpis.pack()
wprowadz_czas_trwania.pack()
wprowadz_czas_symulacji_podpis.pack()
wprowadz_czas_symulacji.pack()
wprowadz_rezystancje_podpis.pack()
wprowadz_rezystancje.pack()
wprowadz_indukcyjnosc_podpis.pack()
wprowadz_indukcyjnosc.pack()
wprowadz_moment_bezwladnosci_podpis.pack()
wprowadz_moment_bezwladnosci.pack()
wprowadz_wspolczynnik_tarcia_lepkiego_podpis.pack()
wprowadz_wspolczynnik_tarcia_lepkiego.pack()
wprowadz_Ke_podpis.pack()
wprowadz_Ke.pack()
wprowadz_Km_podpis.pack()
wprowadz_Km.pack()



wykres = okno.Frame(okno_funkcje_wejsciowe)
wykres.pack(side=okno.RIGHT, expand=1)
wykres2 = okno.Frame(okno_natezenie)
wykres2.pack(side=okno.RIGHT, expand=1)
wykres3 = okno.Frame(okno_funkcje_predkosc_katowa)
wykres3.pack(side=okno.RIGHT, expand=1)
rysuj_funkcje(wykres, 0, 0)
rysuj_funkcje(wykres2, 0, 0)
rysuj_funkcje(wykres3, 0, 0)

Funkcje = ['sinus', 'trojkat', 'prostokat']

for i in range(len(Funkcje)):
    Funkcje[i] = okno.Button(master=zmiany_funkcji, width=23, height=2, text=Funkcje[i], command=lambda btn=Funkcje[i]: on_button_click(btn))
    Funkcje[i].pack(side=okno.LEFT)

window.mainloop()