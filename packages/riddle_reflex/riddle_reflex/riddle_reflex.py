"""Riddle of the Ring – Reflex application."""

import reflex as rx

from . import game_data
from .state import GameState


# ---------------------------------------------------------------------------
# Shared layout / navbar
# ---------------------------------------------------------------------------
def navbar() -> rx.Component:
    return rx.hstack(
        rx.link(rx.button("Home", size="2"), href="/"),
        rx.link(rx.button("Game Info", size="2"), href="/info"),
        rx.cond(
            GameState.is_in_game,
            rx.fragment(
                rx.link(rx.button("Play", size="2"), href="/play"),
                rx.link(rx.button("Exit Game", size="2"), href="/exit"),
            ),
            rx.fragment(
                rx.link(rx.button("Start or Join", size="2"), href="/start"),
                rx.link(rx.button("Resume Game", size="2"), href="/resume"),
            ),
        ),
        rx.link(rx.button("Admin", size="2", variant="outline"), href="/admin"),
        rx.spacer(),
        rx.cond(
            GameState.is_in_game,
            rx.hstack(
                rx.text(
                    "Game: ",
                    rx.text(GameState.game_code, color="blue", as_="span"),
                    size="2",
                    weight="bold",
                ),
                rx.text(
                    "Player: ",
                    rx.text(GameState.player_code, color="blue", as_="span"),
                    size="2",
                    weight="bold",
                ),
                spacing="4",
            ),
        ),
        width="100%",
        padding="8px 16px",
        border_bottom="1px solid var(--gray-5)",
        flex_wrap="wrap",
        spacing="2",
    )


def page_shell(*children: rx.Component) -> rx.Component:
    return rx.box(
        navbar(),
        rx.container(
            *children,
            padding_y="4",
            max_width="100%",
            padding_x="4",
        ),
        width="100%",
    )


# ---------------------------------------------------------------------------
# Index page
# ---------------------------------------------------------------------------
def index() -> rx.Component:
    return page_shell(
        rx.vstack(
            rx.heading("Riddle of the Ring", size="8"),
            rx.text(
                "A multiplayer board game set in Middle-earth. "
                "Race to claim The Ring and deliver it to your objective!",
                size="4",
            ),
            rx.divider(),
            rx.heading("How to Play", size="5"),
            rx.text(game_data.RULES_INTRO, white_space="pre-wrap", size="3"),
            rx.divider(),
            rx.hstack(
                rx.link(rx.button("Start or Join Game", size="3"), href="/start"),
                rx.link(
                    rx.button("Resume Game", size="3", variant="outline"),
                    href="/resume",
                ),
                rx.link(
                    rx.button("Game Info & Rules", size="3", variant="outline"),
                    href="/info",
                ),
                spacing="3",
            ),
            spacing="4",
            max_width="800px",
        ),
    )


# ---------------------------------------------------------------------------
# Start or Join Game page
# ---------------------------------------------------------------------------
def start_or_join_page() -> rx.Component:
    return page_shell(
        rx.vstack(
            rx.heading("Start or Join Game", size="7"),
            rx.input(
                placeholder="Enter your name",
                value=GameState.player_name,
                on_change=GameState.set_player_name,
                width="300px",
            ),
            rx.tabs.root(
                rx.tabs.list(
                    rx.tabs.trigger("Start New Game", value="start"),
                    rx.tabs.trigger("Join with Game Code", value="join"),
                ),
                rx.tabs.content(
                    _start_game_tab(), value="start", padding_top="16px"
                ),
                rx.tabs.content(
                    _join_game_tab(), value="join", padding_top="16px"
                ),
                default_value="start",
                width="100%",
            ),
            spacing="4",
            max_width="600px",
        ),
    )


def _start_game_tab() -> rx.Component:
    return rx.vstack(
        rx.heading("Start New Game", size="5"),
        rx.text("Choose Your Character", weight="bold"),
        rx.select(
            game_data.CHARACTER_NAMES,
            value=GameState.setup_character,
            on_change=GameState.set_setup_character,
        ),
        rx.text("Choose Game Code", weight="bold"),
        rx.text(
            "Share this code with fellow players so they can join.",
            size="2",
            color="gray",
        ),
        rx.select(
            GameState.game_code_options,
            value=GameState.setup_game_code,
            on_change=GameState.set_setup_game_code,
        ),
        rx.text("Choose Player Code", weight="bold"),
        rx.text(
            "Use this to resume your game if you reload.", size="2", color="gray"
        ),
        rx.select(
            GameState.player_code_options,
            value=GameState.setup_player_code,
            on_change=GameState.set_setup_player_code,
        ),
        rx.button(
            "Begin the Quest",
            on_click=GameState.start_new_game,
            size="3",
            color_scheme="green",
        ),
        spacing="3",
    )


def _join_game_tab() -> rx.Component:
    return rx.vstack(
        rx.heading("Join with Game Code", size="5"),
        rx.text("Enter the Game Code shared by the game creator.", size="2"),
        rx.input(
            placeholder="Enter game code",
            value=GameState.join_game_code_input,
            on_change=GameState.set_join_game_code,
            width="300px",
        ),
        rx.cond(
            GameState.available_characters_for_join.length() > 0,
            rx.vstack(
                rx.text("Choose Your Character", weight="bold"),
                rx.select(
                    GameState.available_characters_for_join,
                    value=GameState.setup_character,
                    on_change=GameState.set_join_character,
                ),
                rx.text("Choose Player Code", weight="bold"),
                rx.select(
                    GameState.join_player_code_options,
                    value=GameState.setup_player_code,
                    on_change=GameState.set_join_player_code,
                ),
                rx.button(
                    "Join the Quest",
                    on_click=GameState.join_existing_game,
                    size="3",
                    color_scheme="blue",
                ),
                spacing="3",
            ),
            rx.cond(
                GameState.join_game_code_input != "",
                rx.callout(
                    "That's not a valid game code, or no characters are available.",
                    icon="triangle_alert",
                    color_scheme="red",
                ),
            ),
        ),
        spacing="3",
    )


# ---------------------------------------------------------------------------
# Resume Game page
# ---------------------------------------------------------------------------
def resume_page() -> rx.Component:
    return page_shell(
        rx.vstack(
            rx.heading("Resume Game", size="7"),
            rx.text(
                "Enter your Game Code and Player Code to rejoin.", size="3"
            ),
            rx.input(
                placeholder="Game Code",
                value=GameState.resume_game_code,
                on_change=GameState.set_resume_game_code,
                width="300px",
            ),
            rx.input(
                placeholder="Player Code",
                value=GameState.resume_player_code,
                on_change=GameState.set_resume_player_code,
                width="300px",
            ),
            rx.button(
                "Resume Game",
                on_click=GameState.do_resume_game,
                size="3",
                color_scheme="blue",
            ),
            spacing="4",
            max_width="400px",
        ),
    )


# ---------------------------------------------------------------------------
# Exit Game page
# ---------------------------------------------------------------------------
def exit_page() -> rx.Component:
    return page_shell(
        rx.vstack(
            rx.heading("Exit Game", size="7"),
            rx.text(
                "Are you sure you want to leave the game? "
                "You can resume later using your Game Code and Player Code.",
                size="3",
            ),
            rx.cond(
                GameState.is_in_game,
                rx.vstack(
                    rx.text(
                        "Game Code: ",
                        rx.text(GameState.game_code, weight="bold", as_="span"),
                    ),
                    rx.text(
                        "Player Code: ",
                        rx.text(
                            GameState.player_code, weight="bold", as_="span"
                        ),
                    ),
                    spacing="1",
                ),
            ),
            rx.hstack(
                rx.button(
                    "Exit Game",
                    on_click=GameState.exit_game,
                    color_scheme="red",
                    size="3",
                ),
                rx.link(
                    rx.button("Return to Game", size="3", variant="outline"),
                    href="/play",
                ),
                spacing="3",
            ),
            spacing="4",
            max_width="500px",
        ),
    )


# ---------------------------------------------------------------------------
# Game Info page
# ---------------------------------------------------------------------------
_CARD_ITEMS: list[dict[str, str]] = [
    {
        "id": str(c["id"]),
        "name": c["name"],
        "image": f"/card_images/{c['image']}.png",
    }
    for c in game_data.CARDS
]


def info_page() -> rx.Component:
    return page_shell(
        rx.vstack(
            rx.heading("Game Information", size="7"),
            rx.tabs.root(
                rx.tabs.list(
                    rx.tabs.trigger("Rules", value="rules"),
                    rx.tabs.trigger("Cards", value="cards"),
                ),
                rx.tabs.content(_rules_tab(), value="rules", padding_top="16px"),
                rx.tabs.content(_cards_tab(), value="cards", padding_top="16px"),
                default_value="rules",
                width="100%",
            ),
            spacing="4",
            width="100%",
        ),
    )


def _rules_tab() -> rx.Component:
    return rx.vstack(
        rx.heading("Riddle of the Ring - Rules", size="5"),
        rx.text(game_data.RULES_INTRO, white_space="pre-wrap", size="3"),
        rx.divider(),
        rx.heading("Basic Game Sections", size="4"),
        *[rx.text(s, size="2") for s in game_data.BASIC_GAME_SECTIONS],
        rx.divider(),
        rx.heading("Advanced Game Sections", size="4"),
        *[rx.text(s, size="2") for s in game_data.ADVANCED_GAME_SECTIONS],
        rx.divider(),
        rx.heading("Optional Rules", size="4"),
        *[rx.text(s, size="2") for s in game_data.OPTIONAL_RULES_SECTIONS],
        rx.link(
            rx.button("Download Full Rules PDF", variant="outline"),
            href="/documents/RiddleOfTheRing-rules.pdf",
            is_external=True,
        ),
        spacing="3",
    )


def _cards_tab() -> rx.Component:
    return rx.vstack(
        rx.heading("All Cards", size="5"),
        rx.flex(
            rx.foreach(
                _CARD_ITEMS,
                lambda c: rx.box(
                    rx.image(src=c["image"], width="100px"),
                    rx.text(c["name"], size="1", text_align="center"),
                    padding="4px",
                ),
            ),
            flex_wrap="wrap",
            gap="2",
        ),
        spacing="3",
    )


# ---------------------------------------------------------------------------
# Admin page
# ---------------------------------------------------------------------------
def admin_page() -> rx.Component:
    return page_shell(
        rx.vstack(
            rx.heading("Admin - Debug State Viewer", size="7"),
            rx.button("Refresh", on_click=GameState.load_admin, size="2"),
            rx.divider(),
            rx.heading("Session Info", size="4"),
            rx.text("Game Code: ", GameState.game_code, size="2"),
            rx.text("Player Code: ", GameState.player_code, size="2"),
            rx.text("Player Name: ", GameState.player_name, size="2"),
            rx.divider(),
            rx.heading("Players", size="4"),
            rx.foreach(
                GameState.players_display,
                lambda p: rx.text(
                    p["character"],
                    " (",
                    p["name"],
                    ") - turn: ",
                    p["current_turn"],
                    size="2",
                ),
            ),
            rx.divider(),
            rx.heading("Game Stats", size="4"),
            rx.foreach(
                GameState.game_stats_items,
                lambda s: rx.text(s["label"], ": ", s["value"], size="2"),
            ),
            spacing="3",
            width="100%",
        ),
    )


# ---------------------------------------------------------------------------
# Play page components
# ---------------------------------------------------------------------------
def _game_chat_section() -> rx.Component:
    return rx.box(
        rx.heading("Game Chat", size="4"),
        rx.box(
            rx.foreach(
                GameState.chat_messages,
                _render_chat_message,
            ),
            max_height="300px",
            overflow_y="auto",
            border="1px solid var(--gray-5)",
            border_radius="8px",
            padding="8px",
            margin_bottom="8px",
        ),
        rx.form(
            rx.hstack(
                rx.input(
                    placeholder="Say something or type 'm' to refresh",
                    value=GameState.chat_input_value,
                    on_change=GameState.set_chat_input,
                    name="chat_msg",
                    flex="1",
                ),
                rx.button("Send", type="submit", size="2"),
                width="100%",
            ),
            on_submit=GameState.send_chat,
            reset_on_submit=False,
        ),
        border="1px solid var(--gray-5)",
        border_radius="8px",
        padding="12px",
    )


def _render_chat_message(msg: rx.Var[dict[str, str]]) -> rx.Component:
    return rx.cond(
        msg["type"] == "assistant",
        rx.hstack(
            rx.text("🦁", size="3"),
            rx.text(msg["action"], size="2", color="orange"),
            padding_y="2px",
        ),
        rx.hstack(
            rx.text(msg["character"], size="2", weight="bold"),
            rx.text(": ", size="2"),
            rx.text(msg["action"], size="2"),
            padding_y="2px",
        ),
    )


def _game_stats_section() -> rx.Component:
    return rx.box(
        rx.heading("Game Stats", size="4"),
        rx.flex(
            rx.foreach(
                GameState.game_stats_items,
                lambda item: rx.box(
                    rx.text(item["label"], size="1", color="gray"),
                    rx.text(item["value"], size="3", weight="bold"),
                    padding="4px 8px",
                    border="1px solid var(--gray-4)",
                    border_radius="6px",
                    min_width="80px",
                    text_align="center",
                ),
            ),
            flex_wrap="wrap",
            gap="2",
        ),
        border="1px solid var(--gray-5)",
        border_radius="8px",
        padding="12px",
    )


def _player_section() -> rx.Component:
    return rx.box(
        rx.heading("Players", size="4"),
        rx.foreach(
            GameState.players_display,
            _render_player_item,
        ),
        border="1px solid var(--gray-5)",
        border_radius="8px",
        padding="12px",
    )


def _render_player_item(player: rx.Var[dict[str, str]]) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.text(player["character"], size="3", weight="bold"),
            rx.cond(
                player["is_me"] == "true",
                rx.badge("me", color_scheme="blue"),
                rx.text("(", player["name"], ")", size="2", color="gray"),
            ),
            rx.cond(
                player["current_turn"] == "true",
                rx.badge("Current Turn", color_scheme="green"),
            ),
        ),
        padding_y="4px",
        border_bottom="1px solid var(--gray-3)",
    )


def _cards_section() -> rx.Component:
    return rx.box(
        rx.heading("Player Cards", size="4"),
        # My cards
        rx.text("My Cards", size="2", weight="bold", margin_top="8px"),
        rx.flex(
            rx.foreach(
                GameState.my_cards_display,
                _render_my_card,
            ),
            flex_wrap="wrap",
            gap="1",
        ),
        rx.button(
            "Shuffle my cards",
            on_click=GameState.shuffle_my_cards,
            size="1",
            variant="ghost",
            margin_top="4px",
        ),
        # Other players' cards
        rx.cond(
            GameState.other_players_cards_display.length() > 0,
            rx.box(
                rx.text(
                    "Other Players' Cards",
                    size="2",
                    weight="bold",
                    margin_top="8px",
                ),
                rx.flex(
                    rx.foreach(
                        GameState.other_players_cards_display,
                        _render_other_card,
                    ),
                    flex_wrap="wrap",
                    gap="1",
                ),
            ),
        ),
        # Selected cards display
        rx.cond(
            GameState.selected_cards_display.length() > 0,
            rx.box(
                rx.text(
                    "Selected Cards",
                    size="2",
                    weight="bold",
                    margin_top="8px",
                ),
                rx.flex(
                    rx.foreach(
                        GameState.selected_cards_display,
                        lambda c: rx.box(
                            rx.image(src=c["image"], width="60px"),
                            rx.text(c["name"], size="1", text_align="center"),
                            padding="2px",
                        ),
                    ),
                    gap="2",
                ),
            ),
        ),
        # Special sections
        _riddle_section(),
        _friendly_exchange_section(),
        _show_card_section(),
        _table_cards_section(),
        border="1px solid var(--gray-5)",
        border_radius="8px",
        padding="12px",
    )


def _render_my_card(card: rx.Var[dict[str, str]]) -> rx.Component:
    return rx.box(
        rx.button(
            "Select",
            size="1",
            variant="ghost",
            on_click=GameState.select_card(
                card["card_id"].to(int),
                card["owner_code"],
                card["index"].to(int),
            ),
        ),
        rx.image(src=card["image"], width="60px"),
        rx.text(card["name"], size="1", text_align="center"),
        text_align="center",
        padding="2px",
    )


def _render_other_card(card: rx.Var[dict[str, str]]) -> rx.Component:
    return rx.box(
        rx.button(
            "Select",
            size="1",
            variant="ghost",
            on_click=GameState.select_card(
                card["card_id"].to(int),
                card["owner_code"],
                card["index"].to(int),
            ),
        ),
        rx.image(src=card["image"], width="60px"),
        rx.text(card["owner_character"], size="1", text_align="center", color="gray"),
        text_align="center",
        padding="2px",
    )


def _action_section() -> rx.Component:
    return rx.box(
        rx.heading("General Actions", size="4"),
        rx.flex(
            rx.foreach(
                GameState.general_actions_display,
                _render_action_button,
            ),
            flex_wrap="wrap",
            gap="2",
        ),
        rx.divider(margin_y="8px"),
        rx.heading("Selected Card Actions", size="4"),
        rx.cond(
            GameState.my_selected_cards.length() > 0,
            rx.flex(
                rx.foreach(
                    GameState.card_actions_display,
                    _render_card_action_button,
                ),
                flex_wrap="wrap",
                gap="2",
            ),
            rx.text("No card selected", size="2", color="gray"),
        ),
        # Dialogs
        _show_hand_dialog(),
        _show_card_dialog(),
        _give_card_dialog(),
        border="1px solid var(--gray-5)",
        border_radius="8px",
        padding="12px",
    )


def _render_action_button(btn: rx.Var[dict[str, str]]) -> rx.Component:
    return rx.box(
        rx.image(src=btn["image"], width="50px", margin="0 auto"),
        rx.button(
            btn["name"],
            size="1",
            on_click=GameState.general_action(btn["name"]),
            disabled=btn["disabled"] == "true",
            width="100%",
        ),
        text_align="center",
        min_width="90px",
    )


def _render_card_action_button(btn: rx.Var[dict[str, str]]) -> rx.Component:
    return rx.button(
        btn["name"],
        size="1",
        on_click=GameState.card_action(btn["name"]),
        disabled=btn["disabled"] == "true",
    )


def _show_hand_dialog() -> rx.Component:
    return rx.alert_dialog.root(
        rx.alert_dialog.content(
            rx.alert_dialog.title("Show Hand to Player"),
            rx.alert_dialog.description(
                "Select a character to show your hand to:"
            ),
            rx.vstack(
                rx.foreach(
                    GameState.other_characters,
                    lambda ch: rx.button(
                        ch,
                        on_click=GameState.confirm_show_hand(ch),
                        width="100%",
                        variant="outline",
                    ),
                ),
                spacing="2",
            ),
            rx.flex(
                rx.alert_dialog.cancel(
                    rx.button(
                        "Cancel",
                        variant="soft",
                        on_click=GameState.close_dialog,
                    ),
                ),
                justify="end",
                margin_top="16px",
            ),
        ),
        open=GameState.show_hand_dialog_open,
    )


def _show_card_dialog() -> rx.Component:
    return rx.alert_dialog.root(
        rx.alert_dialog.content(
            rx.alert_dialog.title("Show Card to Player"),
            rx.alert_dialog.description("Select a character:"),
            rx.vstack(
                rx.foreach(
                    GameState.other_characters,
                    lambda ch: rx.button(
                        ch,
                        on_click=GameState.confirm_show_card(ch),
                        width="100%",
                        variant="outline",
                    ),
                ),
                spacing="2",
            ),
            rx.flex(
                rx.alert_dialog.cancel(
                    rx.button(
                        "Cancel",
                        variant="soft",
                        on_click=GameState.close_dialog,
                    ),
                ),
                justify="end",
                margin_top="16px",
            ),
        ),
        open=GameState.show_card_dialog_open,
    )


def _give_card_dialog() -> rx.Component:
    return rx.alert_dialog.root(
        rx.alert_dialog.content(
            rx.alert_dialog.title("Give Card to Player"),
            rx.alert_dialog.description("Select a character:"),
            rx.vstack(
                rx.foreach(
                    GameState.other_characters,
                    lambda ch: rx.button(
                        ch,
                        on_click=GameState.confirm_give_card(ch),
                        width="100%",
                        variant="outline",
                    ),
                ),
                spacing="2",
            ),
            rx.flex(
                rx.alert_dialog.cancel(
                    rx.button(
                        "Cancel",
                        variant="soft",
                        on_click=GameState.close_dialog,
                    ),
                ),
                justify="end",
                margin_top="16px",
            ),
        ),
        open=GameState.give_card_dialog_open,
    )


def _board_section() -> rx.Component:
    return rx.box(
        rx.heading("Board", size="4"),
        rx.image(
            src="/board_v1.png",
            width="100%",
            max_width="600px",
            cursor="crosshair",
        ),
        rx.text(
            "Click the board to move your marker (board interaction simplified)",
            size="1",
            color="gray",
        ),
        border="1px solid var(--gray-5)",
        border_radius="8px",
        padding="12px",
    )


def _activity_section() -> rx.Component:
    return rx.box(
        rx.heading("Activity Log", size="4"),
        rx.box(
            rx.foreach(
                GameState.system_activities,
                lambda a: rx.text(
                    a["character"],
                    " | ",
                    a["action"],
                    size="2",
                ),
            ),
            max_height="400px",
            overflow_y="auto",
        ),
        border="1px solid var(--gray-5)",
        border_radius="8px",
        padding="12px",
    )


def _discard_section() -> rx.Component:
    return rx.box(
        rx.heading("Discard Pile", size="4"),
        rx.box(
            rx.foreach(
                GameState.discard_names,
                lambda d: rx.text(d["name"], size="2"),
            ),
            max_height="400px",
            overflow_y="auto",
        ),
        border="1px solid var(--gray-5)",
        border_radius="8px",
        padding="12px",
    )


def _battle_section() -> rx.Component:
    return rx.cond(
        GameState.has_battle,
        rx.box(
            rx.heading("Battle", size="5"),
            rx.grid(
                _battle_role_column("Attacker", GameState.attacker_cards_display),
                _battle_role_column("Defender", GameState.defender_cards_display),
                columns="2",
                gap="4",
                width="100%",
            ),
            border="2px solid var(--red-7)",
            border_radius="8px",
            padding="12px",
            margin_y="8px",
        ),
    )


def _battle_role_column(
    title: str, cards: rx.Var[list[dict[str, str]]]
) -> rx.Component:
    return rx.box(
        rx.heading(title, size="4"),
        rx.foreach(
            cards,
            lambda c: rx.vstack(
                rx.image(src=c["image"], width="60px"),
                rx.text(c["name"], size="1"),
                rx.hstack(
                    rx.cond(
                        c["is_city"] == "true",
                        rx.button(
                            "Clear",
                            size="1",
                            variant="ghost",
                            on_click=GameState.remove_battle_card(
                                c["card_id"].to(int), c["role"]
                            ),
                        ),
                        rx.fragment(
                            rx.button(
                                "Discard",
                                size="1",
                                on_click=GameState.discard_battle_card(
                                    c["card_id"].to(int), c["role"]
                                ),
                            ),
                            rx.button(
                                "Retain",
                                size="1",
                                variant="outline",
                                on_click=GameState.retain_battle_card(
                                    c["card_id"].to(int), c["role"]
                                ),
                            ),
                        ),
                    ),
                    spacing="1",
                ),
                spacing="1",
                padding="4px",
                border="1px solid var(--gray-4)",
                border_radius="4px",
            ),
        ),
    )


def _riddle_section() -> rx.Component:
    return rx.cond(
        GameState.has_riddle,
        rx.box(
            rx.heading("Riddle Power Play", size="4"),
            rx.text(
                "Riddler: ",
                rx.text(GameState.riddle_riddler, weight="bold", as_="span"),
                " vs ",
                rx.text(
                    GameState.riddle_card_owner, weight="bold", as_="span"
                ),
                size="2",
            ),
            rx.hstack(
                rx.button(
                    "Show Riddler Card",
                    size="2",
                    on_click=GameState.show_riddler_card,
                ),
                rx.button(
                    "Give Card to Riddler",
                    size="2",
                    on_click=GameState.give_card_to_riddler,
                ),
                rx.button(
                    "End Riddle",
                    size="2",
                    variant="outline",
                    on_click=GameState.end_riddle,
                ),
                spacing="2",
            ),
            border="1px solid var(--orange-6)",
            border_radius="6px",
            padding="8px",
            margin_y="4px",
        ),
    )


def _friendly_exchange_section() -> rx.Component:
    return rx.cond(
        GameState.has_exchange,
        rx.box(
            rx.heading("Friendly Exchange", size="4"),
            rx.text(
                "Between ",
                rx.text(
                    GameState.exchange_first_party, weight="bold", as_="span"
                ),
                " and ",
                rx.text(
                    GameState.exchange_second_party, weight="bold", as_="span"
                ),
                size="2",
            ),
            rx.cond(
                GameState.exchange_status == "ready",
                rx.button(
                    "Complete Exchange",
                    on_click=GameState.complete_friendly_exchange,
                    color_scheme="green",
                ),
                rx.text("Pending card selection...", size="2", color="gray"),
            ),
            border="1px solid var(--blue-6)",
            border_radius="6px",
            padding="8px",
            margin_y="4px",
        ),
    )


def _show_card_section() -> rx.Component:
    return rx.cond(
        GameState.has_show_card,
        rx.box(
            rx.heading("Show Card to Player", size="4"),
            rx.text(
                "A card is being shown to: ",
                rx.text(GameState.show_card_target, weight="bold", as_="span"),
                size="2",
            ),
            rx.button(
                "Clear",
                size="1",
                variant="outline",
                on_click=GameState.clear_show_card,
            ),
            border="1px solid var(--green-6)",
            border_radius="6px",
            padding="8px",
            margin_y="4px",
        ),
    )


def _table_cards_section() -> rx.Component:
    return rx.cond(
        GameState.table_cards_display.length() > 0,
        rx.box(
            rx.heading("Table Cards", size="4"),
            rx.text(
                "Cards on the table visible to all players.",
                size="1",
                color="gray",
            ),
            rx.flex(
                rx.foreach(
                    GameState.table_cards_display,
                    lambda c: rx.vstack(
                        rx.image(src=c["image"], width="60px"),
                        rx.text(
                            c["name"],
                            " (",
                            c["owner"],
                            ")",
                            size="1",
                        ),
                        rx.hstack(
                            rx.button(
                                "Discard",
                                size="1",
                                on_click=GameState.discard_table_card(
                                    c["card_id"].to(int)
                                ),
                            ),
                            rx.button(
                                "Retain",
                                size="1",
                                variant="outline",
                                on_click=GameState.retain_table_card(
                                    c["card_id"].to(int)
                                ),
                            ),
                            spacing="1",
                        ),
                        spacing="1",
                        border="1px solid var(--gray-4)",
                        border_radius="4px",
                        padding="4px",
                    ),
                ),
                gap="2",
                flex_wrap="wrap",
            ),
            border="1px solid var(--gray-3)",
            border_radius="6px",
            padding="8px",
            margin_y="4px",
        ),
    )


# ---------------------------------------------------------------------------
# Play page
# ---------------------------------------------------------------------------
def play_page() -> rx.Component:
    return page_shell(
        rx.cond(
            GameState.is_in_game,
            rx.vstack(
                rx.hstack(
                    rx.button(
                        "Refresh Game",
                        on_click=GameState.refresh_game,
                        size="2",
                        variant="outline",
                    ),
                    spacing="2",
                ),
                # Row 1: Chat + Stats
                rx.grid(
                    _game_chat_section(),
                    _game_stats_section(),
                    columns="2",
                    gap="4",
                    width="100%",
                ),
                # Battle (when active)
                _battle_section(),
                # Row 2: Players + Cards + Actions
                rx.grid(
                    _player_section(),
                    _cards_section(),
                    _action_section(),
                    columns="3",
                    gap="4",
                    width="100%",
                ),
                # Row 3: Activity + Board + Discard
                rx.grid(
                    _activity_section(),
                    _board_section(),
                    _discard_section(),
                    columns="3",
                    gap="4",
                    width="100%",
                ),
                spacing="4",
                width="100%",
            ),
            rx.vstack(
                rx.heading("No Active Game", size="6"),
                rx.text("Start or join a game to play."),
                rx.hstack(
                    rx.link(rx.button("Start or Join"), href="/start"),
                    rx.link(
                        rx.button("Resume Game", variant="outline"),
                        href="/resume",
                    ),
                ),
                spacing="3",
            ),
        ),
    )


# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------
app = rx.App(
    theme=rx.theme(appearance="dark"),
)
app.add_page(index, route="/", title="Riddle of the Ring")
app.add_page(
    start_or_join_page,
    route="/start",
    title="Start or Join Game",
    on_load=GameState.generate_start_codes,
)
app.add_page(
    play_page,
    route="/play",
    title="Play - Riddle of the Ring",
    on_load=GameState.on_play_load,
)
app.add_page(resume_page, route="/resume", title="Resume Game")
app.add_page(exit_page, route="/exit", title="Exit Game")
app.add_page(info_page, route="/info", title="Game Info")
app.add_page(
    admin_page,
    route="/admin",
    title="Admin",
    on_load=GameState.load_admin,
)
