# isis_ti_lfa

## Description

None

## Variables

| Variable | Type | Required | Default | Value Restrictions | Description |
| -------- | ---- | -------- | ------- | ------------------ | ----------- |
| isis_ti_lfa | Dictionary |  |  |  | ISIS TI-LFA |
|   enabled | Boolean |  | False |  |  |
|   protection | String |  |  | Valid Values:<br>- link<br>- node |  |
|   local_convergence_delay | Integer |  | 10000 |  | Local convergence delay in mpls |

## YAML

```yaml
isis_ti_lfa:
  enabled: <bool>
  protection: <str>
  local_convergence_delay: <int>
```