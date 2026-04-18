"""Static game data for Riddle of the Ring."""

CHARACTERS: dict = {
    "Frodo": {"color": "yellow", "side": "good", "marker": "white", "marker_color_code": "#ffffff"},
    "Sam": {"color": "green", "side": "good", "marker": "green", "marker_color_code": "#009933"},
    "Merry": {"color": "blue", "side": "good", "marker": "blue", "marker_color_code": "#0066ff"},
    "Pippin": {"color": "violet", "side": "good", "marker": "yellow", "marker_color_code": "#ffff00"},
    "Black Rider 1": {"color": "red", "side": "evil", "marker": "black", "marker_color_code": "#000000"},
    "Black Rider 2": {"color": "black", "side": "evil", "marker": "red", "marker_color_code": "#cc3300"},
    "Black Rider 3": {"color": "black", "side": "evil", "marker": "brown", "marker_color_code": "#663300"},
    "Black Rider 4": {"color": "orange", "side": "evil", "marker": "grey", "marker_color_code": "#999999"},
}

CHARACTER_NAMES: list = list(CHARACTERS.keys())

CARDS: list = [
    {"id": 1, "name": "Boat", "image": "Boat"},
    {"id": 2, "name": "Boat", "image": "Boat"},
    {"id": 3, "name": "Boat", "image": "Boat"},
    {"id": 4, "name": "Boat", "image": "Boat"},
    {"id": 5, "name": "Boat", "image": "Boat"},
    {"id": 6, "name": "Rope", "image": "Rope"},
    {"id": 7, "name": "Rope", "image": "Rope"},
    {"id": 8, "name": "Rope", "image": "Rope"},
    {"id": 9, "name": "Rope", "image": "Rope"},
    {"id": 10, "name": "Rope", "image": "Rope"},
    {"id": 11, "name": "Cloak", "image": "Cloak"},
    {"id": 12, "name": "Cloak", "image": "Cloak"},
    {"id": 13, "name": "Cloak", "image": "Cloak"},
    {"id": 14, "name": "Cloak", "image": "Cloak"},
    {"id": 15, "name": "Cloak", "image": "Cloak"},
    {"id": 16, "name": "Horse", "image": "Horse 1"},
    {"id": 17, "name": "Horse", "image": "Horse 2"},
    {"id": 18, "name": "Horse", "image": "Horse 3"},
    {"id": 19, "name": "Horse", "image": "Horse 4"},
    {"id": 20, "name": "Horse", "image": "Horse 5"},
    {"id": 21, "name": "Horse", "image": "Horse 6"},
    {"id": 22, "name": "Eagles", "image": "Eagles 1", "battle_point": 1},
    {"id": 23, "name": "Eagles", "image": "Eagles 2", "battle_point": 1},
    {"id": 24, "name": "Flying Beasts", "image": "Flying Beasts 1", "battle_point": 1},
    {"id": 25, "name": "Flying Beasts", "image": "Flying Beasts 2", "battle_point": 1},
    {"id": 26, "name": "Good Army", "image": "Good Army 1", "battle_point": 1},
    {"id": 27, "name": "Good Army", "image": "Good Army 2", "battle_point": 1},
    {"id": 28, "name": "Good Army", "image": "Good Army 3", "battle_point": 1},
    {"id": 29, "name": "Good Army", "image": "Good Army 4", "battle_point": 1},
    {"id": 30, "name": "Good Army", "image": "Good Army 5", "battle_point": 1},
    {"id": 31, "name": "Good Army", "image": "Good Army 6", "battle_point": 1},
    {"id": 32, "name": "Good Army", "image": "Good Army 7", "battle_point": 1},
    {"id": 33, "name": "Evil Army", "image": "Evil Army 1", "battle_point": 1},
    {"id": 34, "name": "Evil Army", "image": "Evil Army 2", "battle_point": 1},
    {"id": 35, "name": "Evil Army", "image": "Evil Army 3", "battle_point": 1},
    {"id": 36, "name": "Evil Army", "image": "Evil Army 4", "battle_point": 1},
    {"id": 37, "name": "Evil Army", "image": "Evil Army 5", "battle_point": 1},
    {"id": 38, "name": "Evil Army", "image": "Evil Army 6", "battle_point": 1},
    {"id": 39, "name": "Evil Army", "image": "Evil Army 7", "battle_point": 1},
    {"id": 40, "name": "Neutral Army", "image": "Neutral Army 1", "battle_point": 1},
    {"id": 41, "name": "Neutral Army", "image": "Neutral Army 2", "battle_point": 1},
    {"id": 42, "name": "Neutral Army", "image": "Neutral Army 3", "battle_point": 1},
    {"id": 43, "name": "Neutral Army", "image": "Neutral Army 4", "battle_point": 1},
    {"id": 44, "name": "Frodo", "image": "Frodo", "battle_point": 1},
    {"id": 45, "name": "Sam", "image": "Sam", "battle_point": 1},
    {"id": 46, "name": "Merry", "image": "Merry", "battle_point": 1},
    {"id": 47, "name": "Pippin", "image": "Pippin", "battle_point": 1},
    {"id": 48, "name": "Black Rider 1", "image": "Black Rider 1", "battle_point": 1},
    {"id": 49, "name": "Black Rider 2", "image": "Black Rider 2", "battle_point": 1},
    {"id": 50, "name": "Black Rider 3", "image": "Black Rider 3", "battle_point": 1},
    {"id": 51, "name": "Black Rider 4", "image": "Black Rider 4", "battle_point": 1},
    {"id": 52, "name": "Gandalf", "image": "Gandalf", "battle_point": 1},
    {"id": 53, "name": "Galadriel", "image": "Galadriel", "battle_point": 1},
    {"id": 54, "name": "Sauron", "image": "Sauron", "battle_point": 1},
    {"id": 55, "name": "The Balrog", "image": "The Balrog", "battle_point": 1},
    {"id": 56, "name": "The Ring", "image": "The Ring", "battle_point": 1, "is_discardable": False},
    {"id": 57, "name": "Treebeard", "image": "Treebeard", "battle_point": 1},
    {"id": 58, "name": "Strider", "image": "Strider", "battle_point": 2},
    {"id": 59, "name": "Boromir", "image": "Boromir", "battle_point": 1},
    {"id": 60, "name": "Legolas", "image": "Legolas", "battle_point": 1},
    {"id": 61, "name": "Gimli", "image": "Gimli", "battle_point": 1},
    {"id": 62, "name": "Butterbur", "image": "Butterbur", "battle_point": 1},
    {"id": 63, "name": "Saruman", "image": "Saruman", "battle_point": 1},
    {"id": 64, "name": "Mouth of Sauron", "image": "Mouth of Sauron", "battle_point": 2},
    {"id": 65, "name": "Wormtongue", "image": "Wormtongue", "battle_point": 1},
    {"id": 66, "name": "Grishnakh", "image": "Grishnakh", "battle_point": 1},
    {"id": 67, "name": "Ugluk", "image": "Ugluk", "battle_point": 1},
    {"id": 68, "name": "Bill Ferny", "image": "Bill Ferny", "battle_point": 1},
    {"id": 69, "name": "Gollum", "image": "Gollum"},
    {"id": 70, "name": "Tom Bombadil", "image": "Tom Bombadil"},
    {"id": 71, "name": "Shelob", "image": "Shelob"},
    {"id": 72, "name": "Bilbo", "image": "Bilbo"},
    {"id": 73, "name": "Riddle", "image": "Riddle 1"},
    {"id": 74, "name": "Riddle", "image": "Riddle 2"},
    {"id": 75, "name": "Riddle", "image": "Riddle 3"},
    {"id": 76, "name": "Riddle", "image": "Riddle 4"},
    {"id": 77, "name": "Riddle", "image": "Riddle 5"},
    {"id": 78, "name": "Elf Ring", "image": "Elf Ring 1"},
    {"id": 79, "name": "Elf Ring", "image": "Elf Ring 2"},
    {"id": 80, "name": "Elf Ring", "image": "Elf Ring 3"},
    {"id": 81, "name": "Palantir", "image": "Palantir 1"},
    {"id": 82, "name": "Palantir", "image": "Palantir 2"},
    {"id": 83, "name": "Palantir", "image": "Palantir 3"},
    {"id": 84, "name": "Spy", "image": "Spy 1"},
    {"id": 85, "name": "Spy", "image": "Spy 2"},
    {"id": 86, "name": "Spy", "image": "Spy 3"},
    {"id": 87, "name": "Spy", "image": "Spy 4"},
    {"id": 88, "name": "Spy", "image": "Spy 5"},
    {"id": 89, "name": "Spy", "image": "Spy 6"},
    {"id": 90, "name": "Spy", "image": "Spy 7"},
    {"id": 91, "name": "Good City Battlepoint", "image": "Reverse", "type": "City Battlepoint", "include_in_draw_pile": False},
    {"id": 92, "name": "Evil City Battlepoint", "image": "Reverse", "type": "City Battlepoint", "include_in_draw_pile": False},
]

CARDS_BY_ID: dict = {card["id"]: card for card in CARDS}

ACTION_BUTTONS: list = [
    {"name": "Start Game", "is_pre_start_only": True, "image": "/button_images/start_turn.png"},
    {"name": "Roll Die", "is_post_start_only": True, "is_current_turn_only": True, "image": "/button_images/roll_die.png"},
    {"name": "Draw Card", "is_post_start_only": True, "is_current_turn_only": True, "image": "/button_images/draw_card.png"},
    {"name": "Show Hand to Player", "is_post_start_only": True, "image": "/button_images/show_hand.png"},
    {"name": "Surrender", "is_post_start_only": True, "is_current_turn_only": True, "image": "/button_images/surrender.png"},
    {"name": "Attack from Good City", "is_side": "good", "is_post_start_only": True, "is_current_turn_only": True, "image": "/button_images/attack_good.png"},
    {"name": "Defend from Good City", "is_side": "good", "is_post_start_only": True, "is_not_current_turn_only": True, "image": "/button_images/defend_good.png"},
    {"name": "Attack from Evil City", "is_side": "evil", "is_post_start_only": True, "is_current_turn_only": True, "image": "/button_images/attack_evil.png"},
    {"name": "Defend from Evil City", "is_side": "evil", "is_post_start_only": True, "is_not_current_turn_only": True, "image": "/button_images/defend_evil.png"},
    {"name": "End Turn", "is_post_start_only": True, "is_current_turn_only": True, "image": "/button_images/end_turn.png"},
]

CARD_ACTION_BUTTONS: list = [
    {"name": "Unselect"},
    {"name": "Retain", "is_card_owner_only": True},
    {"name": "Discard", "is_current_turn_only": True, "is_card_owner_only": True},
    {"name": "Power Play", "is_current_turn_only": True, "is_card_owner_only": True},
    {"name": "Use to Attack", "is_current_turn_only": True, "is_card_owner_only": True, "is_battle_card_only": True},
    {"name": "Use to Defend", "is_not_current_turn_only": True, "is_card_owner_only": True, "is_battle_card_only": True},
    {"name": "Place on Table", "is_card_owner_only": True},
    {"name": "Riddle Player", "is_current_turn_only": True},
    {"name": "Take Card in Friendly Exchange", "is_not_card_owner_only": True},
    {"name": "Show Card to Player", "is_card_owner_only": True},
    {"name": "Take Card from Player", "is_not_card_owner_only": True},
    {"name": "Give Card to Player", "is_card_owner_only": True},
]

INITIAL_CHAT_MESSAGES: list = [
    {
        "type": "assistant",
        "action": (
            "Welcome to Riddle of the Ring! I'm your guide, Rex the Lion. "
            "Use your Game Code to invite fellow players to join you on the quest -- or oppose you! "
            "Once everyone has joined, click Start Game (under General Actions). "
            "Each player will receive two cards to begin with. "
            "One player will be selected to start and play will proceed in the order shown in the players area."
        ),
    },
    {
        "type": "assistant",
        "action": (
            "Use the General Actions to roll the die and click the game board to move your marker. "
            "Select cards from your hand to perform special actions. "
            "After you complete your turn, click End Turn (under General Actions)."
        ),
    },
    {
        "type": "assistant",
        "action": (
            "Use the chat input area to share messages with other players. "
            "You can also ask me to cast magic spells, though I'm still learning from Tom Bombadil. "
            'Just ask me by saying "Rex, ...". You might even get me to share a few one liners.'
        ),
    },
]

ASSISTANT_REPLIES: list = [
    "Nice day in the Shire, isn't it?",
    "Have you ever wondered what Gandalf was like as a teenager?",
    "Do you think hobbits ever get tired of second breakfast?",
    "I heard elves have excellent singing voices. Maybe we should start a choir!",
    "Have you ever tried talking to trees? I hear they're great listeners.",
    "I wonder if Gollum ever regrets losing his precious.",
    "Do you think Legolas ever gets jealous of Gimli's beard?",
    "I heard the Ents throw the best parties.",
    "One does not simply walk into Mordor... unless they have really comfy shoes.",
    "I wonder if Sauron ever takes a break from being evil to enjoy a nice sunset.",
    "If Frodo had a GPS, the quest to Mount Doom would have been a lot shorter.",
    "I bet Aragorn gives the best motivational speeches.",
    "I wonder if Bilbo ever regrets not taking a map of the Lonely Mountain.",
    "I hear the food at the Prancing Pony is legendary.",
    "I wonder if Gandalf ever gets tired of saying 'You shall not pass!'",
    "I hear Rivendell is lovely this time of year.",
    "I wonder if Legolas ever gets tired of being so darn cool.",
    "I bet Pippin tells the best jokes around the campfire.",
    "Do you think Smeagol ever wishes he could just go back to being a simple hobbit?",
    "I wonder if anyone ever accidentally stumbled upon the One Ring while gardening.",
    "They say the beacons of Gondor are the best way to communicate in a pinch.",
    "I wonder if the Balrog ever gets lonely down in the depths of Moria.",
    "I bet Arwen gives the best fashion advice.",
    "I wonder if Sam ever gets tired of carrying Frodo's bags.",
    "I heard the Shire has the best mushrooms in all of Middle-earth.",
    "Do you think Gimli ever gets tired of being underestimated because he's short?",
    "I wonder if anyone's ever tried to prank the Eye of Sauron.",
    "I bet Merry and Pippin throw the best parties in the Shire.",
    "I wonder if anyone's ever tried to give the Ringwraiths a makeover.",
    "I heard the elves have some pretty fancy hair care routines.",
    "I bet Gandalf's fireworks are the talk of the town.",
    "I wonder if Legolas ever gets tired of people asking him to shoot things.",
    "I bet the Fellowship had some interesting sing-alongs on their journey.",
    "I wonder if anyone's ever tried to teach an orc how to dance.",
    "I bet the Eagles have some amazing views when they're flying.",
    "I wonder if anyone's ever tried to challenge Treebeard to a staring contest.",
    "I bet the hobbits make the best pies in the Shire.",
    "I wonder if anyone's ever tried to play hide and seek with a Nazgul.",
    "I bet Gimli's beard has its own fan club.",
    "I wonder if Frodo ever gets tired of people asking about his jewelry.",
    "I bet the elves have some pretty fancy dance moves.",
    "I bet Gandalf's staff has some pretty cool tricks up its sleeve.",
    "I bet the hobbits have some wild stories to tell about their adventures.",
    "I bet Aragorn's sword has seen some serious action.",
    "I bet the Ents have some fascinating conversations.",
    "I bet the elves have some incredible recipes for lembas bread.",
    "I bet Gandalf's beard has some interesting secrets hidden in it.",
    "I bet the hobbits have some creative ways of cooking mushrooms.",
    "I bet the elves have some breathtaking gardens in Rivendell.",
    "I bet Gandalf's pipe has some magical tobacco in it.",
    "I bet the hobbits have some amazing gardening tips.",
    "I bet the elves have some legendary feasts.",
    "I bet Gandalf's cloak has some hidden pockets for snacks.",
    "I bet the hobbits have some secret recipes for mushroom stew.",
    "I bet the elves have some epic tales to tell.",
    "I bet Gandalf's map has some secret passages marked on it.",
    "I bet the hobbits have some ingenious inventions for making second breakfast even better.",
    "I bet the elves have some magical remedies for common ailments.",
    "I bet Gandalf's satchel has some mysterious artifacts inside.",
    "I bet the hobbits have some clever tricks for outsmarting hungry trolls.",
    "I bet the elves have some breathtaking views from their treetop homes.",
    "I bet Gandalf's spellbook has some powerful incantations.",
    "I bet the hobbits have some delightful songs about the simple joys of life.",
    "I bet the elves have some exquisite dance routines.",
    "I bet Gandalf's pipe smoke forms some interesting shapes.",
    "I bet the hobbits have some clever tricks for hiding from unfriendly neighbors.",
    "I bet the elves have some beautiful poetry hidden away.",
    "I bet Gandalf's beard has some crumbs from all the snacks he's eaten.",
    "I bet the hobbits have some delightful recipes for tea cakes.",
    "I bet the elves have some magical games they play in the moonlight.",
    "I bet Gandalf's hat has some secret compartments for storing snacks.",
    "I bet the hobbits have some hilarious stories about their adventures.",
    "I bet the elves have some enchanting melodies they sing in the forest.",
    "I bet Gandalf's staff has some intricate carvings on it.",
    "I bet the hobbits have some ingenious inventions for farming.",
    "I bet the elves have some magical rituals they perform under the stars.",
    "I bet Gandalf's pipe has some special herbs mixed into the tobacco.",
    "I bet the hobbits have some cozy recipes for mulled wine.",
    "I bet the elves have some mesmerizing dances they perform at festivals.",
    "I bet Gandalf's cloak has some hidden pockets for storing treasures.",
]

RULES_INTRO: str = (
    "Middle-earth is the setting of J.R.R. Tolkien's master works of fantasy: "
    "The Hobbit, The Fellowship of the Ring, The Two Towers, The Return of the King, "
    "and others. Riddle of the Ring is a game which recreates much of the action in his "
    "famous trilogy, The Lord of the Rings. Players will enjoy many of the same adventures "
    "experienced by the original characters. Players do not have to be familiar with "
    "Tolkien's works or Middle-earth in order to play and enjoy Riddle of the Ring.\n\n"
    "In the Lord of the Rings, the Dark Lord (Sauron of Mordor) has discovered that his "
    "long lost Ring of power has been found by something called 'A Hobbit' and taken to "
    "a place called 'The Shire'. With The Ring back under his control, the evil Sauron "
    "can easily destroy the powers of good and rule Middle-earth. He sends his emissaries, "
    "the Black Riders (also known as Ringwraiths or Nazgul), to find The Ring and bring "
    "it to him at his citadel, the Tower of Barad-dur.\n\n"
    "At about the same time, the good Wizard known as Gandalf learns of the significance "
    "of The Ring. Under his direction and influence, a group of noble characters join "
    "together as 'The Fellowship' to help a Hobbit (called Frodo) take The Ring to the "
    "fires at the Cracks of Doom, where it was created. Only there, in all of Middle-earth, "
    "can it be destroyed.\n\n"
    "Thus, the story becomes a struggle between the forces of evil which are trying to get "
    "The Ring to Sauron at Barad-dur, and the forces of good which are trying to destroy "
    "The Ring at the Cracks of Doom. The Game, Riddle of the Ring, starts at this point "
    "in the story. Each player chooses to be one of the Hobbits or one of the Black Riders. "
    "During the course of play, each player tries to obtain The Ring (The Ring card) and "
    "take it to his appropriate objective space: the Cracks of Doom or Barad-dur."
)

BASIC_GAME_SECTIONS: list = [
    "THE BASIC GAME",
    "B-1 THE GAME COMPONENTS",
    "B-2 Starting The Game",
    "B-3 How To Win The Game",
    "B-4 What To Do During A Turn",
    "B-5 Moving A Marker",
    "B-6 The Spaces On The Board",
    "B-7 Using The Cards",
    "B-8 How To Use The Cards",
    "B-9 Friendly Exchanges",
    "B-10 Power Plays",
    "B-11 Battles",
    "B-12 The Halls Of Mandos (The Other World)",
]

ADVANCED_GAME_SECTIONS: list = [
    "THE ADVANCED GAME",
    "A-1 Special Character Cards",
    "A-2 Spy Cards",
    "A-3 Riddle Cards",
    "A-4 Palantir Cards",
    "A-5 Elf Ring Cards",
]

OPTIONAL_RULES_SECTIONS: list = [
    "OPTIONAL RULES",
    "O-1 Additional Character Cards",
    "O-2 Two Player Game",
    "O-3 Gollum",
    "O-4 Shelob",
    "O-5 Tom Bombadil",
    "O-6 Bilbo",
]


def get_card(card_id: int) -> dict:
    return CARDS_BY_ID.get(card_id, {})


def get_card_image_url(card_id: int) -> str:
    card = get_card(card_id)
    if card:
        return f"/card_images/{card['image']}.png"
    return "/card_images/Reverse.png"


def get_shuffled_deck() -> list:
    import random
    draw_pile = [c["id"] for c in CARDS if c.get("include_in_draw_pile") is not False]
    random.shuffle(draw_pile)
    return draw_pile
