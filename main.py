# encoding:utf8

import time
import ds_api

MB = 1024 * 1024.0
GB = 1024 * MB
HOUR = 3600.0
DAY = 24 * HOUR

ds = ds_api.DownloadStationAPI('localhost')
ds.login('username', 'password')

download_task_list = ds.get_download_task()
sort_task_list = []
size_with_low_upload_rate = 0

print 'get %d tasks' % len(download_task_list)

for download_task in download_task_list:
    title = download_task['title']
    size = download_task['size']
    completed_time = download_task['additional']['detail']['completed_time']
    started_time = download_task['additional']['detail']['started_time']
    size_uploaded = download_task['additional']['transfer']['size_uploaded']

    # 计算每字节每日产生的上传数
    if completed_time is not 0:
        day_interval = ((time.time() - completed_time) / DAY)
    else:
        day_interval = ((time.time() - started_time) / DAY)

    daily_upload = size_uploaded / day_interval
    upload_rate = daily_upload / size * 10000 if size > 0 else -1

    sort_task_list += [{
        'title': title,
        'size': size / GB,
        'upload_rate': upload_rate,
        'day_interval': day_interval,
    }]

sort_task_list.sort(key=lambda e: e['upload_rate'])

ac_gb = 0
for t in sort_task_list:

    if t['day_interval'] > 50:
        ac_gb += t['size']
    print '%8.2fGB %8.2fGB %5.1f Days %8.2f  %s' % (
        ac_gb,
        t['size'],
        t['day_interval'],
        t['upload_rate'],
        t['title']
    )

ds.logout()
