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
    // std::cout << "Counting from 1 to 5 using for loop: ";
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
