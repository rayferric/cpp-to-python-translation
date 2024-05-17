#include <iostream>

class Item {
public:
    std::string name;
    int price;

    void hello() {
        std::cout << "hello" << std::endl;
    }

    Item(std::string new_name, int new_price) {
        this.name = new_name;
        this.price = new_price;
    }
};

int main() {
    Item item = Item("apple", 12);
    item.hello();
    std::cout << item.name << std::endl;
    std::cout << item.price << std::endl;
    return 0;
}