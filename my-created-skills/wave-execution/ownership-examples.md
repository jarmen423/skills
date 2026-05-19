# Ownership Examples

Use these examples when deciding whether a parallel split is safe.

## Safe Splits

### Research/docs vs implementation

- Thread A:
  - `.planning/research/**`
- Thread B:
  - `src/core/**`

Reason:

- documentation and implementation code are disjoint write scopes

### UI vs data layer

- Thread A:
  - `src/ui/**`
- Thread B:
  - `src/services/**`

Reason:

- UI and service layer are separate, assuming the shared interface/schema is already stable

### Two independent packages or modules

- Thread A:
  - `packages/auth/**`
- Thread B:
  - `packages/billing/**`

Reason:

- distinct package boundaries with no shared files, assuming cross-package contracts are locked

### Config/calibration vs validation logic

- Thread A:
  - `config/defaults.json`
- Thread B:
  - `src/validators/**`

Reason:

- safe only if Thread B does not depend on config shape still being finalized

## Unsafe Splits

### Shared root module

- Thread A:
  - `src/services/repository.ts`
- Thread B:
  - `src/services/repository.ts`

Reason:

- direct collision

### Shared types or contracts file

- Thread A:
  - `src/types/index.ts`
- Thread B:
  - `src/types/index.ts`

Reason:

- direct collision and moving schema target

### Semantically coupled files

- Thread A:
  - `config/schema.json`
- Thread B:
  - `src/validators/schema-validator.ts`

Reason:

- looks safe (different files) but is not — the validator depends on the schema shape; if the schema is still moving, the validator work is invalidated

## Practical Rule

If one thread changing meaning can invalidate the other thread's work, the split is not yet safe even if the files differ.

Examples:

- shared types vs modules consuming those types
- API contract vs UI calling that API
- config schema vs logic reading that config
- data shape vs validation rules for that shape

Lock the contract first, then split the downstream work.
