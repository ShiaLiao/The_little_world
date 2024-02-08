import math
import random

def calc_distance(pos1, pos2):
    # pos1, pos2: (x, y)，euclidean distance
    return math.sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)

class Agent:
    def __init__(self, id, pos, age, abilities):
        #basic info
        self.id = id
        self.fullness = 100 # measurement of hunger 
        self.warmth = 100 # measurement of coldness
        self.stamina = 100 # measurement of tiredness
        self.age = age 
        self.is_alive = True
                
        #outside info
        self.pos = pos # (x, y)
        self.food = 0
        self.clothes = 0
        self.tools = 0
        self.time = 0 

        # dashboard of abilities
        self.abilities = abilities
        
    def produce_food(self):
        if self.stamina > 10:
            # the production depends on the ability and tools
            food_productivity = self.abilities['food_production'] + self.tools
            self.tools = max(0, self.tools-0.1)            
            self.food += food_productivity*5
            self.stamina -= 10
        else:
            print("T_T, too tired to produce food.")
            
    def produce_clothes(self):
        if self.stamina > 10:
            # the production depends on the ability and tools
            clothes_productivity = self.abilities['clothes_production'] + self.tools
            self.tools = max(0, self.tools-0.1)
            self.clothes += clothes_productivity*5
            self.stamina -= 10
        else:
            print("T_T, too tired to produce clothes.")
            
    def produce_tools(self):
        if self.stamina > 30:
            # the production only depends on the ability
            tools_productivity = self.abilities['tools_production']
            self.tools += tools_productivity
            self.stamina -= 30
        else:
            print("T_T, too tired to produce tools.")
            
    
    # trade food, clothes, tools with others, the trade ratio depends on the ability        
    def trade_food_with_clothes(self, other):
        if self.food > 0:
            trade_ratio = self.abilities['trade']
            self.food -= 1
            self.clothes += trade_ratio
            other.food += 1
            other.clothes -= trade_ratio
        else:
            print("not enough food to trade")
            
    def trade_food_with_tools(self, other):
        if self.food > 0:
            trade_ratio = self.abilities['trade']
            self.food -= 1
            self.tools += trade_ratio
            other.food += 1
            other.tools -= trade_ratio
        else:
            print("not enough food to trade")
    
    def trade_clothes_with_tools(self, other):
        if self.clothes > 0:
            trade_ratio = self.abilities['trade']
            self.clothes -= 1
            self.tools += trade_ratio
            other.clothes += 1
            other.tools -= trade_ratio
        else:
            print("not enough clothes to trade")
            
    def trade_clothes_with_food(self, other):
        if self.clothes > 0:
            trade_ratio = self.abilities['trade']
            self.clothes -= 1
            self.food += trade_ratio
            other.clothes += 1
            other.food -= trade_ratio
        else:
            print("not enough clothes to trade")
            
    def trade_tools_with_food(self, other):
        if self.tools > 0:
            trade_ratio = self.abilities['trade']
            self.tools -= 1
            self.food += trade_ratio
            other.tools += 1
            other.food -= trade_ratio
        else:
            print("not enough tools to trade")
            
    def trade_tools_with_clothes(self, other):
        if self.tools > 0:
            trade_ratio = self.abilities['trade']
            self.tools -= 1
            self.clothes += trade_ratio
            other.tools += 1
            other.clothes -= trade_ratio
        else:
            print("not enough tools to trade")
            
    def eat(self):
        # eating food can increase fullness
        if self.food > 0:
            self.food -= 1
            self.fullness += 10
        else:
            print("not enough food to eat")
            
    def wear(self):
        # wearing clothes can increase warmth
        if self.clothes > 0:
            self.clothes -= 1
            self.warmth += 10
        else:
            print("not enough clothes to wear")
    
       
            
    def rest(self):
        # resting can increase stamina
        self.stamina = min(100, self.stamina+20)
        
    def give(self, other):
        # give food, clothes, tools to others
        if self.food > 0:
            self.food -= 1
            other.food += 1
        elif self.clothes > 0:
            self.clothes -= 1
            other.clothes += 1
        elif self.tools > 0:
            self.tools -= 1
            other.tools += 1
        else:
            print("nothing to give")
            
    def attack(self, other):
        # attack consumes stamina, and has a probability of taking away food, clothes, tools
        if self.stamina > 10:
            self.stamina -= 10
            other.stamina -= 10
            if random.random() < 0.5:
                if other.food > 0:
                    other.food -= 1
                    self.food += 1
                elif other.clothes > 0:
                    other.clothes -= 1
                    self.clothes += 1
                elif other.tools > 0:
                    other.tools -= 1
                    self.tools += 1
                else:
                    print("nothing to take")
        else:
            print("not enough stamina to attack")
            
    def move(self,new_pos):
        # movement consumes stamina, and the consumption depends on the distance
        distance = calc_distance(self.pos, new_pos)
        if self.stamina > distance:
            self.pos = new_pos
            self.stamina -= distance
        else:
            print("not enough stamina to move")
            
    def decide_action(self):
        # based on the current situation and abilities, decide what to do
        if self.fullness < 20 and self.food > 0:
            self.eat()
        if self.warmth < 20 and self.clothes > 0:
            self.wear()
        if self.stamina < 20:
            self.rest()
        else:
            # 根据能力值决定行动
            best_action = max(
                ['food_production', 'clothes_production', 'tools_production'],
                key=lambda x: self.abilities.get(x, 0)
            )

            if best_action == 'food_production':
                self.produce_food()
            elif best_action == 'clothes_production':
                self.produce_clothes()
            else:
                self.produce_tools()
        
        self.move((self.pos[0]+random.randint(-1,1), self.pos[1]+random.randint(-1,1)))
        
        # 检查周围是否有其他主体进行交易
        for other_agent in agents:
            if self != other_agent and self.calculate_distance(self.pos, other_agent.pos) < 10:
                # 如果找到一个足够近的主体，尝试进行交易
                self.trade_with_other_agent(other_agent)
                break

    def trade_with_other_agent(self, other):
        # 决定交易的商品类型
        if self.food > other.food:
            self.trade(other, 'food', 'clothes')
        elif self.clothes > other.clothes:
            self.trade(other, 'clothes', 'food')
                  
           
            
    def update(self):
        # every time step, the agent will consume food, clothes
        self.fullness -= 3
        self.warmth -= 1
        self.time += 1
        # 死亡判定
        if self.fullness <= 0 or self.warmth <= 0:
            self.is_alive = False
            return  # 如果主体死亡，则不执行后续的行为        
        # decide what to do
        self.decide_action()
            
            
            
    
    
        