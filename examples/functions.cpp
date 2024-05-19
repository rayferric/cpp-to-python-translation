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
