import sys, pygame, gui, core_functs, controls, constants, pytube
from yt_to_mp3 import *

class Program:
    def __init__(self):
        self.tabs = []

        #search tab
        tab = gui.SearchTab([0, 0], [400, 50], title="search")
        self.tabs += [tab]

        #results tab
        tab = gui.SliderTab(gui.get_tab_loc(self.tabs[0], [0, 1]), [self.tabs[0].size[0], constants.screen.get_height() - self.tabs[0].size[1]], title="result")
        self.tabs += [tab]

        #cart tab
        tab = gui.SliderTab(gui.get_tab_loc(self.tabs[0], [1, 0]), [constants.screen.get_width() - self.tabs[0].size[0], constants.screen.get_height()], title="cart")
        self.tabs += [tab]
        self.tab_index = 0

        self.update_order = (1, 2, 0)
    def run(self):
        while True:
            constants.controls.update()
            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            constants.screen.fill((10, 10, 20))

            for i in self.update_order:
                self.tabs[i].update(constants.screen)
            self.tabs[self.tab_index].event_handler()

            if self.tab_index == 0:
                if constants.controls.keydown(controls.to_key("return")[0]):
                    self.tab_index = 1
                    self.tabs[1].slider.update_data(pytube.contrib.search.Search(self.tabs[0].search_bar.text).results)


            pygame.display.update()



Program().run()
