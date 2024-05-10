#include <iostream>

std::string hello() {
    return "Hello, World!";
}

void say_hey(std::string name) {
    std::cout << "Hey, " << name << "!" << std::endl;
}

int main() {
    std::cout << hello() << std::endl;
    std::string name;
    std::cout << "Enter your name: ";
    std::cin >> name;
    say_hey(name);

    return 0;
}
