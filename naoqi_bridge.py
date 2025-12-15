# -*- coding: utf-8 -*-
from naoqi import ALProxy
import sys
import base64

def main():
    if len(sys.argv) < 4:
        print("Usage: python2 naoqi_bridge.py <robot_ip> <port> <base64_utf8_text>")
        sys.exit(1)
    
    robot_ip = sys.argv[1]
    port = int(sys.argv[2])
    b64_text = sys.argv[3]  # ASCII-safe base64 string

    try:
        # 把 base64 -> bytes(UTF-8)
        utf8_bytes = base64.b64decode(b64_text)
    except Exception as e:
        print("ERROR: base64 decode failed: " + str(e))
        sys.exit(1)

    # ALTextToSpeech expects UTF-8 encoded std::string (i.e. bytes in Python2)
    try:
        audioProxy = ALProxy("ALTextToSpeech", robot_ip, port)
        audioProxy.say(utf8_bytes)  # utf8_bytes 是 str (bytes) in Py2
        print("SUCCESS")
    except Exception as e:
        print("ERROR: " + str(e))
        sys.exit(1)

if __name__ == "__main__":
    main()