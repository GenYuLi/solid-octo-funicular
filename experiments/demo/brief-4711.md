# Tier 0 brief — demo/issue-4711.txt

## Anchors
- [quoted] `downcast_ref`
- [path] `src/backtrace.rs`
- [symbol] `Chain::next`
- [call] `context`
- [call] `backtrace`
- [env] `RUST_LIB_BACKTRACE`
- [env] `RUST_BACKTRACE`
- [version] `1.0.86`
- [version] `1.0.104`

## Suspect regions (top 4, score = anchor 多樣性 + 命中數 + 近期被動過)
- **src/lib.rs** — score 55, 4 種 anchor 命中, 31 天前被動過
    - L124 (`downcast_ref`): //!   match root_cause.downcast_ref::<DataStoreError>() {
    - L406 (`downcast_ref`): ///         if let Some(io_error) = cause.downcast_ref::<io::Error>() {
    - L567 (`downcast_ref`): ///         if let Some(e) = err.downcast_ref::<SuspiciousError>() {
    - recent: 1dbe186 2026-07-18 Release 1.0.104
    - recent: 5bdb0e2 2026-06-25 Release 1.0.103
- **src/backtrace.rs** — score 53, 2 種 anchor 命中, 180 天前被動過
    - L2 (`backtrace`): pub(crate) use std::backtrace::Backtrace;
    - L8 (`backtrace`): macro_rules! backtrace {
    - L10 (`backtrace`): Some(std::backtrace::Backtrace::capture())
    - recent: 7fe62b5 2026-02-19 Further simply backtrace conditional compilation
    - recent: efdb11a 2026-02-19 Simplify `std_backtrace` conditional code
- **src/error.rs** — score 49, 3 種 anchor 命中, 54 天前被動過
    - L432 (`downcast_ref`): ///         if let Some(io_error) = cause.downcast_ref::<io::Error>() {
    - L468 (`downcast_ref`): self.downcast_ref::<E>().is_some()
    - L530 (`downcast_ref`): /// match root_cause.downcast_ref::<DataStoreError>() {
    - recent: 6e8c000 2026-06-25 Eliminate pointer->reference->pointer during downcast
    - recent: 7fe62b5 2026-02-19 Further simply backtrace conditional compilation
- **tests/test_context.rs** — score 16, 1 種 anchor 命中, 54 天前被動過
    - L97 (`downcast_ref`): fn test_downcast_ref() {
    - recent: 67c4abd 2026-06-25 Add regression test for issue 451
    - recent: a1a87a6 2021-10-07 Clean up unused field warning in test suite

## git log -S 考古(誰引入/移除過這些字串)
- `downcast_ref`:
    - 67c4abd 2026-06-25 Add regression test for issue 451
    - e1a2017 2025-04-13 Add 2 different conversions to Box<dyn Error + Send + Sync + 'static>
    - 87fdd9e 2021-01-06 Allow running tests under miri
- `context`:
    - 67c4abd 2026-06-25 Add regression test for issue 451
    - a42fc2c 2026-02-19 Remove `feature = "backtrace"` conditional code
    - b155115 2025-12-12 Remove support for compilers without ptr::addr_of
- `backtrace`:
    - 7fe62b5 2026-02-19 Further simply backtrace conditional compilation
    - de27df7 2026-02-19 Delete CI use of --features=backtrace
    - efdb11a 2026-02-19 Simplify `std_backtrace` conditional code
- `RUST_LIB_BACKTRACE`:
    - a42fc2c 2026-02-19 Remove `feature = "backtrace"` conditional code
    - 0ba6408 2021-03-19 Add stable backtrace feature
    - 4bebd2a 2020-03-14 Explain backtrace env variable combinations
- `RUST_BACKTRACE`:
    - a42fc2c 2026-02-19 Remove `feature = "backtrace"` conditional code
    - 0ba6408 2021-03-19 Add stable backtrace feature
    - 4bebd2a 2020-03-14 Explain backtrace env variable combinations
