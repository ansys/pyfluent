# Code Generation Rules

PyFluent contains generated API artifacts. Follow these rules to keep changes safe.

## Generated Output Location

- src/ansys/fluent/core/generated

## Default Policy

- Do not hand-edit generated files unless explicitly requested for a narrow fix.
- Prefer changing generation inputs/scripts and then regenerating output.

## Regeneration Command

- python codegen/allapigen.py
- Optional verbose mode: python codegen/allapigen.py -v

## When Generated Files Change

- Keep generated changes in a dedicated commit segment when possible.
- Note regeneration command and context in PR description.
- Ensure related tests still pass for impacted APIs.

## Review Heuristics

- Verify manual edits did not drift from generator output.
- Check for accidental churn outside intended generated scope.
