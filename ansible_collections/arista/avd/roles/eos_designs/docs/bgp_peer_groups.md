# bgp_peer_groups

## Description

Leverage an Arista EOS switch to generate the encrypted password using the correct peer group name.<br>Note that the name of the peer groups use '-' instead of '_' in EOS configuration.<br>

## Variables

| Variable | Type | Required | Default | Value Restrictions | Description |
| -------- | ---- | -------- | ------- | ------------------ | ----------- |
| bgp_peer_groups | Dictionary |  |  |  | BGP peer group names and encrypted password |
| &nbsp;&nbsp;ipv4_underlay_peers | Dictionary |  |  |  |  |
| &nbsp;&nbsp;&nbsp;&nbsp;name | String |  | IPv4-UNDERLAY-PEERS |  |  |
| &nbsp;&nbsp;&nbsp;&nbsp;password | String |  |  |  | Encrypted Password |
| &nbsp;&nbsp;mlag_ipv4_underlay_peer | Dictionary |  |  |  |  |
| &nbsp;&nbsp;&nbsp;&nbsp;name | String |  | MLAG-IPv4-UNDERLAY-PEER |  |  |
| &nbsp;&nbsp;&nbsp;&nbsp;password | String |  |  |  | Encrypted Password |
| &nbsp;&nbsp;evpn_overlay_peers | Dictionary |  |  |  |  |
| &nbsp;&nbsp;&nbsp;&nbsp;name | String |  | EVPN-OVERLAY-PEERS |  |  |
| &nbsp;&nbsp;&nbsp;&nbsp;password | String |  |  |  | Encrypted Password |
| &nbsp;&nbsp;evpn_overlay_core | Dictionary |  |  |  |  |
| &nbsp;&nbsp;&nbsp;&nbsp;name | String |  | EVPN-OVERLAY-CORE |  |  |
| &nbsp;&nbsp;&nbsp;&nbsp;password | String |  |  |  | Encrypted Password |
| &nbsp;&nbsp;IPv4_UNDERLAY_PEERS | Dictionary |  |  |  |  |
| &nbsp;&nbsp;&nbsp;&nbsp;name | String |  | IPv4-UNDERLAY-PEERS |  |  |
| &nbsp;&nbsp;&nbsp;&nbsp;password | String |  |  |  | Encrypted Password |
| &nbsp;&nbsp;MLAG_IPv4_UNDERLAY_PEER | Dictionary |  |  |  |  |
| &nbsp;&nbsp;&nbsp;&nbsp;name | String |  | MLAG-IPv4-UNDERLAY-PEER |  |  |
| &nbsp;&nbsp;&nbsp;&nbsp;password | String |  |  |  | Encrypted Password |
| &nbsp;&nbsp;EVPN_OVERLAY_PEERS | Dictionary |  |  |  |  |
| &nbsp;&nbsp;&nbsp;&nbsp;name | String |  | EVPN-OVERLAY-PEERS |  |  |
| &nbsp;&nbsp;&nbsp;&nbsp;password | String |  |  |  | Encrypted Password |

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