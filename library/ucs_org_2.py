#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule

def run_module():
    module = AnsibleModule(
        argument_spec=dict(
            hostname=dict(type='str', required=True),
            username=dict(type='str', default='admin'),
            password=dict(type='str', required=True, no_log=True),
            name=dict(type='str'),
            descr=dict(type='str'),
            state=dict(type='str', default='present', choices=['present', 'absent'])
        )
    )

    result = dict(changed=False)

    module.exit_json(**result)

if __name__ == '__main__':
    run_module()
