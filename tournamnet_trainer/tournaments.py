import argparse
import asyncio

import os
import numpy as np
from play_tournament import play_tournament
from play_battle import play_battle
from train_agents import AgentTrainer
from algorithm.ann import Network
from algorithm.genetics import  create_new, crossover, mutate

async def tournaments(
    history_size: int,
    layers= [],
    epoch = 64,
    population= 32,
    best: bool = False
):
    model_name = f"{(history_size + 1) * 50}{'_'.join(map(str, layers))}"
    model_path = f"../models/{model_name}"

    if not os.path.exists(model_path):
        os.makedirs(model_path, exist_ok=True)

    top_player_list = []
    top_player_ids = set()
    best_models = set()
    player_list = []

    base_layers = []
    inp = history_size * 50 + 50
    for i, layer in enumerate(layers):
        base_layers.append([inp, 1, layer])
        inp = layer

    base_net = Network(history_size * 50 + 50, 1, base_layers)

    topology_size = len(base_net.get_topology())
    size = base_net.size() + topology_size

    if best:
        weights_files = [f for f in os.listdir(model_path) if f.endswith(".bin")]
        for weight_file in weights_files:
            with open(os.path.join(model_path, weight_file), "rb") as f:
                weights = np.frombuffer(f.read(), dtype=np.float32)
                agent = AgentTrainer(history_size * 50, weights)
                agent.age = 1
                best_models.add(agent.id)
                player_list.append(agent)
                top_player_list.append(agent)
                top_player_ids.add(agent.id)

        d = len(player_list)
        ind = 0
        while len(player_list) < max(population, d * 2):
            player_a = player_list[ind]
            player_b = player_list[np.random.randint(d)]

            if player_a and player_b and player_a.id!= player_b.id:
                new_weights = mutate(crossover(player_a.get_weights(), player_b.get_weights()))

                weights = np.empty(size, dtype=np.float32)
                weights[:topology_size] = base_net.get_topology()
                weights[topology_size:] = new_weights

                agent = AgentTrainer(history_size * 50, weights)
                player_list.append(agent)

                ind += 1
                ind %= d

    while len(player_list) < population:
        w = create_new(base_net.size(), 2)

        weights = np.empty(size, dtype=np.float32)
        weights[:topology_size] = base_net.get_topology()
        weights[topology_size:] = w

        agent = AgentTrainer(history_size * 50, weights)
        player_list.append(agent)

    player_list = await play_tournament(player_list)

    print(f"0 {player_list[0].id} ({player_list[0].age}) with {player_list[0].score} points")

    current_epoch = 0
    while current_epoch <= epoch:
        player_list = player_list[:len(player_list) // 4]

        for player in player_list:
            player.on_new_epoch()

            if player.age > 1 and player.id not in top_player_ids:
                top_player_ids.add(player.id)
                top_player_list.append(player)
                print(f"add top player {player.id} {len(top_player_list)}")

        d = len(player_list)

        while len(player_list) < population:
            player_a = player_list[ind]
            player_b = player_list[np.random.randint(d)]

            if player_a and player_b and player_a.id!= player_b.id:
                new_weights = mutate(crossover(player_a.get_weights(), player_b.get_weights()))

                weights = np.empty(size, dtype=np.float32)
                weights[:topology_size] = base_net.get_topology()
                weights[topology_size:] = new_weights

                agent = AgentTrainer(history_size * 50, weights)
                player_list.append(agent)
                ind += 1
                ind %= d

        player_list = await play_tournament(player_list)
        current_epoch += 1
        print(f"{current_epoch} {player_list[0].id} ({player_list[0].age}) with {player_list[0].score} points")

    for player in player_list:
        if player.age > 1 and player.id not in top_player_ids:
            top_player_ids.add(player.id)
            top_player_list.append(player)
            print(f"add top player {player.id} {len(top_player_list)}")

    print("-----")
    print(len(top_player_list))
    print("-----")

    for player in top_player_list:
        player.on_new_epoch()

    top_player_list = await play_battle(top_player_list)
    index = 1
    for player in top_player_list:
        code = "\033[32m" if player.id in best_models else "\033[36m"
        reset = "\033[m"
        print(f"{code}{str(index).rjust(4)} {player}{reset}")
        index += 1

    while top_player_list and top_player_list[0].id in best_models:
        print(f"remove {top_player_list[0].id}")
        top_player_list.pop(0)

    if top_player_list:
        player = top_player_list[0]
        print(f"{player.score} {player.id}")
        weights = player.serialize()

        print(weights.shape, weights.shape[0] // 4)
        with open(os.path.join(model_path, f"{player.id}.bin"), "wb") as f:
            f.write(weights.tobytes())


















#added for a single tournament

async def tournaments_single(
    hist: int,
    layer: list[int],
    epoch: int,
    population: int,
    iterations: int,
    best: bool
) -> None:
    """Run tournaments for the specified number of iterations"""
    for _ in range(iterations):
        await tournaments(hist, layer, epoch, population, best)

def main() -> None:
    """Parse arguments and run tournaments_single"""
    parser = argparse.ArgumentParser(description="Trainer")
    parser.add_argument("--history", type=int, default=1, help="History size")
    parser.add_argument("--epoch", type=int, default=64, help="Number of epochs")
    parser.add_argument("--population", type=int, default=32, help="Population size")
    parser.add_argument("--layers", type=int, nargs="+", default=[], help="Layer sizes")
    parser.add_argument("--iterations", type=int, default=1, help="Number of iterations")
    parser.add_argument("--best", action="store_true", help="Use best model")
    args = parser.parse_args()

    asyncio.run(tournaments_single(
        args.history,
        args.layers,
        args.epoch,
        args.population,
        args.iterations,
        args.best
    ))

    print("done")

if __name__ == "__main__":
    main()

































# async def tournaments_single(
#     hist: int,
#     layer: list[int],
#     epoch: int,
#     population: int,
#     iterations: int,
#     best: bool
# ):
#     for _ in range(iterations):
#         await tournaments(hist, layer, epoch, population, best)

# parser = argparse.ArgumentParser(
#     description="Trainer",
#     add_help=True
# )
# parser.add_argument("--history", type=int, default=1, help="History size")
# parser.add_argument("--epoch", type=int, default=64, help="num epoch")
# parser.add_argument("--population", type=int, default=32, help="population size")
# parser.add_argument("--layers", type=int, nargs="+", default=[], help="History size")
# parser.add_argument("--iterations", type=int, default=1, help="population size")
# parser.add_argument("--best", action="store_true")

# args = parser.parse_args()

# tournaments_single(
#     args.history,
#     args.layers,
#     args.epoch,
#     args.population,
#     args.iterations,
#     args.best
# ).then(lambda: print("done"))



