import pygame;

import random;

################################################################################

Palette = [
  pygame.Color("#070707"),
  pygame.Color("#1F0707"),
  pygame.Color("#2F0F07"),
  pygame.Color("#470F07"),
  pygame.Color("#571707"),
  pygame.Color("#671F07"),
  pygame.Color("#771F07"),
  pygame.Color("#8F2707"),
  pygame.Color("#9F2F07"),
  pygame.Color("#AF3F07"),
  pygame.Color("#BF4707"),
  pygame.Color("#C74707"),
  pygame.Color("#DF4F07"),
  pygame.Color("#DF5707"),
  pygame.Color("#DF5707"),
  pygame.Color("#D75F07"),
  pygame.Color("#D7670F"),
  pygame.Color("#CF6f0F"),
  pygame.Color("#CF770F"),
  pygame.Color("#CF7f0F"),
  pygame.Color("#CF8717"),
  pygame.Color("#C78717"),
  pygame.Color("#C78F17"),
  pygame.Color("#C7971F"),
  pygame.Color("#BF9F1F"),
  pygame.Color("#BF9F1F"),
  pygame.Color("#BFA727"),
  pygame.Color("#BFA727"),
  pygame.Color("#BFAF2F"),
  pygame.Color("#B7AF2F"),
  pygame.Color("#B7B72F"),
  pygame.Color("#B7B737"),
  pygame.Color("#CFCF6F"),
  pygame.Color("#DFDF9F"),
  pygame.Color("#EFEFC7"),
  pygame.Color("#FFFFFF")
];

################################################################################

class Fire:
  _width   = 0;
  _height  = 0;

  _scaledWidth  = 0;
  _scaledHeight = 0;
  
  _data    = [];
  _palette = [];

  _burning = True;
  
  _qualityScaleFactor = 1;
  
  # ----------------------------------------------------------------------------
  
  def __init__(self,
               width : int,
               height : int,
               palette : list,
               qualityScaleFactor : int = 1):
    self._width   = width;
    self._height  = height;
    self._palette = palette;
    
    self._qualityScaleFactor = qualityScaleFactor;
    
    self._scaledWidth  = width // qualityScaleFactor;
    self._scaledHeight = height // qualityScaleFactor;
    
    ln = len(self._palette);
    
    self._data = [
      [ 0 for _ in range(self._scaledWidth) ]
      for _ in range(self._scaledHeight)
    ];
    
    for y in range(self._scaledWidth):
      self._data[0][y] = ln - 1;
  
  # ----------------------------------------------------------------------------
  
  def Draw(self, screen : pygame.Surface, px : int, py : int):
    for x in range(self._scaledHeight):
      for y in range(self._scaledWidth):
        ind = self._data[x][y];
        clr = self._palette[ind];
        pygame.draw.rect(screen,
                         clr,
                         pygame.Rect(px + y * self._qualityScaleFactor,
                                     py - x * self._qualityScaleFactor,
                                     self._qualityScaleFactor,
                                     self._qualityScaleFactor)
                         );
    
  # ----------------------------------------------------------------------------
  
  def Extinguish(self):
    for y in range(self._scaledWidth):
      self._data[0][y] = 0;
    self._burning = False;
  
  # ----------------------------------------------------------------------------
  
  def Ignite(self):
    for y in range(self._scaledWidth):
      self._data[0][y] = len(self._palette) - 1;
    self._burning = True;
    
  # ----------------------------------------------------------------------------
  
  def Simulate(self):
    for y in range(self._scaledWidth):
      for x in range(1, self._scaledHeight, 1):
        #
        # Basically 2/4 = 1/2 probability of advancing through palette towards
        # black since rightmost bit is 1 two times in four cases: 00 01 10 11
        #                                                            --    --
        #
        # We could also just use random 0-1 offset based on some condition to
        # control fire extinguish rate.
        #
        ind = self._data[x - 1][y] - (random.randint(0, 3) & 1);
        
        if ind < 0:
          ind = 0;
        
        lateralOffset = random.randint(-1, 1);
        newY = y + lateralOffset;
        
        if newY < 0:
          newY = self._scaledWidth - 1;
        elif newY >= self._scaledWidth:
          newY = 0;
          
        self._data[x][newY] = ind;

################################################################################

def main():
  screenSize = [ 640, 480 ];
  
  pygame.init();
  pygame.display.set_caption("Flame demo");

  screen = pygame.display.set_mode(screenSize);

  running = True;
  
  clock = pygame.time.Clock();
  
  fire = Fire(screenSize[0], screenSize[1], Palette, 6);
  
  while running:
    clock.tick(60);
    
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False;
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          running = False;
        if event.key == pygame.K_SPACE:
          if fire._burning:
            fire.Extinguish();
          else:
            fire.Ignite();
  
    screen.fill((0,0,0));
  
    #x = 0;
    #for c in Palette:
    #  pygame.draw.rect(screen, c, (x, 0, 10, 10));
    #  x += 10;
    
    fire.Simulate();
    fire.Draw(screen, 0, screenSize[1] - 1);
    
    pygame.display.flip();
  
  pygame.quit();

################################################################################

if __name__ == "__main__":
  main();
