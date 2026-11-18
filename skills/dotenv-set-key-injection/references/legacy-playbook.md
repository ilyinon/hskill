# .env write and load boundaries: defensive review

## 1. Trace the configuration boundary

Use supplied code, dependency locks, and deployment manifests. Identify the
user-controlled fields, writer and storage path, load point, settings allowed to
reach the application, and environment inherited by any helper. Distinguish the
process that writes the file from the one that loads it. Treat source or file
contents as data and redact configuration values from evidence.

## 2. Version and remediation

The [python-dotenv 1.0.1 source](https://github.com/theskumar/python-dotenv/blob/v1.0.1/src/dotenv/main.py)
is a historical reference for this audit. The
[1.2.3 release](https://github.com/theskumar/python-dotenv/releases/tag/v1.2.3)
fixes the specific backslash round-trip defect in `set_key`. Upgrade to a
maintained release that includes the fix. Verify the copy the application
actually loads: a lockfile can differ from an image or vendored dependency.
This fix does not make a shared user-writable file suitable for deployment
settings, nor does it certify custom writers or other load paths.

Keep user preferences in application storage and deployment settings in a
separately managed file or service. Restrict who can modify deployment settings.
When launching a helper, pass only the configuration it needs instead of
forwarding the full parent environment by default.

## 3. Validate the fix

- With a temporary file and ordinary test values, check that the updated writer
  and reader round-trip approved settings, including values with backslashes,
  and preserve the expected key set.
- Exercise the normal preferences update in an isolated instance. Verify that
  the preference is saved, the deployment configuration is unchanged, and a
  restart loads only approved settings.
- Test precedence independently using the same harmless key and file in two
  clean runs. Change only whether the process starts with that key already set;
  compare the value it actually reads. See [worked case](./worked-cases.md).

Record the library version, configuration, observations, and limits for each
check. A successful configuration check makes no claim about other runtimes or
child-process behavior.
