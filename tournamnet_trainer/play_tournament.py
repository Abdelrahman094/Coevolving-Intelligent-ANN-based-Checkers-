import math
from typing import List
from play import play

from train_agents import AgentTrainer
async def play_tournament(player_list: List[AgentTrainer]) -> List[AgentTrainer]:
    """
    Play a tournament between agents
    """
    d = math.floor(len(player_list) / 2)

    # Count rounds
    rounds = math.ceil(math.log2(len(player_list))) + 2

    for i in range(rounds):
        for player in player_list:
            player.reset()

        for j in range(d):
            dj = d

            # Find the next opponent
            found = False
            while dj < len(player_list) and not found:
                if player_list[dj].has_played_before(player_list[j]) or player_list[dj].games > i:
                    dj += 1
                else:
                    found = True

            if found:
                score = play(player_list[j], player_list[dj])

                # print(player_list[j].id, player_list[dj].id, score)

                player_list[j].set_result(score, player_list[dj])
                player_list[dj].set_result(-1 * score, player_list[j])

        player_list.sort(key=lambda player: player.score, reverse=True)

        # for player in player_list:
        #     print(player.id, player.score)

        print(f"round {i}: {player_list[0].id} {player_list[0].score:.1f}".ljust(6))

    return player_list