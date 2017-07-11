# szcal
택배를 보낼때 추가배송금액(도선료)가 발생하는 주소인지 판별하는 HTTP API입니다.  
현재는 CJ대한통운만 지원합니다.  
Python3.5+ 에서 작동합니다

## Install
```
pip install -r requirments.txt
```

## Run
```python
python manage.py fetch_zipcode # 우체국으로부터 우편번호 데이터를 받아옵니다.
python manage.py parse_cj # CJ대한통운기준으로 도서산간지방들의 주소, 우편번호, 추가 배송금액을 DB에 저장합니다.
FLASK_APP=app.py flask run # API RUN
```
## Example
[GET] /cj/secluded_place?address="제주특별자치도 서귀포시  가가로 14"
```js
{
    "additional_fee": 3000,
    "address": "제주특별자치도 서귀포시  가가로 14",
    "zipcode": "63534"
}
```  
`요청한 주소가 추가 배송금액이 붙는 주소지가 아니라면 404를 Reponse합니다`
