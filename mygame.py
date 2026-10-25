import math
import random
import arcade
import os
screenwidth = 1000
screenheight=700
playerradius = 18
playerspeed = 250
trashspawntime = 1
maxtrash = 14
trashradius = 13
TITLE = "Ocean Cleanup"
WATER = (12, 68, 120)
enemyspeed = 95
enemyradius = 26
startlives = 3
enemystartscore = 10
enemyspawntime = 3
maxenemies = 4
musicvolume = 0.7
musicfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "music.ogg")
turtlestartscore = 18
turtlegrabradius = 100
turtleradius = 25
dolphinstartscore = 28
dolphinspeed = 750
dolphincooldown = 5
dolphinradius = 40
whalestartscore = 48
whalesongtime = 8
winscore = 70
buttonwidth = 200
buttonheight = 60
buttonx = screenwidth / 2 - buttonwidth / 2
buttony = 200
barwidth = 300
barheight = 10
barx = 16
bary = screenheight - 95
netstartscore = 38
netspeed = 175
netradius = 34
ingamewidth = 100
ingameheight = 40
ingamex = screenwidth - ingamewidth - 16
ingamey = screenheight - 56
netchance = 0.4
bannertime = 3.5
menuitems = [("easy", "Easy"), ("hard", "Hard"), ("extreme", "Extreme")]
menubuttonwidth = 240
menubuttonheight = 60
menutop = 330
pausex = ingamex - ingamewidth - 10
modes = {
    "easy":    {"playerspeed": 260, "enemyspeed": 80,  "netspeed": 120, "lives": 4, "winscore": 60, "maxenemies": 3, "enemyspawntime": 3},
    "hard":    {"playerspeed": 230, "enemyspeed": 110, "netspeed": 170, "lives": 2, "winscore": 70, "maxenemies": 4, "enemyspawntime": 2},
    "extreme": {"playerspeed": 210, "enemyspeed": 180, "netspeed": 200, "lives": 1, "winscore": 90, "maxenemies": 6, "enemyspawntime": 1},
}
def rect(left, bottom, width, height, color):
    arcade.draw_polygon_filled([(left, bottom), (left + width, bottom), (left + width, bottom + height), (left, bottom + height)], color)
class Trash:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.kind = random.choice(["bottle", "chips", "can"])
class Turtle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
class Enemy:
    def __init__(self, x, y, kind, speed, radius):
        self.x = x
        self.y = y
        self.kind = kind
        self.speed = speed
        self.radius = radius
class Dolphin:
    def __init__(self):
        self.active = False
        self.cooldown = 2.0
        self.x = 0
        self.y = 0
        self.vx = 0
class Whale:
    def __init__(self):
        self.x = -250
        self.y = screenheight - 120
        self.song_timer = 3.0
        self.ring = 0.0
class game(arcade.Window):
    def __init__(self):
        super().__init__(screenwidth, screenheight, TITLE)
        self.background_color = WATER
        self.keys = set()
        self.score_text = arcade.Text("", 16, screenheight - 34, (255, 255, 255), 20)
        self.lives_text = arcade.Text("", 16, screenheight - 64, (255, 255, 255), 20)
        self.end_text = arcade.Text("", screenwidth / 2, screenheight / 2, (255, 255, 255), 44, anchor_x="center")
        self.button_text = arcade.Text("Play again", screenwidth / 2, buttony + 18, (255, 255, 255), 24, anchor_x="center")
        self.message_text = arcade.Text("", screenwidth / 2, screenheight - 140, (255, 255, 255), 22, anchor_x="center")
        self.mode = "easy"
        self.title_text = arcade.Text("Ocean Cleanup", screenwidth / 2, 520, (255, 255, 255), 48, anchor_x="center")
        self.subtitle_text = arcade.Text("Choose a Difficulty", screenwidth / 2, 470, (255, 255, 255), 24, anchor_x="center")
        self.menu_texts = []
        for i, (name, label) in enumerate(menuitems):
            self.menu_texts.append(arcade.Text(label, screenwidth / 2, menutop - i * 80 + 18, (255, 255, 255), 24, anchor_x="center"))
        self.menu_button_text = arcade.Text("Menu", ingamex + ingamewidth / 2, ingamey + 10, (255, 255, 255), 20, anchor_x="center")
        self.pause_button_text = arcade.Text("Pause", pausex + ingamewidth / 2, ingamey + 10, (255, 255, 255), 20, anchor_x="center")
        self.paused_text = arcade.Text("Paused", screenwidth / 2, screenheight / 2, (255, 255, 255), 44, anchor_x="center")
        self.anim = 0
        self.bubbles = []
        for i in range(30):
            self.bubbles.append([random.uniform(0, screenwidth), random.uniform(0, screenheight), random.uniform(2, 6), random.uniform(15, 40)])
        self.credits1 = arcade.Text("Made by Yusuf Tabet", screenwidth / 2, 150, (255, 255, 255), 22, anchor_x="center")
        self.credits2 = arcade.Text("Built with Python and the Python Arcade library. Music by poinl from opengameart.org", screenwidth / 2, 118, (255, 255, 255), 18, anchor_x="center")
        self.music_player = None
        print("looking for:", musicfile)
        print("exists:", os.path.exists(musicfile))
        if os.path.exists(musicfile):
            self.music = arcade.load_sound(musicfile)
            self.music_player = arcade.play_sound(self.music, volume=musicvolume, loop=True)
        else:
            print("Music file not found:", musicfile)
        self.reset()
        self.state = "menu"
    def on_close(self):
        if self.music_player is not None:
            arcade.stop_sound(self.music_player)
        super().on_close()
    def draw_background(self):
        for i in range(5):
            x = 100 + i * 200 + math.sin(self.anim * 0.4 + i) * 30
            arcade.draw_polygon_filled([(x, screenheight), (x + 70, screenheight), (x + 20, 0), (x - 90, 0)], (255, 255, 255, 14))
        for bx, by, br, speed in self.bubbles:
            arcade.draw_circle_outline(bx, by, br, (200, 230, 255, 120), 1)
        rect(0, 0, screenwidth, 48, (194, 170, 110))
        for x in range(40, screenwidth, 110):
            sway = math.sin(self.anim * 1.5 + x) * 8
            arcade.draw_line(x, 48, x + sway, 103, (40, 140, 80), 5)
            arcade.draw_line(x + 14, 48, x + 14 - sway, 86, (50, 160, 90), 4)
    def draw_turtle(self):
        x = self.turtle.x
        y = self.turtle.y
        f = self.facing
        flipper = (110, 190, 110)
        arcade.draw_circle_filled(x + 6 * f, y - 14, 7, flipper)
        arcade.draw_circle_filled(x - 6 * f, y - 14, 7, flipper)
        arcade.draw_circle_filled(x + 6 * f, y + 14, 7, flipper)
        arcade.draw_circle_filled(x - 8 * f, y + 14, 7, flipper)
        arcade.draw_ellipse_filled(x, y, 42, 30, (70, 160, 90))
        arcade.draw_circle_filled(x, y, 6, (120, 200, 120))
        arcade.draw_circle_filled(x - 9, y + 2, 3, (120, 200, 120))
        arcade.draw_circle_filled(x + 9, y - 2, 3, (120, 200, 120))
        arcade.draw_circle_filled(x + 24 * f, y, 8, flipper)
        arcade.draw_circle_filled(x + 27 * f, y + 2, 1.5, (20, 20, 20))

    def draw_dolphin(self):
        d = self.dolphin
        s = 1 if d.vx > 0 else -1
        x = d.x
        y = d.y
        body = (110, 150, 195)
        arcade.draw_ellipse_filled(x, y, 90, 28, body)
        arcade.draw_ellipse_filled(x + 6 * s, y - 5, 60, 14, (200, 220, 240))
        arcade.draw_ellipse_filled(x + 42 * s, y - 2, 26, 10, body)
        arcade.draw_triangle_filled(x - 6 * s, y + 12, x + 12 * s, y + 12, x - 14 * s, y + 34, body)
        arcade.draw_triangle_filled(x - 40 * s, y, x - 62 * s, y + 18, x - 62 * s, y - 18, body)
        arcade.draw_circle_filled(x + 26 * s, y + 4, 2.5, (20, 20, 30))

    def draw_whale(self):
        w = self.whale
        x = w.x
        y = w.y
        body = (70, 100, 150)
        arcade.draw_ellipse_filled(x, y, 230, 95, body)
        arcade.draw_ellipse_filled(x + 10, y - 16, 190, 50, (190, 210, 230))
        arcade.draw_triangle_filled(x - 105, y, x - 160, y + 50, x - 150, y - 10, body)
        arcade.draw_triangle_filled(x - 105, y, x - 160, y - 45, x - 150, y + 5, body)
        arcade.draw_circle_filled(x + 78, y + 10, 4, (15, 15, 25))
        if w.ring > 0:
            radius = (1 - w.ring / 1.2) * screenwidth
            arcade.draw_circle_outline(x, y, radius, (255, 255, 255, 170), 4)
    def draw_enemy(self, e):
        x = e.x
        y = e.y
        r = e.radius
        if e.kind == "net":
            green = (90, 190, 110)
            arcade.draw_circle_outline(x, y, r, green, 3)
            for k in (-0.5, 0.0, 0.5):
                half = r * math.sqrt(1 - k * k)
                arcade.draw_line(x - half, y + k * r, x + half, y + k * r, green, 2)
                arcade.draw_line(x + k * r, y - half, x + k * r, y + half, green, 2)
        else:
            dark = (30, 25, 45)
            arcade.draw_circle_filled(x, y, r, dark)
            arcade.draw_circle_filled(x - 16, y - 10, 12, dark)
            arcade.draw_circle_filled(x + 17, y - 8, 10, dark)
            arcade.draw_circle_filled(x - 8, y + 5, 7, (255, 255, 255))
            arcade.draw_circle_filled(x + 8, y + 5, 7, (255, 255, 255))
            arcade.draw_circle_filled(x - 8, y + 5, 3, (220, 40, 40))
            arcade.draw_circle_filled(x + 8, y + 5, 3, (220, 40, 40))
    def draw_trash(self, t):
        x = t.x
        y = t.y
        if t.kind == "bottle":
            arcade.draw_ellipse_filled(x, y - 2, 13, 22, (140, 220, 200, 230))
            rect(x - 3, y + 6, 6, 9, (140, 220, 200, 230))
            arcade.draw_circle_filled(x, y + 17, 3.5, (220, 60, 60))
        elif t.kind == "chips":
            rect(x - 10, y - 13, 20, 26, (250, 215, 60))
            rect(x - 10, y + 12, 20, 4, (225, 185, 40))
            rect(x - 10, y - 16, 20, 4, (225, 185, 40))
            arcade.draw_ellipse_filled(x, y, 15, 13, (210, 50, 40))
            arcade.draw_triangle_filled(x - 3, y - 3, x + 3, y - 3, x, y + 5, (255, 170, 30))
        else:
            rect(x - 8, y - 11, 16, 22, (180, 70, 70))
            rect(x - 8, y - 2, 16, 5, (230, 230, 230))
            arcade.draw_line(x - 8, y + 11, x + 8, y + 11, (210, 210, 210), 2)
    def reset(self):
        self.settings = modes[self.mode]
        self.player_x = screenwidth/2
        self.player_y = screenheight/2
        self.trash_list = []
        self.trash_timer = 0
        self.score = 0
        self.enemy_list = []
        self.enemy_timer = 0
        self.lives = self.settings["lives"]
        self.turtle = None
        self.dolphin = None
        self.whale = None
        self.state = "playing"
        self.seen = set()
        self.message = ""
        self.message_timer = 0
        self.facing = 1
    def announce(self, name, text):
        if name not in self.seen:
            self.seen.add(name)
            self.message = text
            self.message_timer = bannertime
    def toggle_pause(self):
        if self.state == "playing":
            self.state = "paused"
        elif self.state == "paused":
            self.state = "playing"
    def draw_menu(self):
        self.title_text.draw()
        self.subtitle_text.draw()
        for i in range(len(menuitems)): 
            bottom = menutop - i * 80
            left = screenwidth / 2 - menubuttonwidth / 2
            arcade.draw_polygon_filled([(left, bottom), (left + menubuttonwidth, bottom), (left + menubuttonwidth, bottom + menubuttonheight), (left, bottom + menubuttonheight)], (40, 120, 90))
            self.menu_texts[i].draw()
    def draw_player(self):
        x = self.player_x
        y = self.player_y
        f = self.facing
        arcade.draw_circle_filled(x, y, playerradius, (190, 200, 210))
        arcade.draw_circle_outline(x, y, playerradius, (90, 100, 110), 3)
        arcade.draw_ellipse_filled(x + 4 * f, y + 3, 24, 15, (30, 40, 60))
        arcade.draw_circle_filled(x + 9 * f, y + 4, 3, (120, 255, 200))
        arcade.draw_line(x, y + playerradius, x, y + playerradius + 10, (90, 100, 110), 3)
        arcade.draw_circle_filled(x, y + playerradius + 12, 4, (255, 80, 80))
        arcade.draw_circle_filled(x - 20 * f, y - 2, 5, (90, 100, 110))
    def on_draw(self):
        self.clear()
        self.draw_background()
        if self.state == "menu":
            self.draw_menu()
            return
        for t in self.trash_list:
            self.draw_trash(t)
        for e in self.enemy_list:
            self.draw_enemy(e)
        if self.turtle is not None:
            self.draw_turtle()
        if self.dolphin is not None and self.dolphin.active:
            self.draw_dolphin()
        if self.whale is not None:
            self.draw_whale()
        self.draw_player()
        self.score_text.text = f"Trash: {self.score} / {self.settings['winscore']}"
        self.score_text.draw()
        if self.state == "playing" or self.state == "paused":
            arcade.draw_polygon_filled([(ingamex, ingamey), (ingamex + ingamewidth, ingamey), (ingamex + ingamewidth, ingamey + ingameheight), (ingamex, ingamey + ingameheight)], (0, 0, 0, 120))
            self.menu_button_text.draw()
            arcade.draw_polygon_filled([(pausex, ingamey), (pausex + ingamewidth, ingamey), (pausex + ingamewidth, ingamey + ingameheight), (pausex, ingamey + ingameheight)], (0, 0, 0, 120))
            self.pause_button_text.text = "Resume" if self.state == "paused" else "Pause"
            self.pause_button_text.draw()
        if self.state == "paused":
            self.paused_text.draw()
        self.lives_text.text = f"Lives: {self.lives}"
        self.lives_text.draw()
        arcade.draw_polygon_filled([(barx, bary), (barx + barwidth, bary), (barx + barwidth, bary + barheight), (barx, bary + barheight)], (0, 0, 0, 90))
        fraction = min(1.0, self.score / self.settings["winscore"])
        fill = barwidth * fraction
        if fill > 0:
            arcade.draw_polygon_filled([(barx, bary), (barx + fill, bary), (barx + fill, bary + barheight), (barx, bary + barheight)], (120, 255, 180))
        for needed in (enemystartscore, turtlestartscore, dolphinstartscore, whalestartscore, netstartscore):
            tick_x = barx + barwidth * needed / self.settings["winscore"]
            arcade.draw_line(tick_x, bary - 3, tick_x, bary + barheight + 3, (255, 255, 255), 2)
        if self.message_timer > 0:
            self.message_text.text = self.message
            self.message_text.draw()
        if self.state == "won":
            self.end_text.text = "The Ocean Is Clean!"
            self.end_text.draw()
        elif self.state == "lost":
            self.end_text.text = "You Have Failed To Clean The Ocean"
            self.end_text.draw()
        if self.state == "won" or self.state == "lost":
            arcade.draw_polygon_filled([(buttonx, buttony), (buttonx + buttonwidth, buttony), (buttonx + buttonwidth, buttony + buttonheight), (buttonx, buttony + buttonheight)], (40, 120, 90))
            self.button_text.draw()
            self.credits1.draw()
            self.credits2.draw()
    def on_key_press(self, key, modifiers):
        self.keys.add(key)
        if key == arcade.key.P:
            self.toggle_pause()
    def on_key_release(self, key, modifiers):
        self.keys.discard(key)
    def on_mouse_press(self, x, y, button, modifiers):
        if self.state == "menu":
            left = screenwidth / 2 - menubuttonwidth / 2
            for i, (name, label) in enumerate(menuitems):
                bottom = menutop - i * 80
                if left <= x <= left + menubuttonwidth and bottom <= y <= bottom + menubuttonheight:
                    self.mode = name
                    self.reset()
        elif self.state == "won" or self.state == "lost":
            if buttonx <= x <= buttonx + buttonwidth and buttony <= y <= buttony + buttonheight:
                self.reset()
                self.state = "menu"
        else:
            if ingamex <= x <= ingamex + ingamewidth and ingamey <= y <= ingamey + ingameheight:
                self.reset()
                self.state = "menu"
            if pausex <= x <= pausex + ingamewidth and ingamey <= y <= ingamey + ingameheight:
                self.toggle_pause()
    def on_update(self, delta_time):
        self.anim += delta_time
        for b in self.bubbles:
            b[1] += b[3] * delta_time 
            if b[1] > screenheight + 10:
                b[0] = random.uniform(0, screenwidth)
                b[1] = -10
        if self.state != "playing":
            return
        if self.message_timer > 0:
            self.message_timer -= delta_time
        move_x = 0
        move_y = 0
        if arcade.key.LEFT in self.keys:
            move_x -= 1
        if arcade.key.RIGHT in self.keys:
            move_x += 1
        if arcade.key.UP in self.keys:
            move_y += 1
        if arcade.key.DOWN in self.keys:
            move_y -= 1
        if move_x > 0:
            self.facing = 1
        elif move_x < 0:
            self.facing = -1
        self.player_x += move_x * self.settings["playerspeed"] * delta_time
        self.player_y += move_y * self.settings["playerspeed"] * delta_time
        self.player_x = max(playerradius, min(screenwidth - playerradius, self.player_x))
        self.player_y = max(48 + playerradius, min(screenheight - playerradius, self.player_y))
        self.trash_timer -= delta_time
        if self.trash_timer <= 0:
            self.trash_timer = trashspawntime
            if len(self.trash_list) < maxtrash:
                y = random.uniform(70, screenheight - 70)
                speed = random.uniform(15, 45)
                if random.random() < 0.5:
                    x = -20
                else:
                    x = screenwidth + 20
                    speed = -speed
                self.trash_list.append(Trash(x, y, speed))
        for t in self.trash_list[:]:
            t.x += t.speed * delta_time
            if t.x < -40 or t.x > screenwidth + 40:
                self.trash_list.remove(t)
        for t in self.trash_list[:]:
            distance = math.hypot(self.player_x - t.x, self.player_y - t.y)
            if distance < playerradius + trashradius:
                self.trash_list.remove(t)
                self.score += 1
        if self.score >= enemystartscore:
            self.enemy_timer -= delta_time
            if self.enemy_timer <= 0:
                self.enemy_timer = self.settings["enemyspawntime"]
                if len(self.enemy_list) < self.settings["maxenemies"]:
                    y = random.uniform(70, screenheight - 70)
                    if random.random() < 0.5:
                        x = -40
                    else:
                        x = screenwidth + 40
                    if self.score >= netstartscore and random.random() < netchance:
                        self.enemy_list.append(Enemy(x, y, "net", self.settings["netspeed"], netradius))
                    else:
                        self.enemy_list.append(Enemy(x, y, "oil", self.settings["enemyspeed"], enemyradius))
        for e in self.enemy_list[:]:
            dx = self.player_x - e.x
            dy = self.player_y - e.y
            dist = math.hypot(dx, dy)
            if dist > 0:
                e.x += dx / dist * e.speed * delta_time
                e.y += dy / dist * e.speed * delta_time
            if dist < playerradius + e.radius:
                self.enemy_list.remove(e)
                self.lives -= 1
        if self.turtle is None and self.score >= turtlestartscore:
            self.turtle = Turtle(self.player_x - 60, self.player_y + 40)
        if self.turtle is not None:
            target_x = self.player_x - 55
            target_y = self.player_y + 35
            follow = min(1.0, 3.0 * delta_time)
            self.turtle.x += (target_x - self.turtle.x) * follow
            self.turtle.y += (target_y - self.turtle.y) * follow
            for t in self.trash_list[:]:
                if math.hypot(self.turtle.x - t.x, self.turtle.y - t.y) < turtlegrabradius:
                    self.trash_list.remove(t)
                    self.score += 1
        if self.dolphin is None and self.score >= dolphinstartscore:
            self.dolphin = Dolphin()
        if self.dolphin is not None:
            d = self.dolphin
            if not d.active:
                d.cooldown -= delta_time
                if d.cooldown <= 0 and len(self.enemy_list) > 0:
                    target = random.choice(self.enemy_list)
                    d.y = target.y
                    if random.random() < 0.5:
                        d.x = -80
                        d.vx = dolphinspeed
                    else:
                        d.x = screenwidth + 80
                        d.vx = - dolphinspeed
                    d.active = True
            else:
                d.x += d.vx * delta_time
                for e in self.enemy_list[:]:
                    if math.hypot(d.x - e.x, d.y - e.y) < dolphinradius + e.radius:
                        self.enemy_list.remove(e)
                if d.x < -120 or d.x > screenwidth + 120:
                    d.active = False
                    d.cooldown = dolphincooldown
        if self.whale is None and self.score >= whalestartscore:
            self.whale = Whale()
        if self.whale is not None:
            w = self.whale
            w.x += 35 * delta_time
            if w.x > screenwidth + 250:
                w.x = -250
            w.ring = max(0.0, w.ring - delta_time)
            w.song_timer -= delta_time
            if w.song_timer <= 0:
                w.song_timer = whalesongtime
                w.ring = 1.2
                self.enemy_list.clear()
        if self.score >= enemystartscore:
            self.announce("oil", "Oh no! Oil blobs are chasing you!")
        if self.score >= turtlestartscore:
            self.announce("turtle", "A sea turtle joins you! It grabs trash near it.")
        if self.score >= dolphinstartscore:
            self.announce("dolphin", "A dolphin will dash through and sweep away danger!")
        if self.score >= netstartscore:
            self.announce("nets", "Ghost nets are drifting in. They are faster!")
        if self.score >= whalestartscore:
            self.announce("whale", "A whale arrives. Its song scatters every enemy!")
        if self.lives <= 0:
            self.state = "lost"
        elif self.score >= self.settings["winscore"]:
            self.state = "won"
            self.trash_list.clear()
            self.enemy_list.clear()

        
        

        
            
game = game()
arcade.run()
