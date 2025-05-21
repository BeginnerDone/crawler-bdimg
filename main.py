import requests
import os
import re
from urllib.parse import quote
from config import KEYWORD, IMAGE_COUNT, SAVE_DIR

def crawl_baidu_images(keyword=KEYWORD, count=IMAGE_COUNT, save_dir=SAVE_DIR):
    """
    爬取百度图片
    :param keyword: 搜索关键词，默认使用配置文件中的设置
    :param count: 爬取图片数量，默认使用配置文件中的设置
    :param save_dir: 图片保存目录，默认使用配置文件中的设置
    """
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    url = f"https://image.baidu.com/search/flip?tn=baiduimage&word={quote(keyword)}&pn=0"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    
    downloaded = 0
    page = 0
    
    while downloaded < count:
        try:
            response = requests.get(url, headers=headers)
            html = response.text
            img_urls = re.findall('"objURL":"(.*?)"', html)
            
            for img_url in img_urls:
                if downloaded >= count:
                    break
                try:
                    img_data = requests.get(img_url, timeout=10).content
                    with open(os.path.join(save_dir, f"{keyword}_{downloaded}.jpg"), 'wb') as f:
                        f.write(img_data)
                    downloaded += 1
                    print(f"已下载 {downloaded}/{count}")
                except Exception as e:
                    print(f"下载失败: {img_url}, 错误: {e}")
            
            page += 1
            url = f"https://image.baidu.com/search/flip?tn=baiduimage&word={quote(keyword)}&pn={page*20}"
        except Exception as e:
            print(f"请求失败: {e}")
            break
    
    print(f"下载完成，共下载 {downloaded} 张图片")

if __name__ == "__main__":
    # 使用配置文件中的参数
    crawl_baidu_images()