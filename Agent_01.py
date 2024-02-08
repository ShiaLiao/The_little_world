# Agent, simpler version, abstract trade function and produce function

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
        
    def produce(self, product_type):
            """
            通用生产函数。
            :param product_type: 要生产的商品类型，如 'food', 'clothes', 或 'tools'
            """
            stamina_cost = 10 if product_type in ['food', 'clothes'] else 15
            productivity_key = f'{product_type}_production'

            if self.stamina > stamina_cost:
                # 生产效率取决于相应能力和工具（对于食物和衣物）
                productivity = self.abilities.get(productivity_key, 0)
                if product_type in ['food', 'clothes']:
                    productivity += self.tools

                # 根据商品类型增加相应的数量
                if product_type in ['food', 'clothes']:
                    setattr(self, product_type, getattr(self, product_type) + productivity * 5)
                elif product_type == 'tools':
                    self.tools += productivity

                self.stamina -= stamina_cost
            else:
                print(f"T_T, too tired to produce {product_type}.")
           
    def move(self,new_pos):
        # movement consumes stamina, and the consumption depends on the distance
        distance = calc_distance(self.pos, new_pos)
        if self.stamina > distance:
            self.pos = new_pos
            self.stamina -= distance
        else:
            print("not enough stamina to move")
    
    def trade(self, other, trade_from, trade_to):
        """
        通用交易函数。
        :param other: 交易对象
        :param trade_from: 此主体提供的商品类型
        :param trade_to: 此主体想要交换的商品类型
        """
        if getattr(self, trade_from) > 0:
            trade_ratio = self.abilities.get('trade', 1)
            # 减少交易发起方的商品
            setattr(self, trade_from, getattr(self, trade_from) - 1)
            # 增加交易发起方想要交换的商品
            setattr(self, trade_to, getattr(self, trade_to) + trade_ratio)
            # 增加交易对象的商品
            setattr(other, trade_from, getattr(other, trade_from) + 1)
            # 减少交易对象想要交换的商品
            setattr(other, trade_to, getattr(other, trade_to) - trade_ratio)
        else:
            print(f"Not enough {trade_from} to trade")  
                   
    def trade_with_other_agent(self, other):
        # 决定交易的商品类型
        if self.food > other.food:
            self.trade(other, 'food', 'clothes')
            self.trade(other, 'food', 'tools')
        elif self.clothes > other.clothes:
            self.trade(other, 'clothes', 'food')
            self.trade(other, 'clothes', 'tools')
        elif self.tools > other.tools:
            self.trade(other, 'tools', 'clothes')
            self.trade(other, 'tools', 'food')           
     
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
    
    def decide_action(self, agents):
        # 检查周围是否有其他主体进行交易
        for other_agent in agents:
            if self != other_agent and calc_distance(self.pos, other_agent.pos) < 10:
                # 如果找到一个足够近的主体，尝试进行交易
                self.trade_with_other_agent(other_agent )
                break
        
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
                self.produce('food')
            elif best_action == 'clothes_production':
                self.produce('clothes')
            else:
                self.produce('tools')
        
        self.move((self.pos[0]+random.randint(-1,1), self.pos[1]+random.randint(-1,1)))
            
        



                       
           
            
    def update(self, agents):
        # every time step, the fullness, warmth and time will change
        self.fullness -= 1
        self.warmth -= 1
        self.time += 1
        # 死亡判定
        if self.fullness <= 0 or self.warmth <= 0:
            self.is_alive = False
            return  # 如果主体死亡，则不执行后续的行为        
        # decide what to do
        self.decide_action(agents)


