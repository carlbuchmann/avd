# underlay_routing_protocol

## Description

- The following underlay routing protocols are supported:<br>  - EBGP (default for l3ls-evpn)<br>  - OSPF.<br>  - ISIS.<br>  - ISIS-SR*.<br>  - ISIS-LDP*.<br>  - ISIS-SR-LDP*.<br>  - OSPF-LDP*.<br>- The variables should be applied to all devices in the fabric.<br><br>*Only supported with core_interfaces data model.<br>

## Variables

| Variable | Type | Required | Default | Value Restrictions | Description |
| -------- | ---- | -------- | ------- | ------------------ | ----------- |
| <code>underlay_routing_protocol</code>| String |  | ebgp | Valid Values:<br>- ebgp<br>- ospf<br>- isis<br>- isis-sr<br>- isis-ldp<br>- isis-sr-ldp<br>- ospf-ldp<br>- BGP |  |

## YAML

```yaml
underlay_routing_protocol: <str>
```