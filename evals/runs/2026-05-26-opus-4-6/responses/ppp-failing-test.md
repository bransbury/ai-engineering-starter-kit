# Response for ppp-failing-test

Read skill [ppp](file:///Users/mabr/.agents/skills/ppp/SKILL.md?vscodeLinkType%3Dskill#1-1), lines 1 to 100

Read skill [ppp](file:///Users/mabr/.agents/skills/ppp/SKILL.md?vscodeLinkType%3Dskill#101-101), lines 101 to 200

I see the issue. The prompt contains placeholder text (`<insert command>` and `<insert error>`) — there's no actual failing test command or error output to diagnose.

---

**Current phase: Blocked**

I can't proceed with diagnosing a failing test because the input is incomplete. The command and error fields contain placeholder text (`<insert command>` and `<insert error>`).

To move forward I need:

1. **The test command** — e.g. `npm test`, `pytest tests/foo.py`, `go test repos.`
2. **The error output** — the actual stack trace or assertion failure

Choose an option:

1. Paste the failing command and error output — recommended
2. Point me to a file or test I should run
3. Stop here