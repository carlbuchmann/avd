# evpn_prevent_readvertise_to_server

## Description

Configure route-map on eBGP sessions towards route-servers, where prefixes with the peer's ASN in the AS Path are filtered away.<br>This is very useful in very large scale networks, where convergence will be quicker by not having to return all updates received<br>from Route-server-1 to Router-server-2 just for Route-server-2 to throw them away because of AS Path loop detection.<br>

## Variables

| Variable | Type | Required | Default | Value Restrictions | Description |
| -------- | ---- | -------- | ------- | ------------------ | ----------- |
| evpn_prevent_readvertise_to_server | Boolean |  | False |  | EVPN Prevent Readvertise to Server |

## YAML

```yaml
evpn_prevent_readvertise_to_server: <bool>
```