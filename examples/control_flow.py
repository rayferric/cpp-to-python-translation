def main() -> int:
  print("Enter a number: ", end='')
  number = int(input())
  if number > 0:
    print("Number is positive.\n", end='')
  elif number < 0:
    print("Number is negative.\n", end='')
  else:
    print("Number is zero.\n", end='')
  i: int = 1
  print("Counting from 1 to 5 using while loop: ", end='')
  while i <= 5:
    print(i, " ", sep='', end='')
    i += 1
  print("\n", end='')
  print("Counting from 1 to 5 using for loop: ", end='')
  j: int = 1
  while j <= 5:
    print(j, " ", sep='', end='')
    j += 1
  print("\n", end='')
  print("Enter a choice (1-3): ", end='')
  choice = int(input())
  match choice:
    case 1:
      print("You chose first option.\n", end='')
    case 2:
      print("You chose second option.\n", end='')
    case 3:
      print("You chose third option.\n", end='')
    case _:
      print("Invalid choice.\n", end='')
  return 0

exit(main())
