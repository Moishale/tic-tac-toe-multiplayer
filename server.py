import socket
import threading


HOST = '192.168.1.115'
PORT = 9090


class TicTacToe:
    def __init__(self):
        self.you = ''
        self.opponet = ''
        self.turn = 'O'
        self.board = []
        self.game_over = False
        self.winner = None
        self.counter = 0
        self.create_board()

    def create_board(self):
        for i in range(3):
            row = []
            for j in range(3):
                row.append('-')
            self.board.append(row)

    def show_board(self):
        for row in self.board:
            for item in row:
                print(item, end=" ")
            print()

    def parse_move(self, move):
        return [int(n)-1 for n in move.split(',')]

    def fix_move(self, row, col, player):
        if self.game_over:
            return

        self.counter += 1
        self.board[row][col] = player
        self.show_board()

        if self.is_player_win():
            if self.winner == self.you:
                print('You win!')
                exit()
            if self.winner == self.opponet:
                print('You lose!')
                exit()
        else:
            if self.counter == 9:
                print('Its a draw!')
                exit()

    def valid_move(self, row, col):
        if self.board[row][col] == 'O' or self.board[row][col] == 'X':
            return False
        return True

    def swap_player_turn(self):
        self.turn = self.you if self.turn == self.opponet else self.opponet

    def handle(self, client):
        while not self.game_over:
            if self.turn == self.you:
                move = input(
                    "Enter row and column numbers to fix spot(row,column): ")
                row, col = self.parse_move(move)
                if self.valid_move(row, col):
                    self.fix_move(row, col, self.you)
                    print()
                    client.send(move.encode('utf-8'))
                else:
                    print('Invalid Move!')
                    continue
            else:
                data = client.recv(1024)
                if not data:
                    client.close()
                    break
                else:
                    row, col = self.parse_move(data.decode('utf-8'))
                    self.fix_move(row, col, self.opponet)
            self.swap_player_turn()
        client.close()

    def is_player_win(self):
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] != '-':
                self.winner = self.board[row][0]
                self.game_over = True
                return True
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != '-':
                self.winner == self.board[0][col]
                self.game_over = True
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '-':
            self.winner == self.board[0][0]
            self.game_over == True
            return True
        if self.board[2][0] == self.board[1][1] == self.board[0][2] != '-':
            self.winner = self.board[2][0]
            self.game_over = True
            return True
        return False

    def host_game(self, host, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen(1)

        client, addr = server.accept()
        self.you = 'X'
        self.opponet = 'O'
        threading.Thread(target=self.handle, args=(client,)).start()
        server.close()

    def connect_to_game(self, host, port):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))

        self.you = 'O'
        self.opponet = 'X'
        threading.Thread(target=self.handle, args=(client,)).start()


game = TicTacToe()
game.host_game(HOST, PORT)
