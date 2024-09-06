import base64

# ICO转base64 img\rabbit.ico
open_ico = open(r".\img\rabbit.ico","rb")

b64str = base64.b64encode(open_ico.read()) #转换为base64编码
open_ico.close()
write_data = "imgBase64 = %s" % b64str
f = open(r".\img\rabbit.py","w+")
f.write(write_data) # 写入文件
f.close()