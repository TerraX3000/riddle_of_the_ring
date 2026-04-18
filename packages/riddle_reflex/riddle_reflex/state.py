"""Game state management for Riddle of the Ring."""

import random
import threading
from typing import Any

import reflex as rx

from . import game_data

# ---------------------------------------------------------------------------
# Module-level shared store (replaces Redis)
# ---------------------------------------------------------------------------
_lock = threading.Lock()
_store: dict[str, Any] = {}


def _key(category: str, game_code: str = "") -> str:
    return f"{game_code}:{category}" if game_code else category


def store_get(category: str, game_code: str = "") -> Any:
    with _lock:
        return _store.get(_key(category, game_code))


def store_set(category: str, data: Any, game_code: str = "") -> None:
    with _lock:
        _store[_key(category, game_code)] = data


def store_exists(category: str, game_code: str = "") -> bool:
    with _lock:
        return _key(category, game_code) in _store


def _ensure_global_data() -> None:
    if not store_exists("games"):
        store_set("games", [])
    if not store_exists("characters"):
        store_set("characters", game_data.CHARACTERS)


# ---------------------------------------------------------------------------
# Code generation helpers
# ---------------------------------------------------------------------------
_WORD_POOL = [
    "amber", "arctic", "azure", "blazing", "bold", "brave", "bright",
    "calm", "cedar", "clever", "coral", "cosmic", "crystal", "daring",
    "dawn", "deep", "dusk", "eager", "ember", "epic", "fable", "fast",
    "fern", "fierce", "flame", "fleet", "flint", "forest", "frost",
    "gentle", "glacier", "gleam", "golden", "grand", "grove", "harbor",
    "hazel", "hollow", "horizon", "iron", "ivory", "jade", "jovial",
    "keen", "lantern", "lark", "legend", "lunar", "maple", "meadow",
    "mist", "moon", "mossy", "mystic", "noble", "north", "oak",
    "ocean", "olive", "onyx", "orbit", "peak", "pine", "prism",
    "quartz", "quest", "raven", "ridge", "river", "ruby", "sage",
    "scout", "shadow", "shore", "silver", "sky", "spark", "spruce",
    "star", "sterling", "stone", "storm", "summit", "swift", "thorn",
    "thunder", "tide", "timber", "topaz", "trail", "twilight", "vale",
    "velvet", "venture", "violet", "wander", "whisper", "willow", "zephyr",
]


def generate_code_options(count: int = 5, exclude: list | None = None) -> list[str]:
    exclude = set(exclude or [])
    pool = [w for w in _WORD_POOL if w not in exclude]
    random.shuffle(pool)
    return pool[:count]


# ---------------------------------------------------------------------------
# GameState
# ---------------------------------------------------------------------------
class GameState(rx.State):
    """Main game state – one instance per browser tab."""

    # -- identity --
    player_name: str = ""
    player_code: str = ""
    game_code: str = ""

    # -- raw game data (materialised from store via _refresh) --
    players: dict[str, dict] = {}
    activities: list[dict] = []
    draw_pile_count: int = 0
    discards: list[int] = []
    battle: dict[str, list] = {"attacker_cards": [], "defender_cards": []}
    table_cards: list[int] = []
    game_info: dict[str, Any] = {}
    riddle_power_play: dict[str, Any] = {}
    friendly_exchange: dict[str, Any] = {}
    show_card_to_player_data: dict[str, Any] = {}

    # -- UI state --
    chat_input_value: str = ""
    show_hand_dialog_open: bool = False
    show_card_dialog_open: bool = False
    give_card_dialog_open: bool = False

    # -- setup state --
    setup_character: str = ""
    setup_game_code: str = ""
    setup_player_code: str = ""
    join_game_code_input: str = ""
    game_code_options: list[str] = []
    player_code_options: list[str] = []
    join_player_code_options: list[str] = []
    available_characters_for_join: list[str] = []

    # -- resume state --
    resume_game_code: str = ""
    resume_player_code: str = ""

    # ---------------------------------------------------------------
    # Computed vars (all fully typed for rx.foreach)
    # ---------------------------------------------------------------
    @rx.var
    def is_in_game(self) -> bool:
        return bool(self.game_code and self.player_code)

    @rx.var
    def is_game_started(self) -> bool:
        return bool(self.game_info.get("is_started", False))

    @rx.var
    def is_current_turn(self) -> bool:
        p = self.players.get(self.player_code, {})
        return bool(p.get("current_turn", False))

    @rx.var
    def my_character(self) -> str:
        p = self.players.get(self.player_code, {})
        return str(p.get("character", ""))

    @rx.var
    def my_selected_cards(self) -> list[int]:
        p = self.players.get(self.player_code, {})
        return list(p.get("selected_cards", []))

    @rx.var
    def first_selected_card(self) -> int:
        p = self.players.get(self.player_code, {})
        sel = p.get("selected_cards", [])
        return int(sel[0]) if sel else 0

    @rx.var
    def chat_messages(self) -> list[dict[str, str]]:
        result: list[dict[str, str]] = []
        for a in self.activities:
            if a.get("type") != "system":
                player_data = a.get("player", {})
                character = ""
                if isinstance(player_data, dict):
                    character = str(player_data.get("character", ""))
                result.append({
                    "type": str(a.get("type", "user")),
                    "action": str(a.get("action", "")),
                    "character": character,
                })
        return result

    @rx.var
    def system_activities(self) -> list[dict[str, str]]:
        result: list[dict[str, str]] = []
        for a in self.activities:
            if a.get("type") == "system":
                player_data = a.get("player", {})
                character = ""
                if isinstance(player_data, dict):
                    character = str(player_data.get("character", ""))
                result.append({
                    "character": character,
                    "action": str(a.get("action", "")),
                })
        return result

    @rx.var
    def players_display(self) -> list[dict[str, str]]:
        result: list[dict[str, str]] = []
        for p in self.players.values():
            result.append({
                "character": str(p.get("character", "")),
                "name": str(p.get("name", "")),
                "player_code": str(p.get("player_code", "")),
                "current_turn": "true" if p.get("current_turn") else "false",
                "is_me": "true" if p.get("player_code") == self.player_code else "false",
            })
        return result

    @rx.var
    def my_cards_display(self) -> list[dict[str, str]]:
        p = self.players.get(self.player_code, {})
        result: list[dict[str, str]] = []
        for idx, card_id in enumerate(p.get("cards", [])):
            card = game_data.get_card(card_id)
            result.append({
                "card_id": str(card_id),
                "name": card.get("name", "?"),
                "image": f"/card_images/{card.get('image', 'Reverse')}.png",
                "owner_code": self.player_code,
                "index": str(idx),
            })
        return result

    @rx.var
    def other_players_cards_display(self) -> list[dict[str, str]]:
        result: list[dict[str, str]] = []
        for pc, p in self.players.items():
            if pc == self.player_code:
                continue
            show_hand = p.get("special_actions", {}).get("show_hand_to_character")
            my_char = self.players.get(self.player_code, {}).get("character", "")
            can_see = (show_hand == my_char) if show_hand else False
            for idx, card_id in enumerate(p.get("cards", [])):
                card = game_data.get_card(card_id)
                if can_see:
                    img = f"/card_images/{card.get('image', 'Reverse')}.png"
                    name = card.get("name", "?")
                else:
                    img = "/card_images/Reverse.png"
                    name = ""
                result.append({
                    "card_id": str(card_id),
                    "name": name,
                    "image": img,
                    "owner_code": pc,
                    "owner_character": str(p.get("character", "")),
                    "index": str(idx),
                })
        return result

    @rx.var
    def selected_cards_display(self) -> list[dict[str, str]]:
        p = self.players.get(self.player_code, {})
        my_cards = p.get("cards", [])
        result: list[dict[str, str]] = []
        for card_id in p.get("selected_cards", []):
            card = game_data.get_card(card_id)
            is_mine = card_id in my_cards
            if is_mine:
                img = f"/card_images/{card.get('image', 'Reverse')}.png"
                name = card.get("name", "?")
            else:
                img = "/card_images/Reverse.png"
                owner_code = self._get_card_owner_code_sync(card_id)
                owner = self.players.get(owner_code, {})
                name = f"<{owner.get('character', '?')} Card>"
            result.append({
                "card_id": str(card_id),
                "name": name,
                "image": img,
                "is_mine": "true" if is_mine else "false",
            })
        return result

    @rx.var
    def has_battle(self) -> bool:
        return bool(
            self.battle.get("attacker_cards") or self.battle.get("defender_cards")
        )

    @rx.var
    def attacker_cards_display(self) -> list[dict[str, str]]:
        return self._battle_cards_display("attacker")

    @rx.var
    def defender_cards_display(self) -> list[dict[str, str]]:
        return self._battle_cards_display("defender")

    def _battle_cards_display(self, role: str) -> list[dict[str, str]]:
        result: list[dict[str, str]] = []
        for card_id in self.battle.get(f"{role}_cards", []):
            card = game_data.get_card(card_id)
            is_city = card.get("type") == "City Battlepoint"
            result.append({
                "card_id": str(card_id),
                "name": card.get("name", "?"),
                "image": f"/card_images/{card.get('image', 'Reverse')}.png",
                "is_city": "true" if is_city else "false",
                "role": role,
            })
        return result

    @rx.var
    def table_cards_display(self) -> list[dict[str, str]]:
        result: list[dict[str, str]] = []
        for card_id in self.table_cards:
            card = game_data.get_card(card_id)
            owner_code = self._get_card_owner_code_sync(card_id)
            owner = self.players.get(owner_code, {})
            result.append({
                "card_id": str(card_id),
                "name": card.get("name", "?"),
                "image": f"/card_images/{card.get('image', 'Reverse')}.png",
                "owner": str(owner.get("character", "?")),
            })
        return result

    @rx.var
    def has_riddle(self) -> bool:
        return bool(self.riddle_power_play)

    @rx.var
    def riddle_riddler(self) -> str:
        return str(self.riddle_power_play.get("riddler", ""))

    @rx.var
    def riddle_card_owner(self) -> str:
        return str(self.riddle_power_play.get("card_owner", ""))

    @rx.var
    def riddle_card_id(self) -> int:
        return int(self.riddle_power_play.get("riddle_card", 0))

    @rx.var
    def has_exchange(self) -> bool:
        return bool(self.friendly_exchange)

    @rx.var
    def exchange_first_party(self) -> str:
        return str(self.friendly_exchange.get("first_party", ""))

    @rx.var
    def exchange_second_party(self) -> str:
        return str(self.friendly_exchange.get("second_party", ""))

    @rx.var
    def exchange_status(self) -> str:
        return str(self.friendly_exchange.get("status", ""))

    @rx.var
    def has_show_card(self) -> bool:
        return bool(self.show_card_to_player_data)

    @rx.var
    def show_card_target(self) -> str:
        return str(self.show_card_to_player_data.get("show_card_to_character", ""))

    @rx.var
    def game_stats_items(self) -> list[dict[str, str]]:
        draw = self.draw_pile_count
        disc = len(self.discards)
        stats: dict[str, Any] = {"Draw Pile": draw, "Discard Pile": disc}
        stats.update(self.game_info.get("stats", {}))
        for p in self.players.values():
            ch = p.get("character", "?")
            count = sum(
                1
                for a in self.activities
                if a.get("type") == "system"
                and isinstance(a.get("player"), dict)
                and a["player"].get("character") == ch
            )
            stats[f"Activities | {ch}"] = count
        return [{"label": str(k), "value": str(v)} for k, v in stats.items()]

    @rx.var
    def other_characters(self) -> list[str]:
        return [
            str(p["character"])
            for p in self.players.values()
            if p.get("player_code") != self.player_code
        ]

    @rx.var
    def discard_names(self) -> list[dict[str, str]]:
        result: list[dict[str, str]] = []
        for cid in reversed(self.discards):
            card = game_data.get_card(cid)
            result.append({"id": str(cid), "name": card.get("name", "?")})
        return result

    @rx.var
    def general_actions_display(self) -> list[dict[str, str]]:
        p = self.players.get(self.player_code, {})
        is_current = bool(p.get("current_turn", False))
        is_started = bool(self.game_info.get("is_started", False))
        my_char = p.get("character", "")
        my_side = game_data.CHARACTERS.get(my_char, {}).get("side", "")

        result: list[dict[str, str]] = []
        for btn in game_data.ACTION_BUTTONS:
            enabled = True
            if enabled and btn.get("is_pre_start_only") and is_started:
                enabled = False
            if enabled and btn.get("is_post_start_only") and not is_started:
                enabled = False
            if enabled and btn.get("is_current_turn_only") and is_started:
                enabled = is_current
            if enabled and btn.get("is_not_current_turn_only") and is_started:
                enabled = not is_current
            if enabled and btn.get("is_side"):
                if btn["is_side"] != my_side:
                    enabled = False
            result.append({
                "name": btn["name"],
                "image": btn["image"],
                "disabled": "false" if enabled else "true",
            })
        return result

    @rx.var
    def card_actions_display(self) -> list[dict[str, str]]:
        p = self.players.get(self.player_code, {})
        is_current = bool(p.get("current_turn", False))
        is_started = bool(self.game_info.get("is_started", False))
        selected = p.get("selected_cards", [])
        my_cards = p.get("cards", [])
        is_card_owner = bool(selected and selected[0] in my_cards)
        is_battle_point = False
        if selected:
            card = game_data.get_card(selected[0])
            is_battle_point = bool(card.get("battle_point"))

        result: list[dict[str, str]] = []
        for btn in game_data.CARD_ACTION_BUTTONS:
            enabled = True
            if enabled and btn.get("is_current_turn_only"):
                enabled = is_current
            if enabled and btn.get("is_card_owner_only"):
                enabled = is_card_owner
            if enabled and btn.get("is_not_card_owner_only"):
                enabled = not is_card_owner
            if enabled and btn.get("is_not_current_turn_only"):
                enabled = not is_current
            if enabled and btn.get("is_battle_card_only"):
                enabled = is_battle_point
            result.append({
                "name": btn["name"],
                "disabled": "false" if enabled else "true",
            })
        return result

    # ---------------------------------------------------------------
    # Sync helper (for computed vars that can't call async methods)
    # ---------------------------------------------------------------
    def _get_card_owner_code_sync(self, card_id: int) -> str:
        for pc, p in self.players.items():
            if card_id in p.get("cards", []):
                return pc
        return ""

    # ---------------------------------------------------------------
    # Internal helpers
    # ---------------------------------------------------------------
    def _refresh(self) -> None:
        if not self.game_code:
            return
        gc = self.game_code
        self.players = store_get("players", gc) or {}
        self.activities = store_get("activities", gc) or []
        dp = store_get("draw_pile", gc)
        self.draw_pile_count = len(dp) if dp else 0
        self.discards = store_get("discards", gc) or []
        self.battle = store_get("battle", gc) or {
            "attacker_cards": [],
            "defender_cards": [],
        }
        self.table_cards = store_get("table_cards", gc) or []
        self.game_info = store_get("game", gc) or {}
        self.riddle_power_play = store_get("riddle_power_play", gc) or {}
        self.friendly_exchange = store_get("friendly_exchange", gc) or {}
        self.show_card_to_player_data = store_get("show_card_to_player", gc) or {}

    def _add_activity(self, action: str, msg_type: str = "system") -> None:
        gc = self.game_code
        players = store_get("players", gc) or {}
        player = players.get(self.player_code, {})
        activities = store_get("activities", gc) or []
        activity: dict[str, Any] = {
            "player": {"character": player.get("character", "")},
            "action": action,
            "type": msg_type,
        }
        activities.append(activity)
        store_set("activities", activities, gc)

    def _get_card_owner_code(self, card_id: int) -> str:
        gc = self.game_code
        players = store_get("players", gc) or {}
        for pc, p in players.items():
            if card_id in p.get("cards", []):
                return pc
        return ""

    # ---------------------------------------------------------------
    # Setup events
    # ---------------------------------------------------------------
    def generate_start_codes(self) -> None:
        _ensure_global_data()
        games = store_get("games") or []
        current_codes = [g["game_code"] for g in games]
        self.game_code_options = generate_code_options(5, exclude=current_codes)
        self.player_code_options = generate_code_options(5)
        if not self.setup_character:
            self.setup_character = game_data.CHARACTER_NAMES[0]
        if self.game_code_options:
            self.setup_game_code = self.game_code_options[0]
        if self.player_code_options:
            self.setup_player_code = self.player_code_options[0]

    def set_player_name(self, name: str) -> None:
        self.player_name = name

    def set_setup_character(self, character: str) -> None:
        self.setup_character = character

    def set_setup_game_code(self, code: str) -> None:
        self.setup_game_code = code

    def set_setup_player_code(self, code: str) -> None:
        self.setup_player_code = code

    def set_join_game_code(self, code: str) -> None:
        self.join_game_code_input = code.lower().strip()
        if self.join_game_code_input:
            self._load_join_data()

    def set_join_player_code(self, code: str) -> None:
        self.setup_player_code = code

    def set_join_character(self, character: str) -> None:
        self.setup_character = character

    def _load_join_data(self) -> None:
        _ensure_global_data()
        gc = self.join_game_code_input
        games = store_get("games") or []
        valid_codes = [g["game_code"] for g in games]
        if gc not in valid_codes:
            self.available_characters_for_join = []
            return
        players = store_get("players", gc) or {}
        taken = [p["character"] for p in players.values()]
        self.available_characters_for_join = [
            c for c in game_data.CHARACTER_NAMES if c not in taken
        ]
        current_player_codes = list(players.keys())
        self.join_player_code_options = generate_code_options(
            5, exclude=current_player_codes
        )
        if self.available_characters_for_join:
            self.setup_character = self.available_characters_for_join[0]
        if self.join_player_code_options:
            self.setup_player_code = self.join_player_code_options[0]

    def start_new_game(self) -> rx.event.EventSpec | None:
        _ensure_global_data()
        gc = self.setup_game_code
        pc = self.setup_player_code
        character = self.setup_character
        name = self.player_name

        player = {
            "id": 0,
            "name": name,
            "character": character,
            "current_turn": False,
            "cards": [],
            "selected_cards": [],
            "player_code": pc,
            "positions": [],
            "special_actions": {"show_hand_to_character": None},
        }
        store_set("players", {pc: player}, gc)
        store_set("activities", list(game_data.INITIAL_CHAT_MESSAGES), gc)
        store_set("draw_pile", game_data.get_shuffled_deck(), gc)
        store_set("discards", [], gc)
        store_set("battle", {"attacker_cards": [], "defender_cards": []}, gc)
        store_set("table_cards", [], gc)
        store_set("riddle_power_play", {}, gc)
        store_set("friendly_exchange", {}, gc)
        store_set("show_card_to_player", {}, gc)
        idx = list(range(len(game_data.ASSISTANT_REPLIES)))
        random.shuffle(idx)
        store_set("assistant_replies_index", idx, gc)
        metrics = {"Rolls": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0}}
        store_set("game", {"is_started": False, "stats": {}, "metrics": metrics}, gc)

        games = store_get("games") or []
        games.append({"game_code": gc})
        store_set("games", games)

        self.game_code = gc
        self.player_code = pc
        self._refresh()
        return rx.redirect("/play")

    def join_existing_game(self) -> rx.event.EventSpec | None:
        gc = self.join_game_code_input
        pc = self.setup_player_code
        character = self.setup_character
        name = self.player_name

        players = store_get("players", gc) or {}
        player = {
            "id": len(players),
            "name": name,
            "character": character,
            "current_turn": False,
            "cards": [],
            "selected_cards": [],
            "player_code": pc,
            "positions": [],
            "special_actions": {"show_hand_to_character": None},
        }
        players[pc] = player
        store_set("players", players, gc)

        self.game_code = gc
        self.player_code = pc
        self._refresh()
        return rx.redirect("/play")

    # -- resume --
    def set_resume_game_code(self, v: str) -> None:
        self.resume_game_code = v.lower().strip()

    def set_resume_player_code(self, v: str) -> None:
        self.resume_player_code = v.strip()

    def do_resume_game(self) -> rx.event.EventSpec | None:
        gc = self.resume_game_code
        pc = self.resume_player_code
        players = store_get("players", gc)
        if players and pc in players:
            self.game_code = gc
            self.player_code = pc
            self.player_name = players[pc].get("name", "")
            self._refresh()
            return rx.redirect("/play")
        return None

    # ---------------------------------------------------------------
    # Play page events
    # ---------------------------------------------------------------
    def refresh_game(self) -> None:
        self._refresh()

    def on_play_load(self) -> None:
        self._refresh()

    # -- general actions --
    def general_action(self, action: str) -> None:
        gc = self.game_code
        if action == "Attack from Good City":
            self._add_city_battle_card("attacker", "good")
        elif action == "Attack from Evil City":
            self._add_city_battle_card("attacker", "evil")
        elif action == "Defend from Good City":
            self._add_city_battle_card("defender", "good")
        elif action == "Defend from Evil City":
            self._add_city_battle_card("defender", "evil")
        elif action == "Show Hand to Player":
            self.show_hand_dialog_open = True
            self._refresh()
            return
        elif action == "Draw Card":
            self._draw_cards(1)
        elif action == "Roll Die":
            roll = random.randint(1, 6)
            game = store_get("game", gc) or {}
            game.setdefault("stats", {})["Last Roll"] = roll
            game.setdefault("metrics", {}).setdefault(
                "Rolls", {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0}
            )
            game["metrics"]["Rolls"][str(roll)] = (
                game["metrics"]["Rolls"].get(str(roll), 0) + 1
            )
            store_set("game", game, gc)
            action = f"Roll Die: {roll}"
        elif action == "End Turn":
            self._set_next_turn()
        elif action == "Start Game":
            self._start_game()
        elif action == "Surrender":
            pass
        self._add_activity(action)
        self._refresh()

    # -- card actions --
    def select_card(self, card_id: int, owner_code: str, index: int) -> None:
        gc = self.game_code
        pc = self.player_code
        self._unselect_all_cards()
        players = store_get("players", gc) or {}
        actual_id = card_id
        if owner_code != pc:
            owner_cards = players.get(owner_code, {}).get("cards", [])
            if 0 <= index < len(owner_cards):
                actual_id = owner_cards[index]
        players.setdefault(pc, {}).setdefault("selected_cards", []).append(actual_id)
        store_set("players", players, gc)
        self._refresh()

    def card_action(self, action: str) -> None:
        pc = self.player_code
        gc = self.game_code
        players = store_get("players", gc) or {}
        selected = players.get(pc, {}).get("selected_cards", [])
        if not selected:
            return
        card_id = selected[0]
        card = game_data.get_card(card_id)

        if action == "Unselect":
            self._unselect_card(card_id)
        elif action == "Use to Defend":
            self._use_card_for_battle(card_id, "defender")
            self._add_activity(f"Use to Defend ({card.get('name', '')})")
        elif action == "Use to Attack":
            self._use_card_for_battle(card_id, "attacker")
            self._add_activity(f"Use to Attack ({card.get('name', '')})")
        elif action == "Discard":
            self._add_card_to_discard(card_id)
        elif action == "Take Card from Player":
            owner_code = self._get_card_owner_code(card_id)
            owner_players = store_get("players", gc) or {}
            owner_char = owner_players.get(owner_code, {}).get("character", "?")
            self._transfer_card(card_id)
            self._add_activity(f"Take Card from Player (from {owner_char})")
        elif action == "Place on Table":
            self._place_card_on_table(card_id)
            self._add_activity(f"Place on Table ({card.get('name', '')})")
        elif action == "Take Card in Friendly Exchange":
            self._use_card_in_friendly_exchange(card_id)
        elif action == "Riddle Player":
            self._riddle_player(card_id)
        elif action == "Show Card to Player":
            self.show_card_dialog_open = True
            self._refresh()
            return
        elif action == "Give Card to Player":
            self.give_card_dialog_open = True
            self._refresh()
            return
        elif action == "Retain":
            self._unselect_card(card_id)
        elif action == "Power Play":
            self._place_card_on_table(card_id)
            self._add_activity(f"Power Play ({card.get('name', '')})")
        self._refresh()

    # -- chat --
    def set_chat_input(self, value: str) -> None:
        self.chat_input_value = value

    def send_chat(self, _form_data: dict) -> None:
        prompt = self.chat_input_value.strip()
        self.chat_input_value = ""
        if not prompt:
            self._refresh()
            return
        if prompt.lower() == "stats":
            self._get_game_stats_chat()
        elif prompt.lower().startswith("rex, let it rain"):
            self._add_activity(prompt, msg_type="user")
            self._add_activity(
                "That spell is powerful! The skies rumble...", msg_type="assistant"
            )
        elif prompt.lower().startswith("rex"):
            self._add_activity(prompt, msg_type="user")
            reply = self._get_random_assistant_reply()
            self._add_activity(reply, msg_type="assistant")
        elif prompt.lower() != "m":
            self._add_activity(prompt, msg_type="user")
        self._refresh()

    # -- board click --
    def board_click(self, coords: list) -> None:
        if not coords or len(coords) < 2:
            return
        gc = self.game_code
        pc = self.player_code
        players = store_get("players", gc) or {}
        player = players.get(pc)
        if not player:
            return
        position = [int(coords[0]), int(coords[1])]
        positions = player.get("positions", [])
        if position not in positions:
            positions.insert(0, position)
            del positions[2:]
            player["positions"] = positions
            store_set("players", players, gc)
            self._add_activity("Moved")
        self._refresh()

    # -- shuffle cards --
    def shuffle_my_cards(self) -> None:
        gc = self.game_code
        pc = self.player_code
        players = store_get("players", gc) or {}
        cards = players.get(pc, {}).get("cards", [])
        random.shuffle(cards)
        players[pc]["cards"] = cards
        store_set("players", players, gc)
        self._refresh()

    # -- battle actions --
    def discard_battle_card(self, card_id: int, role: str) -> None:
        gc = self.game_code
        battle = store_get("battle", gc) or {"attacker_cards": [], "defender_cards": []}
        key = f"{role}_cards"
        if card_id in battle.get(key, []):
            battle[key].remove(card_id)
            store_set("battle", battle, gc)
        self._add_card_to_discard(card_id)
        self._refresh()

    def retain_battle_card(self, card_id: int, role: str) -> None:
        gc = self.game_code
        battle = store_get("battle", gc) or {"attacker_cards": [], "defender_cards": []}
        key = f"{role}_cards"
        if card_id in battle.get(key, []):
            battle[key].remove(card_id)
            store_set("battle", battle, gc)
        self._refresh()

    def remove_battle_card(self, card_id: int, role: str) -> None:
        gc = self.game_code
        battle = store_get("battle", gc) or {"attacker_cards": [], "defender_cards": []}
        key = f"{role}_cards"
        if card_id in battle.get(key, []):
            battle[key].remove(card_id)
            store_set("battle", battle, gc)
        self._refresh()

    # -- table card actions --
    def discard_table_card(self, card_id: int) -> None:
        self._add_card_to_discard(card_id)
        self._refresh()

    def retain_table_card(self, card_id: int) -> None:
        gc = self.game_code
        table_cards = store_get("table_cards", gc) or []
        if card_id in table_cards:
            table_cards.remove(card_id)
            store_set("table_cards", table_cards, gc)
        self._refresh()

    # -- riddle actions --
    def show_riddler_card(self) -> None:
        gc = self.game_code
        rpp = store_get("riddle_power_play", gc) or {}
        rpp["can_riddler_see_card"] = True
        store_set("riddle_power_play", rpp, gc)
        self._refresh()

    def end_riddle(self) -> None:
        store_set("riddle_power_play", {}, self.game_code)
        self._refresh()

    def give_card_to_riddler(self) -> None:
        card_id = int(self.riddle_power_play.get("riddle_card", 0))
        character = str(self.riddle_power_play.get("riddler", ""))
        if card_id and character:
            self._transfer_card(card_id, character=character)
        store_set("riddle_power_play", {}, self.game_code)
        self._refresh()

    # -- friendly exchange actions --
    def complete_friendly_exchange(self) -> None:
        gc = self.game_code
        fe = store_get("friendly_exchange", gc) or {}
        first_party = fe.get("first_party", "")
        second_party = fe.get("second_party", "")
        fp_data = fe.get(first_party, {})
        sp_data = fe.get(second_party, {})
        fp_card = fp_data.get("card")
        sp_card = sp_data.get("card")
        if fp_card is not None and sp_card is not None:
            self._transfer_card(fp_card, character=first_party)
            self._transfer_card(sp_card, character=second_party)
        store_set("friendly_exchange", {}, gc)
        self._refresh()

    # -- show hand / show card / give card dialog handlers --
    def confirm_show_hand(self, character: str) -> None:
        gc = self.game_code
        pc = self.player_code
        players = store_get("players", gc) or {}
        if pc in players:
            players[pc]["special_actions"]["show_hand_to_character"] = character
            store_set("players", players, gc)
            self._add_activity(f"Show Hand to Player ({character})")
        self.show_hand_dialog_open = False
        self._refresh()

    def confirm_show_card(self, character: str) -> None:
        gc = self.game_code
        pc = self.player_code
        players = store_get("players", gc) or {}
        selected = players.get(pc, {}).get("selected_cards", [])
        if selected:
            card_id = selected[0]
            store_set(
                "show_card_to_player",
                {"show_card_to_character": character, "show_card": card_id},
                gc,
            )
            self._add_activity(f"Show Card to Player ({character})")
        self.show_card_dialog_open = False
        self._refresh()

    def confirm_give_card(self, character: str) -> None:
        gc = self.game_code
        pc = self.player_code
        players = store_get("players", gc) or {}
        selected = players.get(pc, {}).get("selected_cards", [])
        if selected:
            card_id = selected[0]
            self._transfer_card(card_id, character=character)
            self._add_activity(f"Give Card to Player ({character})")
        self.give_card_dialog_open = False
        self._refresh()

    def close_dialog(self) -> None:
        self.show_hand_dialog_open = False
        self.show_card_dialog_open = False
        self.give_card_dialog_open = False

    def clear_show_card(self) -> None:
        store_set("show_card_to_player", {}, self.game_code)
        self._refresh()

    # -- exit game --
    def exit_game(self) -> rx.event.EventSpec:
        self.game_code = ""
        self.player_code = ""
        self.players = {}
        self.activities = []
        return rx.redirect("/")

    # -- admin --
    def load_admin(self) -> None:
        _ensure_global_data()

    # ---------------------------------------------------------------
    # Internal game-logic helpers
    # ---------------------------------------------------------------
    def _draw_cards(self, number: int = 1, target_code: str = "") -> list[int]:
        gc = self.game_code
        pc = target_code or self.player_code
        draw_pile: list[int] = store_get("draw_pile", gc) or []
        if number > len(draw_pile):
            self._reset_draw_pile()
            draw_pile = store_get("draw_pile", gc) or []
        drawn = []
        for _ in range(number):
            if draw_pile:
                drawn.append(draw_pile.pop())
        store_set("draw_pile", draw_pile, gc)
        players = store_get("players", gc) or {}
        players.setdefault(pc, {}).setdefault("cards", []).extend(drawn)
        store_set("players", players, gc)
        return drawn

    def _reset_draw_pile(self) -> None:
        gc = self.game_code
        new_pile = store_get("discards", gc) or []
        random.shuffle(new_pile)
        store_set("draw_pile", new_pile, gc)
        store_set("discards", [], gc)
        self._add_activity("Resetting the draw pile!")

    def _start_game(self) -> None:
        gc = self.game_code
        game = store_get("game", gc) or {}
        if game.get("is_started"):
            return
        game["is_started"] = True
        store_set("game", game, gc)
        players = store_get("players", gc) or {}
        codes = list(players.keys())
        if codes:
            first = random.choice(codes)
            players[first]["current_turn"] = True
            store_set("players", players, gc)
            for code in codes:
                self._draw_cards(number=2, target_code=code)

    def _set_next_turn(self) -> None:
        gc = self.game_code
        pc = self.player_code
        players = store_get("players", gc) or {}
        order = list(players.keys())
        if pc not in order:
            return
        idx = order.index(pc)
        nxt = order[(idx + 1) % len(order)]
        players[pc]["current_turn"] = False
        players[nxt]["current_turn"] = True
        store_set("players", players, gc)

    def _unselect_card(self, card_id: int, for_all: bool = False) -> None:
        gc = self.game_code
        pc = self.player_code
        players = store_get("players", gc) or {}
        if for_all:
            for p in players.values():
                if card_id in p.get("selected_cards", []):
                    p["selected_cards"].remove(card_id)
        else:
            sel = players.get(pc, {}).get("selected_cards", [])
            if card_id in sel:
                sel.remove(card_id)
        store_set("players", players, gc)

    def _unselect_all_cards(self) -> None:
        gc = self.game_code
        pc = self.player_code
        players = store_get("players", gc) or {}
        if pc in players:
            players[pc]["selected_cards"] = []
            store_set("players", players, gc)

    def _add_card_to_discard(self, card_id: int) -> None:
        card = game_data.get_card(card_id)
        if not card.get("is_discardable", True):
            return
        gc = self.game_code
        self._unselect_card(card_id, for_all=True)
        discards = store_get("discards", gc) or []
        if card_id not in discards:
            discards.append(card_id)
            store_set("discards", discards, gc)
            self._remove_card_from_hand(card_id)
            self._remove_table_card(card_id)
            self._add_activity(f"Discard ({card.get('name', '')})")

    def _remove_card_from_hand(self, card_id: int, pc: str = "") -> None:
        gc = self.game_code
        pc = pc or self.player_code
        players = store_get("players", gc) or {}
        cards = players.get(pc, {}).get("cards", [])
        if card_id in cards:
            cards.remove(card_id)
            store_set("players", players, gc)

    def _add_card_to_hand(self, card_id: int, character: str = "") -> None:
        gc = self.game_code
        players = store_get("players", gc) or {}
        target_code = ""
        if character:
            for code, p in players.items():
                if p.get("character") == character:
                    target_code = code
                    break
        else:
            target_code = self.player_code
        if target_code and target_code in players:
            cards = players[target_code].setdefault("cards", [])
            if card_id not in cards:
                cards.append(card_id)
                store_set("players", players, gc)

    def _transfer_card(self, card_id: int, character: str = "") -> None:
        owner_code = self._get_card_owner_code(card_id)
        if owner_code:
            self._remove_card_from_hand(card_id, owner_code)
        self._add_card_to_hand(card_id, character=character)
        self._unselect_card(card_id, for_all=True)

    def _use_card_for_battle(self, card_id: int, role: str) -> None:
        gc = self.game_code
        battle = store_get("battle", gc) or {"attacker_cards": [], "defender_cards": []}
        key = f"{role}_cards"
        if card_id not in battle.setdefault(key, []):
            battle[key].append(card_id)
        store_set("battle", battle, gc)

    def _add_city_battle_card(self, role: str, side: str) -> None:
        card_id = 91 if side == "good" else 92
        self._use_card_for_battle(card_id, role)

    def _place_card_on_table(self, card_id: int) -> None:
        gc = self.game_code
        tc = store_get("table_cards", gc) or []
        tc.append(card_id)
        store_set("table_cards", tc, gc)

    def _remove_table_card(self, card_id: int) -> None:
        gc = self.game_code
        tc = store_get("table_cards", gc) or []
        if card_id in tc:
            tc.remove(card_id)
            store_set("table_cards", tc, gc)

    def _riddle_player(self, card_id: int) -> None:
        gc = self.game_code
        pc = self.player_code
        players = store_get("players", gc) or {}
        this_char = players.get(pc, {}).get("character", "")
        owner_code = self._get_card_owner_code(card_id)
        owner_char = players.get(owner_code, {}).get("character", "")
        rpp = {
            "riddle_card": card_id,
            "card_owner": owner_char,
            "riddler": this_char,
            "can_riddler_see_card": False,
        }
        store_set("riddle_power_play", rpp, gc)
        self._add_activity(f"Riddle Player ({owner_char})")

    def _use_card_in_friendly_exchange(self, card_id: int) -> None:
        gc = self.game_code
        pc = self.player_code
        players = store_get("players", gc) or {}
        this_char = players.get(pc, {}).get("character", "")
        owner_code = self._get_card_owner_code(card_id)
        owner_char = players.get(owner_code, {}).get("character", "")
        fe = store_get("friendly_exchange", gc) or {}
        if fe:
            fe[this_char] = {"character": owner_char, "card": card_id}
            fe["status"] = "ready"
        else:
            fe = {
                this_char: {"character": owner_char, "card": card_id},
                "status": "pending",
                "first_party": this_char,
                "second_party": owner_char,
            }
        store_set("friendly_exchange", fe, gc)
        self._add_activity(f"Friendly Exchange ({owner_char})")

    def _get_random_assistant_reply(self) -> str:
        gc = self.game_code
        idx_list: list[int] = store_get("assistant_replies_index", gc) or []
        if not idx_list:
            idx_list = list(range(len(game_data.ASSISTANT_REPLIES)))
            random.shuffle(idx_list)
        selected = idx_list.pop()
        store_set("assistant_replies_index", idx_list, gc)
        if 0 <= selected < len(game_data.ASSISTANT_REPLIES):
            return game_data.ASSISTANT_REPLIES[selected]
        return "The road goes ever on and on..."

    def _get_game_stats_chat(self) -> None:
        gc = self.game_code
        players = store_get("players", gc) or {}
        hobbits = [
            p["character"]
            for p in players.values()
            if game_data.CHARACTERS.get(p["character"], {}).get("side") == "good"
        ]
        riders = [
            p["character"]
            for p in players.values()
            if game_data.CHARACTERS.get(p["character"], {}).get("side") == "evil"
        ]
        resp = ""
        if hobbits:
            resp += f"For the Hobbits, we have: {', '.join(hobbits)}. "
        else:
            resp += "There are no Hobbits playing. "
        if riders:
            resp += f"For the Black Riders, we have: {', '.join(riders)}"
        else:
            resp += "There are no Black Riders playing."
        self._add_activity(resp, msg_type="assistant")
