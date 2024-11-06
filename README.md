# ASOS
기상청에서 제공하는 ASOS 종관기상관측 자료를 쉽게 다운받기 위한 크롤러입니다.

- [사용전 주의사항](#사용전-주의사항)
- [설치 방법](#설치-방법)
- [사용법](#사용법)
- [라이선스](#라이선스)

## 사용전 주의사항

크롤러를 제작할 때 사용한 파이썬 버전은 3.11.4 버전을 사용했습니다.

key는 아래 사이트에서 신청해서 받을 수 있습니다.

https://www.data.go.kr/index.do

제공받은 키중 Decoding Key를 사용하며 사용법에 따라서 key값을 저장해주세요.

## 설치방법
1. 레포지토리를 클론합니다.

```bash
git clone https://github.com/KangTuna/ASOS.git
```

2. 의존성을 설치합니다.
```bash
pip install -r requirements.txt
```

## 사용법
클론한 폴더에서 cmd 창을 열어 아래 명령어를 입력하고 Keys/DecodingKey.txt 에 key값을 입력해주세요.
```cmd
mkdir Keys
echo. > Keys\DecodingKey.txt
```

크롤러 매개변수
```python
ASOS_Crwaler(std: list, # Area_code
            start_year: str, # YYYY ex) 2021
            end_year: str, # YYYY ex) 2022
            key: list , # decoding key
            datatype: str, # day or hour
            start_date: str= '0101', # MMDD
            end_date: str= '1231', # MMDD
            startHh: str= '00', # HH
            endHh: str= '23', # HH
            ):
```
예제
```python
from ASOS import ASOS_Crwaler

std = [108] # 원하는 지점명 코드 자세한 코드는 API 메뉴얼을 참고
with open('./Keys/DecodingKey.txt', 'r') as f:
    key = f.read().rstrip().split('\n')

# ASOS+Crwaler(지점코드, 시작년도, 종료년도, 키값, 타입)
ASOS_Crwaler(std, 2000, 2010, key, 'day')
```

데이터는 아래 경로와 같이 저장됩니다.
```python
# Day 타입인경우
DataDay/지점명/년도

# Hour 타입인경우
DataHour/지점명/년도
```

## 라이선스

이 프로젝트는 MIT License를 따릅니다. 자세한 내용은  [LICENSE](LICENSE)를 참고하세요.