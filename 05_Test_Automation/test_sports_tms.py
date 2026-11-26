from datetime import date
import pytest
from sports_tms import *

# ---- TC01-TC10: user registration (EP + BVA) ----
@pytest.mark.parametrize("name,email,pw,ok", [
    ("Rahul", "rahul@mail.com", "Passw0rdX", True),            # TC01 valid
    ("Ra", "rahul@mail.com", "Passw0rdX", True),               # TC02 name min boundary (2)
    ("R", "rahul@mail.com", "Passw0rdX", False),               # TC03 name below min
    ("A" * 50, "rahul@mail.com", "Passw0rdX", True),           # TC04 name max boundary
    ("A" * 51, "rahul@mail.com", "Passw0rdX", False),          # TC05 name above max
    ("Rahul", "rahul.mail.com", "Passw0rdX", False),           # TC06 email without @
    ("Rahul", "rahul@mail.com", "Pass0rd", False),             # TC07 password 7 chars
    ("Rahul", "rahul@mail.com", "Pass0rdX", True),             # TC08 password 8 chars (boundary)
    ("Rahul", "rahul@mail.com", "password1", False),           # TC09 no uppercase
    ("Rahul", "rahul@mail.com", "A" + "b1" * 10, False),       # TC10 password 21 chars
], ids=[f"TC{i:02d}" for i in range(1, 11)])
def test_register_user(name, email, pw, ok):
    if ok:
        assert register_user(name, email, pw)["email"] == email.lower()
    else:
        with pytest.raises(ValueError):
            register_user(name, email, pw)

def test_TC11_email_normalised_to_lowercase():
    assert register_user("Rahul", "Rahul@Mail.COM", "Passw0rdX")["email"] == "rahul@mail.com"

# ---- TC12-TC19: team registration ----
@pytest.mark.parametrize("n,ok", [(4, False), (5, True), (6, True), (14, True), (15, True), (16, False)],
                         ids=["TC12", "TC13", "TC14", "TC15", "TC16", "TC17"])
def test_player_count_bva(n, ok):
    players = [f"P{i}" for i in range(n)]
    if ok:
        assert register_team("Warriors", players)["team"] == "Warriors"
    else:
        with pytest.raises(ValueError):
            register_team("Warriors", players)

def test_TC18_duplicate_players_rejected():
    with pytest.raises(ValueError):
        register_team("Warriors", ["A", "B", "C", "D", "a"])

def test_TC19_team_name_too_short():
    with pytest.raises(ValueError):
        register_team("AB", list("12345"))

# ---- TC20-TC26: player age eligibility (BVA 12..45) ----
@pytest.mark.parametrize("age,ok", [(11, False), (12, True), (13, True), (44, True), (45, True), (46, False)],
                         ids=["TC20", "TC21", "TC22", "TC23", "TC24", "TC25"])
def test_player_age(age, ok):
    assert is_player_eligible(age) is ok

def test_TC26_age_non_integer():
    with pytest.raises(TypeError):
        is_player_eligible("twenty")

# ---- TC27-TC30: tournament creation ----
def test_TC27_valid_tournament():
    t = create_tournament("Inter-College Cup", date(2026, 12, 1), date(2026, 12, 10), 8)
    assert t["max_teams"] == 8

def test_TC28_start_equals_end_rejected():
    with pytest.raises(ValueError):
        create_tournament("Cup", date(2026, 12, 1), date(2026, 12, 1), 8)

@pytest.mark.parametrize("m,ok", [(2, False), (4, True), (7, False), (32, True), (34, False)],
                         ids=["TC29a", "TC29b", "TC29c", "TC29d", "TC29e"])
def test_max_teams(m, ok):
    if ok:
        create_tournament("Cup", date(2026, 12, 1), date(2026, 12, 5), m)
    else:
        with pytest.raises(ValueError):
            create_tournament("Cup", date(2026, 12, 1), date(2026, 12, 5), m)

def test_TC30_blank_name_rejected():
    with pytest.raises(ValueError):
        create_tournament("   ", date(2026, 12, 1), date(2026, 12, 5), 8)

# ---- TC31-TC38: decision table, team approval ----
@pytest.mark.parametrize("fee,players,deadline,expected", [
    (True, True, True, "APPROVED"),
    (False, True, True, "PENDING_PAYMENT"),
    (True, False, True, "REJECTED"),
    (False, False, True, "REJECTED"),
    (True, True, False, "REJECTED"),
    (False, True, False, "REJECTED"),
    (True, False, False, "REJECTED"),
    (False, False, False, "REJECTED"),
], ids=[f"TC{i}" for i in range(31, 39)])
def test_team_approval(fee, players, deadline, expected):
    assert team_approval(fee, players, deadline) == expected

# ---- TC39-TC45: match state transitions ----
@pytest.mark.parametrize("path,ok", [
    (["LIVE", "COMPLETED"], True),
    (["CANCELLED"], True),
    (["LIVE", "ABANDONED"], True),
    (["COMPLETED"], False),
    (["LIVE", "CANCELLED"], False),
    (["CANCELLED", "LIVE"], False),
    (["LIVE", "COMPLETED", "LIVE"], False),
], ids=[f"TC{i}" for i in range(39, 46)])
def test_match_transitions(path, ok):
    m = Match("A", "B")
    if ok:
        for s in path:
            m.move_to(s)
        assert m.status == path[-1]
    else:
        with pytest.raises(ValueError):
            for s in path:
                m.move_to(s)

def test_TC46_score_update_requires_live():
    m = Match("A", "B")
    with pytest.raises(ValueError):
        m.set_score(1, 0)

def test_TC47_negative_goals_rejected():
    m = Match("A", "B"); m.move_to("LIVE")
    with pytest.raises(ValueError):
        m.set_score(-1, 0)

def test_TC48_team_cannot_play_itself():
    with pytest.raises(ValueError):
        Match("A", "A")

# ---- TC49-TC53: standings ----
def test_TC49_win_draw_loss_points():
    t = {r["team"]: r for r in build_standings([("A", "B", 2, 0), ("A", "C", 1, 1)])}
    assert (t["A"]["Pts"], t["B"]["Pts"], t["C"]["Pts"]) == (4, 0, 1)

def test_TC50_goal_difference_tiebreak():
    res = [("A", "C", 3, 0), ("B", "D", 1, 0)]
    assert [r["team"] for r in build_standings(res)][:2] == ["A", "B"]

def test_TC51_goals_for_tiebreak_when_gd_equal():
    res = [("A", "C", 3, 1), ("B", "D", 2, 0)]
    assert build_standings(res)[0]["team"] == "A"

def test_TC52_empty_results():
    assert build_standings([]) == []

def test_TC53_played_counts():
    t = {r["team"]: r for r in build_standings([("A", "B", 0, 0), ("B", "A", 2, 1)])}
    assert t["A"]["P"] == 2 and t["B"]["P"] == 2 and t["B"]["Pts"] == 4

# ---- TC54-TC57: fixtures ----
@pytest.mark.parametrize("n,matches", [(2, 1), (4, 6), (8, 28)], ids=["TC54", "TC55", "TC56"])
def test_round_robin_count(n, matches):
    assert len(round_robin([f"T{i}" for i in range(n)])) == matches

def test_TC57_single_team_rejected():
    with pytest.raises(ValueError):
        round_robin(["A"])

# ---- Added after first mutation run (killing surviving mutants) ----
@pytest.mark.parametrize("n,ok", [(2, False), (3, True), (30, True), (31, False)], ids=["TC58", "TC59", "TC60", "TC61"])
def test_team_name_length_bva(n, ok):
    players = list("12345")
    if ok:
        assert register_team("T" * n, players)["team"] == "T" * n
    else:
        with pytest.raises(ValueError):
            register_team("T" * n, players)

def test_TC62_password_max_length_boundary():
    assert register_user("Rahul", "a@b.co", "Abcdefghij1234567890")["name"] == "Rahul"

def test_TC63_new_match_initial_state():
    m = Match("A", "B")
    assert m.status == "SCHEDULED" and m.score == (0, 0)

def test_TC64_negative_away_goals_rejected():
    m = Match("A", "B"); m.move_to("LIVE")
    with pytest.raises(ValueError):
        m.set_score(0, -1)

def test_TC65_zero_goals_allowed_and_stored():
    m = Match("A", "B"); m.move_to("LIVE"); m.set_score(0, 0); m.set_score(2, 1)
    assert m.score == (2, 1)

def test_TC66_full_row_values_home_win_away_win_draw():
    t = {r["team"]: r for r in build_standings([("A", "B", 3, 1), ("C", "A", 2, 0), ("B", "C", 1, 1)])}
    assert t["A"] == {"team": "A", "P": 2, "W": 1, "D": 0, "L": 1, "GF": 3, "GA": 3, "GD": 0, "Pts": 3}
    assert t["B"] == {"team": "B", "P": 2, "W": 0, "D": 1, "L": 1, "GF": 2, "GA": 4, "GD": -2, "Pts": 1}
    assert t["C"] == {"team": "C", "P": 2, "W": 1, "D": 1, "L": 0, "GF": 3, "GA": 1, "GD": 2, "Pts": 4}

def test_TC67_away_win_awards_points_to_away_team():
    t = {r["team"]: r for r in build_standings([("A", "B", 0, 2)])}
    assert t["B"]["W"] == 1 and t["B"]["Pts"] == 3 and t["A"]["L"] == 1 and t["A"]["Pts"] == 0
