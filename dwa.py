import pygame
import ipaddress
import platform

pygame.init()

WIDTH, HEIGHT = 700, 550
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("IP Toolkit")
font = pygame.font.SysFont(None, 28)
small_font = pygame.font.SysFont(None, 24)

# Colors
BLUE = (30, 144, 255)
WHITE = (245, 245, 245)
BLACK = (0, 0, 0)
GREEN = (0, 150, 0)

# Input box now at TOP
input_box = pygame.Rect(50, 40, 600, 40)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
active = False
text = ''
result_lines = []

# -------- Program Info --------
def get_programming_info():
    return [
        f"Language: Python",
        f"Python Version: {platform.python_version()}",
        f"Library: Pygame"
    ]

# -------- IP Analysis --------
def analyze_ip(ip_text):
    lines = []
    try:
        ip = ipaddress.ip_interface(ip_text)
        lines.append(f"Valid IP: {ip.ip}")

        network = ip.network
        lines.append(f"Subnet: {network}")
        lines.append(f"Netmask: {network.netmask}")
        lines.append(f"Broadcast: {network.broadcast_address}")

        if ip.ip.is_private:
            lines.append("Type: Private IP")
        else:
            lines.append("Type: Public IP")

    except ValueError:
        lines.append("Invalid IP address")

    return lines

# -------- Feature Description (BOTTOM HALF) --------
def get_features_list():
    return [
        "What this app can do:",
        "- Validate IP addresses",
        "- Calculate subnet details",
        "- Identify public vs private IPs",
        "- Show programming language info",
        "",
        "Controls:",
        "Type IP at top (example: 192.168.1.1/24)",
        "Press ENTER to analyze",
        "Press I to show program info"
    ]

clock = pygame.time.Clock()
done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                active = not active
            else:
                active = False
            color = color_active if active else color_inactive
        elif event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    result_lines = analyze_ip(text)
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
            else:
                if event.key == pygame.K_i:
                    result_lines = get_programming_info()

    # -------- Draw Background Split --------
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, HEIGHT // 2))  # Top half blue

    # -------- Title --------
    title = font.render("IP Toolkit", True, WHITE)
    screen.blit(title, (50, 10))

    # -------- Input Box (TOP) --------
    txt_surface = font.render(text, True, WHITE)
    width = max(600, txt_surface.get_width()+10)
    input_box.w = width
    screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
    pygame.draw.rect(screen, color, input_box, 2)

    # -------- Results (TOP HALF) --------
    y_offset = 100
    for line in result_lines:
        res_surface = font.render(line, True, WHITE)
        screen.blit(res_surface, (50, y_offset))
        y_offset += 30

    # -------- Feature List (BOTTOM HALF) --------
    y_offset = HEIGHT // 2 + 20
    for line in get_features_list():
        feature_surface = small_font.render(line, True, BLACK)
        screen.blit(feature_surface, (50, y_offset))
        y_offset += 25

    pygame.display.flip()
    clock.tick(30)

pygame.quit()