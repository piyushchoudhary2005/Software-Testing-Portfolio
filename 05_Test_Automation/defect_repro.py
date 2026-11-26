"""Reproduces the defects documented in 04_Defect_Reports. Each line prints the observed (buggy) behaviour."""
from datetime import date
from sports_tms import *

def show(tag, f):
    try: print(tag, "->", f())
    except Exception as e: print(tag, "-> raises", type(e).__name__, e)

show("DEF-01 blank player names accepted", lambda: register_team("Warriors", ["A", "B", "C", " ", ""]))
show("DEF-02 team scheduled against itself", lambda: round_robin(["A", "A", "B"]))
m = Match("A", "B"); m.move_to("LIVE")
show("DEF-03 float goals accepted", lambda: (m.set_score(1.5, 0), m.score)[1])
show("DEF-04 negative goals corrupt standings", lambda: build_standings([("A", "B", -1, 0)])[0])
show("DEF-05 tournament in the past accepted", lambda: create_tournament("Cup", date(2020, 1, 1), date(2020, 1, 2), 8))
show("DEF-06 non-string team name crashes", lambda: register_team(12345, list("12345")))
