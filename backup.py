import os
import time
import shutil

from queue import Queue

# 设置
## 需要备份的文件夹路径
world_path="server/world"
## 备份文件夹路径
backup_path="backup"
## 备份间隔
backup_interval_seconds=5
## 备份最多保存的数量
backup_numbers=5

# 格式化时间
def get_format_time(time_stamp):
    time_array = time.localtime(time_stamp)
    format_time = time.strftime("%Y-%m-%d-%H-%M-%S", time_array)
    return format_time

# 检查路径，如果存在则删除
def check_dir(path):
    if os.path.exists(path):
        shutil.rmtree(path)

if __name__ == '__main__':

    last_time = 0

    queue = Queue(maxsize=backup_numbers + 1)

    while True:
        # 更新最近一次备份时间
        last_time = int(time.time())

        # 创建新的备份文件夹，如果存在则删除
        format_time = get_format_time(last_time)
        backup_dir_name = str(backup_path) + "/" + str(format_time)
        check_dir(backup_dir_name)
        # os.mkdir(backup_dir_name)

        # 复制文件到备份文件夹
        print("[%s][INFO]Backup start" % get_format_time(int(time.time())))
        shutil.copytree(world_path,backup_dir_name)
        print("[%s][INFO]Backup finish" % get_format_time(int(time.time())))

        # 往队列中加入时间戳
        queue.put(last_time)

        if queue.full():
            # 获取队列中最久的时间戳
            time_stamp_remove = queue.get()
            print("[%s][INFO]Remove backup: %s" % (get_format_time(int(time.time())),get_format_time(time_stamp_remove)) ) 

            # 根据时间戳删除最久的备份文件夹
            path = str(backup_path) + "/" + str(get_format_time(time_stamp_remove))

            # 删除备份文件夹
            shutil.rmtree(path)

        # 等待下一次备份
        time.sleep(backup_interval_seconds)