# isis_ti_lfa

## Description

None

## Variables

| Variable | Type | Required | Default | Value Restrictions | Description |
| -------- | ---- | -------- | ------- | ------------------ | ----------- |
| <code>isis_ti_lfa</code>| Dictionary |  |  |  | ISIS TI-LFA |
| <code>&nbsp;&nbsp;enabled</code>| Boolean |  | False |  |  |
| <code>&nbsp;&nbsp;protection</code>| String |  |  | Valid Values:<br>- link<br>- node |  |
| <code>&nbsp;&nbsp;local_convergence_delay</code>| Integer |  | 10000 |  | Local convergence delay in mpls |

## YAML

```yaml
isis_ti_lfa:
  enabled: <bool>
  protection: <str>
  local_convergence_delay: <int>
```