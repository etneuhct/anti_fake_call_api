import subprocess
import os

class MulawConverter:
    OUTPUT_BITRATE = 4096

    def __init__(self, output_file):
        self.CMD = f"ffmpeg -ar 8000 -ac 1 -f mulaw -i pipe: -f wav {output_file}"
        self.audio_file = output_file

    def process_from_raw(self, bytes: bytearray):
        proc = subprocess.Popen(self.CMD.split(), shell=False,
                                            stdout=subprocess.PIPE,
                                            stdin=subprocess.PIPE,
                                            stderr=subprocess.PIPE, close_fds=True)
        
        proc.stdin.write(bytes)
        out, _ = proc.communicate()
        self.write(out[128:])
        proc.terminate()
    
    def process_from_file(self, input_file):
        # with open(input_file, 'rb') as f:
        #     bytes = f.read()
        if os.path.exists(self.audio_file):
            os.remove(self.audio_file)
        proc = subprocess.Popen(self.CMD.replace('pipe:', str(input_file )).split(), shell=False,
                                            stdout=subprocess.PIPE,
                                            stdin=subprocess.PIPE,
                                            stderr=subprocess.PIPE, close_fds=True)
        proc.stdin.close()
        print(proc.communicate())
        return proc.returncode
    
    def write(self, bytes):
        with open(self.audio_file, 'wb') as f:
            f.write(bytes)
