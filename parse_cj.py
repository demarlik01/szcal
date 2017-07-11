from zipcode.dlv_data import cj
from models import Address
from database import session
from zipcode import path
import asyncio
import aiofiles


def make_result(line, local):
    line = list(map(lambda x: x.replace(' ', ''), line))
    if line[12] == '0':
        addr = '{} {} {} {} {}'.format(line[1], line[3], line[5], line[8], line[11])
    else:
        addr = '{} {} {} {} {}-{}'.format(line[1], line[3], line[5], line[8], line[11], line[12])

    return {
        'zipcode': line[0],
        'address': addr,
        'trimmed_address': addr.replace(' ', ''),
        'add_fee': local['add_fee']
    }


def scrap_match_data(line, local_list):
    item = None
    for local in local_list:
        if line[3] == local['sigungu']:
            if 'gil' in local and local['gil'] == line[8]:
                item = make_result(line, local)
            elif 'dong' in local and local['dong'] == line[17]:
                item = make_result(line, local)
            elif 'ri' in local and local['ri'] == line[18]:
                item = make_result(line, local)
            elif 'eupmyeon' in local and local['eupmyeon'] == line[5]:
                item = make_result(line, local)
    return item


async def parse_zipcode(file_name, local_list):
    async with aiofiles.open(file_name, mode='rb') as f:
        result = list()
        async for line in f:
            line = line.decode('cp949').split('|')
            item = scrap_match_data(line, local_list)
            if item is not None:
                result.append(item)

        return result


async def parse_jeonnam_zipcode(file_name, local_list):
    async with aiofiles.open(file_name, mode='rb') as f:
        result = list()
        async for line in f:
            line = line.decode('cp949').split('|')
            item = scrap_match_data(line, local_list)
            if item is not None:
                result.append(item)

            if line[3] == '신안군':
                if line[5] == '압해읍':
                    if line[18] in ['가린리', '고이리', '매화리']:
                        result.append(make_result(line, {'add_fee': 7000}))
                elif line[5] == '지도읍':
                    if line[18] in ['선도리', '어의리']:
                        result.append(make_result(line, {'add_fee': 7000}))
                elif line[5] == '중도면':
                    if line[18] == '병풍리':
                        result.append(make_result(line, {'add_fee': 7000}))
                else:
                    result.append(make_result(line, {'add_fee': 7000}))

        return result


async def parse_incheon_zipcode(file_name, local_list):
    async with aiofiles.open(file_name, mode='rb') as f:
        result = list()
        async for line in f:
            line = line.decode('cp949').split('|')
            item = scrap_match_data(line, local_list)
            if item is not None:
                result.append(item)

            if line[3] == '옹진군':
                if line[5] != '영흥면':
                    result.append(make_result(line, {'add_fee': 6000}))

        return result


async def parse_jeju_zipcode(file_name):
    async with aiofiles.open(file_name, mode='rb') as f:
        result = list()
        async for line in f:
            line = line.decode('cp949').split('|')
            if line[1] == '제주특별자치도':
                if line[5] == '우도면':
                    result.append(make_result(line, {'add_fee': 9000}))
                elif line[5] == '추자면':
                    result.append(make_result(line, {'add_fee': 10000}))
                else:
                    result.append(make_result(line, {'add_fee': 3000}))
        return result


async def main():
    file_list = cj.ADD_FEE_LIST.keys()
    futures = [
        asyncio.ensure_future(
            parse_zipcode('{path}/{f_name}.txt'.format(path=path.DATA_PATH, f_name=f_name), cj.ADD_FEE_LIST[f_name])
        )
        for f_name in file_list
    ]

    futures.extend([
        asyncio.ensure_future(
            parse_jeonnam_zipcode('{path}/전라남도.txt'.format(path=path.DATA_PATH), cj.ADD_FEE_JEONAM)
        ),
        asyncio.ensure_future(
            parse_incheon_zipcode('{path}/인천광역시.txt'.format(path=path.DATA_PATH), cj.ADD_FEE_INCHEON)
        ),
        asyncio.ensure_future(
            parse_jeju_zipcode('{path}/제주특별자치도.txt'.format(path=path.DATA_PATH))
        )
    ])

    results = await asyncio.gather(*futures)
    for result in results:
        session.bulk_save_objects(
            [Address(**item) for item in result]
        )
        session.commit()
