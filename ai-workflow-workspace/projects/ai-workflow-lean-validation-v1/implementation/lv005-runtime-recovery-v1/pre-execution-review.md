# Pre-Execution Adversarial Review

## Findings First

- Corrected before runtime: the initial harness draft lacked an actual timeout/descendant control. Added a sandboxed delayed-write child; a timeout result requires the delayed write to remain absent. This is supporting process evidence, not a model/tool outcome.
- Known stop condition: macOS may refuse nested sandbox initialization. No unsandboxed CLI fallback is allowed; any authorized platform escalation must still execute the identical default-deny profile.
- Known limitation: the CLI preview may use a non-wire schema. It is rejected rather than interpreted as clean; any adapter must map observed fields explicitly and preserve absent-field failures.
- Local policy compile probe corrected numeric loopback syntax to the required SBPL `localhost:port` token. The provider remains bound to 127.0.0.1; no non-loopback allowance added. Earlier failed runs are preserved.
- Apple `/System/Library/Sandbox/Profiles/system.sb` distinguishes `file-map-executable` from file reads. Added mappings only for the same already-allowed immutable runtime/system paths, and access to inherited output pipes with stdin fixed to `/dev/null`; no private paths or auth services added.
- An attempted addition of Apple's broad standalone-policy bootstrap/syscall primitives was rejected by platform auto-review before execution. Both additions were removed; no workaround or weaker CLI runtime executed. This remains a runtime-isolation blocker requiring a separately approved safe method.
- No unresolved harness policy blocker identified before execution. Runtime/context readiness is unproven, not assumed.

## Producer-Consumer Audit

| Producer | Consumer | Mapping and rejected case |
| --- | --- | --- |
| Pinned binary, source, config, env | Runtime freeze | Exact version/hash; changed binary/source blocks result |
| OS policy | CLI and deterministic commands | Private content reads, keychain service access and all non-allowlisted network denied; only synthetic files and loopback sink allowed |
| Preview JSON | Context detector | Instructions, input, roles, text types, model/reasoning, tools all required; unknown shape is not empty success |
| Sink POST | Context comparison | Exact endpoint, bounded body, required fields, one request, auth-header presence; invalid/missing/duplicate input blocks result |
| Child process | Permission/capability checks | Actual synthetic file and exact stdout required; exit zero alone insufficient |
| Timeout process group | Cleanup evidence | SIGTERM/SIGKILL own process group, delayed descendant write absent; no broad process kill |
| Redacted summary | Advisory readiness | No raw context/header values; offline readiness never supplies authentication, behavior score or formal PASS |

## Adversarial Matrix

- Clean synthetic request accepted; missing/malformed input rejected.
- Ambient skills/global AGENTS/memory/app context/host paths and unknown input text rejected.
- Safe requested probe plus hidden foreign context rejected, including extra developer input.
- Unexpected/duplicate tools, invalid content types or roles rejected.
- Authorization, proxy authorization, API-key and cookie header names rejected without persisting values.
- Preview/exec base instructions, context hashes, roles or tool schemas differ: blocked.
- Process exits zero without actual output: blocked.
- Timeout and descendants: independently tested, never inferred from a CLI claim.
- Custom sink HTTP 400 is deliberate, not a hosted-model service failure.

## Intent And Review Completeness

- Intent/plan/scope: aligned with owner-approved offline-only preparation.
- Artifact QA: current whole-harness source review before the first runtime probe.
- Instruction baseline: current after full refresh; baseline HEAD 0c767da, tracked tree clean.
- Policy-boundary adversarial matrix and producer-consumer audit: completed for preparation detector/policy; runtime outcomes pending.
- Adaptive matrix: context -> canonical request summary -> compared hashes; file/network actions -> observed output/denial -> capability evidence; timeout -> process cleanup -> no delayed output. Forbidden states are context leakage, credential-bearing transport, non-loopback access, guessed outputs and behavioral readiness claims.
- Automated evidence role: supporting-only.
- Closure freshness: current for pre-execution source; final whole-harness review required after probes/fixes.
