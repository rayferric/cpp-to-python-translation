class Item:
  def hello(self, ) -> None:
    print("hello", '\n', sep='', end='')
  def __init__(self, new_name: str, new_price: int):
    self.name = new_name
    self.price = new_price

def main() -> int:
  item = Item("apple", 12)
  item.hello()
  print(item.name, '\n', sep='', end='')
  print(item.price, '\n', sep='', end='')
  return 0

exit(main())
