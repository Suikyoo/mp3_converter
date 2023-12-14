import pygame, core_functs, controls, constants, requests, io
from PIL import Image

#instantiates a list and displays it in a slider scrolling manner

#offset = [x, y]
def get_tab_loc(tab, offset):
    return [tab.coords[i] + tab.size[i] * offset[i] for i in range(len(offset))]

def link_to_img(link):
    response = requests.get(link)
    img = pygame.image.load(io.BytesIO(response.content))
    
    return pygame.image.frombytes(pygame.image.tobytes(img, "RGB"), img.get_size(), "RGB")

class Interface:
    def __init__(self, coords, size):
        self.coords = coords
        self.size = size

    def set_control(self, scheme:list):
        self.control_scheme = controls.change_mode(1, *controls.to_key(*scheme))
        self.controls = [False] * len(self.control_scheme)

    def event_handler(self):
        for i in range(len(self.control_scheme)):
            self.controls[i] = constants.controls.keydown(self.control_scheme[i])

    def draw(self, surf):
        pass

    def control_handler(self):
        pass

    def update(self, surf):
        self.control_handler()
        self.draw(surf)

class Slider(Interface):
    def __init__(self, coords, size):
        super().__init__(coords, size)
        self.margin = 10
        self.data = []
        self.thumbnails = []
        #only scrolls on one axis. The second value is for interpolations
        self.scroll = [0, 0]
        self.set_item_size((self.size[0], 100))

        #top index means the top of the displayed items
        self.top_index = 0
        self.current_index = 0

        self.set_control("wsad")

    def control_handler(self):
        if self.controls[0]:
            self.current_index = max(self.current_index - 1, 0)

        elif self.controls[1]:
            self.current_index = min(self.current_index + 1, len(self.data) - 1)

    def set_margin(self, value):
        self.margin = value
        self.set_item_size((self.size[0], 50))

    def set_item_size(self, size:tuple):
        self.item_size = [min(size[i], self.size[i] - self.margin * 2) for i in range(2)]

    def update_data(self, data):
        self.data = data
        for i in data:
            i.thumbnail_img = core_functs.cut(link_to_img(i.thumbnail_url), 0, 0, *self.item_size)

    #returns surface for blitting in the slider
    #items, are just arbitrary objects thrown into into the data list. For this case, I'm probably gonna throw in [Youtube] objects
    #this is abominable from a c perspective
    def render_item(self, item):
        surf = pygame.Surface(self.item_size)
        surf.fill((25, 25, 56))
        surf.blit(item.thumbnail_img, (10, 10))
        surf.blit(constants.font.render(item.title, fgcolor=(255, 255, 255))[0], (20, 20))

        #draw something to the surf
        return surf

    def draw(self, surf):
        pygame.draw.rect(surf, (34, 34, 71), (*self.coords, *self.size))
        pygame.draw.rect(surf, (25, 25, 56), (*[i + self.margin for i in self.coords], *[j - self.margin * 2 for j in self.size]))

        render_amt = (self.size[1] - self.margin * 2) // self.item_size[1]

        prev_top_index = self.top_index
        while self.current_index - self.top_index not in range(render_amt): 
            self.top_index += core_functs.sgn(self.current_index - self.top_index)

        self.scroll[0] += -core_functs.sgn(self.top_index - prev_top_index) * self.item_size[1]

        for i in range(render_amt):
            try:
                item_surf = self.render_item(self.data[self.top_index + i])

                #self.scroll[0] % self.item_size[1] creates an offset whenever scroll is disturbed
                #just a neat trick to simulate a scrolling mechanic
                draw_loc = (self.coords[0] + self.margin, self.coords[1] + self.margin - self.scroll[0] + self.item_size[1] * i)
                if abs((draw_loc[1] + self.size[1]/2) - (self.coords[1] + self.margin + self.size[1]/2)) <self.size[1] + self.margin:
                    surf.blit(item_surf, draw_loc)

            except IndexError:
                pass

        pygame.draw.rect(surf, (184, 205, 255), (*[self.coords[0] + self.margin, self.coords[1] + self.margin + (self.current_index - self.top_index) * self.item_size[1]], *self.item_size), 2)

    def update(self, surf):
        self.scroll[0] = core_functs.lerp(*self.scroll, 0.01)
        super().update(surf)

class Tab(Interface):
    def __init__(self, coords, size, title=""):
        super().__init__(coords, size)
        self.title = title
        self.title_height = 20
        self.title_surf, self.title_rect = constants.font.render(self.title, fgcolor=(255, 255, 255))
    
    def draw_title(self, surf):
        pygame.draw.rect(surf, (55, 55, 82), (*self.coords, *[self.size[0], self.title_height]))
        surf.blit(self.title_surf, (self.coords[0] + 10, self.coords[1] + self.title_height/2 - self.title_rect.height/2))

    def draw(self, surf):
        pygame.draw.rect(surf, (40, 40, 84), (*self.coords, *self.size))
        self.draw_title(surf)

    def update_elements(self, surf):
        pass

    def update(self, surf):
        self.draw(surf)
        self.update_elements(surf)

    def event_handler(self):
        pass

class SliderTab(Tab):
    def __init__(self, coords, size, title=""):
        super().__init__(coords, size, title=title)
        self.slider = Slider([self.coords[0], self.coords[1] + self.title_height], [self.size[0], self.size[1] - self.title_height])

    def update_elements(self, surf):
        self.slider.update(surf)

    def event_handler(self):
        self.slider.event_handler()

class SearchTab(Tab):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.search_bar = SearchBar([self.coords[0], self.coords[1] + self.title_height], [self.size[0], self.size[1] - self.title_height])

    def update_elements(self, surf):
        self.search_bar.update(surf)

    def event_handler(self):
        self.search_bar.event_handler()

class SearchBar(Interface):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = ""
        self.margin = 5
        self.backspace_key = controls.to_key("backspace")[0]
        self.enter_key = controls.to_key("return")[0]
        self.backspace_cooldown = [0, 20]

    def draw(self, surf):
        pygame.draw.rect(surf, (255, 255, 255), (*self.coords, *self.size))

        surf.blit(constants.font.render(self.text)[0], [i + self.margin for i in self.coords])

    def event_handler(self):
        for i in pygame.event.get(eventtype=pygame.TEXTINPUT):
            self.text += i.text

        self.backspace_cooldown[0] = (self.backspace_cooldown[0] + 1) % 20
        
        if not self.backspace_cooldown[0]:
            if constants.controls.hold(self.backspace_key):
                self.text = self.text[:-1]





