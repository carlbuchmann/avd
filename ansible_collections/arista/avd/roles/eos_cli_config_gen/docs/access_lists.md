# access_lists

## Description

AVD currently supports 2 different data models for extended ACLs:<br><br>- The legacy `access_lists` data model, for compatibility with existing deployments<br>- The improved `ip_access_lists` data model, for access to more EOS features<br><br>Both data models can coexists without conflicts, as different keys are used: `access_lists` vs `ip_access_lists`.<br>Access list names must be unique.<br><br>The legacy data model supports simplified ACL definition with `sequence_number` to `action_string` mapping:<br>

## Variables

| Variable | Type | Required | Default | Value Restrictions | Description |
| -------- | ---- | -------- | ------- | ------------------ | ----------- |
| <pre>access_lists | List, items: Dictionary |  |  |  | IP Extended Access-Lists |
| <pre>  - name | String | Required, Unique |  |  | access_list_name |
| <pre>    counters_per_entry | Boolean |  |  |  |  |
| <pre>    sequence_numbers | List, items: Dictionary | Required |  |  |  |
| <pre>      - sequence | Integer | Required, Unique |  |  | sequence_id |
| <pre>        action | String | Required |  |  | action as string |

## YAML

```yaml
access_lists:
  - name: <str>
    counters_per_entry: <bool>
    sequence_numbers:
      - sequence: <int>
        action: <str>
```