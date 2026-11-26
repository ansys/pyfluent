# Comparing the Four Data Externalization Strategies

This guide is for anyone who wants to understand the four ways the solver can
save its results.

## What is data externalization?

While solving a case, the solver produces useful information such as velocity,
pressure, mesh coordinates, and progress measurements. A **snapshot** is a
saved copy of that information for a selected completed solver step.

**Data externalization** means moving those snapshots out of the solver's
calculation flow so that another program can save, share, or display them. The
solver still calculates the answer; the selected strategy controls how the
snapshots are delivered and stored.

The four strategies all send the same kind of snapshot. The sampling interval
controls how often one is created; the selected strategy controls how it is
delivered and how much the solver waits.

## The four strategies in everyday terms

### 1. Synchronous file export (`sync`)

For each selected step, the solver prepares and saves that step's snapshot to
a file. It waits for the file write to finish before continuing.

Think of it as a person making a copy of each page before starting the next
page.

- **Good for:** small runs, straightforward local use, and a simple baseline.
- **Trade-off:** file preparation and writing time is directly part of the
  solver's step time.
- **Data safety:** the snapshot is saved before the solver continues.

### 2. Shared-folder spool (`shared`)

The solver saves each selected snapshot to a shared folder. A separate **poller**
periodically checks that folder and copies newly arrived snapshots to the
destination store.

Think of it as putting completed pages in an inbox; another person checks the
inbox every so often and files the pages elsewhere. In the comparison program,
the poller runs independently from the solver in a background thread. The
included `poll_shared_snapshots.py` tool can also be run as a separate process.

- **Good for:** separating the solver from a later file-processing or
  storage tool.
- **Trade-off:** the solver still has to write each snapshot to the shared
  folder. The poller's interval also affects how quickly the destination gets
  updated.
- **Data safety:** the source spool is retained for replay; it can use
  additional disk space and should be managed.

### 3. Background queue (`async`)

The solver puts each selected snapshot into a short in-memory line (a **queue**). A
background worker takes snapshots from that line and writes them to files while
the solver continues.

Think of leaving completed pages in a tray for another person to file.

- **Good for:** reducing the time the solver spends waiting on local file
  writing.
- **Trade-off:** if the worker cannot keep up, the queue fills and the solver
  must wait for room.
- **Data safety:** queued snapshots are written when the run closes normally.
  A sudden process or machine failure can lose snapshots that have not yet
  reached a file.

### 4. gRPC streaming (`grpc`)

gRPC is a standard way for separate programs to exchange messages. The
solver-side client sends selected snapshots as a stream to a gRPC service, which
receives and saves them. In the local comparison demo, both client and service
run on the same computer; a future deployment could place the service on
another machine.

Think of sending pages along a delivery route to a separate filing office.

- **Good for:** creating a service boundary between the solver and an
  externalization service.
- **Trade-off:** preparing and sending snapshots takes time; network conditions
  matter when the service is remote.
- **Data safety:** the client waits for the service to finish the stream and
  acknowledge it when the run closes.
- **Security note:** the local demo uses an insecure loopback connection.
  Network deployments need TLS and appropriate authentication and
  authorization.

## What does backpressure mean?

The `async` and `grpc` strategies use a **bounded queue**: a waiting line with
a fixed maximum size. Bounding the line prevents it from growing forever and
using all available memory.

**Backpressure** is what happens when the line is full. The solver pauses
publishing snapshots until the worker or service makes room. This implementation
does not silently throw away snapshots to avoid the pause.

For example, with a queue size of 8, up to 8 snapshots can wait to be processed.
If the next snapshot arrives while all 8 spaces are occupied, the solver waits
for one space to become free. Increasing the queue can absorb short bursts, but
it does not make a permanently slower storage service faster.

## Choose how often snapshots are sent

The default is every 10 completed solver steps, plus the final step if it does
not land on that interval. For example, a 23-step run saves steps 10, 20, and
23. Set the interval to 1 to externalize every step:

```powershell
python examples/run_externalized_case.py `
  --case path/to/your-case.json `
  --strategy async `
  --snapshot-every 1
```

In the comparison runner, use the same option:

```powershell
python examples/compare_externalization_strategies.py `
  --steps 100 `
  --snapshot-every 10
```

A larger interval means fewer snapshots to serialize, write, queue, or transfer.
This can reduce storage and network traffic, ease queue pressure, and reduce
waiting, especially for synchronous file output. It does not reduce the
solver's numerical work, and the speedup may be small when solving dominates
the runtime. The trade-off is a less detailed live view and fewer saved
intermediate states. The final state is always externalized.

## Other useful terms

| Term | Plain-language meaning |
| --- | --- |
| **Solver step** | One completed calculation update. |
| **Snapshot** | The fields and progress information saved after a step. |
| **Producer** | The part that creates and sends snapshots; here, the solver-side adapter. |
| **Consumer / worker** | The part that receives snapshots and writes or forwards them. |
| **Spool** | A temporary holding area, such as the shared folder used by `shared`. |
| **Polling interval** | How often the shared-folder poller checks for new snapshots. |
| **Publish time** | Time spent by the solver-side strategy handing off snapshots. |
| **Externalization time** | Time spent writing snapshots downstream. For background strategies, this work can overlap with solving. |
| **Solver time** | Time spent running the backend, including the strategy's solver-side publish work. It is not just the numerical calculation time. |
| **Total time** | Solver time plus draining or closing the externalizer so pending work is completed. |
| **Snapshot count** | Number of snapshots successfully externalized. With sampling, this is lower than the completed step count; it includes interval steps and the final step. |
| **Bytes written** | Approximate size of the snapshot data. Small differences between runs are normal. |
| **Converged** | Whether the solver met its numerical stopping criteria. A timing run can finish its step limit without converging. |

`externalize_seconds` is not always extra time after `solver_seconds`. For
`async` and `grpc`, writing can happen while the solver continues, so the two
durations overlap. Compare `total_seconds` for elapsed time until all
externalization work is drained. Compare `solver_seconds` and `publish_seconds`
to understand how much work is on the solver's path.

## Run a local comparison

Open PowerShell in the project folder. Install the project and its dependencies
if you have not already done so:

```powershell
python -m pip install -e .
```

Run all four strategies against the same case:

```powershell
python examples/compare_externalization_strategies.py --steps 100 --snapshot-every 10
```

The comparison program runs the solver separately for each strategy. By
default, it uses the steady lid-driven cavity case and writes output under
`results/externalization_poc/`.

The default step limit is only 4, to make the first run quick. Use a larger
limit, such as 100 or 500, for a more useful timing sample. A larger limit does
not guarantee convergence; check the `converged` column in the report.
The default snapshot interval is 10 steps. Use `--snapshot-every 1` when you
want every solver step saved, and use the same interval for every strategy in
a fair performance comparison. With the default four-step cap, only the final
step is saved because the run does not reach step 10.

### Choose a case, strategy, or output folder

To compare a different case, pass its JSON file:

```powershell
python examples/compare_externalization_strategies.py `
  --case cases/lid_driven_cavity_re100_transient.json `
  --steps 100
```

To run just one strategy, add `--strategy` with one of `sync`, `shared`,
`async`, or `grpc`:

```powershell
python examples/compare_externalization_strategies.py `
  --strategy grpc `
  --steps 100
```

To keep a separate report for another trial, choose a different output folder:

```powershell
python examples/compare_externalization_strategies.py `
  --steps 100 `
  --output results/externalization_trial_2
```

The `--queue-size` option sets the maximum waiting line for `async` and `grpc`
(default: 8). The `--poll-interval` option sets how often `shared` checks its
spool in seconds (default: 0.1). For example:

```powershell
python examples/compare_externalization_strategies.py `
  --steps 100 `
  --queue-size 16 `
  --poll-interval 0.5
```

## Read the comparison output

The output folder contains:

- `benchmark.csv` and `benchmark.json`: one summary row per strategy.
- A separate folder for each strategy, containing the snapshots and a
  `final_snapshot.png` visualization made from the saved data.
- For `shared`, both the source spool and the poller's destination snapshots.

You can open `benchmark.csv` in a spreadsheet program. Check these items:

1. **Same amount of work:** compare rows with the same case and step count.
2. **All data arrived:** compare `snapshot_count` with the expected number of
   interval snapshots plus the final step, not directly with `steps`.
3. **Solver impact:** compare `solver_seconds` and `publish_seconds`.
4. **End-to-end wait:** compare `total_seconds`; it includes the time to finish
   pending writes or transfers.
5. **Numerical result:** check `converged`. A capped, non-converged run is
   useful for measuring data delivery, but it is not a validated final
   simulation result.

For a presentation-quality comparison, run each strategy several times using
the same case, mesh, step limit, output location type, and computer. Give each
trial a separate `--output` folder so its report is preserved. Avoid running
other heavy applications during the trials. The measurements are local POC
results: in particular, the local gRPC result does not predict performance
over a cloud network.

## Run the shared-folder poller separately

The comparison program starts the shared-folder poller for you. To run the
consumer as a separate process, start it with the matching shared and
destination folders:

```powershell
python examples/poll_shared_snapshots.py `
  --shared results/my_run/shared `
  --destination results/my_run/snapshots `
  --interval 1
```

Stop it with **Ctrl+C** after the solver has finished. It performs a final
check before exiting. The producer and consumer must point to the same shared
folder for this arrangement to work. A Python example that configures the
solver-side producer is in the
[solver guide](./using_the_solver.md#10-compare-data-externalization-strategies).
