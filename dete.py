import chardet

def detect_file_encoding(file_path):
    with open(file_path, 'rb') as f:
        rawdata = f.read()
    result = chardet.detect(rawdata)
    encoding = result['encoding']
    confidence = result['confidence']
    print(f"检测到文件编码: {encoding}，置信度: {confidence}")
    return rawdata, encoding

def find_invalid_utf8_bytes(rawdata):
    # 逐字节尝试解码，定位非法字节位置
    for i in range(len(rawdata)):
        try:
            rawdata[i:i+1].decode('utf-8')
        except UnicodeDecodeError as e:
            print(f"非法UTF-8字节位置: {i}, 字节值: {rawdata[i]}")
            # 可以扩展打印周围上下文
            context = rawdata[max(i-5,0):min(i+6,len(rawdata))]
            print(f"上下文字节: {context}")
            # 这里只打印第一个错误，后面你可以根据需要调整
            break

if __name__ == "__main__":
    path = ".env"  # 根据你的实际路径调整
    try:
        rawdata, encoding = detect_file_encoding(path)
        if encoding.lower() != "utf-8":
            print(f"警告：.env 文件不是 UTF-8 编码，建议转换编码后再试。")
        # 尝试解码，捕获错误
        try:
            rawdata.decode('utf-8')
            print(".env 文件可以用 UTF-8 解码，没有检测到非法字符。")
        except UnicodeDecodeError:
            print(".env 文件中存在非法 UTF-8 字节，开始定位错误字节...")
            find_invalid_utf8_bytes(rawdata)
    except FileNotFoundError:
        print(f"错误：未找到 {path} 文件，请确认路径是否正确。")
