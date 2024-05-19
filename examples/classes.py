class Item:
  def hello(self) -> None:
    print("hello", '\n', sep='', end='')

  def to_string(self) -> str:
    return self.name + " " + str(self.price)

  def __init__(self, name: str, price: int):
    self.name = name
    self.price = price

def main() -> int:
  item: Item = Item("apple", 12)
  item.hello()
  print(item.name, '\n', sep='', end='')
  print(item.price, '\n', sep='', end='')
  print(item.to_string(), '\n', sep='', end='')
  return 0

exit(main())
