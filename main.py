import json
import random
import string
import argparse
from datetime import datetime
import uuid
import time

hosts = []
http_status_codes = [200, 201, 204, 301, 302, 400, 401, 403, 404, 500]
http_methods = ["GET", "POST"]
org_ids = [
    "f4f5d0e2-920b-4e13-8a50-87f81470f927",
    "d8b206fb-61b7-43aa-9e70-6b0c8e08cb14",
    "032e23b5-52e9-4b2c-a66c-9b1dbdca2717",
    "b9461077-2d52-47f5-a26c-6f82ac36a95b",
    "383ba724-ae77-4ab7-bd6c-c3c5db0e5e80",
    "cd68f205-9b33-4a79-991f-9503cfe6e13f",
    "b6c98d1b-b68f-441c-89b2-44068c51a496",
    "a061ba42-001f-4a77-a140-80fb0edcfcdd",
    "0a607fe1-07e7-4e91-96d9-bb5da17d7942",
    "365afad7-810a-4815-9524-3a0952d44ca3"
]
post_uris = [
    "/add/deviceHeartbeat",
    "/add/errors",
    "/add/heartbeats",
    "/add/ffcGroupCount?eventType=0",
    "/add/ffcDetails"
]


def generate_random_string(length):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))


def generate_random_ip():
    return '.'.join(str(random.randint(0, 255)) for _ in range(4))


def generate_current_date_time():
    current_time = datetime.now()
    formatted_time = current_time.strftime('%d/%b/%Y:%H:%M:%S %z')
    return formatted_time


def generate_hostnames():
    i = 0
    while i < 100:
        hosts.append(generate_random_string(10) + ".host.com"),
        i += 1

# Generate fixed hostnames on boot
generate_hostnames()


def generate_log_entry():
    http_method = random.choice(http_methods)
    if http_method == "GET":
        uri = f"/v1.1/customer/get?format=json&mobile={random.randint(1000000000, 9999999999)}&mlp={str(bool(random.getrandbits(1)))}&user_id={str(bool(random.getrandbits(1)))}&next_slab={str(bool(random.getrandbits(1)))}&slab_history={str(bool(random.getrandbits(1)))}&registered_store={str(bool(random.getrandbits(1)))}&registered_till={str(bool(random.getrandbits(1)))}&fraud_details={str(bool(random.getrandbits(1)))}&ndnc_status={str(bool(random.getrandbits(1)))}&optin_status={str(bool(random.getrandbits(1)))}&expiry_schedule={str(bool(random.getrandbits(1)))}&expired_points={str(bool(random.getrandbits(1)))}&points_summary={str(bool(random.getrandbits(1)))}&promotion_points={str(bool(random.getrandbits(1)))}&membership_retention_criteria={str(bool(random.getrandbits(1)))}&tier_upgrade_criteria={str(bool(random.getrandbits(1)))}&gap_to_upgrade_for=0&gap_to_renew_for=0&user_group={str(bool(random.getrandbits(1)))}&transactions={str(bool(random.getrandbits(1)))}&subscriptions={str(bool(random.getrandbits(1)))}&segments={str(bool(random.getrandbits(1)))}&delayed_accrual={str(bool(random.getrandbits(1)))}&tracker_info={str(bool(random.getrandbits(1)))}"
    else:
        uri = random.choice(post_uris)
    pod_id = generate_random_string(6)

    data = {
        "log": json.dumps({
            "host": "storefront.acme.com",
            "remote_addr": generate_random_ip(),
            "remote_user": random.choice(hosts),
            "time_local": "04/Sep/2023:18:30:00 +0530",
            "request": f"{http_method} {uri} HTTP/1.1",
            "request_method": http_method,
            "request_uri": uri,
            "uri": uri,
            "scheme": "http",
            "server_protocol": "HTTP/1.1",
            "status": str(random.choice(http_status_codes)),
            "body_bytes_sent": str(random.randint(1, 100)),
            "http_referer": "-",
            "http_user_agent": f"Java/{generate_random_string(5)}",
            "request_length": str(random.randint(100, 2000)),
            "request_time": f"{random.uniform(0.001, 0.1):.3f}",
            "proxy_upstream_name": "default-storefront-api-8003",
            "proxy_alternative_upstream_name": "",
            "upstream_addr": f"{generate_random_ip()}:8003",
            "response_length": str(random.randint(1, 100)),
            "response_time": f"{random.uniform(0.001, 0.1):.3f}",
            "response_status": str(random.choice(http_status_codes)),
            "req_id": generate_random_string(32),
            "org_id": random.choice(org_ids),
            "till": "-",
            "cap_status_code": "-",
            "is_cache": "-",
            "is_async": "-",
            "is_bulk": "-",
            "uri_path": "-",
            "req_hit_timestamp": str(random.uniform(1600000000, 1700000000)) + ".119"
        }),
        "stream": "stdout",
        "kubernetes": {
            "container_name": "nginx-ingress-controller",
            "pod_name": f"intouch-ingress-nginx-ingress-controller-{pod_id}",
            "host": f"ip-{random.randint(10, 255)}-{random.randint(10, 255)}-{random.randint(10, 255)}-{random.randint(10, 255)}.ec2.internal"
        },
        "key": f"intouch-ingress-nginx-ingress-controller-{pod_id}",
        "app_name": "nginx-ingress"
    }
    return json.dumps(data, separators=(',', ':'))


def generate_logs(num_entries, logs_per_minute):
    interval_seconds = 60.0 / logs_per_minute

    while True:
        for _ in range(num_entries):
            generated_json = generate_log_entry()
            print(generated_json)
        time.sleep(interval_seconds)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate random JSON log entries")
    parser.add_argument("num_entries", type=int, help="Total number of log entries to generate per cycle")
    parser.add_argument("logs_per_minute", type=int, help="Number of log entries to generate per minute")
    args = parser.parse_args()

    generate_logs(args.num_entries, args.logs_per_minute)
