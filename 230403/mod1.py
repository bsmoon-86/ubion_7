def custom_mean(*_list):
    # while문
    # 초기값 지정
    i = 0
    # 합계 변수 생성 0을 대입
    sum = 0
    while i < len(_list):
        # print(_list[i])
        sum += _list[i]
        # i값을 증가
        i += 1   
    # print(sum)
    result = sum / len(_list)
    return result

def custom_max(*_list):
    result = _list[0]
    # 첫번째 원소를 출력?
    # 첫번째 원소와 두번째 원소의 값을 비교하여 큰 값을 result에 대입
    # if result > _list[1]:
    #     result = _list[0]
    # else:
    #     result = _list[1]
    # if result < _list[1]:
    #     result = _list[1]

    # result와 세번째 원소를 비교
    # if result > _list[2]:
    #     result = result
    # else:
    #     result = _list[2]
    # if result < _list[2]:
    #     result = _list[2]

    # for i in range(1, len(_list), 1):
    #     if result < _list[i]:
    #         result = _list[i]
    for i in _list:
        if result < i:
            result = i
    return result
    