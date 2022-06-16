# access_lists

## Description

AVD currently supports 2 different data models for extended ACLs:<br><br>- The legacy `access_lists` data model, for compatibility with existing deployments<br>- The improved `ip_access_lists` data model, for access to more EOS features<br><br>Both data models can coexists without conflicts, as different keys are used: `access_lists` vs `ip_access_lists`.<br>Access list names must be unique.<br><br>The legacy data model supports simplified ACL definition with `sequence_number` to `action_string` mapping:<br>

## Variables

| Variable | Type | Required | Default | Value Restrictions | Description |
| -------- | ---- | -------- | ------- | ------------------ | ----------- |
| <code>access_lists</code>| List, items: Dictionary |  |  |  | IP Extended Access-Lists |
| <code>&nbsp;&nbsp;- name</code>| String | Required, Unique |  |  | access_list_name |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;counters_per_entry</code>| Boolean |  |  |  |  |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;sequence_numbers</code>| List, items: Dictionary | Required |  |  |  |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- sequence</code>| Integer | Required, Unique |  |  | sequence_id |
| <code>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;action</code>| String | Required |  |  | action as string |

## YAML

```yaml
access_lists:
  - name: <str>
    counters_per_entry: <bool>
    sequence_numbers:
      - sequence: <int>
        action: <str>
```