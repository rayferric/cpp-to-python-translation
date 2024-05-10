#include <iostream>

std::string hello() {
    return "Hello, World!";
}

void say_hey() {
    std::cout << "Hey!" << std::endl;
}

int main() {
    std::cout << hello() << std::endl;
    say_hey();

    return 0;
}
