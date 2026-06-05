from collections import deque


TOKA = "Toka od celika"
VINO = "Mesina rujnog vina"
TOPUZ = "Topuz"
SARAC = "Sarac"
BLAGO = "Tri tovara blaga"

RELIC_CYCLE = [
    TOKA,
    VINO,
    TOPUZ,
    SARAC,
    BLAGO,
]

RELIC_ROAD_CAPACITY = 5


def create_relic_road():
    return deque(maxlen=RELIC_ROAD_CAPACITY)


def next_relic(cycle_index):
    new_relic = RELIC_CYCLE[cycle_index]
    next_index = (cycle_index + 1) % len(RELIC_CYCLE)
    return new_relic, next_index


def add_relic_to_front(relic_road, new_relic):
    relic_road.appendleft(new_relic)


def take_front_relic(relic_road):
    if not relic_road:
        return None
    return relic_road.popleft()


def take_rear_relic(relic_road):
    if not relic_road:
        return None
    return relic_road.pop()
