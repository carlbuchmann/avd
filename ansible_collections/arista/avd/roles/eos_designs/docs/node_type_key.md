# node_type_key

## Description

None

## Variables

| Variable | Type | Required | Default | Value Restrictions | Description |
| -------- | ---- | -------- | ------- | ------------------ | ----------- |
| <code>node_type_key</code>| Dictionary |  |  |  | Node Type Structure |
| <code>&nbsp;&nbsp;defaults</code>| Dictionary |  |  |  |  |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;id</code>| Integer | Required |  |  | Node ID<br>Unique identifier used for IP addressing and other algorithms |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;mgmt_ip</code>| String |  |  | Format: cidr | Mgmt Interface IP<br>Management Interface IP Address |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;platform</code>| String |  |  |  | Hardware Platform<br>Arista platform family |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;mgmt_interface</code>| String |  |  |  | Mgmt Interface<br>Management Interface Name<br>Default -> platform_management_interface -> mgmt_interface -> "Management1"<br> |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;rack</code>| String |  |  |  | Rack that the switch is located in (only used in snmp_settings location) |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;link_tracking</code>| Dictionary |  |  |  | This configures the Link Tracking Group on a switch as well as adds the p2p-uplinks of the switch as the upstream interfaces.<br>Useful in EVPN multhoming designs.<br> |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;enabled</code>| Boolean |  | False |  |  |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;groups</code>| List, items: Dictionary |  | [{'name': 'LT_GROUP1'}] |  | Link Tracking Groups<br>By default a single group named "LT_GROUP1" is defined with default values.<br>Any groups defined under "groups" will replace the default.<br> |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- name</code>| String |  |  |  | Tracking Group Name |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;recovery_delay</code>| Integer |  |  | Max: 3600 | default -> platform_settings_mlag_reload_delay -> 300 |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;links_minimum</code>| Integer |  |  | Min: 1<br>Max: 100000 |  |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;lacp_port_id_range</code>| Dictionary |  |  |  | LACP Port ID Range<br>This will generate the "lacp port-id range", "begin" and "end" values based on node "id" and the number of nodes in the "node_group".<br>Unique LACP port-id ranges are recommended for EVPN Multihoming designs.<br> |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;enabled</code>| Boolean |  | False |  |  |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;size</code>| Integer |  | 128 |  | Recommended size > = number of ports in the switch. |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;offset</code>| Integer |  | 0 |  | Offset is used to avoid overlapping port-id ranges of different switches<br>Useful when a "connected-endpoint" is connected to switches in different "node_groups".<br> |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;raw_eos_cli</code>| String |  |  |  | Raw EOS CLI<br>EOS CLI rendered directly on the root level of the final EOS configuration |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;structured_config</code>| String |  |  |  | Custom structured config for eos_cli_config_gen |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;uplink_ipv4_pool</code>| String |  |  | Format: ipv4_cidr | Uplink IPv4 Pool<br>IPv4 subnet to use to connect to uplink switches |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;uplink_interfaces</code>| List, items: String |  |  |  | Local uplink interfaces |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- <str></code>| String |  |  | Pattern: Ethernet[\d/]+ |  |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;uplink_switches</code>| List, items: String |  |  |  |  |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- <str></code>| String |  |  |  | Hostname of uplink switch |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;max_uplink_switches</code>| Integer |  |  |  | Maximum number of uplink switches.<br>Changing this value may change IP Addressing on uplinks.<br>Can be used to reserve IP space for future expansions.<br> |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;max_parallel_uplinks</code>| Integer |  |  |  | Number of parallel links towards uplink switches |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;uplink_ptp</code>| Dictionary |  |  |  | Uplink PTP<br>Enable PTP on all infrastructure links |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;enable</code>| Boolean |  | False |  |  |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;uplink_macsec</code>| Dictionary |  |  |  | Uplink MacSec<br>Enable MacSec on all uplinks |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;profile</code>| String |  |  |  | MacSec profile name |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;uplink_interface_speed</code>| String |  |  |  | Point-to-Point interface speed - will apply to uplinks on both ends<br>< interface_speed | forced interface_speed | auto interface_speed ><br> |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;uplink_switch_interfaces</code>| List, items: String |  |  |  | Interfaces located on uplink switches |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- <str></code>| String |  |  | Pattern: Ethernet[\d/]+ |  |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;short_esi</code>| String |  |  |  | Short ESI<br>short_esi only valid for l2leaf devices using port-channel uplink<br>Setting short_esi to "auto" generates the short_esi automatically using a hash of configuration elements.<br>< 0000:0000:0000 | auto ><br> |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;isis_system_id_prefix</code>| String |  |  | Pattern: [0-9a-f]{4}\.[0-9a-f]{4} | ISIS System ID prefix<br>(4.4 hexadecimal) |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;isis_maximum_paths</code>| Integer |  |  |  | ISIS Maximum Paths<br>Number of path to configure in ECMP for ISIS |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;is_type</code>| String |  | level-2 | Valid Values:<br>- level-1-2<br>- level-1<br>- level-2 | IS Type |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;node_sid_base</code>| Integer |  | 0 |  | Node-SID Base<br>Node-SID base for isis-sr underlay variants. Combined with node id to generate ISIS-SR node-SID. |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;loopback_ipv4_pool</code>| String |  |  | Format: ipv4_cidr | Loopback0 IPv4 Pool<br>IPv4 subnet for Loopback0 allocation |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;vtep_loopback_ipv4_pool</code>| String |  |  | Format: ipv4_cidr | VTEP Loopback IPv4 Pool<br>IPv4 subnet for VTEP-Loopback allocation |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;loopback_ipv4_offset</code>| Integer |  | 0 |  | Loopback IPv4 Offset<br>Offset all assigned loopback IP addresses.<br>Required when the < loopback_ipv4_pool > is same for 2 different node_types (like spine and l3leaf) to avoid over-lapping IPs.<br>For example, set the minimum offset l3leaf.defaults.loopback_ipv4_offset: < total # spine switches > or vice versa.<br> |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;vtep_loopback</code>| String |  |  | Pattern: Loopback[\d/]+ | VTEP Loopback Interface Name<br>Set VXLAN source interface. |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;bgp_as</code>| String |  |  |  | BGP AS Number<br>Required with eBGP |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;bgp_defaults</code>| List, items: String |  |  |  | BGP Defaults<br>List of EOS command to apply to BGP daemon |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- <str></code>| String |  |  |  | EOS Command |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;evpn_role</code>| String |  |  | Valid Values:<br>- client<br>- server<br>- none | EVPN Role<br>Acting role in EVPN control plane. Default is set in node_type definition from node_type_keys. |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;evpn_route_servers</code>| List, items: String |  |  |  | EVPN Route Servers<br>List of nodes acting as EVPN Route-Servers / Route-Reflectors |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- <str></code>| String |  |  |  | EVPN Route Server |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;evpn_services_l2_only</code>| Boolean |  | False |  | EVPN Services Layer2 only<br>Possibility to prevent configuration of Tenant VRFs and SVIs<br>Override node definition "network_services_l3" from node_type_keys<br>This allows support for centralized routing.<br> |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;filter</code>| Dictionary |  |  |  | Network Services Filters<br>Filter L3 and L2 network services based on tenant and tags (and operation filter)<br>If filter is not defined it will default to all<br> |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;tenants</code>| List, items: String |  | ['all'] |  |  |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- <str></code>| String |  |  |  | Tenant |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;tags</code>| List, items: String |  | ['all'] |  |  |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- <str></code>| String |  |  |  | Tag |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;always_include_vrfs_in_tenants</code>| List, items: String |  |  |  | Always Include VRFs in Tenants<br>List of tenants where VRFs will be configured even if VLANs are not included in tags<br>Useful for L3 "border" leaf.<br> |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- <str></code>| String |  |  |  | Tenant |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;igmp_snooping_enabled</code>| Boolean |  | True |  | IGMP Snooping Enabled<br>Activate or deactivate IGMP snooping on device level |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;evpn_gateway</code>| Dictionary |  |  |  | EVPN Gateway<br>Node is acting as EVPN Multi-Domain Gateway<br>New BGP peer-group is generated between EVPN GWs in different domains or between GWs and Route Servers. Name can be changed under "bgp_peer_groups.evpn_overlay_core" variable<br>L3 rechability for different EVPN GWs must be already in place, it is recommended to use DCI & L3 Edge if Route Servers and GWs are not defined under the same Ansible inventory.<br> |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;remote_peers</code>| List, items: Dictionary |  |  |  | Define remote peers of the EVPN VXLAN Gateway.<br>If the hostname can be found in the inventory, ip_address and BGP ASN will be automatically populated. Manual override takes precedence.<br>If the peer's hostname can not be found in the inventory, ip_address and bgp_as must be defined.<br> |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- hostname</code>| String |  |  |  | Hostname of remote EVPN GW server |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ip_address</code>| String |  |  | Format: ipv4 | IP Address<br>Peering IP of remote Route Server |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;bgp_as</code>| String |  |  |  | BGP AS Number<br>BGP ASN of remote Route Server |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;evpn_l2</code>| Dictionary |  |  |  | EVPN L2<br>Enable EVPN Gateway functionality for route-types 2 (MAC-IP) and 3 (IMET) |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;enabled</code>| Boolean |  | False |  |  |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;evpn_l3</code>| Dictionary |  |  |  | EVPN L3<br>Enable EVPN Gateway functionality for route-type 5 (IP-PREFIX) |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;enabled</code>| Boolean |  | False |  |  |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;inter_domain</code>| Boolean |  | True |  |  |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;mlag</code>| Boolean |  | True |  | Enable MLAG<br>Enable / Disable auto MLAG, when two nodes are defined in node group. |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;mlag_dual_primary_detection</code>| Boolean |  | False |  | MLAG Dual Primary Detection<br>Enable / Disable MLAG dual primary detection |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;mlag_interfaces</code>| List, items: String |  |  |  | MLAG interfaces<br>Required when MLAG leafs are present in the topology |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- <str></code>| String |  |  | Pattern: Ethernet[\d/]+ |  |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;mlag_interfaces_speed</code>| String |  |  |  | MLAG interfaces speed<br>< interface_speed | forced interface_speed | auto interface_speed > |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;mlag_peer_l3_vlan</code>| Integer |  | 4093 | Max: 4094 | MLAG L3 Peering VLAN<br>Underlay L3 peering SVI interface id<br>If set to 0 or the same vlan as mlag_peer_vlan, the mlag_peer_vlan will be used for L3 peering<br> |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;mlag_peer_l3_ipv4_pool</code>| String |  |  | Format: ipv4_cidr | MLAG L3 Peering IPv4 Pool<br>IP address pool used for MLAG underlay L3 peering. IP is derived from the node id.<br>Required when MLAG leafs present in topology and they are using a separate L3 peering VLAN.<br> |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;mlag_peer_vlan</code>| Integer |  | 4094 | Min: 1<br>Max: 4094 | MLAG Peer VLAN<br>MLAG Peer Link (control link) SVI interface id |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;mlag_peer_link_allowed_vlans</code>| String |  | 2-4094 |  | MLAG Peer-link Allowed VLAN range |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;mlag_peer_ipv4_pool</code>| String |  |  | Format: ipv4_cidr | MLAG Peer IPv4 Pool<br>IP address pool used for MLAG Peer Link (control link). IP is derived from the node id.<br>Required when MLAG leafs present in topology.<br> |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;spanning_tree_mode</code>| String | Required |  | Valid Values:<br>- mstp<br>- rstp<br>- rapid-pvst<br>- none |  |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;spanning_tree_priority</code>| Integer |  | 32768 |  |  |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;spanning_tree_root_super</code>| Boolean |  | False |  |  |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;virtual_router_mac_address</code>| String | Required |  | Format: mac | Virtual Router MAC Address<br>Virtual router mac address for anycast gateway |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;inband_management_subnet</code>| String |  |  | Format: ipv4_cidr | Optional IP subnet assigned to Inband Management SVI on l2leafs in default VRF.<br>Parent l3leafs will have SVI with "ip virtual-router" and host-route injection based on ARP. This allows all l3leafs to reuse the same subnet<br>SVI IP address will be assigned as follows:<br>virtual-router: <subnet> + 1<br>l3leaf A      : <subnet> + 2 (same IP on all l3leaf A)<br>l3leaf B      : <subnet> + 3 (same IP on all l3leaf B)<br>l2leafs       : <subnet> + 3 + <l2leaf id><br>GW on l2leafs : <subnet> + 1<br>Assign range larger than total l2leafs + 5<br> |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;inband_management_vlan</code>| Integer |  | 4092 |  | Inband Management VLAN<br>VLAN number assigned to Inband Management SVI on l2leafs in default VRF |

## YAML

```yaml
node_type_key:
  defaults:
    id: <int>
    mgmt_ip: <str>
    platform: <str>
    mgmt_interface: <str>
    rack: <str>
    link_tracking:
      enabled: <bool>
      groups:
        - name: <str>
          recovery_delay: <int>
          links_minimum: <int>
    lacp_port_id_range:
      enabled: <bool>
      size: <int>
      offset: <int>
    raw_eos_cli: <str>
    structured_config: <str>
    uplink_ipv4_pool: <str>
    uplink_interfaces:
      - <str>
    uplink_switches:
      - <str>
    max_uplink_switches: <int>
    max_parallel_uplinks: <int>
    uplink_ptp:
      enable: <bool>
    uplink_macsec:
      profile: <str>
    uplink_interface_speed: <str>
    uplink_switch_interfaces:
      - <str>
    short_esi: <str>
    isis_system_id_prefix: <str>
    isis_maximum_paths: <int>
    is_type: <str>
    node_sid_base: <int>
    loopback_ipv4_pool: <str>
    vtep_loopback_ipv4_pool: <str>
    loopback_ipv4_offset: <int>
    vtep_loopback: <str>
    bgp_as: <str>
    bgp_defaults:
      - <str>
    evpn_role: <str>
    evpn_route_servers:
      - <str>
    evpn_services_l2_only: <bool>
    filter:
      tenants:
        - <str>
      tags:
        - <str>
      always_include_vrfs_in_tenants:
        - <str>
    igmp_snooping_enabled: <bool>
    evpn_gateway:
      remote_peers:
        - hostname: <str>
          ip_address: <str>
          bgp_as: <str>
      evpn_l2:
        enabled: <bool>
      evpn_l3:
        enabled: <bool>
        inter_domain: <bool>
    mlag: <bool>
    mlag_dual_primary_detection: <bool>
    mlag_interfaces:
      - <str>
    mlag_interfaces_speed: <str>
    mlag_peer_l3_vlan: <int>
    mlag_peer_l3_ipv4_pool: <str>
    mlag_peer_vlan: <int>
    mlag_peer_link_allowed_vlans: <str>
    mlag_peer_ipv4_pool: <str>
    spanning_tree_mode: <str>
    spanning_tree_priority: <int>
    spanning_tree_root_super: <bool>
    virtual_router_mac_address: <str>
    inband_management_subnet: <str>
    inband_management_vlan: <int>
```