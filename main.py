import tkinter as tk
import threading

import settings
from lib.timers.Clock import Clock, SpawnEvent
from playsound3 import playsound
import lib.logger


class GUIEvent(SpawnEvent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.play_sound = True  # default enabled
        self.margin_of_safety = False  # new flag

    def trigger(self, total_seconds):
        """Trigger event with GUI-controlled sound toggle."""
        self.last_triggered = total_seconds
        lib.logger.info(f"{self.name} spawned", 4)

        if self.play_sound:
            threading.Thread(target=playsound, args=(self.sound_path,), daemon=True).start()


class ClockGUI:
    def __init__(self, root):
        self.root = root
        self.root.title(settings.APP_NAME)
        self.root.geometry("700x650")

        # Replace Clock's events with GUI-aware events
        self.clock = Clock()
        self.clock.events = [
            GUIEvent(e.name, e.frequency, e.sound_path, e.require_nonzero_minute)
            for e in self.clock.events
        ]

        # Mapping: event name -> (label, sound_var, margin_var, event)
        self.widgets = {}

        # Track whether clock is running
        self.clock_running = False

        # Build UI
        self.build_ui()

        # Timer display
        self.timer_var = tk.StringVar(value="00:00:00")
        self.timer_label = tk.Label(
            self.root, textvariable=self.timer_var,
            font=("Arial", 16, "bold"), fg="black"
        )
        self.timer_label.pack(pady=10)

    def build_ui(self):
        """Create lights, checkboxes, and start/reset buttons."""
        controls_frame = tk.Frame(self.root)
        controls_frame.pack(pady=15)

        # Start button
        start_btn = tk.Button(
            controls_frame, text="Start Clock", font=("Arial", 14, "bold"),
            command=self.start_clock, bg="green", fg="white"
        )
        start_btn.pack(side="left", padx=10)

        # Reset button
        reset_btn = tk.Button(
            controls_frame, text="Reset Clock", font=("Arial", 14, "bold"),
            command=self.reset_clock, bg="red", fg="white"
        )
        reset_btn.pack(side="left", padx=10)

        # Frame for events
        events_frame = tk.Frame(self.root)
        events_frame.pack(pady=10)

        for i, event in enumerate(self.clock.events):
            frame = tk.Frame(events_frame)
            frame.grid(row=i, column=0, sticky="w", padx=10, pady=5)

            # Light label
            label = tk.Label(
                frame,
                text=event.name,
                width=20,
                height=2,
                bg="gray",
                fg="white",
                font=("Arial", 12, "bold")
            )
            label.pack(side="left", padx=10)

            # Checkbox for sound toggle
            sound_var = tk.BooleanVar(value=True)
            checkbox_sound = tk.Checkbutton(frame, text="Sound", variable=sound_var)
            checkbox_sound.pack(side="left")

            # Checkbox for margin of safety
            margin_var = tk.BooleanVar(value=True)
            checkbox_margin = tk.Checkbutton(frame, text="Margin of Safety", variable=margin_var)
            checkbox_margin.pack(side="left")

            self.widgets[event.name] = (label, sound_var, margin_var, event)

    def start_clock(self):
        """Start the game clock when button is pressed."""
        if not self.clock_running:
            threading.Thread(target=self.clock.start, daemon=True).start()
            self.clock_running = True
            self.poll_events()
            self.update_timer()

    def reset_clock(self):
        """Stop the clock and reset timer + events."""
        if self.clock_running:
            self.clock.stop()
            self.clock_running = False

        # Reset start time and all events
        self.clock.start_time = None
        for event in self.clock.events:
            event.last_triggered = None

        # Reset timer display
        self.timer_var.set("00:00:00")

        # Reset all lights to gray
        for label, _, _, _ in self.widgets.values():
            label.config(bg="gray")

    def update_timer(self):
        """Update the displayed clock time."""
        if not self.clock_running:
            return
        try:
            h, m, s, _ = self.clock.get_time()
            self.timer_var.set(f"{h:02}:{m:02}:{s:02}")
        except ValueError:
            self.timer_var.set("00:00:00")
        self.root.after(1000, self.update_timer)

    def poll_events(self):
        """Check if events triggered recently and flash lights."""
        if not self.clock_running:
            return

        total_seconds = self.clock.elapsed() if self.clock.start_time else 0

        for name, (label, sound_var, margin_var, event) in self.widgets.items():
            # Update event's flags from checkboxes
            event.play_sound = sound_var.get()
            event.margin_of_safety = margin_var.get()

            # Flash earlier if margin of safety enabled (orange)
            if event.margin_of_safety and event.frequency > 5:
                if (total_seconds + 5) % event.frequency == 0 and event.last_triggered != total_seconds + 5:
                    self.flash_light(label, "orange")

            # Flash at real trigger time (red)
            if event.last_triggered == total_seconds:  # Just triggered
                self.flash_light(label, "red")

        # Re-run every 200ms
        self.root.after(200, self.poll_events)

    def flash_light(self, widget, color):
        """Flash the widget background with a given color."""
        def toggle_color(count=4):
            if count > 0:
                current_color = widget.cget("bg")
                new_color = color if current_color == "gray" else "gray"
                widget.config(bg=new_color)
                self.root.after(200, toggle_color, count - 1)
            else:
                widget.config(bg="gray")  # Reset

        toggle_color()


def main():
    root = tk.Tk()
    app = ClockGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()