# node_type_key

## Description

None

## Variables

| Variable | Type | Required | Default | Value Restrictions | Description |
| -------- | ---- | -------- | ------- | ------------------ | ----------- |
| <pre>node_type_key | Dictionary |  |  |  | Node Type Structure |
| <pre>  defaults | Dictionary |  |  |  |  |
| <pre>    id | Integer | Required |  |  | Node ID<br>Unique identifier used for IP addressing and other algorithms |
| <pre>    mgmt_ip | String |  |  | Format: cidr | Mgmt Interface IP<br>Management Interface IP Address |
| <pre>    platform | String |  |  |  | Hardware Platform<br>Arista platform family |
| <pre>    mgmt_interface | String |  |  |  | Mgmt Interface<br>Management Interface Name<br>Default -> platform_management_interface -> mgmt_interface -> "Management1"<br> |
| <pre>    rack | String |  |  |  | Rack that the switch is located in (only used in snmp_settings location) |
| <pre>    link_tracking | Dictionary |  |  |  | This configures the Link Tracking Group on a switch as well as adds the p2p-uplinks of the switch as the upstream interfaces.<br>Useful in EVPN multhoming designs.<br> |
| <pre>      enabled | Boolean |  | False |  |  |
| <pre>      groups | List, items: Dictionary |  | [{'name': 'LT_GROUP1'}] |  | Link Tracking Groups<br>By default a single group named "LT_GROUP1" is defined with default values.<br>Any groups defined under "groups" will replace the default.<br> |
| <pre>        - name | String |  |  |  | Tracking Group Name |
| <pre>          recovery_delay | Integer |  |  | Max: 3600 | default -> platform_settings_mlag_reload_delay -> 300 |
| <pre>          links_minimum | Integer |  |  | Min: 1<br>Max: 100000 |  |
| <pre>    lacp_port_id_range | Dictionary |  |  |  | LACP Port ID Range<br>This will generate the "lacp port-id range", "begin" and "end" values based on node "id" and the number of nodes in the "node_group".<br>Unique LACP port-id ranges are recommended for EVPN Multihoming designs.<br> |
| <pre>      enabled | Boolean |  | False |  |  |
| <pre>      size | Integer |  | 128 |  | Recommended size > = number of ports in the switch. |
| <pre>      offset | Integer |  | 0 |  | Offset is used to avoid overlapping port-id ranges of different switches<br>Useful when a "connected-endpoint" is connected to switches in different "node_groups".<br> |
| <pre>    raw_eos_cli | String |  |  |  | Raw EOS CLI<br>EOS CLI rendered directly on the root level of the final EOS configuration |
| <pre>    structured_config | String |  |  |  | Custom structured config for eos_cli_config_gen |
| <pre>    uplink_ipv4_pool | String |  |  | Format: ipv4_cidr | Uplink IPv4 Pool<br>IPv4 subnet to use to connect to uplink switches |
| <pre>    uplink_interfaces | List, items: String |  |  |  | Local uplink interfaces |
| <pre>      - <str> | String |  |  | Pattern: Ethernet[\d/]+ |  |
| <pre>    uplink_switches | List, items: String |  |  |  |  |
| <pre>      - <str> | String |  |  |  | Hostname of uplink switch |
| <pre>    max_uplink_switches | Integer |  |  |  | Maximum number of uplink switches.<br>Changing this value may change IP Addressing on uplinks.<br>Can be used to reserve IP space for future expansions.<br> |
| <pre>    max_parallel_uplinks | Integer |  |  |  | Number of parallel links towards uplink switches |
| <pre>    uplink_ptp | Dictionary |  |  |  | Uplink PTP<br>Enable PTP on all infrastructure links |
| <pre>      enable | Boolean |  | False |  |  |
| <pre>    uplink_macsec | Dictionary |  |  |  | Uplink MacSec<br>Enable MacSec on all uplinks |
| <pre>      profile | String |  |  |  | MacSec profile name |
| <pre>    uplink_interface_speed | String |  |  |  | Point-to-Point interface speed - will apply to uplinks on both ends<br>< interface_speed | forced interface_speed | auto interface_speed ><br> |
| <pre>    uplink_switch_interfaces | List, items: String |  |  |  | Interfaces located on uplink switches |
| <pre>      - <str> | String |  |  | Pattern: Ethernet[\d/]+ |  |
| <pre>    short_esi | String |  |  |  | Short ESI<br>short_esi only valid for l2leaf devices using port-channel uplink<br>Setting short_esi to "auto" generates the short_esi automatically using a hash of configuration elements.<br>< 0000:0000:0000 | auto ><br> |
| <pre>    isis_system_id_prefix | String |  |  | Pattern: [0-9a-f]{4}\.[0-9a-f]{4} | ISIS System ID prefix<br>(4.4 hexadecimal) |
| <pre>    isis_maximum_paths | Integer |  |  |  | ISIS Maximum Paths<br>Number of path to configure in ECMP for ISIS |
| <pre>    is_type | String |  | level-2 | Valid Values:<br>- level-1-2<br>- level-1<br>- level-2 | IS Type |
| <pre>    node_sid_base | Integer |  | 0 |  | Node-SID Base<br>Node-SID base for isis-sr underlay variants. Combined with node id to generate ISIS-SR node-SID. |
| <pre>    loopback_ipv4_pool | String |  |  | Format: ipv4_cidr | Loopback0 IPv4 Pool<br>IPv4 subnet for Loopback0 allocation |
| <pre>    vtep_loopback_ipv4_pool | String |  |  | Format: ipv4_cidr | VTEP Loopback IPv4 Pool<br>IPv4 subnet for VTEP-Loopback allocation |
| <pre>    loopback_ipv4_offset | Integer |  | 0 |  | Loopback IPv4 Offset<br>Offset all assigned loopback IP addresses.<br>Required when the < loopback_ipv4_pool > is same for 2 different node_types (like spine and l3leaf) to avoid over-lapping IPs.<br>For example, set the minimum offset l3leaf.defaults.loopback_ipv4_offset: < total # spine switches > or vice versa.<br> |
| <pre>    vtep_loopback | String |  |  | Pattern: Loopback[\d/]+ | VTEP Loopback Interface Name<br>Set VXLAN source interface. |
| <pre>    bgp_as | String |  |  |  | BGP AS Number<br>Required with eBGP |
| <pre>    bgp_defaults | List, items: String |  |  |  | BGP Defaults<br>List of EOS command to apply to BGP daemon |
| <pre>      - <str> | String |  |  |  | EOS Command |
| <pre>    evpn_role | String |  |  | Valid Values:<br>- client<br>- server<br>- none | EVPN Role<br>Acting role in EVPN control plane. Default is set in node_type definition from node_type_keys. |
| <pre>    evpn_route_servers | List, items: String |  |  |  | EVPN Route Servers<br>List of nodes acting as EVPN Route-Servers / Route-Reflectors |
| <pre>      - <str> | String |  |  |  | EVPN Route Server |
| <pre>    evpn_services_l2_only | Boolean |  | False |  | EVPN Services Layer2 only<br>Possibility to prevent configuration of Tenant VRFs and SVIs<br>Override node definition "network_services_l3" from node_type_keys<br>This allows support for centralized routing.<br> |
| <pre>    filter | Dictionary |  |  |  | Network Services Filters<br>Filter L3 and L2 network services based on tenant and tags (and operation filter)<br>If filter is not defined it will default to all<br> |
| <pre>      tenants | List, items: String |  | ['all'] |  |  |
| <pre>        - <str> | String |  |  |  | Tenant |
| <pre>      tags | List, items: String |  | ['all'] |  |  |
| <pre>        - <str> | String |  |  |  | Tag |
| <pre>      always_include_vrfs_in_tenants | List, items: String |  |  |  | Always Include VRFs in Tenants<br>List of tenants where VRFs will be configured even if VLANs are not included in tags<br>Useful for L3 "border" leaf.<br> |
| <pre>        - <str> | String |  |  |  | Tenant |
| <pre>    igmp_snooping_enabled | Boolean |  | True |  | IGMP Snooping Enabled<br>Activate or deactivate IGMP snooping on device level |
| <pre>    evpn_gateway | Dictionary |  |  |  | EVPN Gateway<br>Node is acting as EVPN Multi-Domain Gateway<br>New BGP peer-group is generated between EVPN GWs in different domains or between GWs and Route Servers. Name can be changed under "bgp_peer_groups.evpn_overlay_core" variable<br>L3 rechability for different EVPN GWs must be already in place, it is recommended to use DCI & L3 Edge if Route Servers and GWs are not defined under the same Ansible inventory.<br> |
| <pre>      remote_peers | List, items: Dictionary |  |  |  | Define remote peers of the EVPN VXLAN Gateway.<br>If the hostname can be found in the inventory, ip_address and BGP ASN will be automatically populated. Manual override takes precedence.<br>If the peer's hostname can not be found in the inventory, ip_address and bgp_as must be defined.<br> |
| <pre>        - hostname | String |  |  |  | Hostname of remote EVPN GW server |
| <pre>          ip_address | String |  |  | Format: ipv4 | IP Address<br>Peering IP of remote Route Server |
| <pre>          bgp_as | String |  |  |  | BGP AS Number<br>BGP ASN of remote Route Server |
| <pre>      evpn_l2 | Dictionary |  |  |  | EVPN L2<br>Enable EVPN Gateway functionality for route-types 2 (MAC-IP) and 3 (IMET) |
| <pre>        enabled | Boolean |  | False |  |  |
| <pre>      evpn_l3 | Dictionary |  |  |  | EVPN L3<br>Enable EVPN Gateway functionality for route-type 5 (IP-PREFIX) |
| <pre>        enabled | Boolean |  | False |  |  |
| <pre>        inter_domain | Boolean |  | True |  |  |
| <pre>    mlag | Boolean |  | True |  | Enable MLAG<br>Enable / Disable auto MLAG, when two nodes are defined in node group. |
| <pre>    mlag_dual_primary_detection | Boolean |  | False |  | MLAG Dual Primary Detection<br>Enable / Disable MLAG dual primary detection |
| <pre>    mlag_interfaces | List, items: String |  |  |  | MLAG interfaces<br>Required when MLAG leafs are present in the topology |
| <pre>      - <str> | String |  |  | Pattern: Ethernet[\d/]+ |  |
| <pre>    mlag_interfaces_speed | String |  |  |  | MLAG interfaces speed<br>< interface_speed | forced interface_speed | auto interface_speed > |
| <pre>    mlag_peer_l3_vlan | Integer |  | 4093 | Max: 4094 | MLAG L3 Peering VLAN<br>Underlay L3 peering SVI interface id<br>If set to 0 or the same vlan as mlag_peer_vlan, the mlag_peer_vlan will be used for L3 peering<br> |
| <pre>    mlag_peer_l3_ipv4_pool | String |  |  | Format: ipv4_cidr | MLAG L3 Peering IPv4 Pool<br>IP address pool used for MLAG underlay L3 peering. IP is derived from the node id.<br>Required when MLAG leafs present in topology and they are using a separate L3 peering VLAN.<br> |
| <pre>    mlag_peer_vlan | Integer |  | 4094 | Min: 1<br>Max: 4094 | MLAG Peer VLAN<br>MLAG Peer Link (control link) SVI interface id |
| <pre>    mlag_peer_link_allowed_vlans | String |  | 2-4094 |  | MLAG Peer-link Allowed VLAN range |
| <pre>    mlag_peer_ipv4_pool | String |  |  | Format: ipv4_cidr | MLAG Peer IPv4 Pool<br>IP address pool used for MLAG Peer Link (control link). IP is derived from the node id.<br>Required when MLAG leafs present in topology.<br> |
| <pre>    spanning_tree_mode | String | Required |  | Valid Values:<br>- mstp<br>- rstp<br>- rapid-pvst<br>- none |  |
| <pre>    spanning_tree_priority | Integer |  | 32768 |  |  |
| <pre>    spanning_tree_root_super | Boolean |  | False |  |  |
| <pre>    virtual_router_mac_address | String | Required |  | Format: mac | Virtual Router MAC Address<br>Virtual router mac address for anycast gateway |
| <pre>    inband_management_subnet | String |  |  | Format: ipv4_cidr | Optional IP subnet assigned to Inband Management SVI on l2leafs in default VRF.<br>Parent l3leafs will have SVI with "ip virtual-router" and host-route injection based on ARP. This allows all l3leafs to reuse the same subnet<br>SVI IP address will be assigned as follows:<br>virtual-router: <subnet> + 1<br>l3leaf A      : <subnet> + 2 (same IP on all l3leaf A)<br>l3leaf B      : <subnet> + 3 (same IP on all l3leaf B)<br>l2leafs       : <subnet> + 3 + <l2leaf id><br>GW on l2leafs : <subnet> + 1<br>Assign range larger than total l2leafs + 5<br> |
| <pre>    inband_management_vlan | Integer |  | 4092 |  | Inband Management VLAN<br>VLAN number assigned to Inband Management SVI on l2leafs in default VRF |

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