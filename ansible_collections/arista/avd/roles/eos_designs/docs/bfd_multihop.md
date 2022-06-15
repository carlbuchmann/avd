# bfd_multihop

## Description

None

## Variables

| Variable | Type | Required | Default | Value Restrictions | Description |
| -------- | ---- | -------- | ------- | ------------------ | ----------- |
| bfd_multihop | Dictionary |  |  |  | BFD Multihop tunning |
|   interval | Integer |  | 300 |  |  |
|   min_rx | Integer |  | 300 |  |  |
|   multiplier | Integer |  | 3 |  |  |

## YAML

```yaml
bfd_multihop:
  interval: <int>
  min_rx: <int>
  multiplier: <int>
```