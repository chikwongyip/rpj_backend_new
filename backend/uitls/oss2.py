import hashlib
import hmac
import datetime
import requests

# 配置信息
access_key = "LTAI5tYourAccessKey"      # 替换为你的 AK
secret_key = "YourSecretKey"           # 替换为你的 SK
region = "cn-hangzhou"                 # 地区代码
bucket = "your-bucket"                 # 存储桶名称
endpoint = f"{bucket}.oss-{region}.aliyuncs.com"  # 自动构造 endpoint
object_key = "test/example.txt"        # 上传后的文件路径
file_path = "./example.txt"            # 本地文件路径

# 生成 V4 签名需要的时间戳
now = datetime.datetime.utcnow()
amz_date = now.strftime("%Y%m%dT%H%M%SZ")
date_stamp = now.strftime("%Y%m%d")

# 步骤 1: 生成规范请求 (Canonical Request)
http_method = "PUT"
canonical_uri = f"/{object_key}"
canonical_querystring = ""
signed_headers = "host;x-oss-content-sha64;x-oss-date"

# 计算 payload 哈希（上传内容的 SHA256）
with open(file_path, "rb") as f:
    content = f.read()
payload_hash = hashlib.sha256(content).hexdigest()

# 规范 headers
canonical_headers = f"host:{endpoint}\nx-oss-content-sha64:{payload_hash}\nx-oss-date:{amz_date}\n"

# 创建规范请求字符串
canonical_request = (
    f"{http_method}\n"
    f"{canonical_uri}\n"
    f"{canonical_querystring}\n"
    f"{canonical_headers}\n"
    f"{signed_headers}\n"
    f"{payload_hash}"
)

# 步骤 2: 生成待签字符串 (String to Sign)
algorithm = "OSS4-HMAC-SHA256"
credential_scope = f"{date_stamp}/{region}/oss/aliyun_v4_request"
canonical_request_hash = hashlib.sha256(canonical_request.encode()).hexdigest()

string_to_sign = (
    f"{algorithm}\n"
    f"{amz_date}\n"
    f"{credential_scope}\n"
    f"{canonical_request_hash}"
)

# 步骤 3: 生成签名密钥 (Signing Key)


def sign(key, msg):
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()


signing_key = (
    sign(("OSS4" + secret_key).encode("utf-8"), date_stamp)
)
signing_key = sign(signing_key, region)
signing_key = sign(signing_key, "oss")
signing_key = sign(signing_key, "aliyun_v4_request")

# 步骤 4: 计算签名
signature = hmac.new(
    signing_key, string_to_sign.encode("utf-8"), hashlib.sha256
).hexdigest()

# 步骤 5: 构建 Authorization Header
authorization_header = (
    f"{algorithm} Credential={access_key}/{credential_scope}, "
    f"SignedHeaders={signed_headers}, Signature={signature}"
)

# 发送请求
url = f"https://{endpoint}/{object_key}"
headers = {
    "Host": endpoint,
    "x-oss-date": amz_date,
    "x-oss-content-sha64": payload_hash,
    "Authorization": authorization_header,
    "Content-Type": "application/octet-stream"  # 根据实际文件类型修改
}

with open(file_path, "rb") as f:
    response = requests.put(url, headers=headers, data=f)

print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")
