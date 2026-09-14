# Vertical Batch Adoption

This repository adopts the portfolio-wide canonical batch standard maintained in `darrinbaldwindev/Overseer` while preserving the established MyPrimeDelivery batch history under `docs/overseer/batches/`.

Read in order before every vertical execution cycle:
1. `darrinbaldwindev/Overseer/.overseer/doctrine/PORTFOLIO-BATCH-ENGINE.md`
2. `darrinbaldwindev/Overseer/.overseer/profiles/PROJECT-BATCH-PROFILES.md` — MyPrimeDelivery profile
3. `darrinbaldwindev/Overseer/.overseer/doctrine/VERTICAL-BATCH-EXECUTION.md`
4. current MyPrimeDelivery batch/result files under `docs/overseer/batches/`
5. current repo/PR/CI/research evidence and Overseer #49.

The central engine is the procedure. The project profile is the customization layer. Existing batch files contain project state/history and are not a fork of the common procedure. Central engine/profile changes apply on the next fresh cycle.

Owner `cont` / `continue autonomously` triggers the full fresh-scan → reconcile → execute → verify → fresh-scan → replenish → durable-log cycle.