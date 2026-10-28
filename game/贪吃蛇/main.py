"""贪吃蛇启动入口。"""

import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from game.贪吃蛇.game import SnakeGame


def main():
    SnakeGame().run()


if __name__ == "__main__":
    main()
