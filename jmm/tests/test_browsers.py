# -*- coding: utf-8 -*-

import jmm.browsers as script


# def test_http_return(tmpdir, monkeypatch):
#     results = [{
#             "age": 84,
#             "agreeableness": 0.74
#           }
#         ]
#     def mockreturn(request):
#         return BytesIO(json.dumps(results).encode())
#     monkeypatch.setattr(urllib.request, 'urlopen', mockreturn)
#     p = tmpdir.mkdir("program").join("agents.json")
#     # run script
#     script.main(["--dest", str(p), "--count", "1"])
#     local_res = json.load(open(p))
#     assert local_res == script.get_agents(1)


class TestSeleniumHelper(object):
    def setup_method(self):
        pass

    def teardown_method(self):
        pass
    
    
    ###   Utilities   ###

    def fileContent(self, fpath, encoding=None, asSoup=True):
        with open(fpath, "r") as f:
            content = f.read()
        content = content.decode(encoding=encoding) if encoding else content
        if asSoup:
            content = m.soupify(content, False)
        return content
    
    
    ###   TESTS   ###
    
    # def test_foo(self):
    #     assert False
