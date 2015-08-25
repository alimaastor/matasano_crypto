
import web
import hashlib
import hmac
import time

import utils

urls = (
    '/test', 'Test',
    '/success', 'Success',
)

timeout = 0.050

def hmac_sha1(key, msg):
    return hmac.HMAC(key, msg, hashlib.sha1).hexdigest()

def insecure_compare(key1, key2):
    assert len(key1) == len(key2)
    key_length = len(key1)
    for i in xrange(0, key_length, 2):
        time.sleep(timeout)
        if key1[i:i+2] != key2[i:i+2]:
            return False
    return True

def to_lower_hex_string(key):
    return str(int(key, 16))

class Test:
    def GET(self):
        data = web.input()
        try:
            if not (data.file and data.signature):
                raise web.internalerror()
        except Exception:
            raise web.internalerror()
        else:

            if insecure_compare(
                    to_lower_hex_string(data.signature),
                    to_lower_hex_string(hmac_sha1(utils.get_passwd(), data.file))):
                raise web.seeother('/success')
            else:
                raise web.internalerror()


class Success:
    def GET(self):
        return """<html><head></head><body>
<h1>Success</h1>
</body></html>"""

def main():
    web.config.debug = False
    app = web.application(urls, globals())
    app.run()


if __name__ == "__main__":

    main()
