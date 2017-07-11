
CONVERT_ADDRESS = {
    '경기': '경기도',
    '강원': '강원도',
    '충남': '충청남도',
    '충북': '충청북도',
    '전북': '전라북도',
    '전남': '전라남도',
    '경남': '경상남도',
    '경북': '경상북도',
    '인천': '인천광역시'
}


def replace_if_short_address(address):
    short_address = CONVERT_ADDRESS.keys()
    for s_addr in short_address:
        if s_addr in address:
            return address.replace(s_addr, CONVERT_ADDRESS[s_addr])
    return address
