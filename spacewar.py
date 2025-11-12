import os
import random
import time
#import turtle module
import turtle
turtle.fd(0)
turtle.speed(0)
turtle.bgcolor("black")
#Change the Window Title
turtle.title("SpaceWar")
turtle.ht()
turtle.setundobuffer(1) #saves memory
turtle.tracer(2) #Speeds up drawing

class Sprite(turtle.Turtle):
  def __init__(self, spriteshape, color, startx, starty):
    turtle.Turtle.__init__(self, shape = spriteshape)
    self.speed(0) #animation speed
    self.penup()
    self.color(color)
    self.fd(0)
    self.goto(startx, starty)
    self.speed = 1

  def move(self):
    self.fd(self.speed)

    #Boundary detection
    if self.xcor() > 290:
      self.setx(290)
      self.rt(60)
    if self.xcor() < -290:
      self.setx(-290)
      self.rt(60)
    if self.ycor() > 290:
      self.sety(290)
      self.rt(60)
    if self.ycor() < -290:
      self.sety(-290)
      self.rt(60)

  def is_collision(self, other):
    if (self.xcor()>=(other.xcor()-20)) and (self.xcor()<=(other.xcor()+20)) and (self.ycor()>=(other.ycor()-20)) and (self.ycor()<=(other.ycor()+20)):
      return True
    else:
      return False

class Player(Sprite):
  def __init__(self, spriteshape, color, startx, starty):
    Sprite.__init__(self, spriteshape, color, startx, starty)
    self.shapesize(stretch_wid=0.6,stretch_len=1.1,outline=None)
    self.speed=4
    self.lives=3

  def turn_left(self):
    self.lt(45)

  def turn_right(self):
   self.rt(45)

  def accelerate(self):
    self.speed +=1

  def decelerate(self):
    self.speed -=1

class Enemy(Sprite):
  def __init__(self, spriteshape, color, startx, starty):
    Sprite.__init__(self, spriteshape, color, startx, starty)
    self.speed = 3
    self.setheading(random.randint(0,360))

class Particle(Sprite):
  def __init__(self, spriteshape, color, startx, starty):
    Sprite.__init__(self, spriteshape, color, startx, starty)
    self.shapesize(stretch_wid=0.1,stretch_len=0.1, outline=None)
    self.goto(-1000,1000)

  def explode(self,startx,starty):
    self.goto(startx,starty)
    self.setheading(random.randint(0,360))

  def move(self):
    self.fd(10)

class Missile(Sprite):
  def __init__(self, spriteshape, color, startx, starty):
    Sprite.__init__(self, spriteshape, color, startx, starty)
    self.shapesize(stretch_wid=0.2,stretch_len=0.4, outline=None)
    self.speed=20
    self.status="ready"
    self.goto(-1000,1000)

  def fire(self):
    if self.status == "ready":
      self.goto(player.xcor(),player.ycor())
      self.setheading(player.heading())
      self.status = "firing"
  
  def move(self):
    if self.status == "ready":
      self.goto(-1000,1000)

    if self.status == "firing":
      self.fd(self.speed) 

    #Border Checking
    if self.xcor() > 290 or self.xcor() <-290 or self.ycor() > 290 or self.ycor() < -290:
      self.goto(-1000,1000)
      self.status ="ready"

class Ally(Sprite):
   def __init__(self, spriteshape, color, startx, starty):
    Sprite.__init__(self, spriteshape, color, startx, starty)
    self.speed = 4
    self.setheading(random.randint(0,360))
    
   def move(self):
    self.fd(self.speed)

    #Boundary detection
    if self.xcor() > 290:
      self.setx(290)
      self.lt(60)
    if self.xcor() < -290:
      self.setx(-290)
      self.lt(60)
    if self.ycor() > 290:
      self.sety(290)
      self.lt(60)
    if self.ycor() < -290:
      self.sety(-290)
      self.lt(60)

class Game():
    def __init__(self):
        self.level = 1
        self.score = 0
        self.lives = 3
        self.pen = turtle.Turtle()
        self.pen_d = turtle.Turtle()
        

    def draw_border(self):
    #Draw border
        self.pen_d.speed(0)
        self.pen_d.color("white")
        self.pen_d.pensize(3) 
        self.pen_d.penup()
        self.pen_d.goto(-300,300)
        self.pen_d.pendown()
        for side in range(4):
          self.pen_d.fd(600)
          self.pen_d.rt(90)
        self.pen_d.penup()
        self.pen_d.ht()
        self.pen_d.pendown()
        self.pen_d.penup()

    def border(self):
        self.pen.speed(0)
        self.pen.color("white")
        self.pen.pensize(3) 
        self.pen.penup()
        self.pen.goto(-300,300)
        self.pen.pendown()
        for side in range(4):
          self.pen.fd(600)
          self.pen.rt(90)
        self.pen.penup()
        self.pen.ht()
        self.pen.pendown()
        self.pen.penup()

    def show_status(self):
        self.pen_d.clear()
        msg = f"Score: {self.score}"
        self.pen_d.penup()
        self.pen_d.goto(-300, 300)
        self.pen_d.write(msg , font=("Arial",16,"normal"))
        
    def show_lives(self):
        self.pen_d.penup()
        self.pen_d.goto(-100, 300)
        if self.lives:
          self.pen_d.write(f"Lives: {self.lives}", font=("Arial",16,"normal"))
        else:
          self.endGame() #recursivitate indirecta

    def endGame(self):
        self.pen.color("White")
        self.pen.ht()
        self.pen.penup()
        self.pen.goto(-90,-10)
        self.pen.write("End Game",font=("Arial",30,"normal"))

#Create Game Objects
game=Game()

#Draw The Game Border
game.draw_border()

#Show the game status
game.show_status()

#Show the live status
game.show_lives()

game.border()

#Create my sprites(obj)
player = Player("triangle" ,"white", 0,0)
missile = Missile("triangle", "yellow", 0,0)

#Multiple enemies
enemies = []
for i in range(4):
  enemies.append(Enemy("circle", "red", -100, 0))

#Multiple allies
allies = []
for i in range(3):
  allies.append(Ally("square" , "blue",-100,0))

particles=[]
for i in range(10):
  particles.append(Particle("circle","orange",0,0))

#Creating keybinds
turtle.onkey(player.turn_left, "Left")
turtle.onkey(player.turn_right, "Right")
turtle.onkey(player.accelerate, "Up")
turtle.onkey(player.decelerate, "Down")
turtle.onkey(missile.fire , "space")
turtle.listen()

#Main game loop
while True:
  turtle.update()
  time.sleep(0.01)
  player.move()
  missile.move()
    
  for enemy in enemies:
    enemy.move()
    #Check for a collision with the player
    if player.is_collision(enemy):
      x=random.randint(-250,250)
      y=random.randint(-250,250)
      enemy.goto(x,y)
      game.score -= 100
      game.lives -= 1
      game.show_status()
      game.show_lives()
      #Explode particle
      for particle in particles:
        particle.explode(missile.xcor(),missile.ycor())
      
    #Check for a collision between the missile and the enemy
    if missile.is_collision(enemy):
      x=random.randint(-250,250)
      y=random.randint(-250,250)
      enemy.goto(x,y)
      missile.status ="ready"
      #Increase the score
      game.score += 100
      game.show_status()
      game.show_lives()
      #Explode particle
      for particle in particles:
        particle.explode(missile.xcor(),missile.ycor())
        
  for ally in allies:
    ally.move()
    if missile.is_collision(ally):
        x=random.randint(-250,250)
        y=random.randint(-250,250)
        ally.goto(x,y)
        missile.status ="ready"
        #Decrease the score
        game.score -= 50
        game.show_status()
        game.show_lives()
        #Explode particle
        for particle in particles:
          particle.explode(missile.xcor(),missile.ycor())
          
  for particle in particles:
    particle.move()
  