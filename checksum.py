# 기능: XOR 연산을 수행하여 최종적으로 체크섬을 구한다
# 입력: 피제수 (원본 데이터), 제수 (이진수 문자열로 표현된 다항식)
# 출력: 나머지 (즉, 체크섬)
def xor_division(dividend, divisor):
    dividend = list(dividend)
    divisor_len = len(divisor)

    # 첫 비트가 1인 곳을 찾아 XOR 연산을 수행한다
    for i in range(len(dividend) - divisor_len + 1):
        if dividend[i] == '1':  
            for j in range(divisor_len):
                # XOR 연산 수행
                dividend[i + j] = str(int(dividend[i + j]) ^ int(divisor[j]))

    # 나머지 (즉, 체크섬)을 반환한다.
    return ''.join(dividend[-(divisor_len - 1):])



# 기능: 주어진 다항식의 차수에 따라 알맞은 값을 부여하는 함수
# 입력: 현재 항의 차수, 각 항의 차수를 저장할 딕셔너리, 첫 번째 항인지 여부를 나타내는 변수
# 출력: 최고 차수, 이진수로 변환된 다항식
def create_degree_dict(degree, degree_dict, first_term):
    degree = int(degree)
    
    if first_term == 1:  # 첫 번째 항일 경우
        
        # 최고차수 항에 해당하는 계수는 1, 그 아래 차수항의 계수는 전부 0으로 설정
        for i in range(degree, -1, -1):
            if i == degree: 
                degree_dict[i] = 1
            else:
                degree_dict[i] = 0
                
        return degree, degree_dict  # 첫 번째 항은 차수와 딕셔너리를 모두 반환
    
    # 첫 번째 항이 아닌 경우
    else:
        degree_dict[degree] = 1
    return degree_dict  # 딕셔너리만 반환



# 기능: 다항식을 이진수 형태로 변환하는 함수
# 입력: 다항식 문자열
# 출력: 최고 차수, 이진수로 변환된 다항식
def polynomial(poly):
    first_term = 1 # 첫번째 항인지 여부를 확인하기 위한 변수
    degree_dict = {} # 차수와 계수를 저장할 딕셔너리
    polytoNum = [] #이진수로 변환된 다항식을 저장할 리스트
    
    # 입력한 다항식을 '+'로 구분한다
    poly = poly.replace(" ", "")
    term = poly.split('+') 
    
    # 각 항에 대한 처리
    for i in term:
        if 'x' in i: # 항에 x가 있으면
            if '^' in i: # 항에 ^가 있으면
                caret_position = i.find('^')
                degree = i[caret_position + 1:] # 차수만 추출
            else:
                degree = 1 # 만약 x만 있고 ^가 없다면 차수는 1이다
        else:
            degree = 0 # 상수항이면 차수는 0

        # 첫 번째 항일 경우 (최고차수와 딕셔너리 반환받음)
        if first_term == 1: 
            first_degree, degree_dict = create_degree_dict(degree, degree_dict, first_term)
            
        # 두 번째 항부터 (딕셔너리만 반환받음)
        else:
            degree_dict = create_degree_dict(degree, degree_dict, first_term)

        first_term = 0  # 첫 번째 항이 끝났음을 표시
    
    # 차수에 따라 이진수로 변환
    for i in range(max(degree_dict.keys()), -1, -1):  # 차수의 순서대로 값 생성
        
        # 차수가 존재하면 1을, 존재하지 않으면 0을 부여한다
        if degree_dict.get(i, 0) == 1:
            polytoNum.append('1')
        else:
            polytoNum.append('0')
    
    # 차례대로 추가된 1과 0을 하나의 문자열로 결합한다
    polytoNum_str = ''.join(polytoNum)
 
    # 최고차수, 이진수 문자열 (다항식)을 반환한다
    return first_degree, polytoNum_str 



# 기능: 체크섬을 계산한다
# 입력: 이진수 문자열 (다항식), 원본 데이터, 최고차수
# 출력: x (없음)
def calculate(polytoNum, data_input, first_degree):
    # 데이터를 리스트로 변환 (0을 더하기 위함임)
    data_input = list(data_input)
    
    # 데이터에 0을 최고차수만큼 더한다
    for i in range(first_degree):
        data_input.append('0')
        
    # 데이터를 다시 문자열로 결합
    data_input = ''.join(data_input)
    print("$ 확장된 데이터: ", data_input)
    
    # XOR 나눗셈 수행
    checksum = xor_division(data_input, polytoNum)
    print("$ 계산된 체크섬: ", checksum)
    
    
    
# 기능: 사용자 입력 처리 함수
# 입력: X (없음)
# 출력: X (없음)
def input_poly():
    # 다항식 입력
    poly = input("\n# 생성 다항식 G(x)를 입력해주세요 (예: x^2 + x + 1)\n>> ")
    
    # 다항식을 이진수로 변환 (최고차수와 이진수를 반환받는다)
    first_degree, polytoNum = polynomial(poly)
    print("$ 생성 다항식 (이진수): ", polytoNum)

    # 데이터 입력
    data_input = input("\n# 데이터를 입력해주세요 (예: 101101)\n>> ")
    print("$ 입력된 데이터: ", data_input)
    
    # 체크섬 계산
    calculate(polytoNum, data_input, first_degree)



# 프로그램 실행
input_poly()
