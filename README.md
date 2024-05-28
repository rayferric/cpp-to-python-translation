# Konwerter C++ -> Python
## 1. Dane studentów 
Rafał Żelazko, Adam Tokarz
## 2. Dane kontaktowe 
rayferric@student.agh.edu.pl adamtokarz@student.agh.edu.pl
## 3. Założenia programu
### a) Główne cele programu
Transpilator z języka C++ na Python. Program będzie przyjmował na wejściu plik z kodem C++ i zapisywał obok niego przetłumaczony plik o tej samej nazwie, lecz z rozszerzeniem .py. Transpilator będzie operować na podzbiorze składni języka C++, w szczególności zawierającej w sobie elementy języka odpowiadające za programowanie obiektowe.\
### b) Rodzaj translatora
transpiler
### c) Wynik działania programu
Program tworzy nowy plik źródłowy w Pythonie, który następnie można uruchomić za pomocą interpretera Pythona.
### d) Język implementacji
Implementacja transpilatora w języku Python.
### e) Sposób realizacji programu
 Skaner i parser zostaną wygenerowane przez Antlr4. Pliki z przykładowym kodem C++ zostaną przez nas przygotowane.
## 4. Spis tokenów
CppTokens
## 5. Gramatyka przetwarzanego formatu
CppGrammar
## 6. Informacja o stosowanych generatorach skanerów/parserów, pakietach zewnętrznych,
Antlr4 - generator skanerów i parserów
## 7. Krótka instrukcja obsługi
 I. Sklonuj repozytorium z githuba\
 II. Zainstaluj odpowiednią paczkę Antlr4 do Pythona:
```
pip install antlr4-python3-runtime==4.9.2
```
 III. Uruchom skrypt z pliku gen-grammar\
 IV. Uruchom translate.py w terminalu jako argument podając nazwę pliku do skonwertowania
```
python translate.py examples/functions.cpp
```
 V. Program wygeneruje w folderze „examples” plik py przekonwertowany z C++ na Python
## 8. Przykłady
