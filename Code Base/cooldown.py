# cooldown.py
from collections import deque

class CooldownManager:
    def __init__(self, max_size=20):
        self.cooldown_list = deque(maxlen=max_size)

    def add_song(self, song):
        """Add a song to the cooldown list."""
        if song not in self.cooldown_list:
            self.cooldown_list.append(song)
            return True
        return False

    def is_on_cooldown(self, song):
        """Check if a song is in the cooldown list."""
        return song in self.cooldown_list

    def get_cooldown_list(self):
        """Return the current cooldown list."""
        return list(self.cooldown_list)
