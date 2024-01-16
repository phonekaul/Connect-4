import numpy, os, time


#FUNCTIONS

#clear() clears the screen
def clear(): #Done
  os.system('clear')

#makeGrid() draws the connect4 grid with any existing symbols inside
def makeGrid(): #Done
  gridSquares = []
  for i in range(height):
    row = ("|   "+"   |   ".join(numpy.transpose(board)[i])+"   |\n")
    gridSquares.append(row)
  print(line+spaceLine+(spaceLine+line+spaceLine).join(gridSquares)+spaceLine+line,end="")
  print("    "+"       ".join(numberWidth)+"\n")

#getInput() gets input from the player regarding what column they want to put their piece into and calls findSquare()
def getInput(char): #Done
  while True:
    try:
      playerColumn = int(input("Enter the column: "))
      if findSquare(playerColumn-1, char):
        return
      else:
        print("Invalid input. Please re-enter.\n")
    except:
      print("Invalid input. Please re-enter.")

#winCheck() checks if either of the players have four symbols in a row horizontally, vertically, or diagonally and then returns True/winner or False/'no one'
def winCheck(): #Done
  #Checking horizontally
  for a in range(height): #6
    for b in range(width-(winLength-1)): #4
      horizontal = set()
      for i in range(winLength):
        horizontal.add(board[b+i][a])
      if horizontal == player1Win:
        return True, player1
      elif horizontal == player2Win:
        return True, player2
  #Checking vertically
  for a in range(width): #7
    for b in range(height-(winLength-1)): #3
      vertical = set()
      for i in range(winLength):
        vertical.add(board[a][b+i])
      if vertical == player1Win:
        return True, player1
      elif vertical == player2Win:
        return True, player2
  #Checking diagonally: UpLeft to DownRight and UpRight to DownLeft
  for a in range(width-(winLength-1)): #4
    for b in range(height-(winLength-1)): #3
      ULtoDR = set()
      URtoDL = set()
      for i in range(winLength):
        ULtoDR.add(board[a+i][b+i])
        URtoDL.add(board[a+i][b+winLength-1-i])
      if (ULtoDR == player1Win) or (URtoDL == player1Win):
        return True, player1
      elif (ULtoDR == player2Win) or (URtoDL == player2Win):
        return True, player2
  return False, 'no one'

#findSquare(pc, ch) finds which square in the column to put the player's symbol into, and then puts it in
def findSquare(pc, ch): #Done
  try:
    for a in range((len(board[0])-1),-1,-1):
      if board[pc][a] == ' ':
        board[pc][a] = ch
        return True
    return False
  except:
    return False

#setStyle() gets input from users on game style (names, colours, symbols)
def styleInput(): #Done
  #LOCAL LISTS
  colourList = ['red(1)','orange(2)','green(3)','blue(4)','cyan(5)','purple(6)','white(7)']
  colList = ['\033[0;31m','\033[0;33m','\033[0;32m','\033[0;34m','\033[0;36m','\033[0;35m','\033[0;38m']
  symbolList = [['X','O'],['A','B'],['+','-']]

  #NAME AND COLOUR INPUT
  name1 = input("Player 1, enter your name: ")
  while True:
    try:
      col1 = int(input(f"{name1}, what colour do you want your name and symbols to be? Choose from:\n{', '.join(colourList)}\nEnter choice: "))
      if col1 >= 1 and col1 <= 7:
        name1 = colList[col1-1] + name1 + colList[6]
        break
      else:
        raise Exception
    except:
      print("Invalid input. Re-enter your choice.\n")
  print(f"Welcome {name1}!")
  
  colourList.remove(colourList[col1-1])
  name2 = input("\nPlayer 2, enter your name: ")
  while True:
    try:
      col2 = int(input(f"{name2}, what colour do you want your name and symbols to be? Choose from:\n{', '.join(colourList)}\nEnter choice: "))
      if col2 == col1:
        raise Exception
      elif col1 >= 1 and col1 <= 7:
        name2 = colList[col2-1] + name2 + colList[6]
        break
      else:
        raise Exception
    except:
      print("Invalid input.\n")
  print(f"Welcome {name2}!")
  
  #SYMBOLS
  while True:
    try:
      symbolSet = int(input(f"\nThere are three symbol set options ({name1}, {name2}).\n1: X, O\n2: A, B\n3: +, -\nEnter your choice's corresponding number: "))
      if symbolSet >= 1 and symbolSet <= 3:
        s1 = colList[col1-1] + symbolList[symbolSet-1][0] + colList[6]
        s2 = colList[col2-1] + symbolList[symbolSet-1][1] + colList[6]
        break
      else:
        raise Exception
    except:
      print("That was not an integer that corresponded to a symbol set. Re-enter your choice.")
  input("\nPress Enter to start the game!")
  return name1, name2, s1, s2


#GLOBAL VARIABLES
width = 7 #Standard: 7
height = 6 #Standard: 6
winLength = 4 #Standard: 4
board = []
lineWidth = []
spaceWidth = []
numberWidth = []
for a in range(width):
  board.append([])
  lineWidth.append('-------')
  spaceWidth.append('       ')
  numberWidth.append(str(a+1))
  for b in range(height):
    board[a].append(' ')
line = " " + "-".join(lineWidth) + "\n"
spaceLine = "|" + "|".join(spaceWidth) + "|\n"
player1, player2, symbol1, symbol2 = styleInput()
player1Win = {symbol1}
player2Win = {symbol2}

#GAMEPLAY
startTime = time.time()
turns = 0
while True:
  clear()
  turns += 1
  if turns%2 == 1:
    player, character = player1, symbol1
  else:
    player, character = player2, symbol2
  print(f"Turn {turns}: {player}")
  makeGrid()
  getInput(character)
  isPass, winner = winCheck()
  if isPass:
    message = f"{winner} wins!"
    break
  elif turns == (width*height):
    message = "It's a tie! That's rare!"
    break
clear()
print("Game Over!")
makeGrid()
print(f"{message}\nThanks for playing.\nTime taken: {round((time.time()-startTime),2)} seconds")
