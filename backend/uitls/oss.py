# -*- coding: utf-8 -*-
import oss2
from oss2.credentials import EnvironmentVariableCredentialsProvider
from itertools import islice
import os
import logging

# 设置Endpoint和Region


class AliyunOSS:
    def __init__(self, endpoint, bucket_name, region):
        self.endpoint = endpoint
        auth = oss2.ProviderAuthV4(EnvironmentVariableCredentialsProvider())
        self.bucket = oss2.Bucket(
            auth, endpoint=endpoint, bucket_name=bucket_name, region=region)

    def upload_file(self, name, data):
        try:
            res = self.bucket.put_object(name, data)
            return {'url': self.endpoint + name, 'etag': res.etag, 'key': name}
        except oss2.exceptions.OssError as e:
            logging.error(f"Failed to put file")

    def list_directories(self, prefix='', delimiter='/'):
        result = self.bucket.list_objects_v2(
            prefix=prefix, delimiter=delimiter)
        # print(result.prefix_list)
        directories = []

        # 获取当前层级的目录
        for common_prefix in result.prefix_list:
            directories.append(common_prefix)
        return directories

    def list_objects(self):
        try:
            objects = list(islice(oss2.ObjectIterator(self.bucket), 10))
            data = []
            for obj in objects:
                # key = str(obj.key)

                if not obj.key.endswith('/'):
                    item = {'url': self.endpoint + obj.key,
                            'etag': obj.etag, 'key': obj.key}
                    data.append(item)
            return data
        except oss2.exceptions.OssError as e:
            logging.error(f"Failed to list objects: {e}")

    def delete_object(self, key):
        try:
            self.bucket.delete_object(key)
        except oss2.exceptions.OssError as e:
            logging.error(f"Failed to delete objects: {e}")


if __name__ == "__main__":
    # 配置日志
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    # 检查环境变量是否已设置
    required_env_vars = ['OSS_ACCESS_KEY_ID', 'OSS_ACCESS_KEY_SECRET']
    # print(os.environ)
    for var in required_env_vars:

        if var not in os.environ:
            logging.error(f"Environment variable {var} is not set.")
            exit(1)
    auth = oss2.ProviderAuthV4(EnvironmentVariableCredentialsProvider())
    endpoint = "https://oss-cn-shanghai.aliyuncs.com"
    region = "cn-shanghai"
    oss_client = AliyunOSS(
        endpoint=endpoint, bucket_name='rpjtech', region=region)
    file_list = oss_client.list_objects()
    print(file_list)
# bucket_name = generate_unique_bucket_name()
# bucket = oss2.Bucket(auth, endpoint, 'rpjtech', region=region)
# directories = list_directories(bucket)
# res = upload_file(bucket, 'Tencent/brand/23411.txt', data=b'Hello OSS')
# print(res)
# print(directories)
