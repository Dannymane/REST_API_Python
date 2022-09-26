# -*- coding: utf-8 -*-
from http.server import HTTPServer, BaseHTTPRequestHandler

from io import BytesIO
import json
import os # to check if file is empty

import os.path
from os import path
import base64
#from requests.structures import CaseInsensitiveDict

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def authoritation(self):
        login = "user"
        password = "password" 
        correct_auth_data = base64.b64encode((str(login)+":"+str(password)).encode("utf-8")).decode("utf-8")
        try:
            received_auth_data = self.headers['Authorization'].removeprefix('Basic ')
            if received_auth_data != correct_auth_data:
                self.send_response(401, "Niepoprawny login lub haslo")
                self.end_headers()
                return False
            else: return True
        except AttributeError:
            self.send_response(401, "Proba nieautoryzowanego dostepu")
            self.end_headers()
            return False
    def do_GET(self):
        # path - ścieżka do zasobu
        # Gdy odowłujemy się do adresu http://localhost:8000
        # zwróci /
        # Gdy odowłujemy się do adresu http://localhost:8000/osoby
        # zwróci /osoby
        print(self.path)
        # send_response() i end_headers() są obowiązkowe

        # wfile strumień wyjściowy
        # Prefiks b oznacza, że napis będzie traktowany jako bajty.
        # Nie działa ten sposób konwersji z polskimi znakami, 
        # najprościej zastosować wtedy encode. 
        #self.wfile.write(b'{"x": "Witajcie!"}')
        if self.authoritation():
            ident = str(self.path.removeprefix('/osoby'))
            ident = ident.removeprefix('/')
            # process the request and do your stuff here
            if path.exists('osoby.json'):
                if os.stat("osoby.json").st_size == 0:
                    self.send_response(404, "Baza danych jest pusta")
                    self.end_headers()
                else:
                    with open('osoby.json', 'r') as f:
                        data = json.load(f) #data is dictionary (dict) type
                    if ident == "":
                        self.send_response(200)
                        self.send_header("Content-Type", "application/json")
                        self.end_headers()
                        self.wfile.write(bytes(json.dumps(data),"utf-8"))
                    else:
                        if ident in data:
                            self.send_response(200)
                            self.send_header("Content-Type", "application/json")
                            self.end_headers()
                            self.wfile.write(bytes(json.dumps(data[ident]),"utf-8"))
                        else:
                            self.send_response(404, "Zly identyfikator")
                            self.end_headers()
            else:
                with open('osoby.json', 'w') as f:
                    f.write("")
                self.send_response(404, "Baza danych jest pusta")
                self.end_headers()

    def do_POST(self):
        if self.authoritation():
            content_length = int(self.headers['Content-Length']) #int
        
            # rfile strumień wejściowy
            body = self.rfile.read(content_length)
            #print(body) #b'{"1":{"Imie":"Daniel","Nazwisko":"Yanko","Rok urodzenia":1999}}'
            #print(type(body)) #<class 'bytes'>
            #print(body.decode()) #{"1":{"Imie":"Daniel","Nazwisko":"Yanko","Rok urodzenia":1999}}
            #print(type(body.decode())) #str

            bodyDict = json.loads(body.decode()) #str -> dict
        
        
            with open('osoby.json', 'r') as f:
                if os.stat("osoby.json").st_size != 0:
                    data = json.load(f) #data is dictionary (dict) type
                    bodyDict.update(data)
            with open('osoby.json', 'w') as f:
                json_object = json.dumps(bodyDict)
                f.write(json_object)

            self.send_response(201)
            self.end_headers()
            # Tworzy strumień bajtów w pamięci, w tym przypadku jest wykorzystywany
            # do budowy odpowiedzi.
            response = BytesIO()
            response.write('Żądanie POST\n'.encode())
            response.write(b'Otrzymano:\n')
            response.write(body)
            self.wfile.write(response.getvalue())

        
    def do_PUT(self):
        if self.authoritation():
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            bodyDict = json.loads(body.decode()) #str -> dict
            if os.stat("osoby.json").st_size == 0:
                self.send_response(404, "Baza jest pusta")
                self.end_headers()
                response = BytesIO()
                response.write('Żądanie PUT\n'.encode())
                response.write(b'Otrzymano:\n')
                response.write(body)
                response.write(b'\nNie znaleziono osoby\n')
                self.wfile.write(response.getvalue())
            else:
                with open('osoby.json', 'r') as f:
                    file_data = json.load(f) #dict
                try:
                    ident = str(*bodyDict,) #str # *bodyDict, returns key
                    file_data[ident]["Imie"] = bodyDict[ident]["Imie"]
                    file_data[ident]["Nazwisko"] = bodyDict[ident]["Nazwisko"]
                    file_data[ident]["Rok urodzenia"] = bodyDict[ident]["Rok urodzenia"]
                    with open('osoby.json', 'w') as f:
                        json_object = json.dumps(file_data)
                        f.write(json_object)
                    self.send_response(200)
                except:
                    print("Brak osoby o podanym identyfikatorze")
                    self.send_response(404, "Brak osoby o podanym identyfikatorze")
                self.end_headers()
                response = BytesIO()
                response.write('Żądanie PUT\n'.encode())
                response.write(b'Otrzymano:\n')
                response.write(body)
                self.wfile.write(response.getvalue())

    def do_DELETE(self):
        if self.authoritation():
            ident = str(self.path.removeprefix('/osoby/'))
            if os.stat("osoby.json").st_size == 0:
                self.send_response(404, "Baza jest pusta")
            else:
                with open('osoby.json', 'r') as f:
                    file_data = json.load(f) #data is dictionary (dict) type
                if ident in file_data:
                    try:
                        del file_data[ident]
                        self.send_response(200)
                        with open('osoby.json', 'w') as f:
                            json_object = json.dumps(file_data)
                            f.write(json_object)
                        self.send_response(200)
                    except KeyError as ex:
                        print("Nie znaleziono danej osoby")
                        self.send_response(404, "Nie znaleziono danej osoby")
                    self.end_headers()
                else:
                    self.send_response(404, "Niepoprawny identyfikator")

            self.end_headers()
            response = BytesIO()
            response.write('Żądanie DELETE\n'.encode())
            # path jest stringiem stąd konwersja do bajtów
            response.write(self.path.encode()) 
            self.wfile.write(response.getvalue())
        
        
        


def main():
    # 8000 to numer portu, z którego korzysta serwer do komunikacji
    # Jeżeli port jest zajęty, to trzeba go zmienić na inny.
    httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
    httpd.serve_forever()
    
    
# Uruchamianie:
# python server.py
# Serwer jest uruchomiony w pętli.
if __name__ == "__main__":
    main()