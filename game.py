
import math
import numpy as np
import random
import abc

class GameState(abc.ABC):
    turn = 1
    lastMove = 0
    turnCount = 0
    @abc.abstractmethod
    def copy(self):
        pass
    @abc.abstractmethod
    def display(self):
        pass
    @abc.abstractmethod
    def getMoves (self):
        pass
    @abc.abstractmethod
    def applyMove (self, move):
        pass
    @abc.abstractmethod
    def gameResult(self):
        pass
    @abc.abstractmethod
    def get_user_move(self):
        pass
    @abc.abstractmethod
    def heuristic(self, player):
        pass

class NoughtsAndCrosses(GameState):
    def __init__(self):
        self.board = np.zeros((3, 3), int)
        self.turn = 1
        self.lastMove = None
        self.turnCount = 0
        self._moves = "Not recorded"
        self._result = "Not recorded"

    def copy(self):
        new = NoughtsAndCrosses()
        new.board = self.board.copy()
        new.turn = self.turn
        new.lastMove = self.lastMove
        new.turnCount = self.turnCount
        return new

    def display(self):
        symbols = {0: "_", 1: "O", -1: "X"}
        for row in self.board:
            print(" ".join(symbols[x] for x in row))
        print(" ")

    def getMoves (self):
        if type(self._moves) is str:
            moves = []
            for i in range(3):
                for j in range(3):
                    if self.board[i, j] == 0:
                        moves.append((i, j))
            self._moves = moves
            return moves
        else:
            return self._moves.copy()

    def applyMove (self, move):
        newState = self.copy()
        newState.board[move] = self.turn
        newState.turn *= -1
        newState.lastMove = move
        newState.turnCount += 1
        return newState

    def compute_gameResult(self):
        board = self.board
        for row in range(3):
            if board[row, 0] != 0 and board[row, 0] == board[row, 1] == board[row, 2]:
                return board[row, 0]
        for col in range(3):
            if board[0, col] != 0 and board[0, col] == board[1, col] == board[2, col]:
                return board[0, col]
        if board[0, 0] != 0 and board[0, 0] == board[1, 1] == board[2, 2]:
            return board[0, 0]
        if board[0, 2] != 0 and board[0, 2] == board[1, 1] == board[2, 0]:
            return board[0, 2]
        if (board != 0).all():
            return 0
        else:
            return None

    def gameResult(self):
        if type(self._result) is str:
            self._result = self.compute_gameResult()
        return self._result         

    def get_user_move(self):
        row = int(input("Row: "))
        col = int(input("Column: "))
        return (row, col)

    def heuristic(self, player):
        return 0

class Connect4(GameState):
    def __init__(self):
        self.board = np.zeros((6, 7), int)
        self.turn = 1
        self.lastMove = None
        self.turnCount = 0
        self._moves = "None recorded"
        self._result = "None recorded"

    def copy(self):
        new = Connect4()
        new.board = self.board.copy()
        new.turn = self.turn
        new.lastMove = None
        new.turnCount = 0
        return new

    def display(self):
        symbols = {0: "_", 1: "O", -1: "X"}
        for row in reversed(self.board):
            print(" ".join(symbols[x] for x in row))
        print("0 1 2 3 4 5 6")
        print(" ")

    def compute_getMoves(self):
        moves = []
        for i in range(7):
            if self.board[5, i] == 0:
                    moves.append(i)
        return moves

    def getMoves (self):
        if type(self._moves) is str:
           self._moves = self.compute_getMoves()
        return self._moves.copy()

    def applyMove (self, move):
        newState = self.copy()
        i = 0
        while newState.board[i, move] != 0 and i < 7:
            i += 1
        newState.board[i, move] = self.turn
        newState.turn *= -1
        newState.lastMove = move
        newState.turnCount += 1
        return newState

    def compute_gameResult(self):
        board = self.board
        rows = 6
        cols = 7
        for row in range(rows):
            for col in range(cols):
                if board[row, col] != 0 and (
                    (col < cols - 3 and board[row, col] == board[row, col + 1] == board[row, col + 2] == board[row, col + 3]) # horizontals
                    or (row < rows - 3 and board[row, col] == board[row + 1, col] == board[row + 2, col] == board[row + 3, col]) # verticals
                    or (row < rows - 3 and col < cols - 3 and board[row, col] == board[row + 1, col + 1] == board[row + 2, col + 2] == board[row + 3, col + 3]) # diagonals sinister
                    or (row < rows - 3 and col >= 3 and board[row, col] == board[row + 1, col - 1] == board[row + 2, col - 2] == board[row + 3, col - 3]) # diagonals dexter
                ):
                    return board[row, col]
        if (board != 0).all():
            return 0
        else:
            return None

    def gameResult(self):
        if type(self._result) is str:
            self._result = self.compute_gameResult()
        return self._result

    def get_user_move(self):
        col = int(input("Column: "))
        return col

    def heuristic(self, player):
        return 0

class NineMensMorris(GameState):
    def __init__(self):
        self.board = np.zeros((8, 3), int) # First index represents position on the square clockwise, starting with 0 at the top. Second index represents which of the three squares, with 0 being the innermost one.
        self.turn = 1
        self.supply = {1: 9, -1: 9} # Supply of men yet to be placed on the board.
        self.lastMove = None
        self.turnCount = 0
        self._moves = "None recorded"
        self._result = "None recorded"
        self._menRemaining = {1: "na", -1: "na"}

    def copy(self):
        new = NineMensMorris()
        new.board = self.board.copy()
        new.turn = self.turn
        new.supply = self.supply.copy()
        new.lastMove = self.lastMove
        new.turnCount = self.turnCount
        return new

    def display(self):
        symbols = {3: " ", 0: "_", 1: "O", -1: "X"}
        boardLayout = np.zeros((7, 7), int) + 3
        squarePositions = np.array([[-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1]])
        for j in range(3):
            for i in range(8):
                boardLayout[tuple(np.array([3, 3]) + squarePositions[i,:] * (j + 1))] = self.board[i, j]
        for row in boardLayout:
            print(" ".join(symbols[x] for x in row))
        print(" ")
        print("#############")
        print(" ")

    def is_in_mill(self, player, position, ignore=None):
        squarePos, square = position
        def at(i, j):
            if (i, j) == ignore:
                return 0
            else:
                return self.board[i, j]
        if squarePos % 2 == 0: # Edge positions
            if (player == at(squarePos, (square + 1) % 3) == at(squarePos, (square + 2) % 3)
                or player == at((squarePos - 1) % 8, square) == at((squarePos + 1) % 8, square)
            ):
                return True
            else:
                return False
        else: # Corner positions
            if (player == at((squarePos + 1) % 8, square) == at((squarePos + 2) % 8, square)
                or player == at((squarePos - 1) % 8, square) == at((squarePos - 2) % 8, square)
            ):
                return True
            else:
                return False

    def menRemaining (self, player):
        if type(self._menRemaining[player]) is str:
            self._menRemaining[player] = self.supply[player] + np.sum(self.board == player)
        return self._menRemaining[player]

    def compute_getMoves(self):
        moves = []
        movements = []
        player = self.turn
        board = self.board
        playerPieces = []
        opponentPieces = []
        emptyPositions = []
        vulnerable = []
        for i in range(8):
            for j in range(3):
                pos = (i, j)
                if board[pos] == player:
                    playerPieces.append(pos)
                elif board[pos] == -player:
                    opponentPieces.append(pos)
                else:
                    emptyPositions.append(pos)
        if self.supply[player] > 0: # Placement phase
            for pos in emptyPositions:
                if board[pos] == 0:
                    movements.append({"start": None, "end": pos, "remove": None})
        else: # Movement phase
            flying = self.menRemaining(player) <= 3
            for piece in playerPieces:
                squarePos, square = piece
                if flying:
                    adjacent = emptyPositions
                else:
                    adjacent = [((squarePos + 1) % 8, square), ((squarePos - 1) % 8, square)]
                    if squarePos % 2 == 0:
                        if square != 0:
                            adjacent.append((squarePos, square - 1))
                        if square != 2:
                            adjacent.append((squarePos, square + 1))
                for pos in adjacent:
                    if board[pos] == 0:
                        movements.append({"start": piece, "end": pos, "remove": None})
        for movement in movements:
            if self.is_in_mill(player, movement["end"], movement["start"]):
                if len(vulnerable) == 0:
                    vulnerable = [x for x in opponentPieces if not self.is_in_mill(-player, x)]
                    if len(vulnerable) == 0:
                        vulnerable = opponentPieces
                for opponent in vulnerable:
                    movement["remove"] = opponent
                    moves.insert(0, movement.copy()) # (Add capturing moves to the front of the list.)
            else:
                moves.append(movement)
        return moves  

    def getMoves (self):
        if type(self._moves) is str:
            self._moves = self.compute_getMoves()
        return self._moves.copy()

    def applyMove (self, move):
        newState = self.copy()
        if move["start"] is not None:
            newState.board[move["start"]] = 0
        newState.board[move["end"]] = self.turn
        if newState.supply[self.turn] > 0:
            newState.supply[self.turn] -= 1
        if move["remove"] is not None:
            newState.board[move["remove"]] = 0
        newState.turn *= -1
        newState.lastMove = move
        newState.turnCount += 1
        return newState

    def compute_gameResult(self):
        if self.menRemaining(self.turn) < 3 or len(self.getMoves()) == 0:
            return -self.turn
        elif self.turnCount > 100:
            return 0
        else:
            return None

    def gameResult(self):
        if type(self._result) is str:
            self._result = self.compute_gameResult()
        return self._result

    def get_user_move(self):
        if self.supply[self.turn] == 0:
            print("Piece to move:")
            square = int(input("Square: "))
            sqPos = int(input("Position: "))
            piece = (sqPos, square)
        else:
            piece = None
        print("Move to...")
        square = int(input("Square: "))
        sqPos = int(input("Position: "))
        pos = (sqPos, square)
        remove = None
        if self.is_in_mill(self.turn, pos, piece):
            print("Remove:")
            square = int(input("Square: "))
            sqPos = int(input("Position: "))
            remove = (sqPos, square)
        return {"start": piece, "end": pos, "remove": remove}

    def heuristic(self, player):
        #return (self.menRemaining(-self.turn) - futureState.menRemaining(-self.turn)) - (self.menRemaining(self.turn) - futureState.menRemaining(self.turn))
        #return futureState.menRemaining(self.turn) / self.menRemaining(self.turn) - futureState.menRemaining(-self.turn) / self.menRemaining(-self.turn)
        playerMaterial = self.menRemaining(player)
        opponentMatrial = self.menRemaining(-player)
        return playerMaterial / (playerMaterial + opponentMatrial)

class Draughts(GameState):
    def __init__(self):
        self.board = np.zeros((8, 8), int)
        for i in range(12): # Starting position:
            row = i // 4
            col = i % 4 * 2
            if row == 1:
                col = col + 1
            self.board[row, col] = 1
            self.board[row + 5, (col + 1) % 8] = -1
        self.turn = 1
        self.lastMove = None
        self.turnCount = 0
        self._moves = "None recorded"
        self._result = "None recorded"

    def copy(self):
        new = Draughts()
        new.board = self.board.copy()
        new.turn = self.turn
        new.lastMove = self.lastMove
        new.turnCount = self.turnCount
        return new

    def display(self):
        symbols = {0: "_", 1: "o", 2: "O", -1: "x", -2: "X"}
        for row in reversed(self.board):
            print(" ".join(symbols[x] for x in row))
        print(" ")

    def get_jumps(self, piece_type, start, ignore): # Returns a list of single jumps available to a piece at start.
        jumps = []
        def at(row, col):
            if (row, col) in ignore:
                return 0
            else:
                return self.board[row, col]
        row, col = start
        if abs(piece_type) == 2 or piece_type > 0:
            if row < 6 and col < 6 and at(row + 2, col + 2) == 0 and piece_type * at(row + 1, col + 1) < 0:
                jumps.append({"end": (row + 2, col + 2), "capture": (row + 1, col + 1)})
            if row < 6 and col > 1 and at(row + 2, col - 2) == 0 and piece_type * at(row + 1, col - 1) < 0:
                jumps.append({"end": (row + 2, col - 2), "capture": (row + 1, col - 1)})
        if abs(piece_type) == 2 or piece_type < 0:
            if row > 1 and col < 6 and at(row - 2, col + 2) == 0 and piece_type * at(row - 1, col + 1) < 0:
                jumps.append({"end": (row - 2, col + 2), "capture": (row - 1, col + 1)})
            if row > 1 and col > 1 and at(row - 2, col - 2) == 0 and piece_type * at(row - 1, col - 1) < 0:
                jumps.append({"end": (row - 2, col - 2), "capture": (row - 1, col - 1)})
        return jumps

    def computeCapturingMoves(self, move, piece_type, ignore): # Adds all the possible capturing moves for a given piece to the _moves cache.
        jumps = self.get_jumps(piece_type, move["steps"][-1], ignore)
        if len(jumps) == 0: # No more captures to be made:
            if len(move["steps"]) > 1: # At least one step from the start to count as a move.
                self._moves.append(move)
        else: # Look for further jumps:
            for jump in jumps:
                new = {
                    "steps": move["steps"] + [jump["end"]], 
                    "capture": move["capture"] + [jump["capture"]]
                }
                self.computeCapturingMoves(new, piece_type, ignore + [jump["capture"]])

    def compute_moves(self):
        self._moves = []
        moves = self._moves
        player = self.turn
        board = self.board
        playerPieces = []
        for i in range(8):
            for j in range(8):
                pos = (i, j)
                if board[pos] * player > 0:
                    playerPieces.append(pos)
        # Capturing moves:
        for piece in playerPieces:
            row, col = piece
            piece_type = board[piece]
            proto_move = {"steps": [piece], "capture": []}
            self.computeCapturingMoves(proto_move, piece_type, [piece])
        # If there's none, look for non-capturing moves:
        if len(moves) == 0:
            for piece in playerPieces:
                row, col = piece
                piece_type = board[piece]
                if abs(piece_type) == 2 or piece_type > 0:
                    if row < 7 and col < 7 and board[row + 1, col + 1] == 0:
                        moves.append({"steps": [piece, (row + 1, col + 1)], "capture": []})
                    if row < 7 and col > 0 and board[row + 1, col - 1] == 0:
                        moves.append({"steps": [piece, (row + 1, col - 1)], "capture": []})
                if abs(piece_type) == 2 or piece_type < 0:
                    if row > 0 and col < 7 and board[row - 1, col + 1] == 0:
                        moves.append({"steps": [piece, (row - 1, col + 1)], "capture": []})
                    if row > 0 and col > 0 and board[row - 1, col - 1] == 0:
                        moves.append({"steps": [piece, (row - 1, col - 1)], "capture": []}) 

    def getMoves (self):
        if type(self._moves) is str:
            self.compute_moves()
        return self._moves.copy()

    def applyMove (self, move):
        newState = self.copy()
        start = move["steps"][0]
        end = move["steps"][-1]
        newState.board[start] = 0
        if self.turn == 1 and end[0] == 7 or self.turn == -1 and end[0] == 0:
            newState.board[end] = 2 * self.turn # Promotion.
        else:
            newState.board[end] = self.board[start]
        for capture in move["capture"]:
            newState.board[capture] = 0
        newState.turn *= -1
        newState.lastMove = move
        newState.turnCount += 1
        return newState

    def compute_gameResult(self):
        if len(self.getMoves()) == 0:
            return -self.turn
        elif self.turnCount > 100:
            return 0
        else:
            return None

    def gameResult(self):
        if type(self._result) is str:
            self._result = self.compute_gameResult()
        return self._result

    def get_user_move(self): 
        pass # Can't be bothered until I build a UI.
    
    def heuristic(self, player):
        playerMaterial = np.sum(np.abs(self.board[self.board * player > 0]))
        allMaterial = np.sum(np.abs(self.board))
        return playerMaterial / allMaterial

class Brandubh(GameState):
    def __init__(self, throneReentry = False, throneProtection = True, kingCanCapture = True):
        self.board = np.array([ # Starting position:
            [   0,  0,  0,  1,  0,  0,  0],
            [   0,  0,  0,  1,  0,  0,  0],
            [   0,  0,  0, -1,  0,  0,  0],
            [   1,  1, -1, -2, -1,  1,  1],
            [   0,  0,  0, -1,  0,  0,  0],
            [   0,  0,  0,  1,  0,  0,  0],
            [   0,  0,  0,  1,  0,  0,  0]
        ], int)
        self.turn = 1
        self.lastMove = None
        self.turnCount = 0
        self._moves = "None recorded"
        self._result = "None recorded"

        self.throneReentry = throneReentry
        self.throneProtection = throneProtection
        self.kingCanCapture = kingCanCapture

        self.directions = {(0, 1), (0, -1), (1, 0), (-1, 0)}
        self.corners = {(0, 0), (0, 6), (6, 0), (6, 6)}
        self.throne = (3, 3)
        self.throneside = {(4, 3), (2, 3), (3, 4), (3, 2)}

    def copy(self):
        new = Brandubh()
        new.board = self.board.copy()
        new.turn = self.turn
        new.lastMove = self.lastMove
        new.turnCount = self.turnCount
        return new

    def display(self):
        symbols = {0: "_", 1: "o", -1: "x", -2: "X"}
        for row in reversed(self.board):
            print(" ".join(symbols[x] for x in row))
        print(" ")

    def getRelativePosition(self, position, direction, distance):
        row = position[0] + direction[0] * distance
        col = position[1] + direction[1] * distance
        if row >= 0 and row <= 6 and col >= 0 and col <= 6:
            return (row, col)
        else: # off the board
            return None

    def compute_moves(self):
        self._moves = []
        moves = self._moves
        player = self.turn
        board = self.board
        for i in range(7):
            for j in range(7):
                pos = (i, j)
                piece = board[pos]
                if piece * player > 0:
                    for direction in self.directions:
                        distance = 1
                        while True:
                            target = self.getRelativePosition(pos, direction, distance)
                            if target is not None and board[target] == 0:
                                if (target != self.throne or (self.throneReentry and (piece == 2))) and (target not in self.corners or abs(piece) == 2):
                                    moves.append({"start": pos, "end": target})
                                distance += 1
                            else:
                                break

    def getMoves (self):
        if type(self._moves) is str:
            self.compute_moves()
        return self._moves.copy()

    def applyMove (self, move):
        newState = self.copy()
        start = move["start"]
        end = move["end"]
        board = newState.board
        board[start] = 0
        piece = self.board[start]
        board[end] = piece
        if self.kingCanCapture or abs(piece) == 1:
            for direction in self.directions:
                one_away = self.getRelativePosition(end, direction, 1)
                two_away = self.getRelativePosition(end, direction, 2)
                if one_away is not None and two_away is not None:
                    royalCapture = True
                    if self.throneProtection:
                        if abs(board[one_away]) == 2 and one_away in (self.throneside | {self.throne}): # The king on or beside the throne
                            for dir in self.directions - {direction, (-1 * direction[0], -1 * direction[1])}: # perpendicular directions
                                square = self.getRelativePosition(one_away, dir, 1)
                                if not (board[square] * piece > 0 or square == self.throne):
                                    royalCapture = False
                    if (royalCapture
                        and board[one_away] * piece < 0 
                        and (board[two_away] * piece > 0 or (board[two_away] == 0 and two_away in (self.corners | {self.throne})))
                    ):
                        board[one_away] = 0
        newState.turn *= -1
        newState.lastMove = move
        newState.turnCount += 1
        return newState

    def compute_gameResult(self):
        for corner in self.corners:
            if self.board[corner] == -2:
                return -1
        if np.sum(self.board == -2) < 1:
            return 1
        if self.turnCount > 100 or len(self.getMoves()) == 0:
            return 0
        else:
            return None

    def gameResult(self):
        if type(self._result) is str:
            self._result = self.compute_gameResult()
        return self._result

    def get_user_move(self): 
        pass # Can't be bothered until I build a UI.

    def heuristic(self, player):
        pieceValues = {0: 0, 1: 1, -1: 1.75, -2: 1}
        playerMaterial = sum([pieceValues[x] for x in self.board[self.board * player > 0]])
        allMaterial = sum([pieceValues[x] for x in self.board.ravel()])
        return playerMaterial / allMaterial

def agent_random(state):
    moves = state.getMoves()
    return random.choice(moves)

def agent_user(state):
    move = state.get_user_move()
    if (move in state.getMoves()):
        return move
    else:
        print("Invalid move")
        move = agent_user(state)
    return move  

def treeSearch(initialState, state, depth, alpha, beta):
    inf = 1000
    player = initialState.turn
    turn = state.turn
    result = state.gameResult()
    if result == 0:
        return 0
    elif result is not None:
        return player * result * (inf + depth)
    elif depth == 0:
        return state.heuristic(initialState.turn) - initialState.heuristic(initialState.turn)
    else:
        moves = state.getMoves()
        if player == turn:
            value = -np.inf
            for move in moves:
                value = max(value, treeSearch(initialState, state.applyMove(move), depth - 1, alpha, beta))
                if value >= beta:
                    break
                alpha = max(alpha, value)
            return value
        else:
            value = np.inf
            for move in moves:
                value = min(value, treeSearch(initialState, state.applyMove(move), depth - 1, alpha, beta))
                if value <= alpha:
                    break
                beta = min(beta, value)
            return value

def agent_treeSearch(state, depth=5):
    moves = state.getMoves()
    scored_moves = [{"move": move, "score": treeSearch(state, state.applyMove(move), depth - 1, -np.inf, np.inf)} for move in moves]
    #print(scored_moves)
    best_score = max(x["score"] for x in scored_moves)
    best_moves = [x["move"] for x in scored_moves if x["score"] == best_score]
    return random.choice(best_moves)

class MCTS_Node:
    def __init__(self, state, parent=None, early_terminate=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0.0
        self.untried_moves = state.getMoves()
        self.early_terminate = early_terminate

    def is_terminal(self):
        return self.state.gameResult() is not None

    def is_fully_expanded(self):
        return len(self.untried_moves) == 0

    def expand(self):
        move = self.untried_moves.pop()
        child = MCTS_Node(self.state.applyMove(move), self, self.early_terminate)
        self.children.append(child)
        return child

    def best_child(self):
        for child in self.children:
            if child.visits == 0:
                return child

        def ucb1(child):
                return child.wins / child.visits + math.sqrt(2) * math.sqrt(math.log(self.visits) / child.visits)
        
        return max(self.children, key=ucb1)

    def get_root(self):
        node = self
        while True:
            if node.parent is None:
                return node
            else:
                node = node.parent

    def rollout(self):
        state = self.state
        i = 0
        while self.early_terminate is None or i < self.early_terminate:
            result = state.gameResult()
            if result is not None:
                return result
            else:
                move = random.choice(state.getMoves())
                state = state.applyMove(move)
            i += 1
        result = state.gameResult()
        if result is not None:
            return result
        else:
            return state.heuristic(1) * 2 - 1

    def backPropagate(self, result):
        self.visits += 1
        #if result == 0:
        #    self.wins += 0.5
        #elif result == -self.state.turn: # I think???
        #    self.wins += 1
        self.wins += (result * -self.state.turn + 1) / 2 # I think?
        if self.parent is not None:
            self.parent.backPropagate(result)

    def sever(self):
        self.parent = None

    def get_child(self, move):
        for child in self.children:
            if child.state.lastMove == move:
                return child
        return None

def agent_MCTS(state, iterations=500, memory=None, early_terminate=None):
    root = MCTS_Node(state, early_terminate=early_terminate)
    if memory is None:
        memory = []
    elif state.turnCount < 2:
        memory.clear()
    elif len(memory) > 0:
        previous_node = memory[0]
        current_node = previous_node.get_child(state.lastMove)
        if current_node is not None:
            current_node.sever()
            root = current_node
    for i in range(iterations):
        node = root
        while not node.is_terminal() and node.is_fully_expanded():
            node = node.best_child()
        if not node.is_terminal() and not node.is_fully_expanded():
            node = node.expand()
        result = node.rollout()
        node.backPropagate(result)
    best_node = max(root.children, key=lambda child: child.visits)
    memory.clear()
    memory.append(best_node)
    return best_node.state.lastMove

def play(game, agent1, agent2, display=True, game_kwargs={}, agent1_kwargs={}, agent2_kwargs={}):
    state = game(**game_kwargs)
    if display:
        state.display()
    gameRunning = True
    while gameRunning:
        if state.turn == 1:
            move = agent1(state, **agent1_kwargs)
        else:
            move = agent2(state, **agent2_kwargs)
        state = state.applyMove(move)
        if display:
            state.display()
        if state.gameResult() is not None:
            gameRunning = False
    if display:
        print("Game over")
    return state

def playoff(N, game, agent1, agent2, game_kwargs={}, agent1_kwargs={}, agent2_kwargs={}):
    results = []
    durations = []
    values = {0: "Draw", 1: "Player 1", -1: "Player 2"}
    for i in range(N):
        state = play(game, agent1, agent2, False, game_kwargs, agent1_kwargs, agent2_kwargs)
        results.append(state.gameResult())
        durations.append(state.turnCount // 2)
        print(f"{i + 1}. {values[state.gameResult()]} ({state.turnCount // 2} moves)")
        state.display()
        print("########################")
    results = np.array(results)
    player1 = np.sum(results == 1) / len(results) * 100
    player2 = np.sum(results == -1) / len(results) * 100
    draw = np.sum(results == 0) / len(results) * 100
    print(" ")
    print(f"Player 1: {player1:.1f}")
    print(f"Player 2: {player2:.1f}")
    print(f"Draws   : {draw:.1f}")
    print(f"Median no. of moves: {np.median(durations)}")


#play(NoughtsAndCrosses, agent_MCTS, agent_treeSearch, agent1_kwargs={"iterations": 500}, agent2_kwargs={"depth": 9})
#play(Connect4, agent_treeSearch, agent_MCTS, agent1_kwargs={"depth": 8}, agent2_kwargs={"iterations": 5000, "memory": []})
#play(Connect4, agent_MCTS, agent_user, agent1_kwargs={"iterations": 5000, "memory": []})
#play(NineMensMorris, agent_treeSearch, agent_MCTS, agent1_kwargs={"depth": 5}, agent2_kwargs={"iterations": 10000, "memory": []})
play(Draughts, agent_MCTS, agent_MCTS, agent1_kwargs={"iterations": 1000, "memory": []}, agent2_kwargs={"iterations": 1000, "memory": []})
#play(Brandubh, agent_treeSearch, agent_MCTS, agent1_kwargs={"depth": 3}, agent2_kwargs={"iterations": 1000, "memory": []})
#play(Connect4, agent_MCTS, agent_user, agent1_kwargs={"iterations": 20000, "memory": []})
#play(Brandubh, agent_MCTS, agent_MCTS, game_kwargs={"throneProtection": False}, agent1_kwargs={"iterations": 10000, "memory": [], "early_terminate": 50}, agent2_kwargs={"iterations": 10000, "memory": [], "early_terminate": 50})

#playoff(100, NineMensMorris, agent_treeSearch, agent_MCTS, display=True, agent1_kwargs={"depth": 5}, agent2_kwargs={"iterations": 1000, "memory": []})
#playoff(10, Brandubh, agent_MCTS, agent_MCTS, game_kwargs={"throneProtection": True, "kingCanCapture": True}, agent1_kwargs={"iterations": 50000, "memory": [], "early_terminate": 50}, agent2_kwargs={"iterations": 50000, "memory": [], "early_terminate": 50})