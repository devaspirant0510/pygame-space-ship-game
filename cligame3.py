import random

random_number = random.randint(1, 100)

# 시도횟수
count = 0
while True:
    count += 1
    print(f"업&다운 게임 (시도횟수 : {count})")
    input_number = int(input("1~100사이 숫자를 입력해주세요 (종료 :-1): "))
    if input_number == -1:
        print("게임을 종료합니다")
        break
    if input_number == random_number:
        print('정답입니다!!')
        print(f'시도 횟수 :${count}')
        break
    # 정답값이 내가 입력한값보다 클때
    elif input_number < random_number:
        print("Up!!")
    else:
        print("Down!!")
