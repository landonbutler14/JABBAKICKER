class Player:
    def __init__(self):
        self.credits = 0
        self.boot_level = 1
        self.kick_power = 1  # base credits per kick

    def kick(self):
        """Return how many credits this kick generates."""
        return self.kick_power

    def upgrade_boot(self):
        """Increase boot level and kick power."""
        cost = self.get_upgrade_cost()
        if self.credits >= cost:
            self.credits -= cost
            self.boot_level += 1
            self.kick_power += 1  # or scale exponentially
            return True
        return False

    def get_upgrade_cost(self):
        """Cost grows exponentially for idle-game feel."""
        return 10 * (self.boot_level ** 2)