"""Single-process demo deployment boundary; never reads request bodies or secrets."""
import os
import time
from collections import deque
from dataclasses import dataclass
from urllib.parse import urlsplit

ANALYSIS_PATHS = frozenset({'/api/read', '/api/extract', '/api/explain'})


@dataclass(frozen=True)
class DeploymentPolicy:
    enabled: bool = False
    origin: str = ''
    per_minute: int = 30
    per_hour: int = 240
    concurrent: int = 1

    @classmethod
    def from_environment(cls):
        enabled = os.environ.get('APP_ENV') == 'production' or os.environ.get('RENDER') == 'true'
        if not enabled:
            return cls()
        origin = os.environ.get('PUBLIC_ORIGIN') or os.environ.get('RENDER_EXTERNAL_URL', '')
        parsed = urlsplit(origin)
        if (parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password
                or parsed.path or parsed.query or parsed.fragment or origin.endswith('/')):
            raise ValueError('Production requires one HTTPS PUBLIC_ORIGIN without a path or trailing slash.')
        return cls(True, origin)


class AnalysisBudget:
    """One global budget across all analysis endpoints, with no client identifiers.

    Single Uvicorn worker required. Counters reset on restart and are not a dollar
    spend cap. Deliberately do not trust forwarded-IP headers as a rate-limit key.
    """
    def __init__(self, policy, clock=time.monotonic):
        self.policy, self.clock = policy, clock
        self.minute, self.hour = deque(), deque()
        self.active = 0

    def acquire(self):
        now = self.clock()
        for queue, window in ((self.minute, 60), (self.hour, 3600)):
            while queue and queue[0] <= now - window:
                queue.popleft()
        if (len(self.minute) >= self.policy.per_minute or
                len(self.hour) >= self.policy.per_hour or
                self.active >= self.policy.concurrent):
            return False
        self.minute.append(now)
        self.hour.append(now)
        self.active += 1
        return True

    def release(self):
        self.active -= 1
