def get_credentials():
    d = {}
    d['username'] = 'admin'
    d['password'] = 'passw0rd'
    d['auth_url'] = 'http://192.168.1.10:5000/v2.0'
    d['tenant_name'] = 'admin'
    d['region_name'] = 'RegionOne'
    return d