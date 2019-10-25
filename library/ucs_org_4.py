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
        ),
        required_if=[
            ['state', 'present', ['name']],
        ]
    )

    from ucsmsdk.ucshandle import UcsHandle
    from ucsmsdk.mometa.org.OrgOrg import OrgOrg

    error = False
    changed = False
    kwargs = dict()
    result = dict()

    if module.params['descr'] is not None:
        kwargs['descr'] = module.params['descr']

    try:
        handle = UcsHandle(
            module.params['hostname'],
            module.params['username'],
            module.params['password']
        )
        handle.login()
        ucs_mo = handle.query_dn('org-root/org-' + module.params['name'])

        # Determine state change
        if ucs_mo:
            # Object exists, should it exist? has anything changed?
            if module.params['state'] == 'present':
                # Any Object properties not match, that is a change
                if not ucs_mo.check_prop_match(**kwargs):
                    changed = True

        # Object does not exist but should, that is a change
        else:
            if module.params['state'] == 'present':
                changed = True

        # Object exists but should not, that is a change
        if ucs_mo and module.params['state'] == 'absent':
            changed = True

        # Apply state
        if changed:
            if module.params['state'] == 'absent':
                handle.remove_mo(ucs_mo)
            else:
                kwargs['parent_mo_or_dn'] = 'org-root'
                kwargs['name'] = module.params['name']
                if module.params['descr'] is not None:
                    kwargs['descr'] = module.params['descr']

                ucs_mo = OrgOrg(**kwargs)
                handle.add_mo(ucs_mo, modify_present=True)
            handle.commit()

    except Exception as e:
        error = True
        result['msg'] = "error: %s " % str(e)

    result['changed'] = changed

    if error:
        module.fail_json(**result)

    module.exit_json(**result)

if __name__ == '__main__':
    run_module()
