import json
import os
import subprocess
import datetime
import time


class BackupSql:
    def __init__(self):
        self.json_path = input("setting.json 파일의 경로를 설정해주세요.(파일명 포함) \n미 입력시 현재 디렉토리로 설정됩니다. : ")
        if self.json_path is None or self.json_path == "":
            self.json_path = "./setting.json"
        try:
            print("설정된 경로: ", self.json_path)
            with open(self.json_path, 'r') as f:
                self.setting = json.load(f)
        except FileNotFoundError:
            print("setting.json 파일이 존재하지 않습니다. 프로그램을 종료합니다.")
            return

        try:
            self.base_dir = str(self.setting["BASE_DIR"])
            self.backup_dir = os.path.join(self.base_dir, "backup", "sql")
            self.db_name = str(self.setting["DATABASE_NAME"])
            self.account_id = str(self.setting["ACCOUNT_ID"])
            self.account_pw = str(self.setting["ACCOUNT_PW"])
        except:
            print("설정 값이 유효하지 않습니다. 프로그램을 종료합니다.")
            return

    def backup_sql(self):
        # 현재 시각을 가져옴
        today = datetime.datetime.now()
        # 생성될 파일 이름
        file_name = f'{today.year}-{today.month}-{today.day}.sql'
        # 지워질 파일 이름.
        file_name_prev = f'{today.year}-{today.month - 1}-{today.day}.sql'

        # DB가 저장될 폴더 생성.
        os.makedirs(os.path.join(self.base_dir, "backup", "sql"), exist_ok=True)

        # 백업 명령어 실행부
        operate_statement = f'mysqldump -u{self.account_id} -p{self.account_pw} {self.db_name} > {os.path.join(self.backup_dir, file_name)}'
        exc = subprocess.getstatusoutput(operate_statement)
        if exc[1] == "":
            print(f'{today} 부로 백업이 완료되었습니다. 파일 경로:[{os.path.join(self.backup_dir, file_name)}]')
        else:
            print("DB 연결에 실패하였습니다. setting.json 파일을 다시 봐주세요.")
            return

        # 파일 없음 예외처리
        try:
            os.remove(os.path.join(self.backup_dir, file_name_prev))
            print(f"한달 전 백업파일을 제거하였습니다. 파일명:[{file_name_prev}]")
        except FileNotFoundError:
            print("한달 전 백업된 파일이 없습니다.")

    def excute(self, interval=1, **kwargs):
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
                self.backup_sql()
                time.sleep(INTERVAL)
