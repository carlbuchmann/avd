# bgp_peer_groups

## Description

Leverage an Arista EOS switch to generate the encrypted password using the correct peer group name.<br>Note that the name of the peer groups use '-' instead of '_' in EOS configuration.<br>

## Variables

| Variable | Type | Required | Default | Value Restrictions | Description |
| -------- | ---- | -------- | ------- | ------------------ | ----------- |
| bgp_peer_groups | Dictionary |  |  |  | BGP peer group names and encrypted password |
|   ipv4_underlay_peers | Dictionary |  |  |  |  |
|     name | String |  | IPv4-UNDERLAY-PEERS |  |  |
|     password | String |  |  |  | Encrypted Password |
|   mlag_ipv4_underlay_peer | Dictionary |  |  |  |  |
|     name | String |  | MLAG-IPv4-UNDERLAY-PEER |  |  |
|     password | String |  |  |  | Encrypted Password |
|   evpn_overlay_peers | Dictionary |  |  |  |  |
|     name | String |  | EVPN-OVERLAY-PEERS |  |  |
|     password | String |  |  |  | Encrypted Password |
|   evpn_overlay_core | Dictionary |  |  |  |  |
|     name | String |  | EVPN-OVERLAY-CORE |  |  |
|     password | String |  |  |  | Encrypted Password |
|   IPv4_UNDERLAY_PEERS | Dictionary |  |  |  |  |
|     name | String |  | IPv4-UNDERLAY-PEERS |  |  |
|     password | String |  |  |  | Encrypted Password |
|   MLAG_IPv4_UNDERLAY_PEER | Dictionary |  |  |  |  |
|     name | String |  | MLAG-IPv4-UNDERLAY-PEER |  |  |
|     password | String |  |  |  | Encrypted Password |
|   EVPN_OVERLAY_PEERS | Dictionary |  |  |  |  |
|     name | String |  | EVPN-OVERLAY-PEERS |  |  |
|     password | String |  |  |  | Encrypted Password |

## YAML

```yaml
bgp_peer_groups:
  ipv4_underlay_peers:
    name: <str>
    password: <str>
  mlag_ipv4_underlay_peer:
    name: <str>
    password: <str>
  evpn_overlay_peers:
    name: <str>
    password: <str>
  evpn_overlay_core:
    name: <str>
    password: <str>
  IPv4_UNDERLAY_PEERS:
    name: <str>
    password: <str>
  MLAG_IPv4_UNDERLAY_PEER:
    name: <str>
    password: <str>
  EVPN_OVERLAY_PEERS:
    name: <str>
    password: <str>
```