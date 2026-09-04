---
applyTo: "doc/source/**/*.rst"
---

# PyFluent documentation quality criteria

These rules apply to user-facing documentation pages under `doc/source/`.
They do **not** apply to `doc/source/user_guide/legacy/**` (`tui.rst`, `scheme.rst`,
`rpvars.rst`, `meshing_workflows.rst`), which intentionally documents legacy APIs
for users who still depend on them.

## 1. Show only current, recommended usage patterns

- Prefer the `from_<...>()` session class methods (for example
  `Solver.from_install()`, `Solver.from_container()`, `Solver.from_connection()`,
  `Solver.from_pim()`) in examples over calling `launch_fluent()` /
  `connect_to_fluent()` directly.
  - Exception: the launch guide page(s) that specifically document
    `launch_fluent()` / `connect_to_fluent()` themselves.
- Never use deprecated arguments in examples (for example `show_gui=`,
  `version="2d"/"3d"`). Use the modern equivalents (`ui_mode=`, `dimension=`).
- Use keyword arguments matching the real, current function/method signatures.
  Double-check parameter names against the source (for example
  `use_docker_compose`, not `user_docker_compose`).

## 2. Keep examples concise

- Do not print or paste fully expanded "allowed values" style output (long
  lists of enum-like strings, material lists, etc.) when it adds no value to
  the point being demonstrated.
- When showing that a method like `allowed_values()` returns a list, truncate
  the printed/pasted result to a couple of illustrative items plus a comment
  indicating there are more, for example:

  ```python
  >>> pprint(viscous_model.allowed_values())
  ['inviscid', 'laminar', 'k-omega', ...]  # plus additional models
  ```

- Prefer showing the call and a short description of the result over pasting
  a full raw dump of output.

## 3. Stay on topic

- Each page should stick to the subject implied by its title/section. Don't
  use a page about one subsystem (for example session management) to give an
  in-depth demonstration of another subsystem's settings (for example solver
  model configuration).
- If a deep-dive example belongs conceptually to another page, move it there
  and leave only a short, relevant example plus a cross-reference
  (`:ref:`) on the original page.
- Avoid duplicating the same explanation or example verbatim across multiple
  pages. Link to the canonical location instead of repeating it.

## 4. Use plain, modern language

- Prefer short, direct sentences over multi-clause explanations.
- Avoid promotional or marketing-style language (for example lists of buzzwords
  like "vertical apps", "wider audience", "increasingly broad offerings").
- Avoid unnecessary repetition of the same function/feature name within a
  short span of text.
- Keep descriptive prose proportional to the complexity of the feature being
  documented — trivial features should get brief descriptions.
