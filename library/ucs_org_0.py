#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule

def run_module():
    module = AnsibleModule(
        argument_spec=dict(
        )
    )

    result = dict(changed=False)

    module.exit_json(**result)

if __name__ == '__main__':
    run_module()
