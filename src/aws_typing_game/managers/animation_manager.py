"""
Animation manager for AWS Service Typing Game
"""

import time
from typing import Any, Dict, List, Tuple

import pygame


class Animation:
    """Base animation class"""

    def __init__(self, duration: float, easing: str = "linear"):
        self.duration = duration
        self.start_time = time.time()
        self.easing = easing
        self.finished = False

    def get_progress(self) -> float:
        """Get animation progress (0.0 to 1.0)"""
        elapsed = time.time() - self.start_time
        progress = min(elapsed / self.duration, 1.0)

        if progress >= 1.0:
            self.finished = True

        return self._apply_easing(progress)

    def _apply_easing(self, t: float) -> float:
        """Apply easing function to progress"""
        if self.easing == "ease_in":
            return t * t
        elif self.easing == "ease_out":
            return 1 - (1 - t) * (1 - t)
        elif self.easing == "ease_in_out" or self.easing == "bounce":
            if t < 0.5:
                return 2 * t * t
            else:
                return 1 - 2 * (1 - t) * (1 - t)
        else:  # linear
            return t


class FadeAnimation(Animation):
    """Fade in/out animation"""

    def __init__(
        self, start_alpha: int, end_alpha: int, duration: float, easing: str = "ease_in_out"
    ):
        super().__init__(duration, easing)
        self.start_alpha = start_alpha
        self.end_alpha = end_alpha

    def get_alpha(self) -> int:
        """Get current alpha value"""
        progress = self.get_progress()
        return int(self.start_alpha + (self.end_alpha - self.start_alpha) * progress)


class SlideAnimation(Animation):
    """Slide animation"""

    def __init__(
        self,
        start_pos: Tuple[int, int],
        end_pos: Tuple[int, int],
        duration: float,
        easing: str = "ease_out",
    ):
        super().__init__(duration, easing)
        self.start_pos = start_pos
        self.end_pos = end_pos

    def get_position(self) -> Tuple[int, int]:
        """Get current position"""
        progress = self.get_progress()
        x = int(self.start_pos[0] + (self.end_pos[0] - self.start_pos[0]) * progress)
        y = int(self.start_pos[1] + (self.end_pos[1] - self.start_pos[1]) * progress)
        return x, y


class ScaleAnimation(Animation):
    """Scale animation"""

    def __init__(
        self, start_scale: float, end_scale: float, duration: float, easing: str = "bounce"
    ):
        super().__init__(duration, easing)
        self.start_scale = start_scale
        self.end_scale = end_scale

    def get_scale(self) -> float:
        """Get current scale"""
        progress = self.get_progress()
        return self.start_scale + (self.end_scale - self.start_scale) * progress


class ColorAnimation(Animation):
    """Color transition animation"""

    def __init__(
        self,
        start_color: Tuple[int, int, int],
        end_color: Tuple[int, int, int],
        duration: float,
        easing: str = "linear",
    ):
        super().__init__(duration, easing)
        self.start_color = start_color
        self.end_color = end_color

    def get_color(self) -> Tuple[int, int, int]:
        """Get current color"""
        progress = self.get_progress()
        r = int(self.start_color[0] + (self.end_color[0] - self.start_color[0]) * progress)
        g = int(self.start_color[1] + (self.end_color[1] - self.start_color[1]) * progress)
        b = int(self.start_color[2] + (self.end_color[2] - self.start_color[2]) * progress)
        return r, g, b


class ParticleEffect:
    """Particle effect for typing feedback"""

    def __init__(self, x: int, y: int, color: Tuple[int, int, int], effect_type: str = "success"):
        self.particles = []
        self.creation_time = time.time()
        self.duration = 1.0
        self.x = x
        self.y = y
        self.color = color

        # Create particles based on effect type
        if effect_type == "success":
            self._create_success_particles()
        elif effect_type == "error":
            self._create_error_particles()
        elif effect_type == "typing":
            self._create_typing_particles()

    def _create_success_particles(self):
        """Create success effect particles"""
        import random

        for _ in range(15):
            particle = {
                "x": self.x + random.randint(-20, 20),
                "y": self.y + random.randint(-20, 20),
                "vx": random.uniform(-2, 2),
                "vy": random.uniform(-3, -1),
                "life": 1.0,
                "size": random.randint(2, 5),
            }
            self.particles.append(particle)

    def _create_error_particles(self):
        """Create error effect particles"""
        import random

        for _ in range(10):
            particle = {
                "x": self.x + random.randint(-15, 15),
                "y": self.y + random.randint(-15, 15),
                "vx": random.uniform(-1, 1),
                "vy": random.uniform(-2, 0),
                "life": 0.8,
                "size": random.randint(1, 3),
            }
            self.particles.append(particle)

    def _create_typing_particles(self):
        """Create typing effect particles"""
        import random

        for _ in range(5):
            particle = {
                "x": self.x + random.randint(-10, 10),
                "y": self.y + random.randint(-10, 10),
                "vx": random.uniform(-0.5, 0.5),
                "vy": random.uniform(-1, 0),
                "life": 0.5,
                "size": random.randint(1, 2),
            }
            self.particles.append(particle)

    def update(self):
        """Update particle positions and life"""
        dt = 1 / 60  # Assume 60 FPS
        for particle in self.particles[:]:
            particle["x"] += particle["vx"]
            particle["y"] += particle["vy"]
            particle["vy"] += 0.1  # Gravity
            particle["life"] -= dt / self.duration

            if particle["life"] <= 0:
                self.particles.remove(particle)

    def draw(self, surface):
        """Draw particles"""
        for particle in self.particles:
            alpha = int(255 * particle["life"])
            color = (*self.color, alpha)
            size = int(particle["size"] * particle["life"])
            if size > 0:
                # Create a surface with per-pixel alpha
                particle_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                pygame.draw.circle(particle_surface, color, (size, size), size)
                surface.blit(
                    particle_surface, (int(particle["x"] - size), int(particle["y"] - size))
                )

    def is_finished(self) -> bool:
        """Check if effect is finished"""
        return len(self.particles) == 0 or time.time() - self.creation_time > self.duration


class AnimationManager:
    """Manages all animations and effects in the game"""

    def __init__(self):
        self.animations: Dict[str, Animation] = {}
        self.particle_effects: List[ParticleEffect] = []
        self.screen_transition = None
        self.typing_feedback_enabled = True
        self.transition_surface = None

    def add_animation(self, name: str, animation: Animation):
        """Add a named animation"""
        self.animations[name] = animation

    def remove_animation(self, name: str):
        """Remove an animation"""
        if name in self.animations:
            del self.animations[name]

    def add_particle_effect(
        self, x: int, y: int, color: Tuple[int, int, int], effect_type: str = "success"
    ):
        """Add a particle effect"""
        effect = ParticleEffect(x, y, color, effect_type)
        self.particle_effects.append(effect)

    def start_screen_transition(self, transition_type: str = "fade", duration: float = 0.5):
        """Start a screen transition effect"""
        if transition_type == "fade":
            self.screen_transition = FadeAnimation(0, 255, duration / 2, "ease_in")
        elif transition_type == "slide_left":
            # Will be implemented with slide animation
            pass

    def update(self):
        """Update all animations"""
        # Update named animations
        finished_animations = []
        for name, animation in self.animations.items():
            animation.get_progress()  # Update progress
            if animation.finished:
                finished_animations.append(name)

        # Remove finished animations
        for name in finished_animations:
            del self.animations[name]

        # Update particle effects
        for effect in self.particle_effects[:]:
            effect.update()
            if effect.is_finished():
                self.particle_effects.remove(effect)

        # Update screen transition
        if self.screen_transition:
            self.screen_transition.get_progress()
            if self.screen_transition.finished:
                self.screen_transition = None

    def draw_effects(self, surface):
        """Draw all visual effects"""
        # Draw particle effects
        for effect in self.particle_effects:
            effect.draw(surface)

        # Draw screen transition
        if self.screen_transition:
            alpha = self.screen_transition.get_alpha()
            if alpha > 0:
                # Create transition overlay
                overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, alpha))
                surface.blit(overlay, (0, 0))

    def get_animated_value(self, name: str, default_value: Any) -> Any:
        """Get animated value by name"""
        if name not in self.animations:
            return default_value

        animation = self.animations[name]
        if isinstance(animation, FadeAnimation):
            return animation.get_alpha()
        elif isinstance(animation, SlideAnimation):
            return animation.get_position()
        elif isinstance(animation, ScaleAnimation):
            return animation.get_scale()
        elif isinstance(animation, ColorAnimation):
            return animation.get_color()

        return default_value

    def create_typing_feedback(self, x: int, y: int, is_correct: bool):
        """Create typing feedback effect"""
        if not self.typing_feedback_enabled:
            return

        if is_correct:
            color = (0, 255, 0)  # Green
            effect_type = "success"
        else:
            color = (255, 0, 0)  # Red
            effect_type = "error"

        self.add_particle_effect(x, y, color, effect_type)

    def create_score_popup(self, x: int, y: int, score: int):
        """Create score popup animation"""
        # Add slide and fade animation for score popup
        slide_anim = SlideAnimation((x, y), (x, y - 50), 1.0, "ease_out")
        fade_anim = FadeAnimation(255, 0, 1.0, "ease_in")

        self.add_animation(f"score_slide_{time.time()}", slide_anim)
        self.add_animation(f"score_fade_{time.time()}", fade_anim)

    def create_button_hover_effect(self, name: str):
        """Create button hover effect"""
        scale_anim = ScaleAnimation(1.0, 1.1, 0.2, "ease_out")
        self.add_animation(f"button_hover_{name}", scale_anim)

    def create_pulse_effect(self, name: str, duration: float = 1.0):
        """Create pulsing effect for elements"""
        # Create a repeating scale animation
        scale_anim = ScaleAnimation(1.0, 1.2, duration / 2, "ease_in_out")
        self.add_animation(f"pulse_{name}", scale_anim)

    def is_transitioning(self) -> bool:
        """Check if a screen transition is in progress"""
        return self.screen_transition is not None

    def clear_all_effects(self):
        """Clear all animations and effects"""
        self.animations.clear()
        self.particle_effects.clear()
        self.screen_transition = None
