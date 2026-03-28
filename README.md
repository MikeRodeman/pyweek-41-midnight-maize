# Midnight Maize

Midnight Maize is a survival-horror puzzle game where you must navigate a pitch-black corn maze using glow sticks while being hunted by a supernatural scarecrow. You must find the lookout tower before the field's supernatural guardian finds you.

Game made for the PyWeek 41 game jam on the Python Discord server.

https://pyweek.org/41


https://pyweek.org/e/WoollyDebug_41/


https://www.pythondiscord.com/ 


## Dependencies

* Python 3.10+
* pygame-ce

## How to Run

1. Install Dependencies:

   Install Python 3.10+: https://www.python.org/downloads/
   
   Install pygame-ce with pip:

   pip install pygame-ce

2. Run the Game:
   Navigate to the project folder in a terminal and run:
   
   ```bash
   python run_game.py
   ```
   
---

## Controls

### Movement & Actions
* WASD / Arrow Keys: Move character
* Shift: Sprint (Drains Stamina)
* Spacebar: Drop Glow Stick (Consumes inventory)

---

## What's in the Maize?

* Dynamic Fog of War: A lighting system where only your light and dropped glow sticks reveal your environment.
* Bot: A supernatural scarecrow utilizes A* Pathfinding and a state-based "Brain" to wander, investigate disturbances, and hunt the player.
* Procedural Generation: Every maze is unique. Use the Seed System to replay specific maps or challenge friends.
* Resource Management: You have a limited number of glow sticks. Dropping them provides permanent light but alerts the scarecrow to your location.
* Stamina: Sprinting is vital for survival but requires careful management to avoid exhaustion.

---

## Attributions

### Fonts
m5x7 and m6x11: Created by Daniel Linssen:
   * https://managore.itch.io/m5x7
   * https://managore.itch.io/m6x11
