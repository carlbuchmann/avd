# bgp_peer_groups

## Description

Leverage an Arista EOS switch to generate the encrypted password using the correct peer group name.<br>Note that the name of the peer groups use '-' instead of '_' in EOS configuration.<br>

## Variables

| Variable | Type | Required | Default | Value Restrictions | Description |
| -------- | ---- | -------- | ------- | ------------------ | ----------- |
| <pre>bgp_peer_groups | Dictionary |  |  |  | BGP peer group names and encrypted password |
| <pre>  ipv4_underlay_peers | Dictionary |  |  |  |  |
| <pre>    name | String |  | IPv4-UNDERLAY-PEERS |  |  |
| <pre>    password | String |  |  |  | Encrypted Password |
| <pre>  mlag_ipv4_underlay_peer | Dictionary |  |  |  |  |
| <pre>    name | String |  | MLAG-IPv4-UNDERLAY-PEER |  |  |
| <pre>    password | String |  |  |  | Encrypted Password |
| <pre>  evpn_overlay_peers | Dictionary |  |  |  |  |
| <pre>    name | String |  | EVPN-OVERLAY-PEERS |  |  |
| <pre>    password | String |  |  |  | Encrypted Password |
| <pre>  evpn_overlay_core | Dictionary |  |  |  |  |
| <pre>    name | String |  | EVPN-OVERLAY-CORE |  |  |
| <pre>    password | String |  |  |  | Encrypted Password |
| <pre>  IPv4_UNDERLAY_PEERS | Dictionary |  |  |  |  |
| <pre>    name | String |  | IPv4-UNDERLAY-PEERS |  |  |
| <pre>    password | String |  |  |  | Encrypted Password |
| <pre>  MLAG_IPv4_UNDERLAY_PEER | Dictionary |  |  |  |  |
| <pre>    name | String |  | MLAG-IPv4-UNDERLAY-PEER |  |  |
| <pre>    password | String |  |  |  | Encrypted Password |
| <pre>  EVPN_OVERLAY_PEERS | Dictionary |  |  |  |  |
| <pre>    name | String |  | EVPN-OVERLAY-PEERS |  |  |
| <pre>    password | String |  |  |  | Encrypted Password |

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