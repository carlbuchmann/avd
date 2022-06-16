# vtep_vvtep_ip

## Description

IP Address used as Virtual VTEP. Will be configured as secondary IP on loopback1<br>This is only needed for centralized routing designs<br>

## Variables

| Variable | Type | Required | Default | Value Restrictions | Description |
| -------- | ---- | -------- | ------- | ------------------ | ----------- |
| vtep_vvtep_ip | String |  |  | Format: ipv4_cidr | Virtual VTEP IP |

## YAML

```yaml
vtep_vvtep_ip: <str>
```