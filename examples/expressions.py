def main() -> int:
  x: int = 7
  a = 2 + 3
  b: int = a * (10 + 1) + 2
  b += x
  b -= 1
  b += 1
  return b

exit(main())
