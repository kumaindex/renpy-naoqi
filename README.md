功能
把renpy的台词通过naoqi的扬声器说出来


----------------
目录

naoqi_tts 丢在game文件 游戏项目的目录
naoqi_bridge 丢在renpy的根目录或者game


---------------------
使用前先设置好你机器人的发声语言
设置更改你的robot的ip 接口默认是9559，虚拟机器人另算
        robot_ip="192.168.11.135",
        port=9559,
设置好你的python2.7环境   
在2.7环境中添加naoqi 的包
运行的系统环境python应该为pyhon3


----------
在label start:可以开启关闭
    $ naoqi_tts.enabled = False
    "この台詞は読み上げられません。"
    
    $ naoqi_tts.enabled = True
    "この台詞は再び読み上げられます。
