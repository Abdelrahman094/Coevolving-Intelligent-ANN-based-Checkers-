from play_match import play_match
from train_agents import AgentTrainer

def play_battle(player_list: list[AgentTrainer]):
    for i in range(len(player_list) - 1):
        for j in range(i + 1, len(player_list)):
            score = 0

            # Play the match
            score += play_match(player_list[j], player_list[i])

            # Play the reverse match
            score += play_match(player_list[i], player_list[j]) * -1

            player_list[j].set_result(score, player_list[i])
            player_list[i].set_result(-1 * score, player_list[j])

    player_list.sort(key=lambda x: x.score, reverse=True)

    return player_list