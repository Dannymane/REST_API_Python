import requests
import sys
import os #for clearning console
import json
import base64 #to add authorization headers
from requests.structures import CaseInsensitiveDict #to define header with authorization

# Zdecydowałem, żeby użyć biblioteki requests.
# Jeżeli macie Anacondę, to jest już zainstalowana.
# Jeżeli jej nie ma, to można ją zainstalować poleceniem:
# python -m pip install requests

## Żądanie get
#result = requests.get("http://localhost:8000")
## Kod odpowiedzi HTTP
#print(result.status_code)
## zwykły tekst
#print(result.text)
## skonwertowany do obiektów Pythona json()
## - jak widać nie trzeba jawnie konwertować tekstu
#print(result.json()['x'])
## Żądanie post
## data - ciało żądania
#result = requests.post("http://localhost:8000/osoby/1", data='{"y":[1,2,3]}')
## Nie mogę użyć json(), bo zwracany tekst nie jest json-em.
## Próba zakończyłaby się błędem parsowania tekstu.
#print(result.text)
## Żądanie put i delete, robi się analogicznie.

class Osoba:
    identyfikator = 1
    login = ""
    haslo = ""
    headers = CaseInsensitiveDict()

    def __init__(self, *args):
        if len(args) == 0:
            pass
        elif len(args) == 3:
            self.imie = args[0]
            self.nazwisko = args[1]
            self.rok_urodzenia = args[2]
            self.identyfikator = Osoba.identyfikator
            Osoba.identyfikator += 1
        elif len(args) == 4:
            self.identyfikator = args[0]
            self.imie = args[1]
            self.nazwisko = args[2]
            self.rok_urodzenia = args[3]

    def post_osoba(self):
        url = "http://localhost:8000/osoby/"
        d = '{\"'+str(self.identyfikator)+'\":{"Imie":\"'+self.imie+'\","Nazwisko":\"'+self.nazwisko+'\","Rok urodzenia":\"'+str(self.rok_urodzenia)+'\"}}'
        result = requests.post(url, headers=Osoba.headers, data=d)
        result.status_code
        if result.status_code != 200 or result.status_code != 201:
            return str(result.status_code)+" "+result.reason
        return result.text

    def put_osoba(self):
        url = "http://localhost:8000/"
        d='{\"'+str(self.identyfikator)+'\":{"Imie":\"'+self.imie+'\","Nazwisko":\"'+self.nazwisko+'\","Rok urodzenia":\"'+str(self.rok_urodzenia)+'\"}}'
        result = requests.put(url, headers=Osoba.headers, data = d) 
        if result.status_code != 200:
            return str(result.status_code)+" "+result.reason
        return result.text

    @staticmethod
    def get_osoba(iden):
        url = "http://localhost:8000/osoby/{}".format(iden)
        result = requests.get(url, headers=Osoba.headers)
        if result.status_code != 200:
            return str(result.status_code)+" "+result.reason
        return "Identyfikator: {}\nImie: {}\nNazwisko: {}\nRok urodzenia: {}\n\n".format(iden,json.loads(result.text)["Imie"],json.loads(result.text)["Nazwisko"],json.loads(result.text)["Rok urodzenia"])
    
    @staticmethod
    def get_osoby():
        result = requests.get("http://localhost:8000/",headers=Osoba.headers)
        if result.status_code != 200:
            return str(result.status_code)+" "+result.reason
        lista_kluczy = list(json.loads(result.text).keys())
        Odpowiedz = ""
        for iden in lista_kluczy:
            Odpowiedz += Osoba().get_osoba(iden)
        return Odpowiedz
        #if result.text != "":
        #    lista_kluczy = list(json.loads(result.text).keys())
        #    Odpowiedz = ""
        
        #    for iden in lista_kluczy:
        #        Odpowiedz += Osoba().get_osoba(iden)
        #    return Odpowiedz
        #else: 
        #    return "Brak zapisanych osób"
    @staticmethod
    def delete_osoba(iden):
        result = requests.delete("http://localhost:8000/osoby/{}".format(iden),headers=Osoba.headers)
        if result.status_code != 200:
            return str(result.status_code)+" "+result.reason
        return result.text

    def znajdz_najwiekszy_identyfikator(self):
        url = "http://localhost:8000/osoby/"
        result = requests.get(url, headers=Osoba.headers)
        if result.status_code == 200:
            lista_kluczy = list(json.loads(result.text).keys())
            lista_kluczy.sort()
            return int(lista_kluczy[-1])+1
        else:
            return 1
    @staticmethod
    def autoryzacja(log,has):
        Osoba.login = log
        Osoba.haslo = has
        Osoba.headers["Authorization"] = "Basic " + base64.b64encode((str(log)+":"+str(has)).encode("utf-8")).decode("utf-8")


print("Aplikacja zapamięta login i hasło oraz \nbędzie wysyłać kod autoryzacyjny przy każdym żądaniu")
login = input("Wprowadź login (poprawny: user): ")
haslo = input("Wprowadź hasło (poprawne: password): ")
Osoba().autoryzacja(login,haslo)

def clear(): os.system('cls')
Osoba.identyfikator = Osoba().znajdz_najwiekszy_identyfikator()

#imie = input("Wprowadź imię: ")
#login = input("Wprowadź login (user): ")
#password = input("Wprowadź hasło (password): ")
#header = "Basic " + base64.b64encode((str(login)+":"+str(password)).encode("utf-8")).decode("utf-8")

while True:
    print("""--- Proszę wybrać czynność poprzez wprowadzenie i zatwierdzenie liczby ---
    1 - dodać osobę
    2 - zmodyfikować istniejącą osobę
    3 - pobrać dane osoby
    4 - usunąć osobę
    5 - pobrać dane wszystkich osób
    6 - wyjście""")
    choise = input()
    if choise == "1":
        print("--Wprowadzenie danych osoby--")
        imie = input("Wprowadź imię: ")
        nazwisko = input("Wprowadź nazwisko: ")
        rok_urodzenia = input("Wprowadź rok urodzenia: ")
        o = Osoba(imie,nazwisko,rok_urodzenia)
        print(o.post_osoba())
        przejscie_dalej = input("Przycisnij Enter dla kontynuacji...")
        clear()

    elif choise == "2":
        print("--Modyfikowanie istniejącej osoby--")
        identyfikator = input("Wprowadź aktualny identyfikator: ")
        imie = input("Wprowadź nowe imię: ")
        nazwisko = input("Wprowadź nowe nazwisko: ")
        rok_urodzenia = input("Wprowadź nowy rok urodzenia: ")

        o = Osoba(identyfikator,imie,nazwisko,rok_urodzenia)
        print(o.put_osoba())
        przejscie_dalej = input("Przycisnij Enter dla kontynuacji...")
        clear()

    elif choise == "3":
        print("--Pobranie danych osoby--")
        identyfikator = input("Wprowadź aktualny identyfikator: ")
        print(Osoba().get_osoba(identyfikator))
        przejscie_dalej = input("Przycisnij Enter dla kontynuacji...")
        clear()

    elif choise == "4":
        print("--Usunięcie osoby--")
        identyfikator = input("Wprowadź aktualny identyfikator: ")
        print(Osoba().delete_osoba(identyfikator))
        przejscie_dalej = input("Przycisnij Enter dla kontynuacji...")
        clear()
    elif choise == "5":
        print("--Pobranie danych wszystkich osób--")
        
        print(Osoba().get_osoby())
        przejscie_dalej = input("Przycisnij Enter dla kontynuacji...")
        clear()
    elif choise == "6":
        exit()
    else:
        clear()
        print("Niewłaściwy wybór")
        przejscie_dalej = input("Przycisnij Enter dla kontynuacji...")    
