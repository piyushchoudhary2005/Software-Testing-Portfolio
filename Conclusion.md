# Conclusion

We tested the core rules of a Sports Tournament Management System across seven modules using equivalence partitioning, boundary value analysis, a decision table, state transition testing and scenario-based tests. All 71 automated test cases pass with 100% statement coverage.

Mutation testing was the most useful extra activity. The first suite scored only 64.3% even with high coverage, because many tests did not assert enough; after strengthening it the score reached 97.1%. Separate error-guessing probes found 6 validation defects that the specification-based tests missed, showing that coverage and passing tests alone do not prove quality.

We also tested the system through a website using Playwright in a real browser: 26 UI tests covering registration, teams, tournaments, the match lifecycle and standings. One of them reproduces defect DEF-01 end to end as an expected failure.

**Lessons learned**
1. Boundary values catch off-by-one errors cheaply, but only if the boundaries are all tested (both sides, both ends).
2. Coverage tells you what code ran, mutation score tells you whether the tests would notice a change.
3. Validation should be applied consistently across functions (negative goals were rejected in one place and accepted in another).

**Future work:** fix the six open defects and add regression tests for them, add cross-browser and Selenium runs, REST API tests with Postman, and add performance tests for large tournaments.
