import pandas as pd
import numpy as np
import time
import os
import requests

from datetime import datetime

# 요청 에러 났을 때 예외처리 하기위한 클래스
class RequestError(Exception):
    pass

class ASOS_Crwaler():
    def __init__(self,std: list, # Area_code
                 start_year: str, # YYYY ex) 2021
                 end_year: str, # YYYY ex) 2022
                 key: list , # decoding key
                 datatype: str, # day or hour
                 start_date: str= '0101', # MMDD
                 end_date: str= '1231', # MMDD
                 startHh: str= '00', # HH
                 endHh: str= '23', # HH
                 ):
        self.std = std
        self.start_year = start_year
        self.end_year = end_year
        self.start_date = start_date
        self.key = key
        self.end_date = end_date
        self.startHh = startHh
        self.endHh = endHh
        self.flagmax = 10

        # 시간단위 일단위 확인해서 바로 크롤러 작동
        self.type = datatype.upper()
        if self.type == 'DAY':
            self.CrwalDay()
        elif self.type == 'HOUR':
            self.CrwalHour()
        else:
            print('타입이 잘못됐습니다. day or hour를 입력해주세요')

    def CrwalDay(self):
        url = 'http://apis.data.go.kr/1360000/AsosDalyInfoService/getWthrDataList'
        
        # 지점 하나씩 돌리기
        for std in self.std:
            df = pd.DataFrame()
            print(f'지점번호 {std} 시작 -- {datetime.now().time()}')
            breaker = False
            # 시작 년도 부터 종료 년도 까지
            for year in range(self.start_year,self.end_year+1):
                print(f'지점번호 {std} : {year}년 시작', end = ' ')
                flag = 0
                if breaker == True:
                    break
                key_idx = 0
                while flag<self.flagmax:
                    key = self.key[key_idx]
                    try:
                        # requests 이용해서 데이터 가져오기
                        params ={'serviceKey' : key, 
                                 'pageNo' : '1', 
                                 'numOfRows' : '366', 
                                 'dataType' : 'json', 
                                 'dataCd' : 'ASOS', 
                                 'dateCd' : 'DAY', 
                                 'startDt' : f'{year}{self.start_date}', 
                                 'endDt' : f'{year}{self.end_date}', 
                                 'stnIds' : f'{std}' }
                        response = requests.get(url, params=params)
                        result = response.json()['response']['header']['resultMsg']

                        # 정상적으로 요청이 들어 온경우
                        if result == 'NORMAL_SERVICE':
                            item = response.json()['response']['body']['items']['item']

                            for i in item:
                                # dict의 value가 리스트형태로 만들어야 DF로 만들수 있어서 리스트로 다 변경
                                i = {k: [v] for k,v in i.items()}

                                # 데이터 프레임 합치기
                                ddf = pd.DataFrame(i)
                                df = pd.concat([df,ddf])

                            # 경로 없으면 생성
                            place = df["stnNm"].unique()[0]
                            path = f'./DataDay/{place}'
                            if not os.path.exists(path):
                                os.makedirs(path)
                            
                            # 데이터 프레임 저장
                            df.to_csv(f'{path}/{year}.csv', index=False, encoding='utf-8 sig')
                            print(f'{year}년 끝 -- {datetime.now().time()}')
                            break

                        # 요청이 잘못된경우 에러코드 및 메세지 보여주기
                        else:
                            raise RequestError(f'요청 실패, 에러 코드 :{result}')
                        
                    except RequestError:
                        key_idx += 1
                        key_idx %= len(key)
                    except:
                        # 최대 10회 재시도
                        flag += 1
                        print(f'{year}년 오류 다시 시작. 시도횟수 {flag}/{self.flagmax}', end = ' ')

    def CrwalHour(self):
        url = 'http://apis.data.go.kr/1360000/AsosHourlyInfoService/getWthrDataList'
        
        # 지점 하나씩 돌리기
        for std in self.std:
            df = pd.DataFrame()
            print(f'지점번호 {std} 시작 -- {datetime.now().time()}')
            breaker = False

            # 시작 년도 부터 종료 년도 까지
            for year in range(self.start_year,self.end_year+1):
                print(f'지점번호 {std} : {year}년 시작', end = ' ')
                flag = 0
                if breaker == True:
                    break
                page = 1
                key_idx = 0
                while flag<self.flagmax:
                    key = self.key[key_idx]
                    try:
                        # requests 이용해서 데이터 가져오기
                        params ={'serviceKey' : key, 
                                 'pageNo' : page, 
                                 'numOfRows' : '880', 
                                 'dataType' : 'json', 
                                 'dataCd' : 'ASOS', 
                                 'dateCd' : 'HR', 
                                 'startDt' : f'{year}{self.start_date}', 
                                 'endDt' : f'{year}{self.end_date}', 
                                 'startHh' : self.startHh,
                                 'endHh' : self.endHh,
                                 'stnIds' : f'{std}' }
                        response = requests.get(url, params=params)
                        result = response.json()['response']['header']['resultMsg']

                        # 정상적으로 요청이 들어 온경우
                        if result == 'NORMAL_SERVICE':
                            item = response.json()['response']['body']['items']['item']
                            for i in item:
                                # dict의 value가 리스트형태로 만들어야 DF로 만들수 있어서 리스트로 다 변경
                                i = {k: [v] for k,v in i.items()}

                                # 데이터 프레임 합치기
                                ddf = pd.DataFrame(i)
                                df = pd.concat([df,ddf])
                            print(f'{page}page 끝',end = ' ')
                            page += 1
                            if page >= 11:
                                place = df["stnNm"].unique()[0]
                                path = f'./DataHour/{place}'

                                # 경로 없으면 생성
                                if not os.path.exists(path):
                                    os.makedirs(path)

                                # 데이터 프레임 저장
                                df.to_csv(f'{path}/{year}.csv', index=False, encoding='utf-8 sig')                                
                                print(f'{year}년 끝 -- {datetime.now().time()}')
                                break                                

                        # 요청이 잘못된경우 에러코드 및 메세지 보여주기
                        else:
                            raise RequestError(f'요청 실패, 에러 코드 :{result}')
                        
                    except RequestError:
                        key_idx += 1
                        key_idx %= len(key)
                    except:
                        # 최대 10회 재시도
                        flag += 1
                        page = 1
                        df = pd.DataFrame()
                        print(f'{year}년 오류 다시 시작. 시도횟수 {flag}/{self.flagmax}', end = ' ')
                        time.sleep(1)