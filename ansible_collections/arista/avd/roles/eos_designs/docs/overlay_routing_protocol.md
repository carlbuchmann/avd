# overlay_routing_protocol

## Description

- The following overlay routing protocols are supported:<br>  - EBGP (default for l3ls-evpn)<br>  - IBGP (only with OSPF or ISIS variants in underlay)<br>

## Variables

| Variable | Type | Required | Default | Value Restrictions | Description |
| -------- | ---- | -------- | ------- | ------------------ | ----------- |
| <pre>overlay_routing_protocol | String |  | ebgp | Valid Values:<br>- ebgp<br>- ibgp<br>- BGP |  |

## YAML

```yaml
overlay_routing_protocol: <str>
```