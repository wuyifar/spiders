
import js2py

with open('./test.js', 'r', encoding='utf-8')as f:
    js_str = f.read()

a = js2py.eval_js(js_str)
# print(a.encode(31.185375,121.611191))
print(a.encode(25.087640, 104.934097))
# ctx = execjs.compile(
#     "var windows = 'ss' "
# )
