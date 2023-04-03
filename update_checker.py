"""
RobotGUI
GitHub Update Checker
"""

import semantic_version
import requests


class UpdateChecker:
    def __init__(self, github: str, current: str) -> None:
        self.github = github
        self.current = current
        try:
            # Github API
            self.latest = requests.get(f"https://api.github.com/repos/{github}/releases/latest").json()["name"]
        except (requests.RequestException, KeyError):
            self.latest = "0.0.0"

    @property
    def newer_available(self) -> bool:
        return semantic_version.compare(self.latest, self.current) == 1 | 0
