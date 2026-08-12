# Ticket 01 test implementation plan

## Vertical TDD slices

| Slice | Test | Ticket evidence |
| --- | --- | --- |
| 1 | `First_success_round_is_read_back_with_atomic_series_demand_and_round_evidence` | Requirements 1, 2, 5, and the Round -> Host interface -> real SQL -> HTTP portion of 6 |
| 2 | `Equivalent_success_round_preserves_identity_and_does_not_append_business_events` | Requirement 3 |
| 3 | `Restarted_host_reads_the_same_persisted_projection` | Requirement 4 |

## Planned production files

- Core model/contract/interface under the isolated `MesIngest.Core/SeriesProjection` namespace.
- New `MesIngest.Infrastructure` project containing the `[mesingest]` SQL Server adapter and schema only.
- Host composition plus isolated `/api/v2` read-only endpoint/DTO files.
- `MesIngest.Tests/NewSuccessRoundTracerSpineTests.cs` and a strictly owned disposable SQL Server database helper.

## Verification

- Each slice: demonstrate red, implement only enough production behavior, then rerun the filtered class.
- Re-open every assertion and run a test-gap/assertion-quality review after green.
- Run full non-incremental Release build, full Release suite, and the real SQL Server tracer gate with zero skips.
- Record requirement-to-test evidence in `.testagent/status.md` and the final response.
