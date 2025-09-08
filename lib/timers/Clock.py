class Clock:
    def __init__(self):
        self.start_time = None
        self._stop_flag = False
        self._thread = None

        # Configure all events here in one place
        self.events = [
            SpawnEvent("Lane creeps", LANE_CREEPS_SPAWN_FREQUENCY_IN_SECONDS, "sounds/lane_creeps_spawning.mp3", False),
            SpawnEvent("Forrest creeps", FORREST_CREEPS_SPAWN_FREQUENCY_IN_SECONDS, "sounds/forrest_creeps_spawning.mp3"),
            SpawnEvent("Runes", RUNE_SPAWN_FREQUENCY_IN_SECONDS, "sounds/runes_spawning.mp3"),
            SpawnEvent("Bounty runes", BOUNTY_RUNE_SPAWN_FREQUENCY_IN_SECONDS, "sounds/bounty_runes_spawning.mp3", False),
            SpawnEvent("Wisdom runes", WISDOM_RUNE_FREQUENCY_IN_SECONDS, "sounds/wisdom_runes_spawning.mp3"),
            SpawnEvent("Lotus", LOTUS_SPAWN_FREQUENCY_IN_SECONDS, "sounds/lotus_spawning.mp3"),
            SpawnEvent("Tormentor", TORMENTOR_SPAWN_FREQUENCY_IN_SECONDS, "sounds/tormentor_spawning.mp3"),
        ]

    def start(self):
        lib.logger.info("Starting clock.", 4)
        self.start_time = time.time()
        self._stop_flag = False
        self._thread = threading.Thread(target=self._check_loop, daemon=True)
        self._thread.start()
        lib.logger.success("Clock Started.", 1)

    def elapsed(self):
        if self.start_time is None:
            raise ValueError("Timer has not been started yet.")
        return round(time.time() - self.start_time)

    def get_time(self):
        total_seconds = self.elapsed()
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return hours, minutes, seconds, total_seconds

    def _check_loop(self):
        next_tick = time.time()
        interval = 0.4  # how often we check
        while not self._stop_flag:
            h, m, s, total_seconds = self.get_time()
            for event in self.events:
                if event.should_trigger(total_seconds, m):
                    event.trigger(total_seconds)

            # schedule next loop iteration precisely
            next_tick += interval
            sleep_time = max(0, next_tick - time.time())
            time.sleep(sleep_time)

    def stop(self):
        lib.logger.info("Stopping clock.", 4)
        self._stop_flag = True
        lib.logger.success("Clock stopped.", 1)

    def adjust_timer(self, seconds):
        """Increase or decrease the clock time by a number of seconds."""
        if self.start_time:
            self.start_time -= seconds  # moving start time backward/forward changes elapsed
