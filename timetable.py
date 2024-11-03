import pygame

WIDTH, HEIGHT = 475, 600
VISIBLE_EMPLOYEES = 2  # Number of employees visible at once
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

pygame.init()

FPS = 30
clock = pygame.time.Clock()


class Timetable:
    def __init__(self, x, y, width, height, start_time, end_time, bckgr_colour):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.start_time, self.end_time = start_time, end_time
        self.bckgr_colour = bckgr_colour
        self.data = {'Employee1': [], 'Employee2': [], 'Employee3': [], 'Employee4': [], 'Employee5': []}
        self.font = pygame.font.SysFont('Arial', 10)
        self.employee_offset = 0  # Scroll offset
        self.scrollbar_rect = pygame.Rect(60, HEIGHT - 20, WIDTH - 120, 10)  # Scrollbar position
        self.scrollbar_dragging = False  # To track if scrollbar is being dragged

    def draw_grid(self):
        # Draw horizontal lines for each hour
        for i in range(self.start_time, self.end_time + 1):
            y = 60 + (i - self.start_time) * (self.height - 80) // (self.end_time - self.start_time)
            pygame.draw.line(screen, '#888888', (60, y), (self.width, y), 1)
        # Draw vertical lines for each visible employee column
        for i in range(VISIBLE_EMPLOYEES + 1):
            x = 60 + i * (self.width - 60) // VISIBLE_EMPLOYEES
            pygame.draw.line(screen, '#888888', (x, 60), (x, self.height - 40), 1)

    def draw_legend(self):
        x_pos = 70
        visible_employees = list(self.data.keys())[self.employee_offset:self.employee_offset + VISIBLE_EMPLOYEES]
        for key in visible_employees:
            legend = self.font.render(key, True, 'black')
            screen.blit(legend, (x_pos, 10))
            x_pos += (self.width - 60) // VISIBLE_EMPLOYEES
        y_pos = 70
        for hour in range(self.start_time, self.end_time):
            legend = self.font.render(f"{hour}:00", True, 'black')
            screen.blit(legend, (10, y_pos))
            y_pos += (self.height - 80) // (self.end_time - self.start_time)

    def add_event(self, label, employee, time, duration, colour):
        if employee not in list(self.data.keys())[self.employee_offset:self.employee_offset + VISIBLE_EMPLOYEES]:
            return
        employee_index = list(self.data.keys()).index(employee) - self.employee_offset
        x = 60 + employee_index * (self.width - 60) // VISIBLE_EMPLOYEES
        y = 60 + (time - self.start_time) * (self.height - 80) // (self.end_time - self.start_time)
        width = (self.width - 60) // VISIBLE_EMPLOYEES
        height = duration * (self.height - 80) // (self.end_time - self.start_time)
        event_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, colour, event_rect)

    def draw_scrollbar(self):
        pygame.draw.rect(screen, 'grey', self.scrollbar_rect)
        handle_width = self.scrollbar_rect.width * VISIBLE_EMPLOYEES // len(self.data)
        handle_x = self.scrollbar_rect.x + (self.employee_offset * (self.scrollbar_rect.width - handle_width) // (
                    len(self.data) - VISIBLE_EMPLOYEES))
        handle_rect = pygame.Rect(handle_x, self.scrollbar_rect.y, handle_width, self.scrollbar_rect.height)
        pygame.draw.rect(screen, 'darkgrey', handle_rect)

    def update_scroll(self, mouse_x):
        if self.scrollbar_dragging:
            handle_width = self.scrollbar_rect.width * VISIBLE_EMPLOYEES // len(self.data)
            new_handle_x = max(self.scrollbar_rect.x, min(mouse_x - handle_width // 2,
                                                          self.scrollbar_rect.x + self.scrollbar_rect.width - handle_width))
            self.employee_offset = (new_handle_x - self.scrollbar_rect.x) * (len(self.data) - VISIBLE_EMPLOYEES) // (
                        self.scrollbar_rect.width - handle_width)


# Create the timetable object
ttable = Timetable(0, 0, WIDTH, HEIGHT, 8, 23, 'white')

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if ttable.scrollbar_rect.collidepoint(event.pos):
                ttable.scrollbar_dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            ttable.scrollbar_dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if ttable.scrollbar_dragging:
                ttable.update_scroll(event.pos[0])

    screen.fill('white')
    ttable.draw_grid()
    ttable.draw_legend()
    ttable.add_event('event', 'Employee1', 9, 2, 'red')
    ttable.add_event('event', 'Employee2', 14, 1, 'blue')
    ttable.add_event('event', 'Employee3', 11, 3, 'green')
    ttable.add_event('event', 'Employee4', 10, 2, 'purple')
    ttable.add_event('event', 'Employee5', 15, 1, 'orange')
    ttable.add_event('event', 'Employee3', 10, 2, 'grey')
    ttable.add_event('event', 'Employee3', 13, 2, 'yellow')
    ttable.draw_scrollbar()
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()