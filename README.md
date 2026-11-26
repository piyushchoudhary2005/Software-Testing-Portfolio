# Software-Testing-Portfolio

| | |
|---|---|
| **Subject** | Software Testing (Other Component, 20 marks) |
| **Application under test** | Sports Tournament Management System |
| **Institution** | M.S. Ramaiah Institute of Technology, Bengaluru, B.Tech Information Science & Engineering |
| **Team member** | Piyush (USN 1MS23IS089) |
| **Other team members** | _<name, USN>_ , _<name, USN>_ |
| **Faculty** | _<faculty name>_ |

## Objectives
1. Understand the modules and business rules of a sports tournament management system.
2. Plan testing and design test cases with equivalence partitioning, boundary value analysis, decision tables and state transition testing.
3. Execute the tests, record actual results and document defects.
4. Automate the suite with pytest and measure its strength with coverage and mutation testing.

## Project description
The Sports Tournament Management System lets organisers register users, teams and players, create tournaments, approve team entries, schedule matches, record scores and publish points tables. Its core business rules are implemented in `05_Test_Automation/sports_tms.py`, which is the system under test.

## Modules tested
| # | Module | Technique |
|---|---|---|
| M1 | User registration | EP + BVA |
| M2 | Team and player registration, age eligibility | BVA |
| M3 | Tournament creation | EP + BVA |
| M4 | Team approval | Decision table |
| M5 | Match lifecycle and scoring | State transition |
| M6 | Points table / standings | Scenario-based |
| M7 | Fixture generation | Scenario-based |

## Headline results
| Metric | Result |
|---|---|
| Unit-level test cases executed | 71 (71 passed) |
| Browser (UI) tests on the website | 26 (25 passed, 1 expected failure for open defect DEF-01) |
| Statement coverage | 100% (82/82) |
| Mutation score | 97.1% (68 of 70 mutants killed; the 2 survivors are equivalent mutants) |
| Defects found | 6 (see `04_Defect_Reports`), all still open |

## Testing activities done (requirement: at least four)
1. Test plan, 2. test case design with techniques, 3. test execution, 4. defect reporting, 5. test execution summary, 6. **additional activities: test automation (pytest) + coverage + mutation testing, and end-to-end website testing with Playwright** (`08_Web_UI_Testing`).

## How to run
```bash
cd 05_Test_Automation
pip install -r requirements.txt
pytest -v --cov=sports_tms --cov-report=term-missing
python mutation_test.py     # mutation testing
python defect_repro.py      # reproduces the open defects

# website tests
cd ../08_Web_UI_Testing
pip install -r requirements.txt && python -m playwright install chromium
pytest test_ui.py -v
```

## Repository structure
```
README.md
01_Test_Plan/            Test_Plan.md
02_Test_Case_Design/     Test_Case_Design.md
03_Test_Execution/       Test_Execution_Log.md
04_Defect_Reports/       Defect_Reports.md
05_Test_Automation/      sports_tms.py, test_sports_tms.py, mutation_test.py, defect_repro.py
06_Test_Reports/         Test_Execution_Summary.md, junit.xml, coverage_html/, mutation_results.json
07_Screenshots/          ui_*.png (auto-captured from the website tests), README.md
08_Web_UI_Testing/       webapp/app.py (Flask website), test_ui.py (Playwright), README.md
Conclusion.md
```
