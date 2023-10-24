from requests.adapters import HTTPAdapter
import ssl

class SSLAdapter(HTTPAdapter):

    def init_poolmanager(self, connections, maxsize, block=False, **pool_kwargs):

        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.set_ciphers('DEFAULT@SECLEVEL=1')
        ssl_context.minimum_version = ssl.TLSVersion.TLSv1
        pool_kwargs['ssl_context'] = ssl_context

        return super().init_poolmanager(connections, maxsize, block, **pool_kwargs)