# Contribute

Overall guidance on contributing to a PyAnsys library appears in the
[Contributing] topic in the *PyAnsys developer's guide*. Ensure that you
are thoroughly familiar with this guide before attempting to contribute to
PyFluent.

The following contribution information is specific to PyFluent.

Use the [PyFluent Issues](https://github.com/ansys/pyfluent/issues) page to
submit questions, bug reports, and feature requests directly pertaining to PyFluent.

## Triage guidance: Is the problem in PyFluent or in Fluent?

Follow this checklist to decide where to open a report.

### Quick checklist

- If the behavior concerns Python packaging, installation, import errors,
  or issues specific to Python → open a PyFluent GitHub issue.
- If the issue relates to a particular Fluent physics model, solver behaviour,
  meshing or solver results, or can be reproduced inside Fluent without Python → raise
  it with Ansys ([Support](https://support.ansys.com) or [Developer Forum](https://discuss.ansys.com)).

### How to check

1. Try to reproduce inside Fluent without PyFluent:
   - Use Fluent's journaling/recording capability to record your actions as a Scheme (.jou) or TUI script,
     or translate the Python calls into a Scheme journal.
   - Run the recorded Scheme journal (or equivalent TUI commands) directly in Fluent.
   - If the problem reproduces in Fluent with the Scheme/TUI journal, it is almost certainly a Fluent-side issue.
2. If the issue is only visible when using Python (e.g., wrong parameter mapping, malformed request sent to Fluent, missing API convenience),
   it is likely a PyFluent issue.

### When to contact which channel

- [Ansys Support](https://support.ansys.com): product defects affecting simulation correctness, licensing, installation, or if you need formal tracking.
- [Ansys Developer Forum](https://discuss.ansys.com): general Fluent usage questions, workflow discussion, or community help.
- [PyFluent GitHub](https://github.com/ansys/pyfluent/issues): PyFluent installation, packaging, Python API mapping, client-side bugs, examples, or where there is genuine uncertainty.

### Opening a PyFluent issue

If you open a PyFluent issue (recommended when unsure), please include:

- PyFluent version, Python version, OS.
- Fluent product/version, and whether running Fluent GUI, batch, or headless.
- Short description of expected vs actual behavior.
- Minimal reproduction steps (Python snippet) and, if available, the equivalent Scheme/TUI journal produced by Fluent.
- Attach logs, error output, screenshots, and a small case/mesh if possible and allowed by your policies.
- Mark clearly if you have already reproduced the issue by running the Scheme/TUI journal in Fluent.

[Contributing]: https://dev.docs.pyansys.com/how-to/contributing.html

<!-- Begin content specific to your library here. -->
