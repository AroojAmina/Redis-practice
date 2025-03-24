class RateLimiter:
    def __init__(self, rate_limit):
        self.rate_limit = rate_limit
        self.last_called = 0

    def is_allowed(self):
        import time
        current_time = time.time()
        if current_time - self.last_called >= self.rate_limit:
            self.last_called = current_time
            return True
        return False

    def wait_if_not_allowed(self):
        import time
        while not self.is_allowed():
            time.sleep(0.1)