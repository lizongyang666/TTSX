from django.core.files.storage import Storage
from fdfs_client.client import Fdfs_client
from django.conf import settings



class FastDFSStorage(Storage):
    """自定义的文件存储系统"""
    def __init__(self, client_conf=None, nginx_url=None):
        if client_conf is None:
            client_conf = settings.FASTDFS_CLIENT_CONF
        self.client_conf = client_conf

        if nginx_url is None:
            nginx_url = settings.FASTDFS_NGINX_URL
        self.nginx_url = nginx_url

    def _open(self, name, mode='rb'):
        """如果项目需要打开文件，返回文件内容，代码在此实现"""
        pass

    def _save(self, name, content):
        """
        保存文件的时候，被调用，如何存储文件，代码在此实现
        :param name:  文件名
        :param content:  传送过来的文件对象，即要保存的文件对象
        :return:
        """
        # 创建fastdfs客户端
        client = Fdfs_client(self.client_conf)

        # 利用客户端保存文件到fastdfs服务器
        file_data = content.read()
        ret = client.upload_by_buffer(file_data)
        # ret是字典
        # { 'Group name' : group_name, 'Remote file_id' : remote_file_id, 'Status' : 'Upload successed.',
        # 'Local file name' : '', 'Uploaded size' : upload_size, 'Storage IP' : storage_ip }

        status = ret.get('status')

        # 判断是否上传成功
        if status != "Upload successed.":
            # 上传失败
            raise Exception("保存文件到fastdfs失败")
        else:
            # 上传成功
            file_id = ret.get("Remote file_id")
            return file_id

    def exists(self, name):
        """
        django调用，用来判断要保存的文件是否存在，如果返回False, django会去调用_save()保存文件
        :param name:
        :return:
        """
        return False

    def url(self, name):
        """
        :param name: 数据库中保存的文件信息，在我们的项目中，是之前保存的file_id
        :return:
        """
        return self.nginx_url + name