def main() -> int:
  print("Enter a number: ", sep='', end='')
  number = int(input())
  if number > 0:
    print("Number is positive.\n", sep='', end='')
  elif number < 0:
    print("Number is negative.\n", sep='', end='')
  else:
    print("Number is zero.\n", sep='', end='')
  i: int = 1
  print("Counting from 1 to 5 using while loop: ", sep='', end='')
  while i <= 5:
    print(i, " ", sep='', end='')
    i += 1
  print("\n", sep='', end='')
  print("Counting from 1 to 5 using for loop: ", sep='', end='')
  j: int = 1
  while j <= 5:
    print(j, " ", sep='', end='')
    j += 1
  print("\n", sep='', end='')
  print("Enter a choice (1-3): ", sep='', end='')
  choice = int(input())
  match choice:
    case 1:
      print("You chose first option.\n", sep='', end='')
    case 2:
      print("You chose second option.\n", sep='', end='')
    case 3:
      print("You chose third option.\n", sep='', end='')
    case _:
      print("Invalid choice.\n", sep='', end='')
  return 0

exit(main())
