# bgp_peer_groups

## Description

Leverage an Arista EOS switch to generate the encrypted password using the correct peer group name.<br>Note that the name of the peer groups use '-' instead of '_' in EOS configuration.<br>

## Variables

| Variable | Type | Required | Default | Value Restrictions | Description |
| -------- | ---- | -------- | ------- | ------------------ | ----------- |
| <code>bgp_peer_groups</code>| Dictionary |  |  |  | BGP peer group names and encrypted password |
| <code>&nbsp;&nbsp;ipv4_underlay_peers</code>| Dictionary |  |  |  |  |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;name</code>| String |  | IPv4-UNDERLAY-PEERS |  |  |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;password</code>| String |  |  |  | Encrypted Password |
| <code>&nbsp;&nbsp;mlag_ipv4_underlay_peer</code>| Dictionary |  |  |  |  |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;name</code>| String |  | MLAG-IPv4-UNDERLAY-PEER |  |  |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;password</code>| String |  |  |  | Encrypted Password |
| <code>&nbsp;&nbsp;evpn_overlay_peers</code>| Dictionary |  |  |  |  |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;name</code>| String |  | EVPN-OVERLAY-PEERS |  |  |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;password</code>| String |  |  |  | Encrypted Password |
| <code>&nbsp;&nbsp;evpn_overlay_core</code>| Dictionary |  |  |  |  |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;name</code>| String |  | EVPN-OVERLAY-CORE |  |  |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;password</code>| String |  |  |  | Encrypted Password |
| <code>&nbsp;&nbsp;IPv4_UNDERLAY_PEERS</code>| Dictionary |  |  |  |  |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;name</code>| String |  | IPv4-UNDERLAY-PEERS |  |  |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;password</code>| String |  |  |  | Encrypted Password |
| <code>&nbsp;&nbsp;MLAG_IPv4_UNDERLAY_PEER</code>| Dictionary |  |  |  |  |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;name</code>| String |  | MLAG-IPv4-UNDERLAY-PEER |  |  |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;password</code>| String |  |  |  | Encrypted Password |
| <code>&nbsp;&nbsp;EVPN_OVERLAY_PEERS</code>| Dictionary |  |  |  |  |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;name</code>| String |  | EVPN-OVERLAY-PEERS |  |  |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;password</code>| String |  |  |  | Encrypted Password |

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