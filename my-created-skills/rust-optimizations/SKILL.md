---

Elite Rust optimizer — supercharges Rust code for maximum speed using profiling, zero-cost mastery, PGO, SIMD, and advanced memory tricks. Trigger on optimize my Rust, make it faster, benchmark this, flamegraph analysis, or elite performance review.
---

# Elite Rust Optimizer

## Overview

This skill turns solid Rust into screaming-fast production code. It mandates a scientific approach: profile first, optimize second, exploit zero-cost abstractions while surgically removing hidden costs in allocations, indirection, and missed vectorization opportunities. No guessing. No premature optimization. Pure measured gains.

## Mandatory Workflow (Execute in Order — No Exceptions)

1. **Baseline Everything**  
   Add `criterion = { version = "0.5", features = ["html_reports"] }` to `[dev-dependencies]`. Write `[[bench]]` entries. Run `cargo bench`. Record mean, std dev, and throughput. This is your truth. Anything else is fan fiction.

2. **Profile Like a God**  
   Use `cargo install flamegraph` then `cargo flamegraph --bench <name> -- --bench`. Or `perf record -F 997 --call-graph dwarf cargo run --release -- <args>`. Generate flamegraphs. The widest stacks are your targets. 80/20 rule is law here.

3. **Apply High-Impact Optimizations** (ranked by typical ROI)
   
   **Allocation Elimination**  
   
   - Never `.clone()` in hot paths. Use `&T`, `Cow<'_, str>`, or `Rc`/`Arc` only when truly shared.  
   - Tiny collections → `SmallVec<[T; 8]>` or `arrayvec`.  
   - Short-lived objects → `bumpalo::Bump` or `typed_arena`.  
   - Global allocator → `mimalloc` or `jemallocator` via `#[global_allocator]`.
   
   **Loop & Iterator Mastery**  
   Iterators are zero-cost *when they vectorize*. If not, rewrite as explicit indexed loops with `get_unchecked` (unsafe — wrap in `unsafe {}` and verify with `cargo miri`).  
   Number/string formatting in loops? `itoa` + `ryu` crates beat `format!` by 10-50x.
   
   **SIMD & Vectorization**  
   Nightly: `std::simd` (f32x8, etc.) + `multiversion` for CPU dispatch.  
   Stable: `pulp` or `wide` crates. Auto-vectorization often needs specific loop shapes — inspect with `cargo expand` or godbolt.
   
   **Release Profile (Copy-Paste This)**  
   
   ```toml
   [profile.release]
   opt-level = 3
   lto = "thin"          # or "fat" for smaller binaries
   codegen-units = 1
   panic = "abort"
   strip = true
   ```
   
   **Profile-Guided Optimization (PGO)**  
   For final release binaries: `cargo install cargo-pgo`, then `cargo pgo build --release`. Typical 5-20% gains on real workloads. Do this last.
   
   **Async & Concurrency**  
   
   - Minimize `.await` in hot request paths.  
   - CPU work → `tokio::task::spawn_blocking`.  
   - Runtime tuning: `tokio::runtime::Builder::new_multi_thread().worker_threads(num_cpus::get()).build().unwrap()`.  
   - Locks: `parking_lot` over std::sync for lower contention.
   
   **Unsafe Elite Moves** (Only After Profiling)  
   
   - Zero-copy FFI with raw pointers.  
   - Custom memory layouts (`#[repr(C, packed(1))]`).  
   - Unchecked indexing in verified hot loops.  
   - Always run `cargo miri` and ASAN/TSAN afterward.

4. **Verify & Iterate**  
   After every change: re-bench. If improvement < 3-5% or code becomes unreadable, revert. Use `cargo asm` or `cargo show-asm` to confirm the compiler did what you expected. Micro-optimizations only win when they compound.

5. **Nuclear Options**  
   
   - Full LTO + PGO + BOLT (post-link optimizer) for shipping binaries.  
   - Const generics + const fn for compile-time everything possible.  
   - `rayon` for data-parallel work where Amdahl allows.  
   - Custom global allocators or `allocator_api` on nightly.

## Golden Rules

- Measure before you touch anything.  
- Readability > cleverness unless the profiler says otherwise.  
- Rust's ownership model lets you optimize *aggressively* without segfaults — use that superpower.  
- When in doubt, `cargo expand` and stare at the assembly.

## References & Templates

See `references/` directory for:

- Full Cargo.toml perf template
- Criterion benchmark boilerplate
- PGO walkthrough
- SIMD examples for common patterns (string search, math kernels, etc.)

This skill keeps you in the top 1% of Rust performance engineers. Now go make your code embarrass the competition.