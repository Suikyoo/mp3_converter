import pygame, core_functs

class KeyConstant(int):
    def __init__(self, value):
        super().__int__()
        #0 - 2 represents hold, keydown, and keyup respectively
        self.mode = 0


class KeyControl:
    def __init__(self):
        self.key_modes = ["hold", "keydown", "keyup"]
        self.key_data = {k : {} for k in self.key_modes}
        self.key_data["hold"] = pygame.key.get_pressed()
        self.main_key = "hold"
        self.special_keys = ["keydown", "keyup"]

    def track_key(self, *key_constants):
        for i in key_constants:
            for k in self.special_keys:
                if i not in self.key_data[k]:
                    self.key_data[k][i] = False

    def key_down_handler(self, data_buffer):
        condition = [True, False]
        self.match_key([data_buffer, self.key_data[self.main_key], self.key_data["keydown"]], condition)
        
    def key_up_handler(self, data_buffer):
        condition = [False, True]
        self.match_key([data_buffer, self.key_data[self.main_key], self.key_data["keyup"]], condition)
    
    def match_key(self, data, condition):
        for k in data[2]:
            check_pass = 0
            for i in range(2):
                if data[i][k] != condition[i]:
                    break
                check_pass += 1

            if check_pass == 2:
                data[2][k] = True

            else: 
                data[2][k] = False

    def check_data(self, data, *key_constants):
        self.track_key(*key_constants)
        for k in key_constants:
            try:
                if not data[k]:
                    return False

            except: return False

        return True

    def key(self, *key_constants):
        self.track_key(*key_constants)
        for k in key_constants:
            data = self.key_data[self.key_modes[k.mode]]
            try:
                if not data[k]:
                    return False

            except: return False

        return True

    def hold(self, *key_constants):
        return self.check_data(self.key_data[self.main_key], *key_constants)

    def keydown(self, *key_constants):
        return self.check_data(self.key_data["keydown"], *key_constants)

    def keyup(self, *key_constants):
        return self.check_data(self.key_data["keyup"], *key_constants)

    #returns all recorded keydown constants that are true
    def get_keydowns(self):
        keydowns = []
        for k in self.key_data["keydown"]:
            if self.key_data["keydown"][k]:
                keydowns += [k]

        return keydowns

    #returns all recorded keyup constants that are true
    def get_keyups(self):
        keyups = []
        for k in self.key_data["keyup"]:
            if self.key_data["keyup"][k]:
                keyups += [k]

        return keyups

    def key_handler(self):
        data_buffer = pygame.key.get_pressed()
        self.key_down_handler(data_buffer)
        self.key_up_handler(data_buffer)
        self.key_data[self.main_key] = data_buffer

    def update(self):
        self.key_handler()

#charity methods
def to_key(*strings):
    return [KeyConstant(pygame.key.key_code(i)) for i in strings]

def to_str(*key_constants):
    return [pygame.key.name(i) for i in key_constants]

def change_mode(mode, *key_constants):
    for i in key_constants:
        i.mode = mode
    return list(key_constants)
