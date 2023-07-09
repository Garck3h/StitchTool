# -*- coding:utf-8 -*-
import subprocess
import os
import httpx
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm


class subFinder:
    def getDomain(self):
        # 打开txt文件并读取数据
        with open('data.txt', 'r',encoding='utf-8') as file:
            lines = file.readlines()
        # 遍历每一行数据
        for line in lines:
            q = line.strip()  # 去除换行符等空白字符
            # 构建subfinder命令
            command = f'subfinder -d {q} -o ./data/{q}.txt'
            #command = f'/Users/Garck3h/D/Infiltration/tools/web/subfinder/subfinder -h'
            # 执行命令
            print(command)
            # 执行命令
            subprocess.run(command,text=True, shell=True)
        print("域名解析完毕！！！")


    def mergeDomian(self):
        # 指定要合并的文件夹路径
        folder_path = 'data'
        # 获取文件夹中的所有txt文件
        txt_files = [file for file in os.listdir(folder_path) if file.endswith('.txt')]
        # 创建一个新的txt文件用于存储合并后的内容
        output_file = open(input_file, 'w')
        # 遍历每个txt文件并合并内容
        for file_name in txt_files:
            file_path = os.path.join(folder_path, file_name)
            # 打开当前txt文件并读取数据
            with open(file_path, 'r') as file:
                lines = file.readlines()
            # 将文件内容写入输出文件
            output_file.writelines(lines)
        # 关闭输出文件
        output_file.close()
        print("合并成功！！")


class httpxTest:
    #使用httpx来检查url是否存活
    def check_url_alive(self,url):
        url = "https://" + url
        try:
            response = httpx.head(url)
            if response.status_code == 200:
                return True
            else:
                return False
        except httpx.RequestError:
            return False


    def batch_check_urls(self,input_file, output_file):
        with open(input_file, "r") as file:
            urls = file.readlines()

        # 创建进度条，总数为待检测的 URL 数量
        progress_bar = tqdm(total=len(urls))
        # 存储存活的 URL 列表
        alive_urls = []

        def check_alive_url(url):
            # 检测 URL 是否存活
            if httpxTest.check_url_alive(url):
                # 存活的 URL 添加到列表中,并且添加https头
                url = "https://"+url
                alive_urls.append(url)
            # 更新进度条
            progress_bar.update(1)

        #修改线程数
        max_workers = 20
        # 创建线程池
        with ThreadPoolExecutor(max_workers) as executor:
            # 使用多线程并发处理任务
            executor.map(check_alive_url, urls)

        # 关闭进度条
        progress_bar.close()

        with open(output_file, "w") as file:
            for url in alive_urls:
                # 将存活的 URL 写入输出文件
                file.write(url.strip() + "\n")



class DirSearchScanner:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_urls_from_file(self):
        urls = []
        with open(self.file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith("http") or line.startswith("https"):
                    urls.append(line)
        return urls

    def dirsearch_scan(self, target):
        command = f"dirsearch -u {target}"
        # 执行命令
        print(command)
        # 执行命令
        #process = subprocess.run(command, shell=True, capture_output=True, text=True)  #不显示输出
        process = subprocess.run(command, text=True, capture_output=True,shell=True)


        if process.returncode != 0:
            print(f"Error: {process.stderr}")
        else:
            print(f"Scan results for {target}:")
            print(process.stdout)

    def run_scans(self):
        urls = self.read_urls_from_file()
        for url in urls:
            self.dirsearch_scan(url)


if __name__ == '__main__':
    input_file = "subFinderResult.txt"  # 输出的域名////包含待检测的 URL 的文本文件
    output_file = "aliveUrls.txt"  # 存活的 URL 将保存到该文本文件中

   #实例化一个subfinder对象
    subFinder = subFinder()
    subFinder.getDomain()
    subFinder.mergeDomian()

    # 实例化一个httpxTest对象
    httpxTest = httpxTest()
    httpxTest.batch_check_urls(input_file, output_file)

    dirScanner = DirSearchScanner(output_file)
    dirScanner.run_scans()

