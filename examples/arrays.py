def main() -> int:
  tab = [10, 13, 14, 34, 9]
  print(tab[0], '\n', sep='', end='')
  texts = [i for i in range(2)]
  texts[0] = "hello"
  texts[1] = str(input())
  i: int = 0
  while i < 2:
    print(texts[i], '\n', sep='', end='')
    i += 1

exit(main())
