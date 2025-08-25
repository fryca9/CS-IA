from core.sessions.add_session import AddSession

class TimerLogic:
    def __init__(self, root, protocol, timer_ui):
      
        self.root = root
        self.protocol = protocol
        self.timer_ui = timer_ui

        # state
        self.current_set = 1
        self.current_rep = 1
        self.total_sets = protocol["Total Sets"]
        self.reps_per_set = protocol["Reps Per Set"]
        self.timer_mode = "READY"
        
        self.after_id = None
        self.is_running = False # is a countdown currently scheduled
        self.is_paused = False # is the countdown currently paused
        self.paused_state = None # (remaining, callback, self.timer_mode)
        self.current_remaining = None # remaining time for the current phase stored globally

    def _update_labels(self, remaining):
        self.timer_ui.update_labels(remaining, self.timer_mode, self.current_set, self.current_rep)

    # ---------- scheduling helpers ----------
    # Cancels any scheduled after(...) callback and sets after_id = None, is_running = False. Prevents from multiple timers.
    def _cancel_after(self):
        if self.after_id:
            self.timer_ui.cancel(self.after_id)
            self.after_id = None
        self.is_running = False

    def schedule_timer(self, remaining, callback):
        """
        Non-blocking countdown that won't spawn duplicates.
        Uses timer_ui.schedule/cancel wrappers.
        """
        # Cancel any existing scheduled countdown to avoid overlap
        self._cancel_after()
        self.is_paused = False
        self.paused_state = None
        self.is_running = True
        self.current_remaining = remaining

        def tick(remaining):
            # update labels for this remaining time
            self.current_remaining = remaining
            self._update_labels(remaining)
            if remaining > 0:
                # schedule next tick, store id
                self.after_id = self.timer_ui.schedule(tick, 1, remaining - 1)
            else:
                # done phase
                self.after_id = None
                self.is_running = False
                self.current_remaining = 0
                callback()

        # start ticking immediately
        tick(remaining)

    # ---------- flow control ----------
    def start_timer(self):
        # Prevent starting a second overlapping countdown
        if self.is_running and not self.is_paused:
            return

        # If paused, treat Start as Resume
        if self.is_paused and self.paused_state:
            self.resume_timer()
            return

        # normal fresh start
        if self.protocol["Delay Start"] > 0:
            self.timer_mode = "DELAY"
            self.schedule_timer(self.protocol["Delay Start"], self.start_set)
        else:
            self.start_set()

    def start_set(self):
        if self.current_set <= self.total_sets:
            self.current_rep = 1
            self.timer_mode = "WORK"
            self._update_labels(None)
            # start first rep
            self.start_rep()
        else:
            self.timer_mode = "DONE"
            self._update_labels(0)
            AddSession(self.root, protocol_name=self.protocol["Name"])  # show Add Session window

    def start_rep(self):
        # ensure no duplicate timers
        self.timer_mode = "WORK"
        self.schedule_timer(self.protocol["Hang Time"], self.after_rep)

    def after_rep(self):
        if self.current_rep < self.reps_per_set:
            self.timer_mode = "REST"
            self.schedule_timer(self.protocol["Rest Time"], self.next_rep)
        else:
            # last rep in set
            if self.current_set < self.total_sets:
                self.timer_mode = "REST BETWEEN SETS"
                self.schedule_timer(self.protocol["Rest Between Sets"], self.next_set)
            else:
                self.timer_mode = "DONE"
                self._update_labels(0)
                AddSession(self.root, protocol_name=self.protocol["Name"])  # show Add Session window

    def next_rep(self):
        self.current_rep += 1
        self._update_labels(None)
        self.start_rep()

    def next_set(self):
        self.current_set += 1
        self.current_rep = 1
        self._update_labels(None)
        self.start_set()

    # ---------- pause / resume / reset ----------
    def stop_timer(self):
        # Pause: cancel scheduled callback, store remaining + callback, show Reset/Resume
        if self.after_id:
            self.timer_ui.cancel(self.after_id)
        self.after_id = None
        self.is_running = False
        self.is_paused = True

        remaining = self.current_remaining if self.current_remaining is not None else 0

        # decide which callback to use when resuming based on mode
        if self.timer_mode == "DELAY":
            callback = self.start_set
        elif self.timer_mode == "WORK":
            callback = self.after_rep
        elif self.timer_mode == "REST":
            callback = self.next_rep
        elif self.timer_mode == "REST BETWEEN SETS":
            callback = self.next_set
        else:
            callback = lambda: None

        self.paused_state = (remaining, callback, self.timer_mode)

        # swap Start -> Resume, Stop -> Reset (show/hide)
        self.timer_ui.set_buttons_paused_state()
        self.timer_mode = "PAUSED"
        self._update_labels(remaining)

    def resume_timer(self):
        # Resume from paused state
        if not self.is_paused or not self.paused_state:
            return

        remaining, callback, previous_mode = self.paused_state
        self.timer_mode = previous_mode
        self.paused_state = None
        self.is_paused = False
        self.is_running = True
        # revert buttons back to normal
        self.timer_ui.set_buttons_default()
        # schedule countdown where left off
        self._update_labels(remaining)
        self.schedule_timer(remaining, callback)

    def reset_timer(self):
        # stop everything and reset to initial protocol state
        self._cancel_after()
        self.is_paused = False
        self.paused_state = None

        self.current_set = 1
        self.current_rep = 1
        self.timer_mode = "PRESS START"
        self._update_labels(None)
        # revert buttons
        self.timer_ui.set_buttons_default()

    # ---------- navigation helpers ----------
    def next_round(self):
        # cancel current countdown and jump forward
        self._cancel_after()
        # quick logic: advance rep or set and start rep
        if self.current_rep < self.reps_per_set:
            self.current_rep += 1
        else:
            if self.current_set < self.total_sets:
                self.current_set += 1
                self.current_rep = 1
        self._update_labels(None)
        self.start_rep()

    def previous_round(self):
        # cancel current countdown and go backward
        self._cancel_after()
        if self.current_rep > 1:
            self.current_rep -= 1
        elif self.current_set > 1:
            self.current_set -= 1
            self.current_rep = self.reps_per_set
        self._update_labels(None)
        self.start_rep()

# previous button should disappear on first rep/set and delay
# next button should disappear on last rep/set
# maybe add countdown signal later
