#include <iostream>

class Item {
private:
    std::string name;
    int price;

public:
    void hello() {
        std::cout << "hello" << std::endl;
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
    return 0;
}
