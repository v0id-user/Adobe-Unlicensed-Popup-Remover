from io import TextIOWrapper
from threading import Thread, Lock
import requests, ctypes, time

BLOCKING_AT_LOOPBACK_INTERFACE = False

if not ctypes.windll.shell32.IsUserAnAdmin():
    input("You should run this script as an administrator.")
    exit(1)

class ProcessHostsFile:
    def __init__(self):
        self.hosts_file_path = r'C:\Windows\System32\drivers\etc\hosts'
        self.hosts_fd = None
        self.hosts_content = ""
        self.hosts_content_lines = []
        self.lock = Lock()
        self.__read_hosts_file()

    def __open_hosts_file(self, mode='r+'):
        self.hosts_fd = open(self.hosts_file_path, mode)

    def __read_hosts_file(self):
        with self.lock:
            try:
                with open(self.hosts_file_path, 'r') as f:
                    self.hosts_content_lines = f.readlines()
                    self.hosts_content = "".join(self.hosts_content_lines)
            except IOError:
                raise Exception("Hosts file is not readable. Please run the app as an administrator.")

    def append_to_hosts_file(self, data):
        with self.lock:
            self.__open_hosts_file()
            try:
                self.hosts_content += f"\n{data}"
                self.__write_hosts_file()
            finally:
                self.__close_hosts_file()
    
    def remove_tag_hosts_file(self, tag_start, tag_end):
        with self.lock:
            new_lines = []
            in_tag = False
            for line in self.hosts_content_lines:
                if line.strip() == tag_start:
                    in_tag = True
                    continue
                if line.strip() == tag_end:
                    in_tag = False
                    continue
                if not in_tag:
                    new_lines.append(line)
            self.hosts_content_lines = new_lines
            try:
                with open(self.hosts_file_path, 'w') as f:
                    f.writelines(new_lines)
            except IOError:
                raise Exception("Error writing to hosts file.")
            
    def __write_hosts_file(self):
        self.hosts_fd.seek(0)
        self.hosts_fd.write(self.hosts_content)
        self.hosts_fd.truncate()

    def __close_hosts_file(self):
        if self.hosts_fd:
            self.hosts_fd.close()
            self.hosts_fd = None


class AdobeUpdateServiceBlocker:
    USER_AGENT = "MUCH-THANKS/1.1 @v0id_user" 
    BLOCK_127_ADOBE_HOSTS_ENDPOINT = "https://a.dove.isdumb.one/127.txt"
    BLOCK_0000_ADOBE_HOSTS_ENDPOINT = "https://a.dove.isdumb.one/list.txt"
    BLOCK_TAG_127_START = "# Start Blocking Adobe At 127.0.0.1"
    BLOCK_TAG_127_END = "# End Blocking Adobe At 127.0.0.1"
    BLOCK_TAG_0000_START = "# Start Blocking Adobe At 0.0.0.0"
    BLOCK_TAG_0000_END = "# End Blocking Adobe At 0.0.0.0"
    def __init__(self):
        self.process_hosts_file =  ProcessHostsFile()

    # Optional
    def blocking_at_loopback_interface(self):
        block_list = requests.get(self.BLOCK_127_ADOBE_HOSTS_ENDPOINT, headers={'user-agent': self.USER_AGENT}).text
        hosts_block_list = f"{self.BLOCK_TAG_127_START}\n{block_list}\n{self.BLOCK_TAG_127_END}"
        self.process_hosts_file.append_to_hosts_file(hosts_block_list)

    def blocking_at_service_interface(self):
        block_list = requests.get(self.BLOCK_0000_ADOBE_HOSTS_ENDPOINT, headers={'user-agent': self.USER_AGENT}).text
        hosts_block_list = f"{self.BLOCK_TAG_0000_START}\n{block_list}\n{self.BLOCK_TAG_0000_END}"
        self.process_hosts_file.append_to_hosts_file(hosts_block_list)

    def hosts_file_clean(self):
        self.process_hosts_file.remove_tag_hosts_file(self.BLOCK_TAG_0000_START,self.BLOCK_TAG_0000_END)
        self.process_hosts_file.remove_tag_hosts_file(self.BLOCK_TAG_127_START,self.BLOCK_TAG_127_END)

    def start_block_service(self):
        threads: list = []
        if BLOCKING_AT_LOOPBACK_INTERFACE:
            threads.append(Thread(target=self.blocking_at_loopback_interface))
        threads.append(Thread(target=self.blocking_at_service_interface))
        self.hosts_file_clean()

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()
            


print("Please pay attention...")

AdobeUpdateServiceBlocker().start_block_service()

input('Ok you can close the script now...\nRun it again if the popup appers later...')