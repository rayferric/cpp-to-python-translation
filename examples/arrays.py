def main() -> int:
  tab = [10, 13, 14, 34, 9]
  print("The first item in tab = {10, 13, 14, 34, 9} is ", tab[0], ".", '\n', sep='', end='')
  texts = [None] * 2
  texts[0] = "hello"
  print("Value of the first item is \"", texts[0], "\".", '\n', "Please choose the contents for the second item: ", sep='', end='')
  texts[1] = str(input())
  i: int = 0
  while i < 2:
    print("[", i, "] ", texts[i], '\n', sep='', end='')
    i += 1
  print("Please choose the contents for the third item of tab (numeric value is required): ", end='')
  tab[2] = int(input())
  i: int = 0
  while i < 5:
    print("[", i, "] ", tab[i], '\n', sep='', end='')
    i += 1

exit(main())
