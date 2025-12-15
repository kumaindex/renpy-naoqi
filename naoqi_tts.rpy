init python:
    import subprocess
    import threading
    import os
    import re
    import base64
    
    class NAOqiTTSManager:
        def __init__(self, robot_ip="192.168.11.135", port=9559, python2_path="python2"):
            self.robot_ip = robot_ip
            self.port = port
            self.python2_path = python2_path
            self.enabled = True
            self.bridge_script = None
            self._find_bridge_script()
        
        def _find_bridge_script(self):
            """ブリッジスクリプトのパスを探す"""
            # Ren'pyのベースディレクトリ
            possible_paths = [
                os.path.join(config.basedir, "naoqi_bridge.py"),
                os.path.join(config.gamedir, "naoqi_bridge.py"),
                "naoqi_bridge.py"
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    self.bridge_script = path
                    print("NAOqi bridge script found at: " + path)
                    return
            
            print("WARNING: naoqi_bridge.py not found!")
        
        def speak(self, text):
            """テキストを音声化"""
            if not self.enabled or not text or not self.bridge_script:
                return
            
            # 別スレッドで音声再生
            thread = threading.Thread(
                target=self._speak_thread,
                args=(text,),
                daemon=True
            )
            thread.start()
        
        def _speak_thread(self, text):
            """音声再生スレッド"""

            try:
                clean_text = re.sub(r'\{[^}]*\}', '', text)
                utf8_bytes = clean_text.encode("utf-8")   # bytes
                b64 = base64.b64encode(utf8_bytes).decode("ascii")  # ASCII-safe string
            except Exception as e:
                print("NAOqi TTS encoding error: " + str(e))
                return

            # 调用 Python2 的 bridge，传入 base64 文本（ASCII，不会有系统编码问题）
            result = subprocess.run(
                [self.python2_path, self.bridge_script, self.robot_ip, str(self.port), b64],
                capture_output=True,
                timeout=30
            )

            # 如果需要读取输出，手动 decode（stdout/stderr 是 bytes）
            try:
                stdout = result.stdout.decode("utf-8", "ignore") if result.stdout else ""
                stderr = result.stderr.decode("utf-8", "ignore") if result.stderr else ""
            except:
                stdout = result.stdout
                stderr = result.stderr

            if result.returncode != 0:
                print("NAOqi TTS error: " + stderr)
            else:
                print("NAOqi TTS: " + stdout.strip())
           

        
        
        def test_connection(self):
            """接続テスト"""
            self.speak("接続テスト")
    
    # NAOqiTTSマネージャーのインスタンスを作成
    # 環境に応じてpython2のパスを調整
    naoqi_tts = NAOqiTTSManager(
        robot_ip="192.168.11.135",
        port=9559,
        python2_path="python2"  # または "python2", "C:\\Python27\\python.exe" など
    )
    
    # Ren'pyのsayをフック
    _original_say = renpy.say
    
    def naoqi_say_wrapper(who, what, *args, **kwargs):
        # TTSで読み上げ
        if what and naoqi_tts.enabled:
            naoqi_tts.speak(what)
        
        # 元のsay関数を呼び出し
        return _original_say(who, what, *args, **kwargs)
    
    # sayをオーバーライド
    renpy.say = naoqi_say_wrapper

# 設定用の変数
default naoqi_tts_enabled = True