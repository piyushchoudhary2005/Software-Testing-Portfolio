# Test Plan: Sports Tournament Management System

## 1. Introduction
Test plan for the business logic of a sports tournament management system used by college or club organisers.

## 2. Application understanding
**Actors:** Admin/organiser, team manager, player, spectator.
**Core flow:** register user -> register team and players -> organiser creates tournament -> team entry approved -> fixtures generated -> matches played and scored -> points table published.

## 3. Scope
**In scope (modules):** M1 User registration, M2 Team and player registration, M3 Tournament creation, M4 Team approval, M5 Match lifecycle and scoring, M6 Standings, M7 Fixture generation.
**Out of scope:** UI look and feel, payment gateway internals, performance and load testing, security penetration testing.

## 4. Features to be tested and business rules
| Rule ID | Rule |
|---|---|
| BR-01 | Name 2-50 chars; valid email; password 8-20 chars with at least one digit and one uppercase letter |
| BR-02 | Team name 3-30 chars; 5-15 players; no duplicate players |
| BR-03 | Player age 12-45 inclusive |
| BR-04 | Tournament start before end; max teams even, 4-32; name required |
| BR-05 | Team approved only if fee paid, minimum players met and before deadline; unpaid but otherwise valid is PENDING_PAYMENT |
| BR-06 | Match states: SCHEDULED -> LIVE or CANCELLED; LIVE -> COMPLETED or ABANDONED; others terminal |
| BR-07 | Scores editable only while LIVE; goals non-negative |
| BR-08 | Win 3, draw 1, loss 0; rank by points, goal difference, goals for |
| BR-09 | Round-robin: n teams give n(n-1)/2 matches |

## 5. Test approach
| Technique | Applied to |
|---|---|
| Equivalence partitioning | M1, M3 |
| Boundary value analysis | M1, M2, M3 |
| Decision table | M4 |
| State transition | M5 |
| Scenario / error guessing | M6, M7, extra probes for defects |
| Automation | pytest, pytest-cov |
| Mutation testing | custom AST mutator (`mutation_test.py`) |

## 6. Entry and exit criteria
**Entry:** requirements (business rules) agreed; build available; test environment set up.
**Exit:** all planned test cases executed; 100% statement coverage; mutation score of at least 90%; all defects logged with severity.

## 7. Environment
Python 3.12, pytest, pytest-cov, GitHub for version control.

## 8. Deliverables
Test plan, test case design, execution log, defect reports, automation scripts, test summary report, screenshots, conclusion.

## 9. Roles
| Member | Responsibility |
|---|---|
| Piyush | _<fill: e.g. test design and automation>_ |
| _<member>_ | _<fill>_ |
| _<member>_ | _<fill>_ |

## 10. Risks
| Risk | Mitigation |
|---|---|
| Ambiguous business rules | Rules written down in section 4 and treated as the test oracle |
| Weak tests that pass everything | Mutation testing to measure test strength |
