from src.structs import Sheet
import src.functions as functions
import datetime

s = Sheet("spese")

inp = 0
while inp != -1:
    print('''1 per aggiungere eventi \n 2 per calcolare somma \n -1 per uscire''')
    inp = int(input())
    if inp == 1:
        desc = input("Inserisci descrizione: ")
        cat = input("Inserisci categoria: ")
        amount = float(input("Inserisci cifra: "))
        a = input("Inserisci autore: ")
        data = datetime.datetime.strptime(input("Inserisci giorno (YYYY-MM-DD): "), "%Y-%m-%d").date()
        s.add_cell(desc, cat, amount, a, data)
    elif inp == 2:
        mese = int(input("Inserisci mese"))
        print(functions.SUM(s.filter(2023, mese)))
    else:
        continue