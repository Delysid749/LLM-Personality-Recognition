#!/usr/bin/env python
#coding=utf-8
import time
import os
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkcore.auth.credentials import AccessKeyCredential
from aliyunsdkcore.auth.credentials import StsTokenCredential
from aliyunsdkfacebody.request.v20191230.PedestrianDetectAttributeRequest import PedestrianDetectAttributeRequest
from my_personal_key import ALIBABA_CLOUD_ACCESS_KEY_ID,ALIBABA_CLOUD_ACCESS_KEY_SECRET
# Please ensure that the environment variables ALIBABA_CLOUD_ACCESS_KEY_ID and ALIBABA_CLOUD_ACCESS_KEY_SECRET are set.
# 修改credentials和auth的初始化
credentials = AccessKeyCredential(ALIBABA_CLOUD_ACCESS_KEY_ID, ALIBABA_CLOUD_ACCESS_KEY_SECRET)



with open("../data/test.jpg","rb") as f:
    byte_data = f.read()

import oss2
endpoint = 'oss-cn-shanghai.aliyuncs.com' # 假设你的Bucket处于杭州区域
# 修改OSS的auth初始化
auth = oss2.Auth(ALIBABA_CLOUD_ACCESS_KEY_ID, ALIBABA_CLOUD_ACCESS_KEY_SECRET)
bucket = oss2.Bucket(auth, endpoint, 'get-body-feature-fangfangfang')



def get_body_data(image_url):

    # use STS Token
    # credentials = StsTokenCredential(os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID'], os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET'], os.environ['ALIBABA_CLOUD_SECURITY_TOKEN'])
    client = AcsClient(region_id='cn-shanghai', credential=credentials)

    request = PedestrianDetectAttributeRequest()
    request.set_accept_format('json')

    request.set_ImageURL(image_url)

    response = client.do_action_with_exception(request)
    return response

def upload_file_and_get_url(file_path):
    """
    上传文件到OSS并获取共享URL
    
    参数:
        file_path: 要上传的文件路径
        
    返回:
        文件的共享URL
    """
    # 读取文件内容
    with open(file_path, "rb") as f:
        byte_data = f.read()
    
    # 获取文件名作为OSS的key
    file_name = os.path.basename(file_path)
    
    # 上传文件
    bucket.put_object(file_name, byte_data)
    
    # 设置预签名URL过期时间（单位为秒）
    expires = 3600
    
    # 生成预签名URL
    url = bucket.sign_url('GET', file_name, expires)
    
    return url



def generate_person_description(response_data):
    """
    根据人体属性检测结果生成英文描述文本
    
    参数:
        response_data: 二进制格式的响应数据
        
    返回:
        英文描述文本字符串
    """
    # 将二进制数据转换为字符串
    response_str = str(response_data, encoding='utf-8')
    
    # 解析JSON数据
    import json
    data = json.loads(response_str)
    
    # 提取所需属性
    attributes = data['Data']['Attributes'][0]
    
    # 构建英文描述文本
    description = (
        f"Gender: {attributes['Gender']['Name']} (Confidence: {attributes['Gender']['Score']:.2f})\n"
        f"Orientation: {attributes['Orient']['Name']} (Confidence: {attributes['Orient']['Score']:.2f})\n"
        f"Age: {attributes['Age']['Name']} (Confidence: {attributes['Age']['Score']:.2f})\n"
        f"Upper wear type: {attributes['UpperWear']['Name']} (Confidence: {attributes['UpperWear']['Score']:.2f})\n"
        f"Upper wear color: {attributes['UpperColor']['Name']} (Confidence: {attributes['UpperColor']['Score']:.2f})\n"
        f"Wearing glasses: {attributes['Glasses']['Name']} (Confidence: {attributes['Glasses']['Score']:.2f})"
    )
    
    return description

def analyze_person_image(file_path):
    """
    分析人物图片并返回描述文本
    
    参数:
        file_path: 要分析的图片文件路径
        
    返回:
        人物描述文本字符串
    """
    try:
        # 上传文件并获取URL
        image_url = upload_file_and_get_url(file_path)
        print(f"Image URL: {image_url}")
        time.sleep(1)
        
        # 获取人体数据
        response_data = get_body_data(image_url)
        
        # 生成描述文本
        result = generate_person_description(response_data)
        
        return result
    except Exception as e:
        print(e)
        return f"Error analyzing image: {str(e)}"
    finally:
        # 删除上传的文件
        file_name = os.path.basename(file_path)
        bucket.delete_object(file_name)

# 修改后的主程序
if __name__ == "__main__":
    # 示例用法
    description = analyze_person_image("../data/test.jpg")
    print(description)

