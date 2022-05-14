from avd_schema import DEFAULT_SCHEMA, AvdSchema
import yaml

with open('../../../roles/eos_cli_config_gen/vars/schemas/access_lists.schema.yml', 'r', encoding='utf-8') as schema_file:
    acl_schema = yaml.load(schema_file, Loader=yaml.SafeLoader)

with open('../../../roles/eos_cli_config_gen/vars/schemas/ipv6_standard_access_lists.schema.yml', 'r', encoding='utf-8') as schema_file:
    ipv6_acl_schema = yaml.load(schema_file, Loader=yaml.SafeLoader)

with open('../../../molecule/eos_cli_config_gen_v4.0/inventory/host_vars/acl.yml', 'r', encoding='utf-8') as data_file:
    test_data = yaml.load(data_file, Loader=yaml.SafeLoader)

with open('../../../molecule/eos_cli_config_gen_v4.0/inventory/host_vars/ipv6-access-lists.yml', 'r', encoding='utf-8') as data_file:
    ipv6_test_data = yaml.load(data_file, Loader=yaml.SafeLoader)

invalid_schema = { "hat": "hej" }

schema = AvdSchema()
#print (test_schema)

test_schema = acl_schema

print ("Loading test_schema - no exceptions is a success :) ------------", schema.load_schema(test_schema))
print ("Loaded Schema keys: --------------------------------------------", list(schema._schema.get('keys',{}).keys()))
print ("Validate acl.yml - no exceptions is a success ------------------", schema.validate(test_data))
print ("Validate acl.yml - return boolean: -----------------------------", schema.is_valid(test_data))
print ("Validate ipv6-access-lists.yml - return boolean: ---------------", schema.is_valid(ipv6_test_data))
print ("Extend schema with ipv6_acl ------------------------------------", schema.extend_schema(ipv6_acl_schema))
print ("Loaded Schema keys: --------------------------------------------", list(schema._schema.get('keys',{}).keys()))
print ("Validate ipv6-access-lists.yml - no exceptions is a success ----", schema.validate(ipv6_test_data))
print ("Validate ipv6-access-lists.yml - return boolean: ---------------", schema.is_valid(ipv6_test_data))
print ("Get subschema for 'access_lists.name' --------------------------", schema.subschema(['access_lists', 'name']))
print ("Get subschema for 'access_lists.sequence_numbers.sequence' -----", schema.subschema(['access_lists', 'sequence_numbers', 'sequence']))
print ("Remove schema by loading default schema ------------------------", schema.load_schema(DEFAULT_SCHEMA))
print ("Loaded Schema keys: --------------------------------------------", list(schema._schema.get('keys',{}).keys()))
print ("Validate acl.yml with adhoc schema- no exceptions is a success -", schema.validate(test_data))
print ("Validate acl.yml with adhoc schema - return boolean: -----------", schema.is_valid(test_data))
print ("Get subschema for 'access_list' - exception expected since no schema is loaded ")
schema.subschema(['access_lists', 'name'])
