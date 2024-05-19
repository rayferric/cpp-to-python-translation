def hello() -> str:
  return "Hello, World!"

def say_hey(name: str) -> None:
  print("Hey, ", name, "!", '\n', sep='', end='')

def main() -> int:
  print(hello(), '\n', sep='', end='')
  print("Enter your name: ", end='')
  name = str(input())
  say_hey(name)
  return 0

exit(main())
