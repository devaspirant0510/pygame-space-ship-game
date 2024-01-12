import random

lotto = []
for i in range(7):
    lotto.append(random.randint(1, 5))

ok_count = 0
you_answer_list = []
for i in range(7):
    you_answer = int(input(f"{i + 1}번째 번호: "))
    you_answer_list.append(you_answer)
    if you_answer == lotto[i]:
        ok_count += 1

print(f"7개중 {ok_count}개 맞췄습니다.")
for i in range(7):
    print(f"{i+1}번\t lotto : {lotto[i]}  you : {you_answer_list[i]}")