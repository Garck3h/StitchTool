# StitchTool

##实现的功能

1.将subfinder和dirsearch进行了联动
2.实现了自动化探测子域名，然后使用httpx对所探测到的子域名进行200存活的探测。
3.对200存活的URL进行目录猜测，调用的是dirsearch
4.对dirsearch探测到的所有的200的目录URL进行汇总到一个新的txt

##后续实现的功能
1.联动xray进行批量扫描


##后后期的可能
1.使用springboot建设一个web的系统进行管理资产，进行自动化搜集信息，自动化探测漏洞
2.使用echart进行可视化展示
