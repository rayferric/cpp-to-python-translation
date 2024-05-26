#include <iostream>


int main() {
    int tab[5] = {10, 13, 14, 34, 9};
    std::cout << tab[0] << std::endl;
    std::string texts[2];
    texts[0] = "hello";
    std::cin >> texts[1];
    for(int i = 0 ; i < 2; i++) {
        std::cout << texts[i] << std::endl;
    }
}