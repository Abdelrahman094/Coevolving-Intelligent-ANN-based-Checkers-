
from play_match import play_match
from train_agents import AgentTrainer

def play(player_a: AgentTrainer, player_b: AgentTrainer) -> int:
    """
    Play a match between two agents and return the score.
    
    :param player_a: The first agent
    :param player_b: The second agent
    :return: The score of the match
    """
    score = 0
    # Play the match
    score += play_match(player_a, player_b)
    # Play the reverse match
    score -= play_match(player_b, player_a)
    return score