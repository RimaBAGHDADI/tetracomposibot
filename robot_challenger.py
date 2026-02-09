# Projet "robotique" IA&Jeux 2025
#
# Binome:
#  Prénom Nom No_étudiant/e : Rima BAGHDADI 21304585
#  Prénom Nom No_étudiant/e : Nada BEN ALAYA
#
# check robot.py for sensor naming convention
# all sensor and motor value are normalized (from 0.0 to 1.0 for sensors, -1.0 to +1.0 for motors)

from robot import *
import random
from robot_braitenberg_avoider import avoider
from robot_braitenberg_loveWall import loveWall
from robot_braitenberg_hateWall import hateWall
from robot_braitenberg_loveBot import loveBot
from robot_braitenberg_hateBot import hateBot

nb_robots = 0

class Robot_player(Robot):

    team_name = "Challenger"  # vous pouvez modifier le nom de votre équipe
    robot_id = -1             # ne pas modifier. Permet de connaitre le numéro de votre robot.
    memory = 0                # vous n'avez le droit qu'a une case mémoire qui doit être obligatoirement un entier

    def __init__(self, x_0, y_0, theta_0, name="n/a", team="n/a"):
        global nb_robots
        self.robot_id = nb_robots
        nb_robots+=1
        super().__init__(x_0, y_0, theta_0, name="Robot "+str(self.robot_id), team=self.team_name)

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        MAX_SPEED = 1.0 
        # specialisation du robot pour qui'ils font pas les 4 la meme chose
        if self.robot_id == 0: #suit les murs et explore
            ATTACK_TIME = 10
            explore_speed = 1.0
        elif self.robot_id == 1:#attaque les robot des autres team
            ATTACK_TIME = 40
            explore_speed = 0.8
        elif self.robot_id == 2: #evite les collision
            ATTACK_TIME = 5
            explore_speed = 0.6
        else:
            ATTACK_TIME = 25
            explore_speed = 0.9

        # gestion de memoire
        enemy_detected = any(sensor_robot[i] and sensor_team != self.team_name for i in range(len(sensors)))
        if enemy_detected:
            self.memory = ATTACK_TIME
        elif self.memory > 0:
            self.memory -= 1
        team_robot_detected = any(sensor_robot[i] and sensor_team == self.team_name for i in range(len(sensors)))
        collision = any(sensors[i] < 0.25 for i in range(len(sensors)))

        #Genetic algorith poids pour robor 1 

        if self.robot_id == 1:
            W_left = 0.6
            W_fleft = 1.4
            W_fright = 1.3
            W_right = 0.5
        else :
            W_left = W_fleft = W_fright = W_right = 1.0

        #Architecture subsomption
        #priorite : danger>allies>ennemis>murs>exploration

        
        if collision:               
            return avoider(sensors, sensor_view, sensor_robot, sensor_team)
        if team_robot_detected:    
            return hateBot(sensors, sensor_view, sensor_robot, sensor_team)
        if self.memory > 0:# utlisation de GA
            rotation = 0.0

            # gauche
            if sensor_view[sensor_left] == 2:
                rotation -= W_left * (1 - sensors[sensor_left])

            if sensor_view[sensor_front_left] == 2:
                rotation -= W_fleft * (1 - sensors[sensor_front_left])

            # droite
            if sensor_view[sensor_front_right] == 2:
                rotation += W_fright * (1 - sensors[sensor_front_right])

            if sensor_view[sensor_right] == 2:
                rotation += W_right * (1 - sensors[sensor_right])

            translation = 1.0
            return translation,rotation,False
        
        if sensors[sensor_front] < 0.5: 
            return hateWall(sensors, sensor_view, sensor_robot, sensor_team)
        
        
        translation,rotation = loveWall
        translation *= explore_speed
        return translation,rotation,False

       

