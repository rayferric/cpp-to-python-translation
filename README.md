# Konwerter C++ -> Python
## 1. Dane studentów 
Rafał Żelazko, Adam Tokarz
## 2. Dane kontaktowe 
rayferric@student.agh.edu.pl adamtokarz@student.agh.edu.pl
## 3. Założenia programu
### a) Główne cele programu
Transpilator z języka C++ na Python. Program będzie przyjmował na wejściu plik z kodem C++ i zapisywał obok niego przetłumaczony plik o tej samej nazwie, lecz z rozszerzeniem .py. Transpilator będzie operować na podzbiorze składni języka C++, w szczególności zawierającej w sobie elementy języka odpowiadające za programowanie obiektowe.\
### b) Rodzaj translatora
transpilator
### c) Wynik działania programu
Program tworzy nowy plik źródłowy w Pythonie, który następnie można uruchomić za pomocą interpretera Pythona.
### d) Język implementacji
Implementacja transpilatora w języku Python.
### e) Sposób realizacji programu
 Skaner i parser zostaną wygenerowane przez Antlr4. Pliki z przykładowym kodem C++ zostaną przez nas przygotowane. W programie napiszemy funkcje konwertujące elementy języka C++ na elementy języka Python.
## 4. Spis tokenów
[CppTokens](https://github.com/rayferric/cpp-to-python-translation/blob/main/grammar/CppTokens.g4)
## 5. Gramatyka przetwarzanego formatu
[CppGrammar](https://github.com/rayferric/cpp-to-python-translation/blob/main/grammar/Cpp.g4)
## 6. Informacja o stosowanych generatorach skanerów/parserów, pakietach zewnętrznych,
Antlr4 - generator skanerów i parserów
## 7. Krótka instrukcja obsługi
 I. Sklonuj repozytorium z githuba\
 II. Zainstaluj odpowiednią paczkę Antlr4 do Pythona:
```
pip install antlr4-python3-runtime==4.9.2
```
 III. Uruchom skrypt z pliku [gen-grammar](https://github.com/rayferric/cpp-to-python-translation/blob/main/scripts/gen-grammar)\
 IV. Uruchom translate.py w terminalu jako argument podając nazwę pliku do skonwertowania
```
python translate.py examples/functions.cpp
```
 V. Program wygeneruje w folderze „examples” plik py przekonwertowany z C++ na Python
## 8. Przykłady
### Przykład funkcje: functions.cpp -> functions.py
```cpp
#include <iostream>

int add(int a, int b) {
    return a + b;
}

float divide(float a, float b) {
    return a / b;
}

void say_number(int number) {
    std::cout << "Number is " << number << std::endl;
}

int main() {
    std::cout << "2 + 3 = " << add(2, 3) << std::endl;
    std::cout << "10 / 3 = " << divide(10, 3) << std::endl;
    say_number(5);

    return 0;
}
```
Transpilator tłumaczy na
```python
def add(a: int, b: int) -> int:
  return a+b

def divide(a: float, b: float) -> float:
  return a / b

def say_number(number: int) -> None:
  print("Number is ", number, '\n', sep='', end='')

def main() -> int:
  print("2 + 3 = ", add(2, 3), '\n', sep='', end='')
  print("10 / 3 = ", divide(10, 3), '\n', sep='', end='')
  say_number(5)
  return 0

exit(main())
```
### Przykład pętle, if i switch: control_flow.cpp -> control_flow.py
```cpp
#include <iostream>

int main() {
    int number;

    // Demonstrate if-else control flow
    std::cout << "Enter a number: ";
    std::cin >> number;
    if (number > 0) {
        std::cout << "Number is positive.\n";
    } else if (number < 0) {
        std::cout << "Number is negative.\n";
    } else {
        std::cout << "Number is zero.\n";
    }

    // Demonstrate while loop
    int i = 1;
    std::cout << "Counting from 1 to 5 using while loop: ";
    while (i <= 5) {
        std::cout << i << " ";
        i++;
    }
    std::cout << "\n";

    // Demonstrate for loop
    std::cout << "Counting from 1 to 5 using for loop: ";
    for (int j = 1; j <= 5; j++) {
        std::cout << j << " ";
    }
    std::cout << "\n";

    // Demonstrate switch-case control flow
    int choice;
    std::cout << "Enter a choice (1-3): ";
    std::cin >> choice;
    switch (choice) {
        case 1:
            std::cout << "You chose first option.\n";
            break;
        case 2:
            std::cout << "You chose second option.\n";
            break;
        case 3:
            std::cout << "You chose third option.\n";
            break;
        default:
            std::cout << "Invalid choice.\n";
    }

    return 0;
}

```
Transpilator tłumaczy na 
```python
def main() -> int:
  print("Enter a number: ", end='')
  number = int(input())
  if number > 0:
    print("Number is positive.\n", end='')
  elif number < 0:
    print("Number is negative.\n", end='')
  else:
    print("Number is zero.\n", end='')
  i: int = 1
  print("Counting from 1 to 5 using while loop: ", end='')
  while i <= 5:
    print(i, " ", sep='', end='')
    i += 1
  print("\n", end='')
  print("Counting from 1 to 5 using for loop: ", end='')
  j: int = 1
  while j <= 5:
    print(j, " ", sep='', end='')
    j += 1
  print("\n", end='')
  print("Enter a choice (1-3): ", end='')
  choice = int(input())
  match choice:
    case 1:
      print("You chose first option.\n", end='')
    case 2:
      print("You chose second option.\n", end='')
    case 3:
      print("You chose third option.\n", end='')
    case _:
      print("Invalid choice.\n", end='')
  return 0

exit(main())

```
### Przykład klasy i dziedziczenie: classes.cpp -> classes.py
```cpp
#include <iostream>

class Base {
public:
    Base() {
        std::cout << "Base constructor" << std::endl;
    }

    void hello() {
        std::cout << "hello from Base" << std::endl;
    }
};

class Item : public Base {
public:
    std::string name;
    int price;

    void hello() {
        Base::hello();
        std::cout << "hello from Item" << std::endl;
    }
    
    std::string to_string() {
        return this->name + " " + std::to_string(this->price);
    }

    Item(std::string name, int price) {
        this->name = name;
        this->price = price;
    }
};

int main() {
    Item item = Item("apple", 12);
    item.hello();
    std::cout << item.name << std::endl;
    std::cout << item.price << std::endl;
    std::cout << item.to_string() << std::endl;
    Base base = Base();
    base.hello();
    return 0;
}
```
Transpilator tłumaczy na 
```python
class Base:
  def __init__(self, ):
    print("Base constructor", '\n', sep='', end='')

  def hello(self) -> None:
    print("hello from Base", '\n', sep='', end='')

class Item(Base):
  def hello(self) -> None:
    super().hello()
    print("hello from Item", '\n', sep='', end='')

  def to_string(self) -> str:
    return self.name + " " + str(self.price)

  def __init__(self, name: str, price: int):
    super().__init__()
    self.name = name
    self.price = price

def main() -> int:
  item: Item = Item("apple", 12)
  item.hello()
  print(item.name, '\n', sep='', end='')
  print(item.price, '\n', sep='', end='')
  print(item.to_string(), '\n', sep='', end='')
  base: Base = Base()
  base.hello()
  return 0

exit(main())

```
### Przykład tablice: arrays.cpp -> arrays.py
```cpp
#include <iostream>


int main() {
    int tab[5] = {10, 13, 14, 34, 9};
    std::cout << "The first item in tab = {10, 13, 14, 34, 9} is " << tab[0] << "." << std::endl;
    std::string texts[2];
    texts[0] = "hello";
    std::cout << "Value of the first item is \"" << texts[0] << "\"." << std::endl << "Please choose the contents for the second item: ";
    std::cin >> texts[1];
    for(int i = 0 ; i < 2; i++) {
        std::cout << "[" << i << "] " << texts[i] << std::endl;
    }
    std::cout << "Please choose the contents for the third item of tab (numeric value is required): ";
    std::cin >> tab[2];
    for(int i = 0 ; i < 5; i++) {
        std::cout << "[" << i << "] " << tab[i] << std::endl;
    }
}
```
Transpilator tłumaczy na
```python
def main() -> int:
  tab = [10, 13, 14, 34, 9]
  print("The first item in tab = {10, 13, 14, 34, 9} is ", tab[0], ".", '\n', sep='', end='')
  texts = [None] * 2
  texts[0] = "hello"
  print("Value of the first item is \"", texts[0], "\".", '\n', "Please choose the contents for the second item: ", sep='', end='')
  texts[1] = str(input())
  i: int = 0
  while i < 2:
    print("[", i, "] ", texts[i], '\n', sep='', end='')
    i += 1
  print("Please choose the contents for the third item of tab (numeric value is required): ", end='')
  tab[2] = int(input())
  i: int = 0
  while i < 5:
    print("[", i, "] ", tab[i], '\n', sep='', end='')
    i += 1

exit(main())

```
