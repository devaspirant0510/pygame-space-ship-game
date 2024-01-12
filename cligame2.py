import random


def generate_secret_number():
    return random.sample(range(1, 10), 4)


def compare_numbers(secret, guess):
    strike = 0
    ball = 0
    for i in range(4):
        if guess[i] == secret[i]:
            strike += 1
        elif guess[i] in secret:
            ball += 1
    return strike, ball


def main():
    print("숫자 야구 게임을 시작합니다. 1부터 9까지의 서로 다른 숫자로 이루어진 네 자리 수를 맞춰보세요.")

    secret_number = generate_secret_number()
    attempts = 0

    while True:
        user_input = input("네 자리 숫자를 입력하세요(ex : 1234) 종료버튼은 : ")

        try:
            user_guess = [int(digit) for digit in user_input]
        except ValueError:
            print("올바른 형식의 숫자를 입력하세요.")
            continue

        if len(user_guess) != 4 or len(set(user_guess)) != 4:
            print("서로 다른 세 자리 숫자를 입력하세요.")
            continue

        attempts += 1

        strike, ball = compare_numbers(secret_number, user_guess)

        print(f"결과: {strike} 스트라이크, {ball} 볼")

        if strike == 3:
            print(f"축하합니다! {attempts}번째 시도에 정답을 맞추셨습니다.")
            break


main()
