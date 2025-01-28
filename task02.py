import time
from typing import Dict
import random

class ThrottlingRateLimiter:
    def __init__(self, min_interval: float = 10.0):        
        self.min_interval = min_interval
        self.last_message_time: Dict[str, float] = {}

    def can_send_message(self, user_id: str) -> bool:        
        current_time = time.time()
        last_time = self.last_message_time.get(user_id, 0)
        return current_time - last_time >= self.min_interval

    def record_message(self, user_id: str) -> bool:        
        if self.can_send_message(user_id):
            self.last_message_time[user_id] = time.time()
            return True
        return False

    def time_until_next_allowed(self, user_id: str) -> float:        
        current_time = time.time()
        last_time = self.last_message_time.get(user_id, 0)
        return max(0.0, self.min_interval - (current_time - last_time))

def test_throttling_limiter():    
    limiter = ThrottlingRateLimiter(min_interval=10.0)

    print("\n=== Симуляція потоку повідомлень (Throttling) ===")
    for message_id in range(1, 11):
        user_id = message_id % 5 + 1
        result = limiter.record_message(str(user_id))
        wait_time = limiter.time_until_next_allowed(str(user_id))
        print(f"Повідомлення   {message_id:2d} | Користувач  {user_id} | "
              f"{'\u2713' if result else f'\u00d7 (очікування  {wait_time:.1f}s)'}")
        time.sleep(random.uniform(0.1, 1.0))

    print("\nОчікуємо 4 секунди...")
    time.sleep(4)

    print("\n=== Нова серія повідомлень після очікування ===")
    for message_id in range(11, 21):
        user_id = message_id % 5 + 1
        result = limiter.record_message(str(user_id))
        wait_time = limiter.time_until_next_allowed(str(user_id))
        print(f"Повідомлення   {message_id:2d} | Користувач  {user_id} | "
              f"{'\u2713' if result else f'\u00d7 (очікування  {wait_time:.1f}s)'}")
        time.sleep(random.uniform(0.1, 1.0))

if __name__ == "__main__":
    test_throttling_limiter()
