# ipv6_standard_access_lists

## Description

None

## Variables

| Variable | Type | Required | Default | Value Restrictions | Description |
| -------- | ---- | -------- | ------- | ------------------ | ----------- |
| <pre>ipv6_standard_access_lists | List, items: Dictionary |  |  |  | IPv6 Standard Access-Lists |
| <pre>  - name | String | Required, Unique |  |  | ipv6_access_list_name |
| <pre>    counters_per_entry | Boolean |  |  |  |  |
| <pre>    sequence_numbers | List, items: Dictionary | Required |  |  |  |
| <pre>      - sequence | Integer | Required, Unique |  |  | sequence_id |
| <pre>        action | String | Required |  |  | action as string |

## YAML

```yaml
ipv6_standard_access_lists:
  - name: <str>
    counters_per_entry: <bool>
    sequence_numbers:
      - sequence: <int>
        action: <str>
```