# ipv6_standard_access_lists

## Description

None

## Variables

| Variable | Type | Required | Default | Value Restrictions | Description |
| -------- | ---- | -------- | ------- | ------------------ | ----------- |
| ipv6_standard_access_lists | List, items: Dictionary |  |  |  | IPv6 Standard Access-Lists |
| &nbsp;&nbsp;- name | String | Required, Unique |  |  | ipv6_access_list_name |
| &nbsp;&nbsp;&nbsp;&nbsp;counters_per_entry | Boolean |  |  |  |  |
| &nbsp;&nbsp;&nbsp;&nbsp;sequence_numbers | List, items: Dictionary | Required |  |  |  |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- sequence | Integer | Required, Unique |  |  | sequence_id |
| &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;action | String | Required |  |  | action as string |

## YAML

```yaml
ipv6_standard_access_lists:
  - name: <str>
    counters_per_entry: <bool>
    sequence_numbers:
      - sequence: <int>
        action: <str>
```