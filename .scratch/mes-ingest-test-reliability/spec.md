# MesIngest Test Reliability

Status: ready-for-agent

## Problem

MesIngest 的 Host/API 契约测试包含依赖真实日历推进的夹具。测试可能在业务行为未变化时跨过 GONE 24 小时或 ChangeFeed 48 小时边界而失败。

## Scope

- Host 的生产运行继续使用真实系统 UTC，测试可以用同一个可控时钟验证 Demand、DemandChangeFeed 与 Bootstrap 时间契约。
- MesIngest Release 时间契约测试不依赖执行当天日期。

## Non-goals

- 不改变 GONE 默认最近 24 小时、所有 VISIBLE 永远可见或 ChangeFeed 默认保留 48 小时的业务契约。
- 不改变正式只读 GET API。

## Issues

- `issues/01-deterministic-host-api-clock.md`
- `issues/02-canonical-openapi-line-endings.md`
