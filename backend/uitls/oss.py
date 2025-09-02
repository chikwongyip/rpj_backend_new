import oss2
import logging
from typing import List, Dict
from itertools import islice
import asyncio
import os
env_dist = os.environ


class AliyunOSS:
    def __init__(
        self,

        endpoint: str,
        bucket_name: str,
        region: str
    ):
        access_key_id = env_dist.get('OSS_ACCESS_KEY_ID')
        access_key_secret = env_dist.get('OSS_ACCESS_KEY_SECRET')
        self.auth = oss2.Auth(access_key_id, access_key_secret)
        self.bucket = oss2.Bucket(
            self.auth, endpoint=endpoint, bucket_name=bucket_name, region=region
        )
        self.bucket_name = bucket_name
        self.endpoint = endpoint

    def _generate_url(self, key: str) -> str:
        """生成标准 OSS 访问 URL"""
        return f"https://{self.bucket_name}.{self.endpoint.lstrip('https://')}/{key}"

    async def upload_file(self, name: str, data: bytes) -> Dict:
        """上传文件到 OSS"""
        # print('3')
        loop = asyncio.get_event_loop()
        try:
            name = name.lstrip('/')  # 规范路径
            res = await loop.run_in_executor(
                None, self.bucket.put_object, name, data
            )
            print('3')
            return {
                'url': self._generate_url(name),
                'etag': res.etag,
                'key': name
            }
        except oss2.exceptions.OssError as e:
            logging.error(f"OSS Error: {e.message}")
            raise RuntimeError(f"文件上传失败: {e.message}")

    async def list_directories(self, prefix: str = '', delimiter: str = '/') -> List[str]:
        """列举目录"""
        prefix = prefix.lstrip('/')
        result = self.bucket.list_objects_v2(
            prefix=prefix, delimiter=delimiter
        )
        return [cp.prefix for cp in result.prefix_list]

    async def list_objects(self, limit: int = 10) -> List[Dict]:
        """列举对象"""
        try:
            iterator = oss2.ObjectIterator(self.bucket)
            objects = list(islice(iterator, limit))
            return [
                {
                    'url': self._generate_url(obj.key),
                    'etag': obj.etag,
                    'key': obj.key
                }
                for obj in objects if not obj.key.endswith('/')
            ]
        except oss2.exceptions.OssError as e:
            logging.error(f"列举对象失败: {e}")
            raise

    async def delete_object(self, key: str) -> bool:
        """删除对象"""
        try:
            await asyncio.get_event_loop().run_in_executor(
                None, self.bucket.delete_object, key.lstrip('/')
            )
            return True
        except oss2.exceptions.OssError as e:
            logging.error(f"删除失败: {e}")
            return False
