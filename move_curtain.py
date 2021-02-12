from stepper import Stepper

stepper = Stepper(22, 23, 24, 25)

total_turns = 0

while True:
  try:
    turns = int(input("Enter turns you wana go: "))
    print(f"Total turns: {total_turns}, going -> {turns}")
    total_turns += turns
    stepper.turn(turns)
    print(f"Done. New total: {total_turns}")
  except KeyboardInterrupt:
    break
  except:
    pass
  