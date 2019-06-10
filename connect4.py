#!/usr/bin/env python3
# # -*- coding: utf-8 -*-
""" Connect 4 MiniMax . Play against the computer in an exciting game of connect 4! """
__author__="Joe Koss"

#Initialize varibles
import sys, random, re

board = []
currentRow = []
moveVals = []
numMoves = 0
userIn = ""

#Create the board and initialize values
def initializeBoard():
	global board
	global currentRow
	global moveVals

	currentRow = [5,5,5,5,5,5,5]
	board = [[" "," "," "," "," "," "," "], [" "," "," "," "," "," "," "], [" "," "," "," "," "," "," "],
	[" "," "," "," "," "," "," "],[" "," "," "," "," "," "," "],[" "," "," "," "," "," "," "]]
	moveVals = [[5,5,5,5,5,5,5],[5,5,5,5,5,5,5],[5,5,5,5,5,5,5],[5,5,5,5,5,5,5],[5,5,5,5,5,5,5],[5,5,5,5,5,5,5]]

#Display the board and coordinates for each point
def displayBoard():
	boardCoords ="  1    2    3    4    5    6    7"

	for x in range(0,len(board)):
		print(board[x])
	print(boardCoords)

#Update the board after a move has been made
def updateBoard(col, player):
	global board
	global currentRow
	global numMoves

	if player == 1:
		board[currentRow[int(col)]][int(col)] = "O"
	else:
		board[currentRow[int(col)]][int(col)] = "X"

	currentRow[int(col)] -= 1
	numMoves += 1

#Recursive methods that return a value based on number of matching pieces in a row
def checkForLeftHorizontal(row, col, n, symbol, tBoard):
	if col - 1 >= 0:
		if tBoard[row][col-1] != symbol:
			return n
		else:
			return 5 + checkForLeftHorizontal(row, col - 1, n, symbol, tBoard)
	else:
		return n

#Recursive
def checkForLeftUpDiagonal(row, col, n, symbol, tBoard):
	if row - 1 >= 0:
		if col - 1 >= 0:
			#top left diagonal and checks for left horizontal
			if tBoard[row-1][col-1] != symbol:
				return n
			else:
				return 5 + checkForLeftUpDiagonal(row - 1, col - 1, n, symbol, tBoard)
		else:
			return n
	else:
		return n

#Recursive
def checkForLeftDownDiagonal(row, col, n, symbol, tBoard):
	if row + 1 <= 5:
		if col - 1 >= 0:
				if tBoard[row+1][col-1] == symbol:
					return n
				else:
					return 5 + checkForLeftDownDiagonal(row + 1, col - 1, n, symbol, tBoard)
		else:
			return n
	else:
		return n

#Recursive
def checkForRightHorizontal(row, col, n, symbol, tBoard):
	if col + 1 <= 6:
		if tBoard[row][col+1] != symbol:
			return n
		else:
			return 5 + checkForRightHorizontal(row, col + 1, n, symbol, tBoard)
	else:
		return n

#Recursive
def checkForRightUpDiagonal(row, col, n, symbol, tBoard):
	if row - 1 >= 0:
		if col + 1 <= 6:
			#top left diagonal and checks for left horizontal
			if tBoard[row-1][col+1] != symbol:
				return n
			else:
				return 5 + checkForLeftUpDiagonal(row - 1, col + 1, n, symbol, tBoard)
		else:
			return n
	else:
		return n

#Recursive
def checkForRightDownDiagonal(row, col, n, symbol, tBoard):
	if row + 1 <= 5:
		if col + 1 <= 6:
				if tBoard[row+1][col+1] != symbol:
					return n
				else:
					return 5 + checkForLeftDownDiagonal(row + 1, col + 1, n, symbol, tBoard)
		else:
			return n
	else:
		return n

#Recursive
def checkForUpVertical(row, col, n, symbol, tBoard):
	if row - 1 >= 0:
		if tBoard[row-1][col] != symbol:
			return n
		else:
			return 5 + checkForUpVertical(row - 1, col, n, symbol, tBoard)
	else:
		return n

#Recursive
def checkForDownVertical(row, col, n, symbol, tBoard):
	if row + 1 <= 5:
		if tBoard[row+1][col] != symbol:
			return n
		else:
			return 5 + checkForDownVertical(row + 1, col, n, symbol, tBoard)
	else:
		return n

#Gets the value of an empty space
def getVal(row, col, symbol, tBoard):
	newVal = 5
	left, leftUp, leftDown, right, rightUp, rightDown, vertUp, vertDown = 0,0,0,0,0,0,0,0

	left = checkForLeftHorizontal(row, col, left, symbol, tBoard)
	leftUp = checkForLeftUpDiagonal(row, col, leftUp, symbol, tBoard)
	leftDown = checkForLeftDownDiagonal(row, col, leftDown, symbol, tBoard)
	right = checkForRightHorizontal(row, col, right, symbol, tBoard)
	rightUp = checkForRightUpDiagonal(row, col, rightUp, symbol, tBoard)
	rightDown = checkForRightDownDiagonal(row, col, rightDown, symbol, tBoard)
	vertUp = checkForUpVertical(row, col, vertUp, symbol, tBoard)
	vertDown = checkForDownVertical(row, col, vertDown, symbol, tBoard)

	if (left == 15 or leftUp == 15 or leftDown == 15 or right == 15 or rightUp == 15 or rightDown == 15 
		or vertUp == 15 or vertDown==15):
		newVal = 999
	else:
		newVal += left + leftUp + leftDown + right + rightUp + rightDown + vertUp + vertDown

	return newVal

#Checks whether or not there is a win condition. Similar to N-Queens.
def checkWin(symbol):
	verticalWin = False
	diagonalUpWin = False
	diagonalDownWin = False
	horizontalWin = False

	for row in range(5,-1,-1):
		for col in range(0,7):
			if board[row][col] != " " and board[row][col] == symbol:
				verticalWin = checkVertical(row, col, symbol)
				diagonalUpWin = checkDiagonalUp(row, col, symbol)
				diagonalDownWin = checkDiagonalDown(row, col, symbol)
				horizontalWin = checkHorizontal(row, col, symbol)

			if verticalWin == True or diagonalUpWin == True or  diagonalDownWin == True or horizontalWin == True:
				return True
	return False

#Checks for a vertical win condition
def checkVertical(row, col, symbol):
	if (row - 3) < 0:
		return False
	else:
		for nextRows in range(1, 4):
			if board[row - nextRows][col] == " ":
				return False
			elif board[row - nextRows][col] != symbol:
				return False
	return True

#Checks for a diagonal win condition
def checkDiagonalUp(row, col, symbol):
	if (row - 3) < 0:
		return False
	if(col + 3) > 6:
		return False
	else:
		for nextDiag in range(1, 4):
			if board[row - nextDiag][col + nextDiag] == " ":
				return False
			elif board[row - nextDiag][col + nextDiag] != symbol:
				return False
	return True

#Checks for a diagonal win condition
def checkDiagonalDown(row, col, symbol):
	if (row + 3) > 5:
		return False
	if(col + 3) > 6:
		return False
	else:
		for nextDiag in range(1, 4):
			if board[row + nextDiag][col + nextDiag] == " ":
				return False
			elif board[row + nextDiag][col + nextDiag] != symbol:
				return False
	return True

#Checks for a horizontal win condition
def checkHorizontal(row, col, symbol):
	if (col + 3) > 6:
		return False
	else:
		for nextCols in range(1, 4):
			if board[row][col + nextCols] == " ":
				return False
			elif board[row][col + nextCols] != symbol:
				return False
	return True

#Updates the values in a moveVal array
def updateMoveVals(symbol, tMoves, tBoard):
	
	for col in range(0,7):
		for row in range(5,currentRow[col] -1,-1):
			if board[row][col] == " ":
				tMoves[row][col] = getVal(row, col, symbol, tBoard)
	return tMoves

#Copy the arrays to prevent overwriting data
def copyBoardAndVals(arr):
	copiedArr = []
	tempArr = []

	for x in range(0, 6):
		tempArr = []
		for y in range(0,7):
			tempArr.append(arr[x][y])
		copiedArr.append(tempArr)

	return copiedArr

#Takes the move that is best for the AI
def minimizePlayerBoardVal():
	smallestMax = 0
	bestCol = -1

	#If a value is 999, a win condition is met. Move there.
	for x in range(0, 7):
		if moveVals[currentRow[x]][x] == 999:
			return x

	#Check future board states
	for col in range(0,7):
		tempBoard = copyBoardAndVals(board)
		tempMoveVals = copyBoardAndVals(moveVals)
		tempCurRow = currentRow[:]

		#Since we want to minimize the player's values, update values as if they had another piece there.
		tempBoard[tempCurRow[col]][col] = "O"
		tempCurRow[col] -= 1
		tempMoveVals = updateMoveVals("O", tempMoveVals, tempBoard)

		#Take the largest value, preventing the player from taking that option after their move. 
		largestMax = 0
		for nextCols in range(0,7):
			if tempMoveVals[currentRow[nextCols]][nextCols] > largestMax:
				largestMax = tempMoveVals[currentRow[nextCols]][nextCols]
				bestCol = nextCols
		if largestMax > smallestMax:
			smallestMax = largestMax
			bestCol = nextCols 
			
	return bestCol
		
#Prompt user for a move
def playerPlays():
	global board
	global moveVals
	global userIn

	displayBoard()

	userIn = input("Your move!\nEnter the column of your move: ")

	if (re.search(r'(exit|quit)', userIn, re.I) != None):
		sys.exit()

	if (re.search(r'[1234567]', userIn, re.I) == None):
		print("Invalid input. Please enter a number between 1 and 7.")
		while re.search(r'[1234567]', userIn, re.I) == None:
			userIn = input("Enter a valid column: ")

	while (int(userIn) > 7 or int(userIn) == 0 or currentRow[int(userIn) - 1] < 0):
		print("Invalid move! Please try again.")
		userIn = input("Enter a valid column: ")
	print()

	#Set the current value to 0 since that space has been occupied
	moveVals[currentRow[int(userIn)-1]][int(userIn)-1] = 0
	#Update the board
	updateBoard(int(userIn) - 1, 1)
	#Updates the values for the AI since it goes next
	moveVals = updateMoveVals("X", moveVals, board)

#Computer makes it's move. Currently, the move it makes is random.
def comPlays():
	global board
	global moveVals
	playInCol = -1

	#For each possible move, calculates the player values and chooses the move that has the next smallest maximum
	playInCol = minimizePlayerBoardVal()

	moveVals[currentRow[playInCol]][playInCol] = 0
	updateBoard(playInCol, 2)
	#Updates the values for the player to properly calculate moveVals
	moveVals = updateMoveVals("O", moveVals, board)

	print("The computer placed a piece in column " + str(playInCol + 1) + "!")

#Runs the game
#Alternates turns until a winner is found or the board is filled
def playGame():
	winner = False
	playerSymbol = "O"
	comSymbol = "X"

	while numMoves != 42 and winner == False:

		playerPlays()
		if numMoves >= 7:
			winner = checkWin(playerSymbol)
			if winner == True:
				print("You win!")
				break;

		if numMoves < 42 and winner == False:
			comPlays()
			if numMoves >= 7:
				winner = checkWin(comSymbol)
				if winner == True:
					print("You lose!")
					break;
	if winner == False:
		print("Tie game!")

	displayBoard()

#Runs the program
def main():
	if len(sys.argv) > 1:
		uStr = sys.argv[1]
		if (re.search(r'(help)', uStr, re.I) != None):
			print()
			print("Welcome to my connect 4 game!")
			print("The board will be displayed as a grid on this command prompt. It will look like this:")
			initializeBoard()
			displayBoard()
			tempIn = input("Press enter to continue...")
			print()
			print("You will get the first move. Each column has a number associated with it.")
			print("Simply enter the number of the desired column and a piece will be placed there.")
			print("Your pieces are represented as a \"O\" and the computer is represented as a \"X\".")
			tempIn = input("Press enter to continue...")
			print()
			print("For example, if we enter \"3\":")
			updateBoard(2, 1)
			displayBoard()
			print("Our piece is set! The first to connect 4 wins. If you get tired of playing, type \"quit\" or \"exit\".")
			print("I hope you enjoy the game!")
			tempIn = input("Press enter to start the game!")
		else:
			print()
			print("Invalid command. Restart and type \"help\" if you do not wish to immediately start the game.")
			print("You may type \"quit\" or \"exit\" to end the game.")
	print()
	print("If you need help, type \"help\" when running this program from the command line.")
	print()
	initializeBoard()
	playGame()

if __name__ == '__main__':
	main()