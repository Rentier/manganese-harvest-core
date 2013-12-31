from harvest.agents import *
from harvest.environments import *

class Harvester():
    
    def __init__(self, field, agent, time, animator=None):
        self.field = field
        self.agent = agent
        self.time = time
        self.animator = animator
        
    def play(self):
        for t in reversed(xrange(0, self.time + 1)):
            self.update(t)
            if self.animator: self.animator.on_update(self.field, self.time - t)
            
    def update(self,t ):
        # Thank you Mr Asimov        
        for i, robot in enumerate(self.field.robots):
            # Calc has the side effect of moving the robot,
            # updating it in place
            self.agent.calc(robot, self.field, t)
            
if __name__ == '__main__':
	pass       
