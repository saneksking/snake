import pygame
import random

from tools.database import save_score, get_leaderboard_records

pygame.init()

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
darkblue = (0, 0, 255)
darkgreen = (0, 200, 0)

background_image = pygame.image.load('data/images/snake.png')
background_music = 'data/music/background_music.mp3'
pygame.mixer.music.set_volume(0.5)
button_click_sound = pygame.mixer.Sound('data/sounds/button.wav')
eat_sound = pygame.mixer.Sound('data/sounds/eat.wav')


title_font = pygame.font.SysFont("bahnschrift", 50)

width = 600
height = 600
display = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake')

clock = pygame.time.Clock()
snake_block = 10
snake_speed = 15
snake_color = green

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)


def our_snake(snake_block, snake_list, head_color):
    for x in snake_list[:-1]:
        pygame.draw.rect(display, snake_color, [x[0], x[1], snake_block, snake_block], border_radius=5)

    head_x, head_y = snake_list[-1]
    pygame.draw.circle(display, head_color,
                       (head_x + snake_block // 2, head_y + snake_block // 2), snake_block // 2)


def your_score(score):
    value = score_font.render("Score: " + str(score), True, white)
    display.blit(value, [0, 0])


def end(msg, color):
    message = font_style.render(msg, True, color)
    message_rect = message.get_rect(center=(width / 2, height / 2))
    display.blit(message, message_rect)


def draw_start_buttons():
    start_button_color = (148, 148, 27)
    settings_button_color = (120, 188, 153)
    start_button_rect = pygame.Rect(width / 4, height / 3, width / 2, 50)
    settings_button_rect = pygame.Rect(width / 4, height / 2, width / 2, 50)

    mouse_pos = pygame.mouse.get_pos()

    if start_button_rect.collidepoint(mouse_pos):
        start_button_color = (78, 66, 24)
    if settings_button_rect.collidepoint(mouse_pos):
        settings_button_color = (52, 84, 87)

    pygame.draw.rect(display, start_button_color, start_button_rect, border_radius=10)
    pygame.draw.rect(display, settings_button_color, settings_button_rect, border_radius=10)

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
        "Green": (0, 200, 0),
        "Red": (200, 0, 0),
        "Blue": (0, 0, 200),
        "Yellow": (200, 200, 0),
    }
    selected_color = snake_color

    while True:
        display.blit(background_image, (0, 0))

        settings_title = title_font.render("Settings", True, (148, 148, 27))
        title_rect = settings_title.get_rect(center=(width / 2, settings_title.get_height() / 2))

        padding = 10
        rect_x = 0
        rect_y = 0
        rect_width = width
        rect_height = title_rect.height + padding * 2
        pygame.draw.rect(display, black, (rect_x, rect_y, rect_width, rect_height))

        display.blit(settings_title, (title_rect.x, title_rect.y + padding))

        label_text = font_style.render("Speed:", True, green)
        display.blit(label_text, (label_rect.x, label_rect.y + 10))

        txt_surface = font_style.render(text, True, color)
        txt_width = max(200, txt_surface.get_width() + 10)
        input_box.w = txt_width
        pygame.draw.rect(display, white, input_box)
        display.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(display, color, input_box, 2)

        color_label = font_style.render("Snake Color:", True, green)
        display.blit(color_label, (label_rect.x, label_rect.y + 70))

        button_y = label_rect.y + 100
        button_width = 80
        button_spacing = 10
        for i, (color_name, color_value) in enumerate(colors.items()):
            button_rect = pygame.Rect(width / 4 + i * (button_width + button_spacing), button_y, button_width, 30)
            if button_rect.x + button_width > width - 20:
                break

            button_color = color_value
            if color_name == selected_color:
                button_color = tuple(min(c + 50, 255) for c in color_value)

            pygame.draw.rect(display, button_color, button_rect, border_radius=10)

            if color_name == "Yellow":
                color_text = font_style.render("Yellow", True, black)
            else:
                color_text = font_style.render(color_name, True, white)
            display.blit(color_text, (button_rect.x + 5, button_rect.y + 5))

            if pygame.mouse.get_pressed()[0] and button_rect.collidepoint(pygame.mouse.get_pos()):
                selected_color = color_value

        apply_button_rect = pygame.Rect(width / 4, button_y + 50, width / 2, 50)
        if apply_button_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(display, (78, 66, 24), apply_button_rect, border_radius=10)
        else:
            pygame.draw.rect(display, (148, 148, 27), apply_button_rect, border_radius=10)
        apply_text = font_style.render("Apply", True, white)
        display.blit(apply_text, (apply_button_rect.x + (apply_button_rect.width - apply_text.get_width())
                                  / 2, apply_button_rect.y + 10))

        if pygame.mouse.get_pressed()[0] and apply_button_rect.collidepoint(pygame.mouse.get_pos()):
            button_click_sound.play()
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
    pygame.mixer.music.stop()
    pygame.mixer.music.load('data/music/music.mp3')
    pygame.mixer.music.play(-1)
    while True:
        display.blit(background_image, (0, 0))

        title_text = title_font.render("Old Snake", True, (148, 148, 27))
        title_rect = title_text.get_rect(center=(width / 2, title_text.get_height() / 2))

        padding = 10
        rect_x = 0
        rect_y = 0
        rect_width = width
        rect_height = title_rect.height + padding * 2
        pygame.draw.rect(display, black, (rect_x, rect_y, rect_width, rect_height))

        display.blit(title_text, (title_rect.x, title_rect.y + padding))

        start_button_rect, settings_button_rect = draw_start_buttons()
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    button_click_sound.play()
                    pygame.mixer.music.stop()
                    return
                elif settings_button_rect.collidepoint(event.pos):
                    button_click_sound.play()
                    settings_screen()


def enter_nickname(score):
    input_box_width = width / 2
    input_box_height = 50
    input_box = pygame.Rect((width - input_box_width) / 2, (height - input_box_height) / 2, input_box_width,
                            input_box_height)

    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    nickname = ''

    # Создаем текст для надписи
    label_text = font_style.render("Enter your nickname:", True, green)
    label_rect = label_text.get_rect(center=(width / 2, input_box.top - 20))

    while True:
        display.fill(blue)
        your_score(score)

        display.blit(label_text, label_rect)

        txt_surface = font_style.render(nickname, True, color)
        input_box.w = max(200, txt_surface.get_width() + 10)
        pygame.draw.rect(display, white, input_box)
        display.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(display, color, input_box, 2)

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
                        save_score(nickname, score)
                        return
                    elif event.key == pygame.K_BACKSPACE:
                        nickname = nickname[:-1]
                    else:
                        nickname += event.unicode

        pygame.display.update()


def display_leaderboard(records):
    start_y = 100
    padding = 30

    title_text = title_font.render("Leaderboard", True, green)
    display.blit(title_text, (width / 2 - title_text.get_width() / 2, start_y - 50))

    for index, (nickname, score) in enumerate(records):
        record_text = font_style.render(f"{index + 1}. {nickname} - {score}", True, white)
        display.blit(record_text, (width / 2 - record_text.get_width() / 2, start_y + index * padding))

    pygame.display.update()


def show_leaderboard_screen():
    records = get_leaderboard_records()
    while True:
        display.fill(blue)
        display_leaderboard(records)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return

        pygame.display.update()


def game_loop():
    pygame.mixer.music.stop()
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
            pygame.mixer.music.stop()

            pygame.mixer.music.load('data/music/game_over.mp3')
            pygame.mixer.music.play(-1)

            end("You lost! Press C to continue or Q to exit!", green)
            your_score(score * snake_speed)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_close = False
                        enter_nickname(score * snake_speed)
                        show_leaderboard_screen()
                        start_screen()
                        game_loop()

        # Перемещение змейки
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
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
                elif event.key == pygame.K_SPACE:  # Добавлено для паузы
                    paused = not paused

        if paused:
            display.fill(blue)
            end("Paused! Press SPACE to continue", green)
            your_score(score * snake_speed)
            pygame.display.update()
            continue

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
                game_close = True

        our_snake(snake_block, snake_list, head_color=(255, 255, 255))
        your_score(score * snake_speed)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            length_of_snake += 1
            score += 1
            eat_sound.play()

        clock.tick(snake_speed)

    pygame.quit()
    quit()


start_screen()
game_loop()
