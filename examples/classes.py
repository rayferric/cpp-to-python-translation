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
