"""Sports Tournament Management System - core business logic (system under test).

Modules: user registration, team registration, player eligibility,
tournament creation, team approval, match lifecycle, standings, fixtures.
"""
import re

EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


# ---------- Module 1: User registration ----------
def register_user(name, email, password):
    name = (name or "").strip()
    if not 2 <= len(name) <= 50:
        raise ValueError("name must be 2-50 characters")
    if not EMAIL_RE.match(email or ""):
        raise ValueError("invalid email")
    if not 8 <= len(password or "") <= 20:
        raise ValueError("password must be 8-20 characters")
    if not any(c.isdigit() for c in password) or not any(c.isupper() for c in password):
        raise ValueError("password needs a digit and an uppercase letter")
    return {"name": name, "email": email.lower()}


# ---------- Module 2: Team and player registration ----------
def register_team(team_name, players):
    team_name = (team_name or "").strip()
    if not 3 <= len(team_name) <= 30:
        raise ValueError("team name must be 3-30 characters")
    if not 5 <= len(players) <= 15:
        raise ValueError("team needs 5-15 players")
    if len(set(p.lower() for p in players)) != len(players):
        raise ValueError("duplicate player names")
    return {"team": team_name, "players": list(players)}


def is_player_eligible(age):
    if not isinstance(age, int):
        raise TypeError("age must be an integer")
    return 12 <= age <= 45


# ---------- Module 3: Tournament creation ----------
def create_tournament(name, start, end, max_teams):
    if not (name or "").strip():
        raise ValueError("tournament name required")
    if not start < end:
        raise ValueError("start date must be before end date")
    if not 4 <= max_teams <= 32 or max_teams % 2:
        raise ValueError("max_teams must be even and between 4 and 32")
    return {"name": name.strip(), "start": start, "end": end, "max_teams": max_teams}


# ---------- Module 4: Team approval (decision table) ----------
def team_approval(fee_paid, min_players_met, before_deadline):
    if not before_deadline:
        return "REJECTED"
    if fee_paid and min_players_met:
        return "APPROVED"
    if min_players_met and not fee_paid:
        return "PENDING_PAYMENT"
    return "REJECTED"


# ---------- Module 5: Match lifecycle (state machine) ----------
TRANSITIONS = {
    "SCHEDULED": {"LIVE", "CANCELLED"},
    "LIVE": {"COMPLETED", "ABANDONED"},
    "COMPLETED": set(),
    "CANCELLED": set(),
    "ABANDONED": set(),
}


class Match:
    def __init__(self, home, away):
        if home == away:
            raise ValueError("a team cannot play itself")
        self.home, self.away = home, away
        self.status = "SCHEDULED"
        self.score = (0, 0)

    def move_to(self, new_status):
        if new_status not in TRANSITIONS[self.status]:
            raise ValueError(f"illegal transition {self.status} -> {new_status}")
        self.status = new_status

    def set_score(self, home_goals, away_goals):
        if self.status != "LIVE":
            raise ValueError("score can only be updated for a LIVE match")
        if home_goals < 0 or away_goals < 0:
            raise ValueError("goals cannot be negative")
        self.score = (home_goals, away_goals)


# ---------- Module 6: Standings ----------
def build_standings(results):
    """results: iterable of (home, away, home_goals, away_goals) for completed matches."""
    table = {}

    def row(t):
        return table.setdefault(t, {"team": t, "P": 0, "W": 0, "D": 0, "L": 0,
                                    "GF": 0, "GA": 0, "GD": 0, "Pts": 0})
    for home, away, hg, ag in results:
        h, a = row(home), row(away)
        h["P"] += 1; a["P"] += 1
        h["GF"] += hg; h["GA"] += ag
        a["GF"] += ag; a["GA"] += hg
        if hg > ag:
            h["W"] += 1; a["L"] += 1; h["Pts"] += 3
        elif hg < ag:
            a["W"] += 1; h["L"] += 1; a["Pts"] += 3
        else:
            h["D"] += 1; a["D"] += 1; h["Pts"] += 1; a["Pts"] += 1
    for r in table.values():
        r["GD"] = r["GF"] - r["GA"]
    return sorted(table.values(), key=lambda r: (-r["Pts"], -r["GD"], -r["GF"], r["team"]))


# ---------- Module 7: Fixture generation ----------
def round_robin(teams):
    teams = list(teams)
    if len(teams) < 2:
        raise ValueError("need at least 2 teams")
    return [(teams[i], teams[j]) for i in range(len(teams)) for j in range(i + 1, len(teams))]
