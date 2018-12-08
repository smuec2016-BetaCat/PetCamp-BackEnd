from alipay import AliPay


app_private_key_string = """-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAzlz5evuv7a0DDrTwQ4tCKdIyBUSk9krtte7iFgSUKzMV632s
uEUK6nGch9MMF/Zqb6Ew19w/c6OjKhrJxMwq9VjTfn4bVyLDbTGHeji+2l/OXaEH
wEejDnsIb1E0HS7MxbgKX6XgpGRTNCm9Mu36Io0qMtUqc2YyN4V/sznk6S0XgNXH
nZq63pHfJcWAHJ9kZFuOFES/5vjZ38mMC/L3r37067uDmDvKLwGZ2C7nmPwIe8ku
cCY4cQ9octtIZv82g4YnGdAPxNBAyRQ/AouXuXTByOEwBwgugkuT/gjoalxa7Yg3
nHM3KCWXnyrP7zje6ZbqOwb+5lAohcwy7OW3EQIDAQABAoIBAFJE0JTN6AoZ0kE3
sx1KVDs1+AkPn7AsmO3R6UIb2zIJsLBsLsJbjAmA94VShty6uR39peo4fPdOAktT
2KJjPrEHE3G3NpEbY8uRVlBMdRG75hp/iwaFyKSKOgee2ObVdH9SaphNGeyPrnf6
N9oo83J40pznTIAq+tQVnZ5G81JdlwDSSRJoPTAv4eF2mB+TiKuXLtnLmlKt09/x
a+10KH92hiKKyXYiKkvrtiD9E+e2+BsLGmaQpqrBZQ+8moSG4QTpmuDZ+bK4gGhm
fo4poI0kz7D5+eUXC8CqBZorTiS9U+lem3mBhPWgplyFSMyeTCrcH1mVHz60Lg+T
W9JvlhECgYEA9QRJQh7k2DBGaGjc4b2ZLWZWmjb4uYzQJ9NkT7EYJj8B4pghQvrh
WCkvpVW81C6Kk348l3fFQqlfrfPn6bBtKXZxHJ0fGIzMe91NYpiDC4CasERSRVhC
EKEZjBWnhlpJPrhzOd96W9FR/hBf7iO6hQll6aVSz3yTFk7NhFo7uBUCgYEA150d
mJXFysTSA2ib+v4m48OsBNraTf6aLIT/7rbmKj67jKhZR6aOvBPP4Jy2epCAQRGz
xMzTKCstfctP4gnVH+84fkTfMEv90gW0PCCVZqhc1otA9ngrKIN/Hwolbx0aDQDc
n4RE+aTTJjNoRNPDKqV8rCVfIL8n6f7HJq6xZg0CgYEAzRWxXC8PzgVaabqcaDeT
J3UpuBubRXSgJzXCGRJa7GiA43IDJVVpmamfv/xr+g6a36oifYY7DvlGpQwramfK
d5I0S4cYqCvyXRt30rdluRMEZ9ZIJtMhOVofUCov9z1LYbxydlagzIoA33BFW8d8
MC8VpuRC1HmphFqhm88LfaECgYAvyjVLIrdKcEGUW9Vm1npMNYylLtUAQJRvlbMc
eBGf/3OWg6H2TaaJbWLACDwyAmFLCt9rmXKcDqXwoeW81i0U/PLqmd1WWSGTMYx3
X0l+DYc2TntBpfT679p3SMpvTGX/x9cezDR1mODsMKzFxKIXi8KMbWQeYAA6zyvZ
GRNc6QKBgAP4kqhqaGdLicuMJoF3pR52zLpr/ztAFcqfb8Wsv+3aVzSN3Gn1jD28
iWCZsTXcKeXXcy5Ob3aGWjd5UAfWaPImUdzTRUxFC4VwR5knQt1xVYAsy0d17E2z
HubIrRdm4zZEzFBmN1Xxewatgz1tJV7ZvDK4LAyJGUSEoHHvy+2+
-----END RSA PRIVATE KEY-----
"""

alipay_public_key_string = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA2VMU1LiL3vdU8dEjHVJ0YzA66BPsghz/f3bnt
FCVS1d1Pd81qIfnFpnMQ44vL3aEfgFfMmPyGw12uXBwPsowEQaKCkBglhX4bvAk4QP611r47KVerH5H
EnjIdoXhgV1mZitXxnlPbqEM8fiJj7ONOvG+QffjTT76vhHzV95lMNUTUs0duzHIZc1zAZDsigb30hxGbo+Cv
6TgSJNeMx2d9FWY2F0OnidrjC098FRN7I5vAHWQx0a6EuvcEaSOkKr6gKy8pHpZxBOsnFalqvf51Ni66P
xWf7Z6hAa6hR8JsJKflL3kB1X6MKL7e3+DD/o8sSOmCIM0Eynm1QWtH8EQSwIDAQAB
-----END PUBLIC KEY-----
"""

alipay = AliPay(
    appid="2016092000552187",
    app_notify_url=None,  # 默认回调url
    app_private_key_string=app_private_key_string,
    # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
    alipay_public_key_string=alipay_public_key_string
)

order_string = alipay.api_alipay_trade_page_pay(
    out_trade_no="200",
    subject="iPhone XR MIN",
    total_amount=1211.12,
    return_url="http://www.itsyuekao.com"
)

print("https://openapi.alipaydev.com/gateway.do?" + order_string)
