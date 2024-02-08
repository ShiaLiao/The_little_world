class Belief():
    def __init__(self):
        self._memory = []

    def classify(self, input):
        pass
    
    def remember(self, memory):
        self._memory.append(memory)

    def forget(self):
        self._memory = []
        
    def recall(self):
        return self._memory