import pygame
import random

WIN_WIDTH = 800
WIN_HEIGHT = 600
FPS = 30

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (121, 121, 121)

def init(title):
    pygame.init()
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption(title)
    clock = pygame.time.Clock()
    return screen, clock

def draw_text(text, x, y):
    base_font = pygame.font.SysFont('Arial', 36, True)
    text = base_font.render(text, True, BLACK)
    text_rect = text.get_rect()
    text_rect.centerx = x
    text_rect.y = y
    return text, text_rect

screen, clock = init('Безумная трасса')

class Car(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('car_1.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
class Enemy_car(pygame.sprite.Sprite):
    image_list = ['car_2.png',
                  'car_3.png',
                  'car_4.png'
                  ]

    def __init__(self, speed):
        super().__init__()
        img = Enemy_car.image_list[random.randint(0, 2)]
        self.image = pygame.image.load(img).convert_alpha()
        self.image = pygame.transform.rotate(self.image, 180)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIN_WIDTH)
        self.rect.y = random.randrange(-200, WIN_HEIGHT - 400)
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > WIN_HEIGHT:
            self.__init__(self.speed)
            self.rect.y = -50
        
all_sprites_list = pygame.sprite.Group()
enemy_car_list = pygame.sprite.Group()

for i in range(10):
    enemy_car = Enemy_car(random.randint(5, 8))
    enemy_car_list.add(enemy_car)
    all_sprites_list.add(enemy_car)

player = Car(WIN_WIDTH // 2, WIN_HEIGHT - 100)
all_sprites_list.add(player)

run = True

current_state = "menu"

button = pygame.Surface((300, 50))
button.fill(WHITE)
screen_button_pos_x = WIN_WIDTH // 3.5
screen_button_pos_y1 = 100
screen_button_pos_y2 = 200
screen_button_pos_y3 = 300

def draw_button():
    screen.blit(button, (screen_button_pos_x, screen_button_pos_y1))
    text_1, text_rect_1 = draw_text('Играть', screen_button_pos_x + 150, screen_button_pos_y1 + 5)
    screen.blit(text_1, text_rect_1)
    screen.blit(button, (screen_button_pos_x, screen_button_pos_y2))
    text_2, text_rect_2 = draw_text('Управление', screen_button_pos_x + 150, screen_button_pos_y2 + 5)
    screen.blit(text_2, text_rect_2)
    screen.blit(button, (screen_button_pos_x, screen_button_pos_y3))
    text_3, text_rect_3 = draw_text('Выйти', screen_button_pos_x + 150, screen_button_pos_y3 + 5)
    screen.blit(text_3, text_rect_3)
    
def draw_control():
    text_1, text_rect_1 = draw_text('Управление машиной - движение мышью', 380, 105)
    screen.blit(text_1, text_rect_1)
    text_2, text_rect_2 = draw_text('Закрыть игру - Q', 380, 205)
    screen.blit(text_2, text_rect_2)
    text_3, text_rect_3 = draw_text('Выйти в меню - пробел', 380, 305)
    screen.blit(text_3, text_rect_3)
    
def handle_mouse_action(event):
    global current_state
    pos_x, pos_y = pygame.mouse.get_pos()
    check_pos_x_button = screen_button_pos_x <= pos_x <= (screen_button_pos_x + 300)
    check_pos_y1_button = screen_button_pos_y1 <= pos_y <= screen_button_pos_y1 + 50
    check_pos_y2_button = screen_button_pos_y2 <= pos_y <= screen_button_pos_y2 + 50
    check_pos_y3_button = screen_button_pos_y3 <= pos_y <= screen_button_pos_y3 + 50
    if event.type == pygame.MOUSEBUTTONDOWN:
        if check_pos_x_button and check_pos_y1_button:
           current_state = "game"
        if check_pos_x_button and check_pos_y2_button:
          current_state = "control"
        if check_pos_x_button and check_pos_y3_button:
            pygame.quit()

first_c = 0
timer = 0

while True:
    first_c += 1
    if first_c == 30:
        timer += 1
        first_c = 0
        
    for event in pygame.event.get():
        handle_mouse_action(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                break
            elif event.key == pygame.K_SPACE:
                if current_state == "control": 
                    current_state = "menu"
    
    if current_state == "game":
        pos = pygame.mouse.get_pos()
        player.rect.x = pos[0] - player.rect.width // 2
        enemy_car_list.update()
        if pygame.sprite.spritecollideany(player, enemy_car_list):
            current_state = "menu"
            first_c = 0
            timer = 0
            all_sprites_list = pygame.sprite.Group()
            enemy_car_list = pygame.sprite.Group()

            for i in range(10):
                enemy_car = Enemy_car(random.randint(5, 8))
                enemy_car_list.add(enemy_car)
                all_sprites_list.add(enemy_car)

            player = Car(WIN_WIDTH // 2, WIN_HEIGHT - 100)
            all_sprites_list.add(player)
    
    screen.fill(GRAY)

    if current_state == "menu":
        draw_button()
        
    elif current_state == "game":
        all_sprites_list.draw(screen)
        text_fps, text_rect_fps = draw_text("sec: " + str(timer), 50, 30)
        screen.blit(text_fps, text_rect_fps)
    
    elif current_state == "control":
        draw_control()
        
    pygame.display.update()
    
    clock.tick(FPS)