# Cloud GPU RAG Runbook

This runbook covers short-lived Vast and RunPod staging runs for the OARC RAG gateway.

Cloud GPU runs are for iteration and acceptance evidence. They do not replace the final HPC
promotion gate. The default workflow builds a public-corpus FAISS index locally, transfers only an
audited runtime bundle plus that index, starts vLLM and the RAG gateway on remote loopback, tunnels
the gateway back to the laptop, runs the acceptance harness, and destroys provider-created compute.

## What Is Automated

- Provider selection defaults to RunPod with an RTX 4090 for 7B-class models and A100 for larger
  models. Vast can search for a matching RTX 4090/A100 offer or use `--vast-offer-id`.
- RunPod Pods use the official `runpod-torch-v280` template by default, expose `22/tcp` for SSH,
  and set a three-hour `--terminate-after` safety window in addition to runner cleanup.
- The public FAISS index can be built locally with `--build-index`; ServiceNow is forced to
  `/dev/null` for this path.
- The transfer bundle uses an allowlist plus a blocklist. `.env*`, `.git`, `.venv`, `logs/`,
  `mlruns/`, `models/`, `results/`, `runtime/`, and `docs/servicenow` are blocked.
- Targeted reruns can pass repeated `--question-id` values, and deliberate review runs can pass
  `--include-full-answer` so `results.jsonl` stores complete generated answers instead of excerpts.
- Created RunPod Pods are deleted with `runpodctl pod delete`; created Vast instances are destroyed
  with `vastai destroy instance` unless `--keep-instance` is explicitly passed.
- Each executed cloud run writes `cloud_run_ledger.json` and `cloud_run_ledger.md` next to the
  acceptance artifacts, including start/end balance, provider resource ID, requested GPU, runtime,
  estimated cost, cleanup status, and artifact paths.
- Cloud wrapper runs default to provider-specific output roots, for example
  `logs/rag_v1_acceptance/cloud/runpod/<timestamp>/`.
- Manual review is narrowed to rows where hard checks pass but expected answer topics or expected
  source hints are missing.

## Not Automated

- Installing `runpodctl` or `vastai`.
- Creating or funding provider accounts.
- Verifying provider CLI authentication, because that can expose account details in terminal output.
- Judging whether newly drafted candidate questions are good enough to promote into the main gate.

## Cost And Runtime Estimate

As of July 30, 2026, public pricing pages list RunPod RTX 4090 rates around `$0.34` to `$0.69` per
GPU-hour, RunPod A100 PCIe from about `$1.39` per GPU-hour, and Vast RTX 4090 marketplace offers
from about `$0.13` per GPU-hour with a live median around `$0.36`. Check live prices before launch;
storage, network volumes, bandwidth, and stopped-but-not-destroyed resources can add cost.

Expected wall clock for the default `Qwen/Qwen2.5-7B-Instruct` path:

| Run type | First run | Warm rerun | GPU cost ballpark |
| --- | ---: | ---: | ---: |
| 3-question smoke | 30-60 min | 10-25 min | `$0.10-$0.70` on 4090-class GPUs |
| Full 18-question gate | 45-90 min | 20-45 min | `$0.20-$1.50` on 4090-class GPUs |
| Candidate suite | 45-120 min | 25-60 min | depends on selected question count |

First runs spend most time on image start, dependency install, model download, and local index build.
A100-class runs are mainly for larger models; use them only when the model will not fit on a 24 GB
4090.

## Preflight

Keep API keys outside this repo. The provider CLIs should read their own user config or environment;
do not place keys in `.env` files that might be bundled.

```bash
runpodctl --help
vastai --help
```

Provider setup commands, run outside the repo if needed:

```bash
runpodctl config --apiKey "$RUNPOD_API_KEY"
runpodctl ssh add-key --key-file ~/.runpod/ssh/runpodctl-ssh-key.pub
vastai set api-key "$VAST_API_KEY"
vastai create ssh-key ~/.ssh/id_ed25519.pub
```

If RunPod does not currently list RTX 4090 capacity, use a 7B-class fallback such as:

```bash
.venv/bin/python scripts/evaluation/run_cloud_acceptance.py \
  --provider runpod \
  --runpod-gpu "NVIDIA A40" \
  --build-index \
  --execute
```

## Dry-Run Plan

Build the local public index and print the RunPod plan without launching paid compute:

```bash
.venv/bin/python scripts/evaluation/run_cloud_acceptance.py \
  --provider runpod \
  --build-index \
  --full-acceptance
```

Print a Vast plan. Without `--vast-offer-id`, the plan shows the search command that will be used at
execution time.

```bash
.venv/bin/python scripts/evaluation/run_cloud_acceptance.py \
  --provider vast \
  --build-index \
  --full-acceptance
```

Use an already-running SSH host without creating or deleting provider compute:

```bash
.venv/bin/python scripts/evaluation/run_cloud_acceptance.py \
  --provider existing \
  --ssh-target root@example-host \
  --ssh-port 22022 \
  --full-acceptance
```

## Run The Cloud Loop

Run a three-question RunPod smoke. The instance is deleted after the harness exits or fails:

```bash
.venv/bin/python scripts/evaluation/run_cloud_acceptance.py \
  --provider runpod \
  --build-index \
  --execute
```

Run a targeted advisory subset and keep complete answer transcripts:

```bash
.venv/bin/python scripts/evaluation/run_cloud_acceptance.py \
  --provider runpod \
  --execute \
  --include-full-answer \
  --question-id amarel_login \
  --question-id amarel_storage \
  --question-id amarel_modules \
  --question-id amarel_data_transfer \
  --question-id support_helpdesk \
  --question-id support_allocations \
  --question-id support_onboarding
```

Run the full active acceptance gate:

```bash
.venv/bin/python scripts/evaluation/run_cloud_acceptance.py \
  --provider runpod \
  --build-index \
  --execute \
  --full-acceptance \
  --include-full-answer
```

Run the same path on Vast with an explicit offer:

```bash
.venv/bin/python scripts/evaluation/run_cloud_acceptance.py \
  --provider vast \
  --vast-offer-id <offer-id> \
  --build-index \
  --execute \
  --full-acceptance
```

Run the candidate question suite instead of the active gate:

```bash
.venv/bin/python scripts/evaluation/run_cloud_acceptance.py \
  --provider runpod \
  --build-index \
  --execute \
  --questions data/evaluation/acceptance/rag_v1_candidate_questions.jsonl \
  --full-acceptance
```

The default vector-mode gateway also enables the local-guide fallback from the FAISS docstore for
selected local-policy questions. This keeps cloud transfers limited to the source bundle plus
prebuilt public FAISS index while improving source recall for Amarel access, Open OnDemand,
`/scratch`, job-array, owned-resource, login-node, and interactive `srun` questions. Disable it for
an ablation with `RAG_LOCAL_GUIDE_FALLBACK_ENABLED=false` in the remote environment.

Run a hybrid retrieval benchmark against the active gate:

```bash
.venv/bin/python scripts/evaluation/run_cloud_acceptance.py \
  --provider runpod \
  --execute \
  --retrieval-mode hybrid \
  --full-acceptance \
  --include-full-answer
```

Run the synthetic attachment row on RunPod. This starts the remote gateway with
`RAG_UI_ATTACHMENTS_ENABLED=true`, uses only generated non-sensitive attachment text, and lets the
browser UI's generated `sample-attachment.md` control be tested through the same private tunnel:

```bash
.venv/bin/python scripts/evaluation/run_cloud_acceptance.py \
  --provider runpod \
  --execute \
  --enable-ui-attachments \
  --question-id attachment_synthetic_marker \
  --include-full-answer
```

## Question Suites

The active suite is `data/evaluation/acceptance/rag_v1_questions.jsonl` and currently covers Slurm,
Amarel access, support policy, safety refusals, and synthetic attachments.

The candidate suite is `data/evaluation/acceptance/rag_v1_candidate_questions.jsonl`. It adds
reviewed candidates for login-node policy, access rules, Open OnDemand, storage quotas, file
transfer, interactive Slurm usage, community software support, owned resources, and Research Data
Finder topics.

## SSH Host Keys

Cloud pods and instances are short-lived and provider IPs/ports can be recycled. The cloud runner
uses per-resource known-hosts files under `runtime/cloud_acceptance/known_hosts/` instead of the
user's global `~/.ssh/known_hosts`. This avoids recycled-host-key collisions while keeping
`StrictHostKeyChecking=accept-new` for each individual resource.

Draft more candidates from approved Markdown roots:

```bash
.venv/bin/python scripts/evaluation/draft_acceptance_questions.py \
  --max-questions 40 \
  --output data/evaluation/acceptance/rag_v1_candidate_questions.generated.jsonl
```

The drafter is deterministic and offline. It skips `docs/servicenow` and writes source excerpts so
the rows can be reviewed before promotion. Promote only rows with clear expected topics, a source
hint that appears in returned source metadata, and a non-sensitive source excerpt.

Keep the active 18-question suite as the blocking promotion gate. Use the larger candidate suite for
non-blocking regression and coverage work until candidates are repeatable enough to promote.

## Run Artifacts

Executed cloud runs write the usual acceptance files under provider-specific roots such as
`logs/rag_v1_acceptance/cloud/runpod/<timestamp>/`:

- `results.jsonl`: per-question evidence; includes full `answer` values only when
  `--include-full-answer` is passed.
- `summary.json`: machine-readable gate metrics and artifact paths.
- `report.md`: human-review summary.
- `plots/`: report-associated SVG charts for latency, time to first token, and source counts.
- `cloud_run_ledger.json`: provider ledger with start/end balance, resource ID, requested GPU,
  runtime, estimated cost, cleanup status, question IDs, and artifact paths.
- `cloud_run_ledger.md`: compact ledger summary for quick review.

## Live UI Screenshot

The gateway-hosted `/ui` is the same assistant-ui React app used locally, on Mac mini, and through
cloud tunnels. A live RunPod screenshot is useful for visual evidence that the browser UI, SSH
tunnel, FastAPI gateway, vLLM model, and source/metadata inspector are wired together.

Use a short-lived RunPod pod, keep it alive only for the screenshot window, open the tunneled
`http://127.0.0.1:<local-gateway-port>/ui`, send one non-sensitive acceptance-style question, and
capture the browser image after the answer and sources render. Delete the pod immediately after the
capture. The screenshot is not an accuracy gate; use `summary.json`, `report.md`, `results.jsonl`,
plots, and `cloud_run_ledger.md` for performance, cost, and promotion evidence.

## Manual Review

Manual review is needed for:

- candidate questions before they become part of the main gate;
- acceptance rows listed in `manual_review_question_ids`;
- any safety row that passes automated string checks but sounds permissive or speculative;
- any run where the retrieved sources are non-empty but visibly wrong.

For stable promotion, compare at least two full runs:

```bash
.venv/bin/python scripts/evaluation/run_v1_acceptance.py \
  --compare-runs logs/rag_v1_acceptance/<run-a> logs/rag_v1_acceptance/<run-b>
```

## Troubleshooting

`runpodctl pod create` returning `graphql error: Unauthorized` means the CLI key can authenticate
but is not allowed to create Pods for the account or role. Create or select a RunPod API key with
Pod deployment permissions, configure it with `runpodctl config --apiKey`, then rerun the smoke.
This failure happens before transfer, so no repository bundle or FAISS index is uploaded.

If `ssh info` points at `~/.runpod/ssh/runpodctl-ssh-key` but SSH fails with
`Permission denied (publickey,password)`, register that generated public key with:

```bash
runpodctl ssh add-key --key-file ~/.runpod/ssh/runpodctl-ssh-key.pub
```

The runner waits for RunPod SSH readiness, accepts new host keys non-interactively, pins
`transformers>=4.48.2,<5` for the current vLLM 0.7.x path, and sends one direct warmup completion
before measuring acceptance TTFT.

## References

- Vast CLI workflow: <https://docs.vast.ai/cli/hello-world>
- Vast instance creation: <https://docs.vast.ai/cli/reference/create-instance>
- Vast live pricing: <https://vast.ai/pricing>
- RunPod Pod management: <https://docs.runpod.io/pods/manage-pods>
- RunPod `runpodctl pod` reference: <https://docs.runpod.io/runpodctl/reference/runpodctl-pod>
- RunPod GPU pricing: <https://www.runpod.io/pricing>
- vLLM on RunPod: <https://docs.vllm.ai/en/latest/deployment/frameworks/runpod/>
