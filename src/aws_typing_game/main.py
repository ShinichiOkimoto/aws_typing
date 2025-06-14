#!/usr/bin/env python3
"""
AWS Service Typing Game

Main entry point for the AWS Service Typing Game.
A typing practice game featuring AWS service names with Japanese translations.
"""

import sys

import pygame

# Import from relative modules
from .core.config import AccessibilityConfig, AnimationConfig, GameConfig
from .core.game import Game
from .managers.accessibility_manager import AccessibilityManager
from .managers.animation_manager import AnimationManager
from .managers.audio_manager import AudioManager
from .managers.data_manager import DataManager
from .managers.font_manager import FontManager
from .managers.responsive_manager import ResponsiveManager
from .ui.ui_manager import UIManager


def main():
    """Main game function."""
    # Initialize pygame
    pygame.init()

    # Initialize responsive manager for screen sizing
    responsive_manager = ResponsiveManager()
    screen_width, screen_height = responsive_manager.get_screen_size()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption(GameConfig.WINDOW_TITLE)

    # Initialize managers
    font_manager = FontManager()
    data_manager = DataManager()
    audio_manager = AudioManager()
    animation_manager = AnimationManager()
    accessibility_manager = AccessibilityManager()

    # Initialize UI manager with dependencies
    ui_manager = UIManager(screen, font_manager)
    ui_manager.set_responsive_manager(responsive_manager)
    ui_manager.set_accessibility_manager(accessibility_manager)
    ui_manager.set_animation_manager(animation_manager)

    # Initialize game
    game = Game(data_manager)
    game.set_audio_manager(audio_manager)
    game.set_animation_manager(animation_manager)

    # Create audio folders (don't auto-start music)
    try:
        audio_manager.create_audio_folders()
        # BGM is off by default, user must enable it manually
    except Exception as e:
        print(f"Audio initialization warning: {e}")

    # Print startup information
    print("AWS Service Typing Game started")
    print(f"Screen size: {screen_width}x{screen_height}")
    print(f"Audio: {'Enabled' if audio_manager.audio_enabled else 'Disabled'}")
    print("Controls: F1=Color modes, F2=High contrast, F3=SFX toggle, F4=Music toggle")
    print("Press Space to start the game!")

    # Game loop
    clock = pygame.time.Clock()
    space_key_released = True
    ignore_next_space = False

    running = True
    while running:
        events = pygame.event.get()

        # Handle quit event
        for event in events:
            if event.type == pygame.QUIT:
                running = False

            # Handle accessibility navigation
            if AccessibilityConfig.ENABLE_KEYBOARD_NAVIGATION:
                nav_result = accessibility_manager.handle_navigation_input(event)
                if nav_result.startswith("activate_"):
                    audio_manager.play_menu_sound("select")

            # Handle space key release
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                space_key_released = True

            # Handle accessibility shortcuts
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:  # Toggle color blind mode
                    modes = ["normal", "protanopia", "deuteranopia", "tritanopia"]
                    current_mode = accessibility_manager.color_blind_mode
                    current_index = modes.index(current_mode)
                    next_mode = modes[(current_index + 1) % len(modes)]
                    accessibility_manager.set_color_blind_mode(next_mode)
                elif event.key == pygame.K_F2:  # Toggle high contrast
                    accessibility_manager.toggle_high_contrast()
                elif event.key == pygame.K_F3:  # Toggle audio
                    audio_manager.toggle_sfx()
                elif event.key == pygame.K_F4:  # Toggle music
                    audio_manager.toggle_music()
                    # Start or stop background music based on new state
                    if audio_manager.music_enabled and audio_manager.music_tracks:
                        audio_manager.start_background_music()
                    elif not audio_manager.music_enabled:
                        audio_manager.stop_background_music()

        # Handle state-specific events
        if game.game_state == "menu":
            # Get button rectangles for click detection
            button_rects = ui_manager.get_menu_button_rects(screen_width, screen_height)

            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and space_key_released:
                        game.reset_game()
                        game.game_state = "playing"
                        space_key_released = False
                        ignore_next_space = True
                        audio_manager.play_game_start_sound()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        mouse_pos = event.pos
                        if button_rects["sfx_button"].collidepoint(mouse_pos):
                            audio_manager.toggle_sfx()
                            audio_manager.play_menu_sound("select")
                        elif button_rects["music_button"].collidepoint(mouse_pos):
                            audio_manager.toggle_music()
                            audio_manager.play_menu_sound("select")
                            # Start or stop background music based on new state
                            if audio_manager.music_enabled and audio_manager.music_tracks:
                                audio_manager.start_background_music()
                            elif not audio_manager.music_enabled:
                                audio_manager.stop_background_music()
                        elif button_rects["start_button"].collidepoint(mouse_pos):
                            game.reset_game()
                            game.game_state = "playing"
                            audio_manager.play_game_start_sound()

        elif game.game_state == "playing":
            game.update(events, ignore_next_space)
            ignore_next_space = False

            # Update animations
            if AnimationConfig.ENABLE_ANIMATIONS:
                animation_manager.update()

        elif game.game_state == "game_over":
            game.handle_game_over_events(events)

        elif game.game_state == "service_info":
            game.handle_service_info_events(events)

        # Render current state
        if game.game_state == "menu":
            ui_manager.draw_menu(
                high_score=game.get_high_score(),
                sfx_enabled=audio_manager.sfx_enabled,
                music_enabled=audio_manager.music_enabled,
            )

        elif game.game_state == "playing":
            ui_manager.draw_game(
                current_word=game.current_word,
                typed_text=game.typed_text,
                service_name=game.current_service_name,
                score=game.score,
                mistakes=game.mistakes,
                remaining_time=game.get_remaining_time(),
                total_chars=game.total_chars,
                start_time=game.start_time,
            )

        elif game.game_state == "game_over":
            ui_manager.draw_game_over(
                score=game.score,
                high_score=game.get_high_score(),
                total_chars=game.total_chars,
                start_time=game.start_time,
                answered_services=game.answered_services,
                correct_chars=game.correct_chars,
                mistakes=game.mistakes,
            )

        elif game.game_state == "service_info":
            description, example_sentence, translation = game.get_service_info()
            ui_manager.draw_service_info(
                answered_services=game.answered_services,
                current_service_index=game.current_service_index,
                service_description=description,
                example_sentence=example_sentence,
                translation=translation,
            )

        # Draw animation effects
        if AnimationConfig.ENABLE_ANIMATIONS:
            animation_manager.draw_effects(screen)

        pygame.display.flip()
        clock.tick(GameConfig.TARGET_FPS)

    # Cleanup
    try:
        if audio_manager.audio_enabled:
            audio_manager.stop_background_music()
        pygame.quit()
        print("Game closed successfully")
    except Exception as e:
        print(f"Cleanup warning: {e}")
    finally:
        sys.exit()


if __name__ == "__main__":
    main()
