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