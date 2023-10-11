import pygame


def display_timer(window, timer_font, shared_timer):
    while True:
        window.fill((255, 255, 255))  # Clear the window
        timer_text = timer_font.render(f"Time: {int(shared_timer[0])} seconds", True,
                                       (0, 0, 0))  # Render the timer text
        text_rect = timer_text.get_rect(center=(window.get_width() // 2, window.get_height() // 2))
        window.blit(timer_text, text_rect)  # Blit the text onto the window
        pygame.display.flip()
