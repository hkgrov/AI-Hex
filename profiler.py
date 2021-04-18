from game import Game
import cProfile, pstats,io

if __name__ == "__main__":
    pr = cProfile.Profile()
    pr.enable()

    Game(size = 4, play_type = 2, start_player = 1, plotter = False, simulations = 10000, visualization = False)

    pr.disable()
    s = io.StringIO()
    sortby = pstats.SortKey.TIME
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats(15)
    print(s.getvalue())