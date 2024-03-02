import flet as ft
from loguru import logger

from game import Game, Player, SimpleStrategy, AdvancedStrategy


logger.add("error.log", format="{time} {level} {message}", level="ERROR")


@logger.catch
def main(page: ft.Page):

    def on_sw_deck_52_change(e):
        """ Колбек на свитч размера колоды """
        sw_deck_52.label = "52 cards" if sw_deck_52.value else "36 cards"
        page.update(sw_deck_52)

    def on_sld_players_change(e):
        """ Колбек на слайдер количества игроков """
        value = int(sld_players.value)
        sld_advanced.min = 0
        sld_advanced.max = value
        sld_advanced.divisions = value
        sld_advanced.value = 1
        sld_advanced.label = "{value}"
        page.update(sld_advanced)

    def on_btn_click(e):
        """ Колбек на кнопку Play """

        txt_info.value = ""
        page.update(txt_info)

        deck_52 = sw_deck_52.value
        num_players = int(sld_players.value)
        num_advanced = int(sld_advanced.value)
        num_games = int(dd_games.value)

        players = []
        for i in range(num_players):
            strategy = AdvancedStrategy() if i < num_advanced else SimpleStrategy()
            players.append(Player(strategy))

        game = Game(players, deck_52=deck_52)
        for i in range(num_games):
            game.play()
            pb.value = (i + 1) / num_games
            page.update(pb)

        stats = f"Games played: {num_games}"
        stats += "\n------"
        for idx, player in enumerate(players):
            win_percent = int((player.win_count / num_games) * 100)
            stats += f"\nPlayer {idx} ({str(player.strategy)}) won {player.win_count} times ({win_percent}%)"
        txt_info.value = stats
        page.update(txt_info)

    page.title = "Nine Game Strategy"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.window_width = 400
    page.window_height = 600
    page.window_resizable = False
    page.window_maximizable = False

    sw_deck_52 = ft.Switch(label="52 cards", value=True, on_change=on_sw_deck_52_change)
    sld_players = ft.Slider(min=2, max=4, divisions=2, value=4, label="{value}", on_change=on_sld_players_change)
    sld_advanced = ft.Slider(min=0, max=4, divisions=4, value=1, label="{value}")
    dd_games = ft.Dropdown(
        label="Number of games",
        options=[
            ft.dropdown.Option("10"),
            ft.dropdown.Option("50"),
            ft.dropdown.Option("100"),
            ft.dropdown.Option("500"),
            ft.dropdown.Option("1000"),
        ],
        value="100"
    )
    btn = ft.TextButton("Play", width=400, on_click=on_btn_click)
    pb = ft.ProgressBar(value=0)
    txt_info = ft.Text()

    page.add(
        sw_deck_52,
        ft.Text("Number of players"),
        sld_players,
        ft.Text("Number of advanced players"),
        sld_advanced,
        dd_games,
        btn,
        pb,
        txt_info
    )


if __name__ == '__main__':
    ft.app(target=main)
