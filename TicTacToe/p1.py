import mysql.connector
from datetime import datetime

# MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",           # change this
    password="yourpassword",  # change this
    database="tictactoe"
)
cursor = db.cursor()

from datetime import datetime

def login_user(username):
    cursor.execute("SELECT last_login, login_frequency FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()
    now = datetime.now()

    if user:
        last_login, freq = user
        cursor.execute("UPDATE users SET last_login=%s, login_frequency=%s WHERE username=%s",
                       (now, freq + 1, username))
    else:
        cursor.execute("INSERT INTO users (username, last_login, login_frequency) VALUES (%s, %s, %s)",
                       (username, now, 1))
    db.commit()


def logout_user(username):
    now = datetime.now()
    cursor.execute("UPDATE users SET last_logout=%s WHERE username=%s", (now, username))
    db.commit()
# ------- Define the players ---------
current_player = "player1"
opponent_player = "computer"

#----------- Log the player into the database -------
login_user(current_player)

def save_game_result(player1, player2, winner, mode):
    cursor.execute(
        "INSERT INTO game_results (player1, player2, winner, game_mode) VALUES (%s, %s, %s, %s)",
        (player1, player2, winner, mode)
    )

    # Update user stats
    cursor.execute("UPDATE users SET total_games = total_games + 1 WHERE username IN (%s, %s)",
                   (player1, player2))
    if winner == "Draw":
        cursor.execute("UPDATE users SET total_draws = total_draws + 1 WHERE username IN (%s, %s)",
                       (player1, player2))
    else:
        cursor.execute("UPDATE users SET total_wins = total_wins + 1 WHERE username=%s", (winner,))
    db.commit()


from tkinter import *

root = Tk()
root.geometry("300x400")
root.title("Tic Tac Toe")
root.resizable(0,0)

frame1 = Frame(root)
frame1.pack()
titleLabel = Label(frame1, text="Tic Tac Toe", font = ("Arial",18, "bold"),bg="Yellow", width=18, borderwidth=2)
titleLabel.grid(row=0, column=0)

optionFrame = Frame(root, bg="grey")
optionFrame.pack()

frame2 = Frame(root, bg="black", )
frame2.pack()

board={1:" ", 2:" ", 3:" ",
       4:" ", 5:" ", 6:" ",
       7:" ", 8:" ", 9:" "}

turn = "X"
game_end = False
mode="singlePlayer"

def changeModeToSinglePlayer():
    global mode, turn, game_end
    mode = "singlePlayer"
    singlePlayerButton["bg"]="green"
    multiPlayerButton["bg"]="lightgrey"
    restartGame()

def changeModeToMultiPlayer():
    global mode, turn, game_end
    mode ="multiPlayer"
    multiPlayerButton["bg"]="green"
    singlePlayerButton["bg"]="lightgrey"
    restartGame()

def updateBoard():
    for key in board.keys():
        buttons[key-1]["text"]=board[key]

def checkForWin(player):
    #row
    if board[1]==board[2]==board[3]==player:
        return True
    if board[4]==board[5]==board[6]==player:
        return True
    if board[7]==board[8]==board[9]==player:
        return True
    #column
    if board[1]==board[4]==board[7]==player:
        return True
    if board[2]==board[5]==board[8]==player:
        return True
    if board[3]==board[6]==board[9]==player:
        return True
    #Diagonal
    if board[1]==board[5]==board[9]==player:
        return True
    if board[3]==board[5]==board[7]==player:
        return True
    return False

def checkForDraw():
    return all(board[i] != " " for i in board.keys())

def restartGame():
    global game_end, turn
    game_end= False
    turn = "X"
    for button in buttons:
        button["text"]=" "
    for i in board.keys():
        board[i]=" "
    titleLabel.config(text="Tic Tac Toe", bg="Yellow", fg="black")

def minimax(board_state, isMaximizing):
    if checkForWin("O"):
        return 1
    if checkForWin("X"):
        return -1
    if checkForDraw():
        return 0
    if isMaximizing:
        bestScore = -100
        for key in board_state.keys():
            if board_state[key]==" ":
                board_state[key]="O"
                score = minimax(board_state, False)
                board_state[key]=" "
                if score>bestScore:
                    bestScore = score
        return bestScore
    else:
        bestScore = 100
        for key in board_state.keys():
            if board_state[key]==" ":
                board_state[key]="X"
                score = minimax(board_state, True)
                board_state[key]=" "
                if score<bestScore:
                    bestScore = score
        return bestScore

def playComputer():
    bestScore = -100
    bestMove = None
    for key in board.keys():
        if board[key]==" ":
            board[key]="O"
            score = minimax(board, False)
            board[key]= " "
            if score > bestScore :
                bestScore = score
                bestMove = key
    if bestMove is not None:
        board[bestMove]="O"

def play(event):
    global turn, game_end, mode

    if game_end:
        return

    button = event.widget
    try:
        clicked = buttons.index(button)+1
    except ValueError:
        return

    if board[clicked] == " ":
        board[clicked] = turn
        updateBoard()

        if checkForWin(turn):
            titleLabel.config(text=f"{turn} wins the game!", bg="Red", fg="white")
            game_end = True
            return

        if checkForDraw():
            titleLabel.config(text="Game Draw", bg="Red", fg="white")
            game_end = True
            return

        if mode == "singlePlayer":
            if turn == "X":
                turn = "O"
                playComputer()
                updateBoard()
                if checkForWin("O"):
                    titleLabel.config(text="O wins the game!", bg="Red", fg="white")
                    game_end = True
                    return
                if checkForDraw():
                    titleLabel.config(text="Game Draw", bg="Red", fg="white")
                    game_end = True
                    return
                turn = "X"
        else:
            turn = "O" if turn == "X" else "X"

singlePlayerButton = Button(optionFrame, text="Single Player", width=10, height = 1, font=("Arial", 15 ), bg="green", relief = RAISED, borderwidth=5, command=changeModeToSinglePlayer )
singlePlayerButton.grid(row=0, column=0, columnspan=1, sticky=NE)

multiPlayerButton = Button(optionFrame, text="Multi Player", width=10, height = 1, font=("Arial", 15 ), bg="lightgrey", relief = RAISED, borderwidth=5, command=changeModeToMultiPlayer )
multiPlayerButton.grid(row=0, column=1, columnspan=1, sticky=NW)

button1 = Button(frame2, text=" ", width=3, height=1, font=("Arial", 35), bg="blue", fg="white")
button1.grid(row = 0, column = 0)
button1.bind("<Button-1>", play)

button2 = Button(frame2, text=" ", width=3, height=1, font=("Arial", 35), bg="blue", fg="white")
button2.grid(row = 0, column = 1)
button2.bind("<Button-1>", play)

button3 = Button(frame2, text=" ", width=3, height=1, font=("Arial", 35), bg="blue", fg="white")
button3.grid(row = 0, column = 2)
button3.bind("<Button-1>", play)

button4 = Button(frame2, text=" ", width=3, height=1, font=("Arial", 35), bg="blue", fg="white")
button4.grid(row = 1, column = 0)
button4.bind("<Button-1>", play)

button5 = Button(frame2, text=" ", width=3, height=1, font=("Arial", 35), bg="blue", fg="white")
button5.grid(row = 1, column = 1)
button5.bind("<Button-1>", play)

button6 = Button(frame2, text=" ", width=3, height=1, font=("Arial", 35), bg="blue", fg="white")
button6.grid(row = 1, column = 2)
button6.bind("<Button-1>", play)

button7 = Button(frame2, text=" ", width=3, height=1, font=("Arial", 35), bg="blue", fg="white")
button7.grid(row = 2, column = 0)
button7.bind("<Button-1>", play)

button8 = Button(frame2, text=" ", width=3, height=1, font=("Arial", 35), bg="blue", fg="white")
button8.grid(row = 2, column = 1)
button8.bind("<Button-1>", play)

button9 = Button(frame2, text=" ", width=3, height=1, font=("Arial", 35), bg="blue", fg="white")
button9.grid(row = 2, column = 2)
button9.bind("<Button-1>", play)

restartButton = Button(frame2, text="Restart Game", width=10, height=1, font=("Arial", 10), bg="orange", fg="blue", relief=RAISED, borderwidth=5, command=restartGame)
restartButton.grid(row=4, column=0, columnspan=3)

buttons=[button1, button2, button3, button4, button5, button6, button7, button8, button9]

root.mainloop()