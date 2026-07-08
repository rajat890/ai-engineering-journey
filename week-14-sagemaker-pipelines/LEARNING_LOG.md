## Week 14: SageMaker Pipelines — Process → Train → Evaluate → Gate

Built a 4-step SageMaker Pipeline in local mode (Docker), orchestrating an
existing training script into a repeatable, versioned workflow with an
automated accuracy gate.

**What each file does:**

| File | Step | Purpose |
|---|---|---|
| `preprocessing.py` | PreprocessData | Splits raw data 80/20, stratified by label |
| `train.py` | TrainModel | Fits `CountVectorizer` + `MultinomialNB` (unchanged from Week 13, one path fix) |
| `evaluate.py` | EvaluateModel | Scores the model against the held-out 20%; writes `evaluation.json` |
| `register_model.py` | RegisterModelPlaceholder | Placeholder "pass" action — proves the gate's pass branch fires; real Model Registry registration deferred |
| `pipeline.py` | — | Defines all steps, their dependencies, and the pass/fail gate; the file you actually run |

**Pipeline flow:**

```
 [pipeline.py defines this DAG]

 PreprocessData  →  TrainModel  →  EvaluateModel  →  CheckAccuracyThreshold
 (80/20 split)      (fit model)    (score on test)        │
                                                    ┌───────┴───────┐
                                              accuracy ≥ 0.7?   accuracy < 0.7?
                                                    │                │
                                          RegisterModelPlaceholder  AccuracyBelowThreshold
                                             (pass -- placeholder)   (fail -- halts pipeline,
                                                                      execution status = FAILED)

 S3 sits underneath every arrow above: each step writes its output to S3,
 the next step reads its input from S3 -- even though compute runs locally.
```

**Key learnings:**

- **Pipeline step hand-offs (`step.properties`) require real S3**, even when
  compute runs entirely in local Docker — only the actual script execution
  is local; data hand-offs between steps are not.
- **Training artifacts are always packaged as `model.tar.gz`** — a downstream
  step must extract the tarball before it can load `model.pkl`/`vectorizer.pkl`.
- **`ConditionStep` has no container or job of its own** — it's pure
  orchestrator logic (compare a value, pick a branch). This is why it didn't
  appear in `list_steps()` output until a real action existed on at least one
  branch to observe — an empty branch running "successfully" is
  indistinguishable from not running at all.
- **`PropertyFile` + `JsonGet`** let a later step read a specific value out of
  an earlier step's JSON output (e.g. `classification_metrics.accuracy.value`)
  without writing manual S3-download-and-parse code — resolved automatically
  at execution time.
- **Confirmed the gate works end-to-end**: the model's actual accuracy
  (0.667) correctly failed against a 0.7 threshold, and the *pipeline
  execution's overall status* reflected `FAILED` — not just a quietly bad
  number buried in a log. This is the same shape as a CI pipeline failing a
  build when tests don't pass.