# Run this in a Google Colab cell (signed in to the Google account that holds MyDrive/ATML_PA3).
# It collects the raw log/result files that are not in the repository zip (they are stored on Drive as
# generic binary files or exceed 10 MB) and packs them, with their repository paths, into
# MyDrive/ATML_PA3/repo_extras.zip. Unzip that archive into the repository root before committing.
import os
import shutil
from google.colab import drive

drive.mount("/content/drive")
DRIVE = "/content/drive/MyDrive/ATML_PA3"
OUT = "/content/repo_extras"

# repository path  <-  path under MyDrive/ATML_PA3
FILES = {
    # Task 1: per-update training logs and recovery-checkpoint logs
    **{f"task1/runs/{m}/{f}": f"task1/runs/{m}/{f}"
       for m in ["full_ft", "l2sp", "lora4", "lora16", "oplora16"]
       for f in ["train_log.jsonl", "checkpoints.jsonl"]},
    # Task 2: per-update training log, development-evaluation log, selected example IDs
    "task2/runs/vis196/train_log.jsonl": "task2/runs/vis196/train_log.jsonl",
    "task2/runs/vis196/dev_log.jsonl": "task2/runs/vis196/dev_log.jsonl",
    "task2/ids/selection.json": "task2/data/selection.json",
    # Task 3: live-generation records and offline prefix-simulation results
    "task3/results/live_records.jsonl": "task3/results/live_records.jsonl",
    "task3/results/prefix_results_MATH.parquet": "task3/results/prefix_results_MATH.parquet",
    "task3/results/prefix_results_MathVista.parquet": "task3/results/prefix_results_MathVista.parquet",
}

shutil.rmtree(OUT, ignore_errors=True)
missing = []
for dst, src in FILES.items():
    s = os.path.join(DRIVE, src)
    if not os.path.exists(s):
        missing.append(src)
        continue
    os.makedirs(os.path.dirname(os.path.join(OUT, dst)), exist_ok=True)
    shutil.copy(s, os.path.join(OUT, dst))
    print(f"{dst:55s} {os.path.getsize(s) / 1e6:7.2f} MB")

archive = shutil.make_archive(os.path.join(DRIVE, "repo_extras"), "zip", OUT)
print("\nwrote", archive, "| missing:", missing or "none")
