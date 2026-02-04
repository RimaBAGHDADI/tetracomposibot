from robot_braitenberg_hateWall import BraitenbergHateWall
from robot_braitenberg_loveBot import BraitenbergLoveBot
from robot import * 

class Robot_player(Robot):
    team_name = "Subsomption"
    robot_id = -1

    def __init__(self,x_0, y_0, theta_0, name="n/a" ,team="n/a"):
        super().__init__(x_0, y_0, theta_0, name=name, team=team)
        self.hate_wall = BraitenbergHateWall()
        self.love_bot = BraitenbergLoveBot()

    def step(self, sensors, sensor_view=None, sensor_robot=None, sensor_team=None):
        if min(sensors) < 0.5 : # mur proche
            translation, rotation = self.hate_wall.step(sensors,sensor_view)
        elif min(sensors) < 1.0 : # robot proche
            translation, rotation = self.love_bot.step(sensors,sensor_view)
        else:
            translation, rotation = 1.0, 0.0 # tout droit
        return translation,rotation, False