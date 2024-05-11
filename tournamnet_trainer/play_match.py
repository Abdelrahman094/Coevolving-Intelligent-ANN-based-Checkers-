from enums import Player, Position
from game import AI_Game
from train_agents import AgentTrainer

RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128,128,128)

def play_match(white: AgentTrainer, black: AgentTrainer) -> int:
    """
    Play a match between two agents and return the score.
    """
    game = AI_Game()


    while not game.winner():
        # Get current player
        player = white if game.turn == WHITE else black
        # Get the move from the player
        move = player.get_move(game.get_game_state())
        game.select(*move.split('-'))
        game.change_turn()

    # Calculate the score
    winner = game.winner()
    score = 250
    for row in game.board.board:
        for piece in row:
            if piece and piece.color == winner:
                if piece.king:
                    score += 7
                else:
                    score += 3

    # Adjust score based on game length
    score -= len(game.board.board)

    # Set the result, if white won, the score is positive, if black won, the score is negative
    return score if winner == WHITE else -score
