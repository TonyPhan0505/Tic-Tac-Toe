import pygame

def main():
   # initialize all pygame modules (some need initialization)
   pygame.init()
   # create a pygame display window
   pygame.display.set_mode((500, 400))
   # set the title of the display window
   pygame.display.set_caption('Tic Tac Toe')   
   # get the display surface
   w_surface = pygame.display.get_surface() 
   # create a game object
   game = Game(w_surface)
   # start the main game loop by calling the play method on the game object
   game.play() 
   # quit pygame and clean up the pygame window
   pygame.quit() 

   
# User-defined classes

class Game:
   # An object in this class represents a complete game.

   def __init__(self, surface):
      # Initialize a Game.
      # - self is the Game to initialize
      # - surface is the display window surface object

      # === objects that are part of every game that we will discuss
      self.surface = surface
      self.bg_color = pygame.Color('black')
      
      self.FPS = 60
      self.game_clock = pygame.time.Clock()
      self.close_clicked = False
      self.continue_game = True
      
      # === game specific objects
      # board: list of rows, each row is list of tiles
      self.board_size = 3
      self.board = self.create_tiles()
      self.player_1 = 'X'
      self.player_2 = 'O'
      self.turn = self.player_1
      self.filled_count = 0
      self.rows_data = [[] for _ in range(self.board_size)]
      self.cols_data = [[] for _ in range(self.board_size)]
      self.diags_data = [[],[]]
      self.row_win = None
      self.col_win = None
      self.diag_win = None

   def create_tiles(self):
      size = self.surface.get_size() # (500,400) here
      surface_width = size[0] # 500 here
      surface_height = size[1] # 400 here
      # Tile size:
      tile_width = surface_width // self.board_size
      tile_height = surface_height // self.board_size
      
      tiles = [ ]
      for row_index in range(self.board_size):
          row = [ ]
          for col_index in range(self.board_size):
              # Scaling from col_index, row_index to the width/height
              x = col_index * tile_width
              y = row_index * tile_height        
              tile = Tile(x, y, tile_width, tile_height, self.surface, row_index, col_index)
              row.append(tile)
          tiles.append(row)
      return tiles

   def play(self):
      # Play the game until the player presses the close box.
      # - self is the Game that should be continued or not.

      while not self.close_clicked:  # until player clicks close box
         # play frame
         self.handle_events()
         self.draw()            
         if self.continue_game:
            self.decide_continue()
         self.game_clock.tick(self.FPS) 
         # run at most with FPS Frames Per Second 

   def handle_events(self):
      # Handle each user event by changing the game state appropriately.
      # - self is the Game whose events will be handled

      events = pygame.event.get()
      for event in events:
         if event.type == pygame.QUIT:
            self.close_clicked = True
         elif event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_down(event)

   def handle_mouse_down(self, event):
      # event.pos is the location of the mouse click
      # Ask each tile if it has been selected
      # if yes: 
      #     if tile is empty: make a move there
      #     else: flash
      for row in self.board:
         for tile in row:
            if tile.select(event.pos):
               if self.continue_game:
                  if tile.get_content() == '':
                     tile.set_content(self.turn)
                     self.filled_count += 1
                     self.change_turn()
                     self.update(tile.row, tile.col)
                  else:
                     #flash the tile
                     tile.set_flashing(True)
               else:
                  tile.set_flashing(True)

   def draw(self):
      # Draw all game objects.
      # - self is the Game to draw
      
      self.surface.fill(self.bg_color) # clear the display surface first
      self.draw_all_tiles()
      pygame.display.update() # make the updated surface appear on the display

   def draw_all_tiles(self):
      for row in self.board:
         for tile in row:
            tile.draw()

   def update(self, row, col):
      # Update rows data, diags data and verticals data
      
      content = self.board[row][col].get_content()

      self.rows_data[row].append(content)
      self.cols_data[col].append(content)
      
      if row == col:
         self.diags_data[0].append(content)
      if row+col == self.board_size-1:
         self.diags_data[1].append(content)      

   def decide_continue(self):
      # Check and remember if the game should continue
      # - self is the Game to check
      
      # this should check for a win or a tie
      if self.is_tie() or self.is_win():
         self.continue_game = False

   def opponent(self):
      if self.turn == 'X':
         return 'O'
      else:
         return 'X'

   def change_turn(self):
      self.turn = self.opponent()
   
   def all_tiles_occupied(self):
      return self.filled_count == self.board_size **2
   
   def is_tie(self):
      return self.all_tiles_occupied() and not self.is_win()

   def is_win(self):
      return self.is_row_win() or self.is_col_win() or self.is_diag_win()

   def is_col_win(self):
      for c in range(len(self.cols_data)):
         if len(self.cols_data[c]) == self.board_size and len(set(self.cols_data[c])) == 1:
            self.col_win = c
            return True

   def is_diag_win(self):
      for d in range(len(self.diags_data)):
            if len(self.diags_data[d]) == self.board_size and len(set(self.diags_data[d])) == 1:
               self.diag_win = d
               return True

   def is_row_win(self):
      for r in range(len(self.rows_data)):
         if len(self.rows_data[r]) == self.board_size and len(set(self.rows_data[r])) == 1:
            self.row_win = r
            return True


class Tile:
   # A tile is a rectangle on a surface
   
   def __init__(self, x, y, width, height, surface, row, col):
      self.color = pygame.Color('white')
      self.rect = pygame.Rect(x, y, width, height)
      self.surface = surface
      self.line_width = 3
      self.content = ''
      self.flashing = False
      self.row = row
      self.col = col
      self.win_tile = False

   def set_flashing(self, value):
      if value:
         self.flashing = True
      else:
         self.flashing = True
         self.win_tile = True

   def draw(self):
      # Draw the tile on the surface
      # - self is the Tile

      if self.flashing and not self.win_tile:
         pygame.draw.rect(self.surface, self.color, self.rect)
         self.flashing = False
      elif self.flashing and self.win_tile:
         pygame.draw.rect(self.surface, self.color, self.rect)
         pygame.time.delay(500)
         self.flashing = False
      else:
         pygame.draw.rect(self.surface, self.color, self.rect, self.line_width)
      # draw the content as a string
      self.draw_content()
   
   def draw_content(self):
      def create_text_image(content, size, color):
         text_string = content
         text_color = pygame.Color(color)
         text_font = pygame.font.SysFont("Times New Roman", size, bold = True, italic = False)
         text_image = text_font.render(text_string, True, text_color)
         return text_image
      fontsize = 100
      text_image = create_text_image(self.content, fontsize, self.color)
      x = self.rect.x + self.rect.width//2 - text_image.get_width()//2
      y = self.rect.y + self.rect.height//2 - text_image.get_height()//2
      location = (x,y)
      self.surface.blit(text_image, location)

   def select(self, pos):
      # is the pos inside this tile?
      return self.rect.collidepoint(pos)
   
   def get_content(self):
      return self.content
   
   def set_content(self, new_content):
      self.content = new_content
main()