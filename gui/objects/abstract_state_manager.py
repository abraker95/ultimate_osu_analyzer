class AbstractStateManager():

    def __init__(self):
        self.abstract_states = {}
        self.active_state = None


    def switch_to(self, state):
        if state in self.abstract_states:
            self.active_state = self.abstract_states[state]


    def __len__(self):
        return len(self.abstract_states)


    def get(self):
        return self.active_state


    def add(self, abstract_state, state):
        if not state in self.abstract_states:
            self.abstract_states[state] = abstract_state
        else:
            raise Exception('Abstract state with state ' + str(state) + ' already exists')

    
    def rmv(self, state):
        if state not in self.abstract_states: return

        if self.active_state == self.abstract_states[state]:
            if len(self.abstract_states.values() > 1):
                self.active_state = self.abstract_states.values()[0]
            else:
                self.active_state = None

        del self.abstract_states[state]


    def save_states(self):
        for abstract_state in self.abstract_states.values():
            abstract_state.save_state()

        # TODO: record what is active state
        

    def load_states(self):
        # TODO
        pass