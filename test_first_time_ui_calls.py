import requests
import json
import hashlib
import pytest

# all required variables
#obj = json.load(open('/opt/scripts/deployment/hosts.json'))
s_sid = ''
# ip = obj['LC'][0]['host'][5:]
# ip = '143.110.181.14'
# core_ip = obj.get('core', None)
lc_ip = "null"

f = open('/var/tmp/credentials.txt', 'r')
credentials = {}
for line in f:
    k, v = line.strip().split('=')
    credentials[k.strip()] = v.strip()
f.close()


orgNAme = credentials['OrganisationName']
licenseKey = credentials['licenseKey']
clusterName = credentials['ClusterName']
_pass = hashlib.md5(credentials['Password'].encode('utf-8')).hexdigest()
ip = credentials['PublicIP']
core_ip = credentials['PrivateIp']
email = credentials['MailId']
name = credentials['Name']
phone = ""
status = "active"
password = _pass


def test_state_call():
    url = 'https://{}/lc/state'.format(ip)
    response = requests.get(url=url, verify=False)
    res = response.json()
    print(res)
    assert res['status'] == 'success'


def test_api_lc_mgmt_org():
    url = 'https://{}/lc/mgmt/org/'.format(ip)
    body = {"orgName": orgNAme}
    headers = {"Content-Type": "application/json"}
    response = requests.post(url=url, verify=False,
                             data=json.dumps(body), headers=headers)
    res = response.json()
    print(res)
    assert res['status'] == 'success'


def test_api_lc_mgmt_users():
    url = 'https://{}/lc/mgmt/users/'.format(ip)
    body = {
        "emailId": email,
        "isAdmin": True,
        "mfa_flag": False,
        "name": name,
        "orgName": orgNAme,
        "password": password,
        "phone": phone,
        "status": status
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(url=url, verify=False,
                             data=json.dumps(body), headers=headers)
    res = response.json()
    print(res)
    assert res['status'] == 'success'


def test_lc_mgmt_connections():
    url = 'https://{}/lc/mgmt/connections/'.format(ip)
    body = {"coreIP": core_ip}
    headers = {"Content-Type": "application/json"}
    response = requests.post(url=url, verify=False,
                             data=json.dumps(body), headers=headers)
    res = response.json()
    print(res)
    assert res['status'] == 'success'


def test_lc_cluster_core_config():
    url = 'https://{}/lc/cluster/core_config'.format(ip)
    body = {"coreIP": core_ip}
    headers = {"Content-Type": "application/json"}
    response = requests.put(url=url, verify=False,
                            data=json.dumps(body), headers=headers)
    res = response.json()
    print(res)
    assert res['status'] == 'success'


def test_lc_cluster_setup():
    url = 'https://{}/lc/cluster/setup'.format(ip)
    body = {
        "clusterName": clusterName,
        "coreIP": core_ip,
        "localConsoleIp": lc_ip,
        "time_zone": "Asia/Kolkata"
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url=url, verify=False,
                             data=json.dumps(body), headers=headers)
    res = response.json()
    print(res)
    assert res['status'] == 'success'


def test_mgmt_license_fetch():
    url = 'https://{}/mgmt/license/fetch'.format(ip)
    body = {
        "cluster_key": licenseKey
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url=url, verify=False,
                             data=json.dumps(body), headers=headers)
    res = response.json()
    print(res)
    assert res['status'] == 'success'


def test_lc_cluster_license_flag():
    url = 'https://{}/lc/mgmt/cluster/license_flag'.format(ip)
    headers = {"Content-Type": "application/json"}
    response = requests.post(url=url, verify=False, headers=headers)
    res = response.json()
    print(res)
    assert res['status'] == 'success'


def test_init_login():
    url_init = 'https://{}/lc/users/init'.format(ip)
    body = {
        "emailId": email
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url=url_init, verify=False,
                             data=json.dumps(body), headers=headers)
    res = response.json()
    print(res)
    ch_id = res['data']['chId']
    assert res['status'] == 'success'
    # login call
    url_login = 'https://{}/lc/users/login'.format(ip)
    hash_obj = hashlib.md5()
    # pass_one = hashlib.md5(password.encode('utf-8'))
    hash_obj.update(ch_id.encode('utf-8') + password.encode('utf-8'))
    cst_pass = hash_obj.hexdigest()
    body = {
        "cstPass": cst_pass,
        "emailId": email}
    headers = {"Content-type": "application/json"}
    response = requests.post(url=url_login, verify=False,
                             data=json.dumps(body), headers=headers)
    res = response.json()
    print(res)
    global s_sid
    s_sid = res['data']['SSID']
    clusterId=res['data']['access'][0]['clusterId']
    assert res['status'] == 'success'


def test_mgmt_scope_list():
    url = 'https://{}/mgmt/scope/list'.format(ip)
    headers1 = {"Content-Type": "application/json", "ssid": s_sid}
    response = requests.get(url=url, verify=False, headers=headers1)
    res = response.json()
    print(res)
    assert res['status'] == 'success'


def test_wrk_api_vfields():
    url = 'https://{}/wrk/api/vfields'.format(ip)
    body = {"scope_id": "default"}
    headers1 = {"Content-Type": "application/json", "ssid": s_sid}
    response = requests.post(url=url, verify=False,
                             data=json.dumps(body), headers=headers1)
    res = response.json()
    print(res)
    assert res['status'] == 'success'


def test_wrk_api_vfields_two():
    url = 'https://{}/wrk/api/vfields'.format(ip)
    body = {"scope_id": "default"}
    headers1 = {"Content-Type": "application/json", "ssid": s_sid}
    response = requests.post(url=url, verify=False,
                             data=json.dumps(body), headers=headers1)
    res = response.json()
    print(res)
    assert res['status'] == 'success'


def test_mgmt_components_list():
    url = 'https://{}/mgmt/components/list'.format(ip)
    headers1 = {"Content-Type": "application/json", "ssid": s_sid}
    response = requests.get(url=url, verify=False, headers=headers1)
    res = response.json()
    print(res)
    assert res['status'] == 'success'


def test_mgmt_scope_list_two():
    url = 'https://{}/mgmt/scope/list'.format(ip)
    headers1 = {"Content-Type": "application/json", "ssid": s_sid}
    response = requests.get(url=url, verify=False, headers=headers1)
    res = response.json()
    print(res)
    assert res['status'] == 'success'


# def test_mgmt_dn_system_master():
#     url = 'https://{}/mgmt/dn/system'.format(ip)
#     body = {
#         "hostName": "cicd-02",
#         "is_master": True,
#         "localIPv4Address": "10.139.216.177",
#         "ssid": s_sid,
#         "systemClassType": "dn",
#         "systemName": "dl-master"
#     }
#     headers1 = {"Content-Type": "application/json", "ssid": s_sid}
#     response = requests.put(url=url, verify=False,
#                             data=json.dumps(body), headers=headers1)
#     res = response.json()
#     print(res)
#     assert res['status'] == 'success'


 def test_mgmt_onboard_dn_components():
     url = 'https://{}/mgmt/components/list'.format(ip)
     headers1 = {"Content-Type": "application/json", "ssid": s_sid}
     response = requests.get(url=url, verify=False, headers=headers1)
     res = response.json()
     print(res)
     hostname=res['data'][1]['hostName']
     localIp=res['data'][1]['localIPv4Address']
     systemType=res['data'][1]['systemClassType']
     systemName=res['data'][1]['systemName']
     tempId=res['data'][1]['tempId']

     assert res['status'] == 'success'
     url = 'https://{}/mgmt/dn/system'.format(ip)
     body = {
         "hostName": "cicd-03",
         "is_master": False,
         "localIPv4Address": "10.139.216.178",
         "ssid": s_sid,
         "systemClassType": "dn",
         "systemName": "dl-slave"}

     headers1 = {"Content-Type": "application/json", "ssid": s_sid}
     response = requests.put(url=url, verify=False,
                             data=json.dumps(body), headers=headers1)
     res = response.json()
     print(res)
     assert res['status'] == 'success'


# def test_mgmt_components_five():
#     url = 'https://{}/mgmt/components/list'.format(ip)
#     headers1 = {"Content-Type": "application/json", "ssid": s_sid}
#     response = requests.get(url=url, verify=False, headers=headers1)
#     res = response.json()
#     print(res)
#     assert res['status'] == 'success'


# def test_mgmt_scope_list_six():
#     url = 'https://{}/mgmt/scope/list'.format(ip)
#     headers1 = {"Content-Type": "application/json", "ssid": s_sid}
#     response = requests.get(url=url, verify=False, headers=headers1)
#     res = response.json()
#     print(res)
#     assert res['status'] == 'success'


# def test_mgmt_dn_system_slave_two():
#     url = 'https://{}/mgmt/dn/system'.format(ip)

#     body = {
#         "hostName": "cicd-00",
#         "is_master": False,
#         "localIPv4Address": "10.139.216.180",
#         "ssid": s_sid,
#         "systemClassType": "dn",
#         "systemName": "dl-slave-2"}
#     headers1 = {"Content-Type": "application/json", "ssid": s_sid}
#     response = requests.put(url=url, verify=False,
#                             data=json.dumps(body), headers=headers1)
#     res = response.json()
#     print(res)
#     assert res['status'] == 'success'


def test_mgmt_components_list_three():
    url = 'https://{}/mgmt/components/list'.format(ip)
    headers1 = {"Content-Type": "application/json", "ssid": s_sid}
    response = requests.get(url=url, verify=False, headers=headers1)
    res = response.json()
    print(res)
    hostname=res['data'][0]['hostName']
    localIp=res['data'][0]['localIPv4Address']
    systemType=res['data'][0]['systemClassType']
    systemName=res['data'][0]['systemName']
    tempId=res['data'][0]['tempId']
    assert res['status'] == 'success'
    url = 'https://{}/mgmt/ad/system'.format(ip)
    body = {
        "systemName": systemName,
        "systemClassType": systemType,
        "localIPv4Address": localIp,
        "hostName": hostname,
        "scopeId": ["default"],
        "tempId": tempId,
        "ssid": s_sid
        }
    headers1 = {"Content-Type": "application/json", "ssid": s_sid}
    response = requests.put(url=url, verify=False,
                            data=json.dumps(body), headers=headers1)
    res = response.json()
    print(res)
    assert res['status'] == 'success'


# def test_mgmt_components_list_four():
#     url = 'https://{}/mgmt/components/list'.format(ip)
#     headers1 = {"Content-Type": "application/json", "ssid": s_sid}
#     response = requests.get(url=url, verify=False, headers=headers1)
#     res = response.json()
#     print(res)
#     assert res['status'] == 'success'


# def test_mgmt_components_list_five():
#     url = 'https://{}/mgmt/components/list'.format(ip)
#     headers1 = {"Content-Type": "application/json", "ssid": s_sid}
#     response = requests.get(url=url, verify=False, headers=headers1)
#     res = response.json()
#     print(res)
#     assert res['status'] == 'success'
