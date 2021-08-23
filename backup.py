import os
import subprocess
import datetime
import time

BASE_DIR = "/data/"
BACKUP_DIR = os.path.join(BASE_DIR, "backup", "sql")


def backup_sql():
    # 현재 시각을 가져옴
    today = datetime.datetime.now()
    # 생성될 파일 이름
    file_name = f'{today.year}-{today.month}-{today.day}.sql'
    # 지워질 파일 이름.
    file_name_prev = f'{today.year}-{today.month - 1}-{today.day}.sql'

    # 백업 명령어 실행부
    print(subprocess.getstatusoutput(f'mysqldump -uroot -pwebproj3971-- IBAS > {os.path.join(BACKUP_DIR, file_name)}'))
    print(f'{today} 부로 백업이 완료되었습니다. 파일 경로:[{os.path.join(BACKUP_DIR, file_name)}]')

    # 파일 없음 예외처리
    try:
        os.remove(os.path.join(BACKUP_DIR, file_name_prev))
        print(f"한달 전 백업파일을 제거하였습니다. 파일명:[{file_name_prev}]")
    except FileNotFoundError:
        print("한달 전 백업된 파일이 없습니다.")


def excute(interval=1, **kwargs):
    INTERVAL = -1
    try:
        unit = str(kwargs.get("unit"))
    except TypeError:
        print("숫자를 입력하지 마세요.")
        return
    if unit.lower() == "s":
        INTERVAL = interval
    elif unit.lower() == "m":
        INTERVAL = interval * 60
    elif unit.lower() == "h":
        INTERVAL = interval * 3600
    elif unit.lower() == "d":
        INTERVAL = interval * 86400
    else:
        print("단위를 잘못 입력하였습니다.")
        return

    if INTERVAL != -1:
        while True:
            backup_sql()
            time.sleep(INTERVAL)
