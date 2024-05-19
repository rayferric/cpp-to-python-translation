def add(a: int, b: int) -> int:
  return a + b

def divide(a: float, b: float) -> float:
  return a / b

def say_number(number: int) -> None:
  print("Number is ", number, '\n', sep='', end='')

def main() -> int:
  print("2 + 3 = ", add(2, 3), '\n', sep='', end='')
  print("10 / 3 = ", divide(10, 3), '\n', sep='', end='')
  say_number(5)
  return 0

exit(main())
