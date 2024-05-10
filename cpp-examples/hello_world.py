def hello() -> str:
  return "Hello, World!"

def say_hey() -> None:
  print("Hey!", '\n', sep='', end='')

def main() -> int:
  print(hello(), '\n', sep='', end='')
  say_hey()
  return 0

exit(main())
