#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule

def run_module():
    """ Run the module """

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

    from ucsmsdk.ucshandle import UcsHandle
    from ucsmsdk.mometa.org.OrgOrg import OrgOrg

    handle = UcsHandle(
        module.params['hostname'],
        module.params['username'],
        module.params['password']
    )
    handle.login()

    ucs_mo = OrgOrg(
        parent_mo_or_dn='org-root',
        name=module.params['name'],
        descr=module.params['descr']
    )

    handle.add_mo(ucs_mo, modify_present=True)
    handle.commit()
    handle.logout()

    # TODO: Add delete object code

    result = dict(changed=True)

    module.exit_json(**result)

if __name__ == '__main__':
    run_module()
