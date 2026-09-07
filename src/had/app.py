from collections.abc import Iterator

import config, game, ui


def blocks_for(game_instance: game.Game) -> Iterator[ui.Block]:
    head, *rest_of_body = game_instance.player.body
    yield ui.Block(*head,config.SNAKE_HEAD_COLOR)
    for x, y in rest_of_body:
        yield ui.Block(x,y,config.SNAKE_COLOR)
    for food in game_instance.food_pieces:
        yield ui.Block(*food.position, food.color)

def gameloop(game_instance: game.Game, view: ui.View):
    if game_instance.update_player_position():
        view.draw_game(blocks_for(game_instance))
        view.after(config.MS_PER_FRAME, gameloop, game_instance, view)

def main():
    game_instance = game.Game()
    view = ui.View()
    gameloop(game_instance, view)
    view.mainloop()

if __name__ == "__main__":
    main()