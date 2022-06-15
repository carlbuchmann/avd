# ipv6_standard_access_lists

## Description

None

## Variables

| Variable | Type | Required | Default | Value Restrictions | Description |
| -------- | ---- | -------- | ------- | ------------------ | ----------- |
| ipv6_standard_access_lists | List, items: Dictionary |  |  |  | IPv6 Standard Access-Lists |
|   - name | String | Required, Unique |  |  | ipv6_access_list_name |
|     counters_per_entry | Boolean |  |  |  |  |
|     sequence_numbers | List, items: Dictionary | Required |  |  |  |
|       - sequence | Integer | Required, Unique |  |  | sequence_id |
|         action | String | Required |  |  | action as string |

## YAML

```yaml
ipv6_standard_access_lists:
  - name: <str>
    counters_per_entry: <bool>
    sequence_numbers:
      - sequence: <int>
        action: <str>
```