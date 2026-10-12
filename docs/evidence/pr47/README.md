# PR #47 reproducible evaluation evidence

These files capture fresh executions on 2026-10-12, in UTC+03:00 (Asia/Damascus). They do not reconstruct unsaved historical output.

The baseline replay uses the training data, training script and predictor from commit `4267ae5495b83b28b2f079803726cfa345a29429` in a private temporary snapshot. Its evaluator comes from tested local commit `213281c9cc717f1677451cb31db8c47b50d81173` so the output omits evaluation text. The updated replay uses the training data, training script, predictor and corrected evaluator from that tested local commit, which incorporates main `0706db3add33fab7f5007049d30be6ef25a81115`.

Both runs used the same unchanged local evaluation CSV. Its contents are not included; its SHA-256 and the exact executed argument lists and working directories are in [manifest.json](manifest.json). Case IDs map to file rows under that hash.

For either source snapshot, with its dependencies installed and a private local evaluation CSV available, the model commands are:

```text
python ai/train.py
python ai/evaluate_heldout.py --csv PATH_TO_LOCAL_EVALUATION_CSV
```

The first command performs split evaluation and five-fold CV, then fits and saves a model on all training rows. The second command measures that final saved model on the separate six-case set. Saved model hashes are recorded in the manifest; model binaries are local-only.

Files prefixed `baseline-` capture the 36-row version; `updated-` captures the 42-row version. `*-train.txt` includes the real split report and CV output. `*-evaluation.txt` includes only case IDs, labels, confidences, file hash and counts. Matching stderr captures are provided; no stderr was produced in these runs.

Shared text captures use UTF-8 with LF line endings so their manifest hashes match the committed GitHub artifacts. Only line endings are normalized; output values are unchanged. Empty stderr is represented by `No stderr output.` in its artifact.

The 36-row replay is balanced (12 per category). The 42-row replay has 12 access, 12 billing and 18 technical examples. Both separate-set scores are 4/6. Split/CV scores across the two training datasets are not controlled measurements on identical evaluation cases.

This previously exposed evaluation set is not a blind benchmark. The original historical reports lacked tested-run metadata; this evidence describes the fresh source-pinned replays instead. Group discussion and supervisor approval remain pending.
