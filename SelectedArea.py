class SelectedArea:

    def __init__(self, rectangle, pos = (1, 1), dim = (5, 5)):
        self.dim = dim
        self.pos = pos
        self.rectangle = rectangle
        self.length = 3
        self.height = 5
        self.top_left = (0,1)
        self.bottom_right = (1,0)
        self.initiated = False

    def adjustRectangle(self, event=None, values=None):
        self.initiated = True
        if event == 'graph':
            self.pos = values['graph']
        elif event == ',':
            self.pos = (self.pos[0] - 1, self.pos[1])
        elif event == ';':
            self.pos = (self.pos[0], self.pos[1] - 1)
        elif event == '/':
            self.pos = (self.pos[0] + 1, self.pos[1])
        elif event == '.':
            self.pos = (self.pos[0], self.pos[1] + 1)
        elif event == 'MouseWheel:Up' and self.length < 120: 
            self.length += 3
            self.height += 5
        elif event == 'MouseWheel:Down' and self.length > 3:
            self.length -= 3
            self.height -= 5
        
        self.top_left = (self.pos[0] - self.length, self.pos[1] + self.height)
        self.bottom_right = (self.pos[0] + self.length, self.pos[1] - self.height)

        return (self.top_left, self.bottom_right)
    
    def getCrop(self):

        self.coords = [self.bottom_right[1], self.top_left[1], 
                self.top_left[0], self.bottom_right[0]] 

        for x in range(len(self.coords)):
            if self.coords[x-1] < 0:
                self.coords[x-1] = 0

        return self.coords