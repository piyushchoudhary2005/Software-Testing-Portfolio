# Defect Reports

Found by error-guessing probes after the 61-case suite passed. Reproduce all with `python 05_Test_Automation/defect_repro.py` (output saved in `06_Test_Reports/defect_repro_output.txt`). Status of all defects: **Open**.

| ID | Module | Summary | Severity | Priority |
|---|---|---|---|---|
| DEF-01 | M2 Team registration | Blank or empty player names accepted | Medium | Medium |
| DEF-02 | M7 Fixtures | Duplicate team names produce a team playing itself | High | High |
| DEF-03 | M5 Scoring | Non-integer goals (1.5) accepted | Medium | Medium |
| DEF-04 | M6 Standings | Negative goals accepted and corrupt GA/GD | High | High |
| DEF-05 | M3 Tournament | Tournament with dates in the past accepted | Low | Medium |
| DEF-06 | M2 Team registration | Non-string team name crashes with AttributeError instead of a validation error | Low | Low |

---
### DEF-01 Blank player names accepted
- **Steps:** `register_team("Warriors", ["A","B","C"," ",""])`
- **Expected:** ValueError, every player needs a non-blank name.
- **Actual:** team created with players `['A','B','C',' ','']`.
- **Suggested fix:** reject any player where `not p.strip()`.

### DEF-02 Team plays itself in generated fixtures
- **Steps:** `round_robin(["A","A","B"])`
- **Expected:** ValueError for duplicate team names (BR-09 assumes distinct teams).
- **Actual:** `[('A','A'),('A','B'),('A','B')]`, so a team is scheduled against itself and A-B twice. `Match("A","A")` is correctly rejected elsewhere, so the guard is missing here.
- **Suggested fix:** check `len(set(teams)) == len(teams)`.

### DEF-03 Float goals accepted
- **Steps:** `m = Match("A","B"); m.move_to("LIVE"); m.set_score(1.5, 0)`
- **Expected:** reject non-integer goals.
- **Actual:** score stored as `(1.5, 0)`.
- **Suggested fix:** type-check `int` in `set_score`.

### DEF-04 Negative goals corrupt standings
- **Steps:** `build_standings([("A","B",-1,0)])`
- **Expected:** reject negative goals, as `Match.set_score` does (BR-07).
- **Actual:** B gets GA = -1, GD = +1 and 3 points although it conceded nothing; A shows GF = -1.
- **Suggested fix:** validate goals in `build_standings`.

### DEF-05 Past-dated tournament accepted
- **Steps:** `create_tournament("Cup", date(2020,1,1), date(2020,1,2), 8)`
- **Expected:** to be confirmed with the product owner; a new tournament normally cannot start in the past.
- **Actual:** accepted.
- **Note:** BR-04 does not currently forbid this, so this may be a requirements gap rather than a code bug.

### DEF-06 Unhandled exception on non-string team name
- **Steps:** `register_team(12345, list("12345"))`
- **Expected:** ValueError or TypeError with a clear message.
- **Actual:** `AttributeError: 'int' object has no attribute 'strip'`.
