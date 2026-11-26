# Test Case Design

Test IDs match the automated tests in `05_Test_Automation/test_sports_tms.py`.

## 1. Equivalence partitioning and BVA: user registration (BR-01)
| Input | Valid partition | Invalid partitions |
|---|---|---|
| Name length | 2-50 | 0-1, 51+ |
| Email | `local@domain.tld` | no `@`, missing domain |
| Password | 8-20 chars, digit + uppercase | under 8, over 20, no digit, no uppercase |

| ID | Name | Email | Password | Expected |
|---|---|---|---|---|
| TC01 | Rahul | rahul@mail.com | Passw0rdX | Accept |
| TC02 | 2-char name | valid | valid | Accept (min boundary) |
| TC03 | 1-char name | valid | valid | Reject |
| TC04 | 50-char name | valid | valid | Accept (max boundary) |
| TC05 | 51-char name | valid | valid | Reject |
| TC06 | Rahul | rahul.mail.com | valid | Reject |
| TC07 | Rahul | valid | 7 chars | Reject |
| TC08 | Rahul | valid | 8 chars | Accept (min boundary) |
| TC09 | Rahul | valid | no uppercase | Reject |
| TC10 | Rahul | valid | 21 chars | Reject |
| TC11 | Rahul | Rahul@Mail.COM | valid | Accept, email stored lowercase |
| TC62 | Rahul | valid | 20 chars | Accept (max boundary) |

## 2. BVA: team and player registration (BR-02, BR-03)
| ID | Input | Expected |
|---|---|---|
| TC12 / TC13 / TC14 | 4 / 5 / 6 players | Reject / Accept / Accept |
| TC15 / TC16 / TC17 | 14 / 15 / 16 players | Accept / Accept / Reject |
| TC18 | duplicate player (case-insensitive) | Reject |
| TC19 | team name of 2 chars | Reject |
| TC58-TC61 | team name 2 / 3 / 30 / 31 chars | Reject / Accept / Accept / Reject |
| TC20-TC25 | age 11 / 12 / 13 / 44 / 45 / 46 | Reject / Accept / Accept / Accept / Accept / Reject |
| TC26 | age "twenty" | TypeError |

## 3. EP and BVA: tournament creation (BR-04)
| ID | Input | Expected |
|---|---|---|
| TC27 | valid dates, 8 teams | Accept |
| TC28 | start = end | Reject |
| TC29a-e | max teams 2 / 4 / 7 / 32 / 34 | Reject / Accept / Reject (odd) / Accept / Reject |
| TC30 | blank name | Reject |

## 4. Decision table: team approval (BR-05)
| Rule | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 |
|---|---|---|---|---|---|---|---|---|
| Fee paid | T | F | T | F | T | F | T | F |
| Min players met | T | T | F | F | T | T | F | F |
| Before deadline | T | T | T | T | F | F | F | F |
| **Outcome** | APPROVED | PENDING_PAYMENT | REJECTED | REJECTED | REJECTED | REJECTED | REJECTED | REJECTED |
| Test ID | TC31 | TC32 | TC33 | TC34 | TC35 | TC36 | TC37 | TC38 |

## 5. State transition: match lifecycle (BR-06, BR-07)
```
SCHEDULED --> LIVE --> COMPLETED
    |           |
    v           v
CANCELLED   ABANDONED
```
| ID | Path | Expected |
|---|---|---|
| TC39 | SCHEDULED -> LIVE -> COMPLETED | Valid |
| TC40 | SCHEDULED -> CANCELLED | Valid |
| TC41 | SCHEDULED -> LIVE -> ABANDONED | Valid |
| TC42 | SCHEDULED -> COMPLETED | Invalid |
| TC43 | SCHEDULED -> LIVE -> CANCELLED | Invalid |
| TC44 | CANCELLED -> LIVE | Invalid |
| TC45 | COMPLETED -> LIVE | Invalid |
| TC46 | set score while SCHEDULED | Reject |
| TC47 / TC64 | negative home / away goals | Reject |
| TC48 | team vs itself | Reject |
| TC63 | new match | SCHEDULED, score 0-0 |
| TC65 | set 0-0 then 2-1 | Score stored as 2-1 |

## 6. Scenario-based: standings and fixtures (BR-08, BR-09)
| ID | Scenario | Expected |
|---|---|---|
| TC49 | win and draw | 3 pts for winner, 1 each for draw |
| TC50 | equal points, different goal difference | higher GD ranks first |
| TC51 | equal points and GD, different goals for | higher GF ranks first |
| TC52 | no results | empty table |
| TC53 | same pair plays twice | P = 2 for both |
| TC66 | three-match table | full W/D/L/GF/GA/GD/Pts rows verified |
| TC67 | away win | points go to away team |
| TC54-TC56 | 2 / 4 / 8 teams | 1 / 6 / 28 fixtures |
| TC57 | 1 team | Reject |

## 7. Exploratory / error-guessing probes (led to defects)
Blank player names, duplicate team names in fixtures, float and negative goals, past-dated tournament, non-string team name. See `05_Test_Automation/defect_repro.py`.
