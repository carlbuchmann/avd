# ipv6_standard_access_lists

## Description

None

## Variables

| Variable | Type | Required | Default | Value Restrictions | Description |
| -------- | ---- | -------- | ------- | ------------------ | ----------- |
| <code>ipv6_standard_access_lists</code>| List, items: Dictionary |  |  |  | IPv6 Standard Access-Lists |
| <code>&nbsp;&nbsp;- name</code>| String | Required, Unique |  |  | ipv6_access_list_name |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;counters_per_entry</code>| Boolean |  |  |  |  |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;sequence_numbers</code>| List, items: Dictionary | Required |  |  |  |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- sequence</code>| Integer | Required, Unique |  |  | sequence_id |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;action</code>| String | Required |  |  | action as string |

## YAML

```yaml
ipv6_standard_access_lists:
  - name: <str>
    counters_per_entry: <bool>
    sequence_numbers:
      - sequence: <int>
        action: <str>
```