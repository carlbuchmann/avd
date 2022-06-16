# evpn_hostflap_detection

## Description

None

## Variables

| Variable | Type | Required | Default | Value Restrictions | Description |
| -------- | ---- | -------- | ------- | ------------------ | ----------- |
| <code>evpn_hostflap_detection</code>| Dictionary |  |  |  | EVPN Host Flapping Settings |
| <code>&nbsp;&nbsp;enabled</code>| Boolean |  | True |  | If set to false it will disable EVPN host-flap detection |
| <code>&nbsp;&nbsp;threshold</code>| Integer |  | 5 |  | Minimum number of MAC moves that indicate a MAC duplication issue |
| <code>&nbsp;&nbsp;window</code>| Integer |  | 180 |  | Time (in seconds) to detect a MAC duplication issue |
| <code>&nbsp;&nbsp;expiry_timeout</code>| Integer |  |  |  | Time (in seconds) to purge a MAC duplication issue |

## YAML

```yaml
evpn_hostflap_detection:
  enabled: <bool>
  threshold: <int>
  window: <int>
  expiry_timeout: <int>
```