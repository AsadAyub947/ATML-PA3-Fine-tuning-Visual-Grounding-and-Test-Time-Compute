# ATML PA3 — Fine-tuning, Visual Grounding and Test-Time Compute

Code, configurations, example IDs and machine-readable results for the three tasks of ATML Programming
Assignment 3:

| Task | Topic | Models |
|---|---|---|
| 1 | Mathematical fine-tuning and retention: Full FT, Full FT + L2-SP, LoRA-4, LoRA-16, OPLoRA-16 | Qwen3-0.6B |
| 2 | A small VLM: SigLIP features → MLP connector → Qwen3-0.6B, trained in three curriculum stages | SigLIP-base-patch16-224, Qwen3-0.6B |
| 3 | Test-time compute: sampling, selection, signals, adaptive stopping, and live strategies | Qwen2.5-3B-Instruct (live); supplied MATH / MathVista rollouts |

All experiments ran on a single NVIDIA Tesla T4 (16 GB) on Google Colab or Kaggle, with seed **6304**.

## Repository layout

```
notebooks/                       the exact notebooks that produced the results (outputs kept as run logs)
  task1_colab_fullft_eval_diagnostics_analysis.ipynb
  task1_kaggle_partA_l2sp_lora4.ipynb
  task1_kaggle_partB_lora16_oplora16.ipynb
  task2_kaggle_vlm_grounding.ipynb
  task3_colab_offline_and_analysis.ipynb
  task3_kaggle_live_generation.ipynb
task1/
  ids/        probe_set.json (activation-probe IDs), train_meta.json (selected MetaMathQA training examples)
  runs/<method>/   summary.json (config, time, memory, displacement), export_*.json, oplora_overhead.json,
                   train_log.jsonl (per-update log), checkpoints.jsonl (recovery-checkpoint log)
  eval/<condition>/{gsm8k,mc}/   lm-eval results.json + run_info.json (exact command)
  tables/     benchmarks.csv, paired_comparisons.csv, gsm8k_extraction.csv, resources.csv, diagnostics*.csv,
              qualitative_all_168.csv, qualitative_annotation_42.csv (manual annotation),
              qualitative_annotation_summary.csv, per_example/ (per-question scores for every condition)
  figures/    benchmarks.png, learning_curves.png, diagnostics.png
task2/
  ids/        mismatch maps, per-stage sampling schedules, selection.json (selected example IDs)
  runs/vis196/  train_summary.json, calibration.json, final_test_records.json, final_eval_info.json,
                train_log.jsonl (per-update log), dev_log.jsonl (development evaluations)
  tables/     final_vis196.csv, final_advantages_vis196.csv, final_per_example_vis196.csv,
              dev_curves_vis196.csv, resources.csv, qualitative_vis196.md
  figures/    learning_curves_vis196.png, qualitative_pairs_vis196.png
task3/
  ids/        splits_{MATH,MathVista}.json (dev/eval/live IDs), orders_*.json (candidate orders)
  results/    adaptive_frozen_*.json (dev-selected thresholds), live_records.jsonl (live-generation records),
              prefix_results_{MATH,MathVista}.parquet (offline prefix results), live_generation_kaggle.log
  tables/     selection_*, bootstrap_*, failure_decomposition_*, per_question_*, signals_*,
              conf_vision_corr_*, adaptive_*, live_*, failure_cases.md
  figures/    compute_allocation_*, failure_decomposition_*, conf_vision_corr_hist, illustrative_trajectories_mathvista
scripts/fetch_large_files_colab.py   copies the raw logs and result files above from Drive (used to assemble this repo)
requirements.txt
```

## Reproducing each task

### Task 1 — LLM fine-tuning (≈ 18 GPU-hours on a T4: 13 h training + 5 h evaluation)
Notebook: `task1_*.ipynb` (identical code; only the configuration cell differs).
Training data: 40,000 MetaMathQA examples (IDs in `task1/ids/train_meta.json`), 1,250 updates at an
effective batch of 32, maximum length 2,048. Full FT and L2-SP: lr 2e-5 (L2-SP λ = 1e-3);
LoRA / OPLoRA: lr 2e-4, ranks 4 and 16 (α = 2r), OPLoRA protects the top-128 singular directions.
Evaluation (lm-eval 0.4.13, zero-shot): `gsm8k_cot` with the chat template, thinking disabled, greedy,
1,024 new tokens; `hellaswag`, `boolq`, `arc_easy` by log-likelihood. The Full FT midpoint is update 625.

To reproduce in one go, run the notebook with the default configuration (all methods, all flags on).
The reported results were produced in four sessions, all writing to the same results folder:

| Session | Platform | Configuration cell | What it produced |
|---|---|---|---|
| 1 | Colab | default configuration (all methods); the free GPU quota ran out after Full FT finished | Full FT training + midpoint/final exports (2.45 h); the interrupted L2-SP run was discarded |
| 2 | Kaggle (`task1_kaggle_partA_…`) | `RUN_METHODS = EVAL_CONDITIONS = ["l2sp","lora4"]`, flags `True, True, False, False` | L2-SP, LoRA-4 training + evaluation |
| 3 | Kaggle (`task1_kaggle_partB_…`) | `RUN_METHODS = EVAL_CONDITIONS = ["lora16","oplora16"]`, flags `True, True, False, False` | LoRA-16, OPLoRA-16 training + evaluation |
| 4 | Colab (`task1_colab_…`) | `RUN_METHODS = []`, `EVAL_CONDITIONS = ["baseline","full_ft_mid","full_ft"]`, flags `False, True, True, True` | baseline + Full FT evaluations, diagnostics, all tables and figures |

The Kaggle `runs/` and `eval/` outputs were copied into the Colab results folder before session 4.
The notebook kept for session 4 is the same notebook used for session 1; its outputs show session 4.

### Task 2 — VLM grounding (≈ 2 GPU-hours on a T4)
Notebook: `task2_kaggle_vlm_grounding.ipynb`, all stage flags on, `RUN_COMPRESSED = False`.
It downloads COCO 2014 annotations/images and VQAv2 complementary pairs itself, selects the data with
the fixed seed (6,000 caption images; 24/64 grounding dev/test pairs; 1,536/32/96 VQA train/dev/test
pairs), caches SigLIP features (9,283 images, 2.6 GB), trains 4,500 updates in three stages
(caption 2,250 → grounding instruction 1,500 → VQA 750; LoRA r = 16 from stage 2), evaluates the test
sets under correct / complementary / mismatched / no-image conditions and writes all tables and figures.

### Task 3 — Test-time compute (CPU for the offline parts; ≈ 2.3 GPU-hours for live generation)
Data: the course-supplied `ATML-PA3-Data` (not redistributed). Put `ATML-PA3-Data.zip` in the Task 3
work folder; the configuration cell unzips it. Live model: `Qwen/Qwen2.5-3B-Instruct` at revision
`aa8e72537993ba99e69dfaafa59ed015b17504d1`, with the prompt format given in the supplied README.

| Session | Platform | Flags `OFFLINE, SIGNALS, ADAPTIVE, LIVE, ANALYSIS` | What it produced |
|---|---|---|---|
| 1 | Colab CPU | `True, True, True, False, True` | grading, selection, signals, adaptive stopping, figures |
| 2 | Kaggle T4 (`task3_kaggle_live_generation.ipynb`) | `False, False, False, True, False` | 50-question live generation (2 h 18 min) |
| 3 | Colab CPU (`task3_colab_offline_and_analysis.ipynb`) | `True, True, True, True, True` | final scoring of live strategies and all tables/figures |

Session 2 read the graded data cached by session 1 (`prepared_*.pkl`, `splits_*.json`), uploaded as a
private Kaggle dataset; its `live_records.jsonl` was copied back before session 3. The saved outputs of
`task3_kaggle_live_generation.ipynb` were cleared (they predated the committed run); that run's log is
`task3/results/live_generation_kaggle.log`.

## Where the report's evidence comes from

| Task | Evidence | Files |
|---|---|---|
| 1 | Benchmarks, 7 conditions × 4 benchmarks, Δ in pp | `task1/tables/benchmarks.csv`, `paired_comparisons.csv`, `gsm8k_extraction.csv`, `figures/benchmarks.png` |
| 1 | SFT loss; L2-SP penalty and displacement | `figures/learning_curves.png`, `tables/resources.csv`, `runs/*/summary.json`, `runs/*/train_log.jsonl` |
| 1 | Resources | `tables/resources.csv` |
| 1 | Diagnostics (ρ_k, η, R(z)) | `tables/diagnostics.csv`, `diagnostics_R_per_probe.csv`, `figures/diagnostics.png` |
| 1 | Qualitative (42 annotated responses) | `tables/qualitative_annotation_42.csv`, `qualitative_annotation_summary.csv`, `qualitative_all_168.csv` |
| 2 | Learning curves with stage boundaries | `figures/learning_curves_vis196.png`, `tables/dev_curves_vis196.csv`, `runs/vis196/{train,dev}_log.jsonl` |
| 2 | Final results, pair diagnostics, advantages, CIs | `tables/final_vis196.csv`, `final_advantages_vis196.csv`, `final_per_example_vis196.csv` |
| 2 | Qualitative pairs | `tables/qualitative_vis196.md`, `figures/qualitative_pairs_vis196.png` |
| 2 | Resources incl. feature caching | `tables/resources.csv`, `runs/vis196/train_summary.json` |
| 3 | Sampling/selection curves, method comparison, failure decomposition | `figures/compute_allocation_*.png`, `tables/selection_*_eval.csv`, `bootstrap_*_eval.csv`, `failure_decomposition_*` |
| 3 | Signal analysis, confidence–vision relationship | `tables/signals_*.csv`, `conf_vision_corr_*`, `figures/conf_vision_corr_hist.png`, `illustrative_trajectories_mathvista.png` |
| 3 | Live inference (50 questions) | `tables/live_strategies.csv`, `live_bootstrap.json`, `live_revision_transitions.json`, `live_revision_cases.json`, `live_per_question.csv`, `results/live_records.jsonl` |
| 3 | Adaptive inference | `tables/adaptive_dev_grid_*.csv`, `adaptive_eval_*.csv`, `adaptive_vs_pool_*.csv`, `results/adaptive_frozen_*.json` |
| 3 | Qualitative | `tables/failure_cases.md` |

## Notes and deviations

- **Task 1, GSM8K strict-match is 0 for every condition.** lm-eval's strict filter requires
  "The answer is N."; the baseline does not use that phrase and the fine-tuned models produce MetaMathQA's
  "The answer is: N". Flexible-extract EM is reported as the GSM8K metric.
- **Task 2, mixed precision.** The FP16 gradient scaler skipped 5 of 4,500 updates (1, 2, 3, 6, 7) on
  overflow while calibrating its loss scale; they are listed in `runs/vis196/train_summary.json`. The optional 49-token compression
  experiment was not run.
- **Task 3, problem text for live generation.** The supplied generations store the problem in a
  `question_text` column, which the loader did not map at run time; the live session therefore read the
  problem text from `DigitalLearningGmbH/MATH-lighteval` (test split, revision
  `0530c78699ea5e8eb5530600900e1f328b48acad`, the source named in the supplied README), with all 50 live
  questions checked against the supplied gold answers (50/50 match). MathVista attention columns were set
  with `COLUMN_OVERRIDES`.
- **Task 3, grading.** A small number of math-verify comparisons timed out and count as "not equal".
- No setting was tuned on evaluation data: Task 1 uses fixed hyperparameters, Task 2 uses its development
  split only for monitoring, and Task 3 chooses adaptive-stopping thresholds on the 200 development
  questions before the 800 held-out questions are scored. Task 3 selection and stopping rules use neither
  gold answers nor unrevealed candidates.

## Not included

- Raw datasets (course-supplied `ATML-PA3-Data`, COCO, VQAv2, MetaMathQA, benchmark data): the notebooks
  download them or read them from the course folder.
- Model weights and large intermediates: merged/exported models, LoRA adapters, recovery checkpoints,
  diagnostic weight deltas (`diag_*.pt`), SigLIP feature caches, cached graded data (`prepared_*.pkl`),
  lm-eval per-sample logs (the per-example CSVs in `task1/tables/per_example/` cover them).