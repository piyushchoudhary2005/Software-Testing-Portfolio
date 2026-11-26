# Test Execution Summary

| Item | Value |
|---|---|
| Application | Sports Tournament Management System (business logic) |
| Date | 2026-11-24 |
| Tools | Python 3.12, pytest, pytest-cov, custom AST mutation tester |
| Test cases executed | 71 |
| Passed / Failed | 71 / 0 |
| Statement coverage | 100% (82 of 82 statements) |
| Mutants generated / killed | 70 / 68 (97.1%) |
| Defects logged | 6 (2 high, 2 medium, 2 low), all open |

## Test coverage by module
| Module | Technique | Tests |
|---|---|---|
| M1 User registration | EP + BVA | 12 |
| M2 Team, player | BVA | 19 |
| M3 Tournament | EP + BVA | 8 |
| M4 Approval | Decision table | 8 |
| M5 Match lifecycle | State transition | 13 |
| M6 Standings | Scenario | 7 |
| M7 Fixtures | Scenario | 4 |

## Mutation testing
First run: 70 mutants, 45 killed (64.3%). The 25 survivors showed that team-name boundaries, password max length, initial match state, away-side negative goals and several standings fields were not asserted. Tests TC58-TC67 were added; the second run killed 68 of 70 (97.1%).
The two survivors are equivalent mutants: `max_teams <= 32` -> `<= 33` (33 is odd and already rejected by the even check), and the initial `"GD": 0` value, which is overwritten before use.

## Website (UI) testing
The business logic is exposed through a Flask website (`08_Web_UI_Testing/webapp`) and tested in Chromium with Playwright: 26 tests, 25 passed, 1 expected failure (UI08, which reproduces DEF-01 through the browser). Results: `ui_junit.xml`; screenshots: `../07_Screenshots/ui_*.png`; case list: `../08_Web_UI_Testing/README.md`.

## Observations
- The suite passes fully, yet error-guessing found 6 defects in input validation that the specification-driven tests did not cover. Passing tests and 100% coverage do not mean the validation is complete.
- Defects cluster around input type and value checks that are inconsistent between functions (DEF-03, DEF-04).

## Evidence files
`junit.xml`, `coverage_html/index.html`, `mutation_results.json`, `defect_repro_output.txt`, `../03_Test_Execution/Test_Execution_Log.md`.
