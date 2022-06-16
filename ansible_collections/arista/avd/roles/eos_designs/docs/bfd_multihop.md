# bfd_multihop

## Description

None

## Variables

| Variable | Type | Required | Default | Value Restrictions | Description |
| -------- | ---- | -------- | ------- | ------------------ | ----------- |
| <code>bfd_multihop</code>| Dictionary |  |  |  | BFD Multihop tunning |
| <code>&nbsp;&nbsp;interval</code>| Integer |  | 300 |  |  |
| <code>&nbsp;&nbsp;min_rx</code>| Integer |  | 300 |  |  |
| <code>&nbsp;&nbsp;multiplier</code>| Integer |  | 3 |  |  |

## YAML

```yaml
bfd_multihop:
  interval: <int>
  min_rx: <int>
  multiplier: <int>
```