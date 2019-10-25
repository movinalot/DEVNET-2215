from ucsmsdk.ucshandle import UcsHandle
def ucs_login(hostname, username, password):
    """ Login to UCS """

    HANDLE = UcsHandle(hostname, username, password)
    HANDLE.login()
    return HANDLE


