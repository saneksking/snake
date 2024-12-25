import pygame
import random

pygame.init()

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
darkblue = (0, 0, 255)

title_font = pygame.font.SysFont("bahnschrift", 50)

width = 600
height = 400
display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake')

clock = pygame.time.Clock()
snake_block = 10
snake_speed = 15
snake_color = green

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)


def our_snake(snake, snake_list):
    for x in snake_list:
        pygame.draw.rect(display, snake_color, [x[0], x[1], snake, snake_block])


def your_score(score):
    value = score_font.render("Score: " + str(score), True, white)
    display.blit(value, [0, 0])


def end(msg, color):
    message = font_style.render(msg, True, color)
    message_rect = message.get_rect(center=(width / 2, height / 2))
    display.blit(message, message_rect)


def draw_start_buttons():
    start_button_color = green
    settings_button_color = darkblue
    start_button_rect = pygame.Rect(width / 4, height / 3, width / 2, 50)
    settings_button_rect = pygame.Rect(width / 4, height / 2, width / 2, 50)

    pygame.draw.rect(display, start_button_color, start_button_rect)
    pygame.draw.rect(display, settings_button_color, settings_button_rect)

    start_text = font_style.render("Start", True, white)
    settings_text = font_style.render("Settings", True, white)

    display.blit(start_text, (start_button_rect.x + (start_button_rect.width - start_text.get_width())
                              / 2, start_button_rect.y + 10))
    display.blit(settings_text, (settings_button_rect.x + (settings_button_rect.width - settings_text.get_width())
                                 / 2, settings_button_rect.y + 10))

    return start_button_rect, settings_button_rect


def settings_screen():
    global snake_speed, snake_color
    input_box = pygame.Rect(width / 4 + 100, height / 3, 100, 50)
    label_rect = pygame.Rect(width / 4, height / 3, 100, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = str(snake_speed)

    colors = {
        "Green": (0, 255, 0),
        "Red": (255, 0, 0),
        "Blue": (0, 0, 255),
        "Yellow": (255, 255, 0),
    }
    selected_color = snake_color

    while True:
        display.fill(blue)

        # Заголовок "Settings"
        settings_title = title_font.render("Settings", True, green)
        display.blit(settings_title, (width / 2 - settings_title.get_width() / 2, height / 6))

        label_text = font_style.render("Speed:", True, white)
        display.blit(label_text, (label_rect.x, label_rect.y + 10))

        txt_surface = font_style.render(text, True, color)
        txt_width = max(200, txt_surface.get_width() + 10)
        input_box.w = txt_width
        pygame.draw.rect(display, white, input_box)
        display.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(display, color, input_box, 2)

        color_label = font_style.render("Snake Color:", True, white)
        display.blit(color_label, (label_rect.x, label_rect.y + 70))

        button_y = label_rect.y + 100
        button_width = 80
        button_spacing = 10
        for i, (color_name, color_value) in enumerate(colors.items()):
            button_rect = pygame.Rect(width / 4 + i * (button_width + button_spacing), button_y, button_width, 30)
            if button_rect.x + button_width > width - 20:
                break
            pygame.draw.rect(display, color_value, button_rect)
            if color_name == "Yellow":
                color_text = font_style.render("Yellow", True, black)
            else:
                color_text = font_style.render(color_name, True, white)
            display.blit(color_text, (button_rect.x + 5, button_rect.y + 5))

            if pygame.mouse.get_pressed()[0] and button_rect.collidepoint(pygame.mouse.get_pos()):
                selected_color = color_value

        apply_button_rect = pygame.Rect(width / 4, button_y + 50, width / 2, 50)
        pygame.draw.rect(display, green, apply_button_rect)
        apply_text = font_style.render("Apply", True, white)
        display.blit(apply_text, (apply_button_rect.x + (apply_button_rect.width - apply_text.get_width())
                                  / 2, apply_button_rect.y + 10))

        if pygame.mouse.get_pressed()[0] and apply_button_rect.collidepoint(pygame.mouse.get_pos()):
            snake_color = selected_color
            return

        if text == "":
            snake_speed = 15
        else:
            try:
                snake_speed = int(text)
            except ValueError:
                snake_speed = snake_speed

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        if text == "":
                            snake_speed = 15
                        else:
                            try:
                                snake_speed = int(text)
                            except ValueError:
                                snake_speed = snake_speed
                        return
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
        pygame.display.update()



def start_screen():
    while True:
        display.fill(blue)

        title_text = title_font.render("Old Snake", True, green)
        display.blit(title_text, (width / 2 - title_text.get_width() / 2, height / 6))

        start_button_rect, settings_button_rect = draw_start_buttons()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if start_button_rect.collidepoint(event.pos):
                        return
                    elif settings_button_rect.collidepoint(event.pos):
                        settings_screen()


def game_loop():
    game_over = False
    game_close = False
    paused = False

    x1 = width / 2
    y1 = height / 2

    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1
    score = 0

    foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    while not game_over:
        while game_close:
            display.fill(blue)
            end("You lost! Press C to continue or Q to exit!", red)
            your_score(score)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_close = False
                        start_screen()
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused

                if not paused:  # Обрабатываем управление только если не на паузе
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        x1_change = -snake_block
                        y1_change = 0
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        x1_change = snake_block
                        y1_change = 0
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        y1_change = -snake_block
                        x1_change = 0
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        y1_change = snake_block
                        x1_change = 0

        if paused:
            display.fill(blue)
            end("Paused! Press SPACE to continue", red)
            your_score(score)
            pygame.display.update()
            continue

        # Логика игры
        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        display.fill(blue)
        pygame.draw.rect(display, red, [foodx, foody, snake_block, snake_block])
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = False

        our_snake(snake_block, snake_list)
        your_score(score)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            length_of_snake += 1
            score += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()


start_screen()
game_loop()
