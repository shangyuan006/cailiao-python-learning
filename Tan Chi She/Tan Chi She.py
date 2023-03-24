# 导入依赖库
import pygame
import sys
import random

# 显示分数的函数
def display_screen(screen,score):
    font = pygame.font.Font(None, 36)   # 设置字体大小
    text = font.render(f"Score: {score}", True, (255, 255, 255))    # 渲染分数文字
    screen.blit(text, (10, 10))     # 在屏幕上显示分数

# 暂停游戏的函数
def pause_game(screen, pause):
    if pause:
        font = pygame.font.Font(None, 36) # 设置字体大小
        text = font.render("Press SPACE to unpause", True, (255, 255, 255))     # 渲染暂停文字
        screen.blit(text, (170, 200))       # 在屏幕上显示暂停提示
        pygame.display.update()     # 更新屏幕显示

# 显示开始屏幕的函数
def display_start_screen(screen):
    screen.fill((0, 0, 0))      # 填充屏幕背景色
    font = pygame.font.Font(None, 36)       # 设置字体大小
    text = font.render("Press ENTER to start", True, (255, 255, 255))   # 渲染开始提示文字
    screen.blit(text, (140, 200))       # 在屏幕上显示开始提示
    pygame.display.update()     # 更新屏幕显示

# 处理输入事件的函数
def process_input_events(running, direction, change_to, pause, screen):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:        # TODO:烂尾了，小红书作者缺少

# 更新蛇的位置
def update_snake_position(snake_position, direction, block_size):       # TODO:烂尾了，小红书作者缺少


# 显示游戏结束屏幕的函数
def display_game_over_screen(screen, score):
    screen.fill((0, 0, 0))      # 填充屏幕背景色
    font = pygame.font.Font(None, 36)       # 设置字体大小
    text = font.render(f"HAHA,886! Score: {score}", True, (255, 255, 255))      # 渲染游戏结束文字
    screen.blit(text, (140, 200))       # 在屏幕上显示游戏结束提示

    encouragement_text = font.render("XiGua8Hao is laughing at you! Press ENTER to restart", True, (255, 255, 255))
    screen.blit(encouragement_text, (50, 240))      # 在屏幕上显示鼓励文字

    pygame.display.update()     # 更新屏幕显示


# 检查碰撞的函数
def check_collision(snake_position, screen_size, block_size, snake_body):
    return (
            snake_position[0] < 0
            or snake_position[0] > screen_size[0] - block_size
            or snake_position[1] < 0
            or snake_position[1] > screen_size[1] - block_size
            or snake_position in snake_body[1:]
    )

# 主函数
def main():
    pygame.init()       # 初始化 pygame
    screen_size = (640, 480)
    screen = pygame.display.set_mode(screen_size)       # 设置屏幕尺寸
    pygame.display.set_caption("Tan Chi She")       # 设置窗口标题

    clock = pygame.time.Clock()     # 创建时钟对象
    speed = 15      # 设置蛇的速度
    block_size = 20     # 设置蛇身体块大小
    snake_position = [100, 200]      # 设置蛇的初始位置
    snake_body = [[100, 100], [90, 100], [80, 100]]     # 设置蛇身体的初始位置

    food_position = [random.randrange(1, 32) * 20, random.randrange(1, 24) * 20]        # 设置食物的初始位置
    food_spawn = True       # 设置食物生成标志

    direction = "RIGHT"     # 设置蛇的初始方向
    change_to = direction       # 设置方向的改变


    score = 0       # 初始化分数

    running = False     # 设置游戏运行标志
    pause = False       # 设置游戏暂停标志

    display_start_screen(screen)        # 显示开始屏幕

    while True:
        running, change_to, pause = process_input_events(running, direction, change_to, pause, screen)      # 处理输入事件
        if pause:
            continue

        if not running:
            continue

        direction = change_to

        # 更新蛇的位置
        snake_position = update_snake_position(snake_position, direction, block_size)

        # 更新蛇的身体
        snake_body.insert(0, list(snake_position))

        # 检查蛇是否吃到食物
        if snake_position == food_position:
            score += 1
            food_spawn = False
        else:
            snake_body.pop()

        # 生成新的食物
        if not food_spawn:
            food_position = [random.randrange(1, 32) * 20, random.randrange(1, 24) * 20]
        food_spawn = True

        # 清空屏幕
        screen.fill((0, 0, 0))

        # 绘制蛇的身体
        for pos in snake_body:
            pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(pos[0], pos[1], block_size, block_size))
        # 绘制食物
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(food_position[0], food_position[1], block_size, block_size))

        # 显示分数
        display_score(screen, score)

        # 更新屏幕显示
        pygame.display.flip()

        # 检查碰撞
        if check_collision(snake_position, screen_size, block_size, snake_body):
            display_game_over_screen(screen, score)
            running = False
            while not running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        running = True
                        break
            score = 0
            snake_position = [100, 100]
            snake_body = [[100, 100], [90, 100], [80, 100]]
            direction = "RIGHT"
            change_to = direction

        # 控制游戏速度
        clock.tick(speed)

if __name__ == "__main__":
    main()


