# evpn_ebgp_gateway_multihop

## Description

Default of 15, considering a large value to avoid BGP reachability issues in very complex DCI networks.<br>Adapt the value for your specific topology.<br>

## Variables

| Variable | Type | Required | Default | Value Restrictions | Description |
| -------- | ---- | -------- | ------- | ------------------ | ----------- |
| <pre>evpn_ebgp_gateway_multihop | Integer |  | 15 |  | EVPN Gateway EBGP Multihop |

## YAML

```yaml
evpn_ebgp_gateway_multihop: <int>
```