# Worked case: isolate environment precedence

This is a synthetic, source-derived teaching case. The expected readings below
are not a recorded run. The original notes report a separate lab observation;
the repository has no run artifact or automated test for it. That report does
not raise the verification status above `source-reviewed`.

**Goal.** Explain why a value visible in a parsed test file may differ from a
setting read by an application using `load_dotenv(override=False)`.

**First approach and failure.** Changing the setting name between reads does
not isolate precedence: the application may simply ignore the new name.

**Revised control.** In an isolated environment, use a temporary file with
`APP_TEST_LABEL=from_file` and a reader that reports only that harmless setting.
Use a fresh process for each condition. Keep the same file, key, reader, and
loader options; vary only the initial value of that key in the process:

| Initial state | Expected effective value |
|---|---|
| `APP_TEST_LABEL` absent | `from_file` |
| `APP_TEST_LABEL=from_environment` | `from_environment` |

**Result and limits.** These expectations follow from the
[versioned loader source](https://github.com/theskumar/python-dotenv/blob/v1.0.1/src/dotenv/main.py).
If observed, the comparison supports precedence for that configuration only.
It does not establish the behavior of any helper, other application, or
deployment.
