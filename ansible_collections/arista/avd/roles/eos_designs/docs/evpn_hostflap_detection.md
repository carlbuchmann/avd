# evpn_hostflap_detection

## Description

None

## Variables

| Variable | Type | Required | Default | Value Restrictions | Description |
| -------- | ---- | -------- | ------- | ------------------ | ----------- |
| <pre>evpn_hostflap_detection | Dictionary |  |  |  | EVPN Host Flapping Settings |
| <pre>  enabled | Boolean |  | True |  | If set to false it will disable EVPN host-flap detection |
| <pre>  threshold | Integer |  | 5 |  | Minimum number of MAC moves that indicate a MAC duplication issue |
| <pre>  window | Integer |  | 180 |  | Time (in seconds) to detect a MAC duplication issue |
| <pre>  expiry_timeout | Integer |  |  |  | Time (in seconds) to purge a MAC duplication issue |

## YAML

```yaml
evpn_hostflap_detection:
  enabled: <bool>
  threshold: <int>
  window: <int>
  expiry_timeout: <int>
```