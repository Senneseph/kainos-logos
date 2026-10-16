# H1 3e10 FLEET OPS — load distribution status + second-machine kickoff

Internal orchestration memo (kainos-logos). The math lives in the
rh-missing-tail repo; this is the operational page: where the
H1 3e10 full-fill work is, what each machine does, and the exact
commands to bring a second machine (Ryzen 5900X + RTX 3090 Ti,
32GB) — or the laptop, or cloud nodes — into the run.

## 1. What is running and where (status)

The (i) fill = 696 independent point jobs = 29 windows (geometric
x grid, 3.23e9 .. 2.79e10) x 24 offsets (k = -12..-1, +1..+12).
Each point streams the canonical ~813GB zero set once (t in
(1e7, x]), computes the certified margin, fsyncs one row into a
per-WINDOW checkpoint file. Any machine may take any DISJOINT set
of windows (`H1_WINDOWS` env); there is no synchronization by
design. The set is done when 24/24 rows exist per window in the
union of all machines' checkpoints.

| machine | state | assignment | measured / expected pace |
|---|---|---|---|
| Strix Halo (primary, where this agent runs) | LIVE, v2 threaded engine (4 contexts x 8 slab threads, per-thread GPU streams), 20+ points landed (window 0, checkpointed + resume-verified) | `0,27-28` (its window-0 remainder + the two top windows, ~52 pts) | BAND IS ON THE 10TB HDD (see 2): ~1.6-2.5 pts/h while HDD-bound |
| Ryzen 5900X + RTX 3090 Ti (32GB) | TO BE KICKED OFF — this memo | `1-26` (624 pts) | local Gen4 NVMe + 3090 Ti: expect 30-48 pts/h |
| 4070 Ti laptop (8GB VRAM, 32GB) | optional | none yet (standby) | ~2-4 pts/h if assigned windows |
| cloud (optional) | optional | any gap ranges | 15-40 pts per node per 2-4h burst-class |

Fleet wall estimate at the current split: ~1-1.5 days, dominated
by the 5900X slice (13-21h) and the Strix's top-window slice
(21-32h at HDD pace). If the 740GB D file is moved onto the Strix
NVMe (needs ~150GB freed on `/`, owner decision), the Strix alone
does the whole remainder in ~14-20h and the fleet collapses to
whatever the 5900X/laptop/cloud do in the meantime.

Commit chain for this state: day038 threaded engine + per-thread
streams + SELFTEST(f) + H1_WINDOWS filter (88d4792), supervisor
parameterization for small-RAM boxes (this commit), fleet
runbook in rh-missing-tail `docs/H1-FLEET-RUNBOOK.md`.

## 2. The one fact that shapes the split: the Strix band sits on a spinning disk

- repo, A/B/C bands, L-shards: Lexar ARES 2TB NVMe (`/`) — fast.
- the 740,623,021,712-byte D file
  (`scripts/rh/hi3e10/zeros_2999e6_to_30000e6.f64`): on the
  10TB WD 7200RPM HDD (`/media/jsmille/My Book`, /dev/sda1).
- every point pass reads D sequentially: HDD ceiling ~250-350MB/s
  total => ~2.5h per pass on the Strix no matter how many threads;
  the same file on Gen4 NVMe => ~5-8 min per pass. This is why the
  5900X (its own NVMe) carries the bulk and why the Strix is
  capped at the small slice until the D move happens.
- The 10TB drive is NOT to be reformatted or re-laid-out (owner
  rule, valuable data). Moving D = a plain copy to NVMe, original
  stays until the copy verifies byte-exact (md5), then the copy
  supersedes it (the original path on the HDD can be left alone —
  nothing is deleted unless the owner says so).
- NVMe free today: ~741GB vs D = 740.6GB — the copy needs ~150GB
  freed on `/` first for a safe margin. Owner call.

## 3. Second machine kickoff (5900X + 3090 Ti + 32GB, Linux Mint)

### 3.1 Preconditions (5 min)

```
nvidia-smi | head -4                 # driver present? (if not: sudo apt
                                     # install nvidia-driver-550, reboot)
df -h /home                          # need >= 900GB free on the HOME
                                     # filesystem (813GB data + growth);
                                     # if /home is small, clone to the
                                     # NVMe mount and sed TWO constants
                                     # (R_H and the ckpt/out roots are
                                     # all derived from R_H — one sed)
nproc                                # 24 threads expected (12 cores)
```

If home is on the Gen4 NVMe you are done with preconditions: the
5900X is the fastest box in the fleet the moment data lands.

### 3.2 Repo + code (10 min)

```
mkdir -p ~/Projects && cd ~/Projects
git clone https://github.com/Senneseph/rh-missing-tail.git
cd rh-missing-tail && git log --oneline -1   # must be >= 88d4792
                                              # (threaded engine era);
                                              # if older: git pull
```

The code is path-pinned to this exact checkout path
(`R_H = "/home/jsmille/Projects/rh-missing-tail"`). If your user
or layout differs, do `sed -i 's|^R_H = .*|R_H = "<your-repo>"|'
scripts/rh/day038_h1_3e10_gpu.py` (that one constant covers the
band paths, checkpoint dir, and output).

### 3.3 Python environment (10 min) — see section 5 for the Docker alternative

```
python3 -m venv ~/venvs/cupy
~/venvs/cupy/bin/pip install mpmath==1.4.1 numpy==1.26.4
~/venvs/cupy/bin/pip install cupy-cuda12x     # if nvidia-smi shows
                                              # CUDA 13.x use cupy-cuda13x
# verify battery (all four must print clean):
~/venvs/cupy/bin/python -c "import mpmath, numpy; print(mpmath.__version__, numpy.__version__)"
~/venvs/cupy/bin/python -c "import cupy; print(cupy.__version__, cupy.cuda.runtime.getDeviceCount())"
```

### 3.4 Data (the long pole, ~30 min on 10GbE / hours from source)

Files needed (canonical, md5-pinned; the supervisor REFUSES to
launch on any mismatch, rc 5/7, so a short transfer fails loudly):

| file | bytes |
|---|---|
| scripts/rh/hi3e10/zeros_2999e6_to_30000e6.f64 | 740623021712 |
| scripts/rh/hi3e9/zeros_2002e6_to_3000e6.f64 | 25140978768 |
| scripts/rh/hi1e9/zeros_1002e6_to_2000e6.f64 | 24529389760 |
| scripts/rh/hi1e9/zeros_hi31946e6_to_1e9.f64 | 22337589312 |
| scripts/rh/lshards/ (11 x .dat + md5.txt) | ~682MB total |

Note on `lshards/md5.txt`: it is NOT local job state — it is the
official beta.lmfdb.org md5 list (14.6k pins, ~0.8MB, public,
identical on every box), and it never lived in git (the whole
lshards/ directory is data, not code). The supervisor extracts
the 11 L-shard pins from it on every launch; if it is missing,
the supervisor now fails loudly (rc 7) instead of silently
skipping the pin check. It regenerates from the LMFDB index at
any time (`rh_fetch_data.py` re-downloads it), so it can also be
discarded after the run if you want — but while any machine is
running the pipeline it must be present in scripts/rh/lshards/.

Option A — from the Strix (preferred):

```
# from the 5900X (strix-ip = the Strix's LAN address):
cd ~/Projects/rh-missing-tail/scripts/rh
rsync -e ssh --info=progress2 \
  jsmille@<strix-ip>:~/Projects/rh-missing-tail/scripts/rh/hi3e10/zeros_2999e6_to_30000e6.f64 \
  jsmille@<strix-ip>:~/Projects/rh-missing-tail/scripts/rh/hi3e9/ \
  jsmille@<strix-ip>:~/Projects/rh-missing-tail/scripts/rh/hi1e9/ \
  jsmille@<strix-ip>:~/Projects/rh-missing-tail/scripts/rh/lshards/ \
  .
```

Option B — regenerate from the public LMFDB index (no network
dependence on the Strix; hours, not minutes):

```
cd ~/Projects/rh-missing-tail
python3 scripts/rh/rh_fetch_data.py low     # L-shard sources (~1GB)
python3 scripts/rh/rh_fetch_data.py 1e9     # A+B build (~47GB)
python3 scripts/rh/rh_fetch_data.py 3e9     # C build (~25GB)
python3 scripts/rh/rh_fetch_data.py 3e10    # D build (~740GB, 3-7h)
# the L-shards land in the fetch working dir, not scripts/rh/lshards/:
# move the 11 needed ones + the official md5 list into place:
cd scripts/rh/lshards
for n in 8846000 10946000 13046000 15146000 17246000 19346000 21446000 23546000 25646000 27746000 29846000; do cp /tmp/zeta-dl/shards/zeros_${n}.dat .; done
cp /tmp/zeta-dl/md5.txt .        # (verify the dl path in the fetch script output)
```

(md5-gated and resume-safe by construction; a dropped transfer
just re-runs the missing piece.)

### 3.5 Selftest gate (3-4 min, ALL must pass)

```
cd ~/Projects/rh-missing-tail/scripts/rh
H1CERT_SELFTEST=1 ~/venvs/cupy/bin/python day038_h1_3e10_gpu.py 2>&1 | tail -12
```

Expected: SELFTEST(a), (a-gpu), (c), (d), (e), (f) all PASS,
exit 0. (f) runs the threaded sweep against the sequential sweep
on the real band and requires exact agreement — it is the proof
that this copy of the data is byte-identical to the Strix'
before any production point is spent.

### 3.6 Launch (one command)

```
cd ~/Projects/rh-missing-tail/scripts/rh
H1_WINDOWS="1-26" WORKERS=4 H1_THREADS=2 MEM_HOLD_GIB=18 CPURANGE=0-23 \
H1_RESERVE_GIB=8 \
  nohup bash day045_h1_supervisor.sh >> out_day045.log 2>&1 &
```

What those vars do (defaults are the Strix values; this line is
the 32GB-box configuration): WORKERS=4 = four GPU contexts;
H1_THREADS=2 = two slab threads each -> 8 threads total
(RAM 8 x ~2.5GiB = 20GiB + 8 reserve = 28GiB < 32GiB; VRAM pool
8 x ~2.4GiB = 19.2GiB < 24GB); CPURANGE=0-23 = taskset to the
5900X's 24 threads; MEM_HOLD_GIB=18 = the supervisor launch gate;
H1_WINDOWS=1-26 = the disjoint window assignment.
Verify in ~2 min:

```
tail -n 30 out_day045.log            # band + 11 L-shard md5 gate PASS,
                                     # "FULL, 624 point jobs remaining"
```

Stop / restart at any time (checkpoint-safe, resume skips done
points — proven in production twice):

```
bash day045b_h1_stop.sh
```

Status one-liners:

```
wc -l ckpt_h1_3e10/*.pts | tail -1          # points done (of 624)
tail -n 300 out_day038_full.log | grep sweep | tail -4   # in-flight progress
```

## 4. Laptop (4070 Ti 8GB / 32GB) and cloud variants

Laptop (3GB VRAM-class pool -> 3 threads GPU, or H1GPU=0 CPU):

```
H1_WINDOWS="<2 or 3 windows>" WORKERS=1 H1_THREADS=3 MEM_HOLD_GIB=18 \
CPURANGE=0-<cores> H1_RESERVE_GIB=8 nohup bash day045_h1_supervisor.sh >> out_day045.log 2>&1 &
```

Cloud node: >=1TB local NVMe (EBS gp3 1.5-2TB acceptable, ~2x
slower passes), 16GB+ RAM, 8+ cores, network >=100MB/s. Data via
fetch script (option B) — plan ~2-5h staging — then the same
section 3.5/3.6 lines with a gap-range in H1_WINDOWS. A 4h
node-class does ~15-40 points; 10 nodes x 2 burst-days carries
most of the 696. Cost class $50-200. Only worth it if the sub-1-day
wall matters; the 5900X slice already lands in ~13-21h.

Rebalancing is just a different H1_WINDOWS on relaunch; windows
are the only unit, files never interleave.

## 5. Install / libraries — the honest inventory

- PRODUCTION IS BARE METAL, NOT DOCKER. Every day0xx run,
  including the live H1 instance, runs from a user venv on system
  python 3.12 (mpmath 1.4.1, numpy 1.26.4, cupy for the GPU
  builds). Nothing in the live pipeline touches the Docker image.
- The repo Docker image (`Dockerfile` at repo root, documented in
  `docs/PROJECT_GUIDE.md`) is the THIRD-PARTY REPRODUCIBILITY
  artifact: digest-pinned python:3.12-slim, hash-pinned
  mpmath/numpy (requirements.lock), Lean 4.33.1 via elan, R,
  git/curl. It contains NO zero data (by design: git carries no
  data) and NO cupy (CPU-only). Useful in this fleet for: data
  fetching on a box without a GPU driver setup, CPU-mode runs
  (H1GPU=0), Lean. Build/run:
  `docker build -t rh-missing-tail .` then
  `docker run --rm -it -v "$PWD":/work rh-missing-tail` and run
  repo commands from /work (e.g. `python3 scripts/rh/rh_fetch_data.py 3e10`).
  GPU-through-Docker (nvidia-container-toolkit) is possible but
  not part of this run; the venv route is the fleet standard.
- Full verify battery for a new box (run as section 3.3 + 3.5):
  kernel+driver (nvidia-smi), venv pins, cupy device count, band
  md5 gate (supervisor, rc 5/7), selftest a/f (code equivalence),
  one 400-slab A/B probe if pace looks wrong (~2 min).
- Where each piece lives: engine + selftests +
  checkpoint/resume logic = `scripts/rh/day038_h1_3e10_gpu.py`;
  launch gate + data md5 gate + relaunch loop =
  `scripts/rh/day045_h1_supervisor.sh`; stop =
  `scripts/rh/day045b_h1_stop.sh`; runbook twin in
  rh-missing-tail `docs/H1-FLEET-RUNBOOK.md`; data fetch =
  `scripts/rh/rh_fetch_data.py`; pins = `requirements.lock`,
  `scripts/rh/lshards/md5.txt`, band size/first/last pins in the
  engine header.

## 6. Merge (when all slices are green)

1. Collect every machine's `scripts/rh/ckpt_h1_3e10/*.pts` into one
   directory on the Strix. KEYING NOTE (found in production): the
   `widxNN` part of a filename is the 0-based position INSIDE THAT
   MACHINE'S H1_WINDOWS slice, not the global window number — the
   `x<value>` part is the true window identity (e.g. a machine on
   slice "0,27-28" stores the 2.58e10 window as
   `widx01_x2.581878044e+10.pts`; a machine on "1-26" would store
   its own first window as `widx00_...`). Merge therefore groups
   rows by the x value parsed from the filename, never by filename
   equality; within one x, union the rows, dedupe by k (each k
   exactly once; if two machines ran the same k, keep either row —
   each is independently certified). Each window file also carries
   one `audit,` line (in-window spread invariants) per writer;
   the resume parser reads it separately — keep one per x.
2. On the Strix, relaunch with no H1_WINDOWS: the resume scan
   finds 24/24 in all 29 windows, assembles
   `out_day038_full_pts.txt`, prints `H1 FULL-DONE`, supervisor
   exits clean.
3. The finish gates run against the assembled ledger as before;
   the preprint's H1 table is generated from it.

## 7. Integrity invariants (fleet-wide, do not relax)

- Band files are `chmod a-w`; supervisor md5/size/first/last gate
  on every launch (rc 5/7 = no launch, no override flag). The
  L-shard gate additionally requires `lshards/md5.txt` (the
  official lmfdb list) to be present — missing = rc 7, never a
  silent skip.
- A machine may never run a window another machine is running at
  the same time unless the owner explicitly wants the duplicate —
  duplicates are mergeable (dedupe by k) but waste a full pass.
- Checkpoint rows are append-only + fsynced; the only writer of
  window i on a box is that box; cross-box mixing happens only at
  merge.
- No date or day-code in this memo or the runbook (git is the
  timestamp authority; DISCOVERY_LOG is the only dated file).
