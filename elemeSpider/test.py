import execjs

with open('./test.js', 'r', encoding='utf-8')as f:
    js_str = f.read()

ctx = execjs.compile(js_str)
# ctx = execjs.compile(
#     "var windows = 'ss' " 
# )
print(ctx.call("aa()"))