# evpn_import_pruning

## Description

Enable VPN import pruning (Min. EOS 4.24.2F)<br>The Route Target extended communities carried by incoming VPN paths will<br>be examined. If none of those Route Targets have been configured for import,<br>the path will be immediately discarded<br>

## Variables

| Variable | Type | Required | Default | Value Restrictions | Description |
| -------- | ---- | -------- | ------- | ------------------ | ----------- |
| <code>evpn_import_pruning</code>| Boolean |  | False |  | EVPN Import Pruning |

## YAML

```yaml
evpn_import_pruning: <bool>
```