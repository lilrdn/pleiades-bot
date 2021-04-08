from dialogic import SOURCES

from core.dm import csc, Pr, PTurn


@csc.add_handler(priority=Pr.CRITICAL)
def log_polylog(turn: PTurn):
    if turn.ctx.source != SOURCES.VK:
        return
    # todo: finish it

