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
