import tkinter
import tkinter.font
from tkinter import ttk

import random

# tkinter 초기화
window = tkinter.Tk()
# 화면 상단 제목 설정
window.title("up&down Game")
# 화면 크키 및 시작 좌표
window.geometry("800x530+100+100")
# 화면 크기 조절 불가
window.resizable(False, False)

# TODO : entry 에 String var 사용하기
# 1에서 100사이
# 수학적으로 접근했을땐 6에서 7사이
random_number = random.randint(1, 100)
print(random_number)
count = 10
font15 = tkinter.font.Font(family="consolas", size=15)
font20 = tkinter.font.Font(family="consolas", size=20)
font25 = tkinter.font.Font(family="consolas", size=25)
font25bold = tkinter.font.Font(family="consolas", size=25).config(weight="bold")
font30 = tkinter.font.Font(family="consolas", size=30)
font30bold = tkinter.font.Font(family="consolas",size=30)
font30bold.config(weight="bold")
font50 = tkinter.font.Font(family="consolas", size=50)
font50.config(weight="bold")
font15bold = font30.config(weight='bold')

game_title_label = tkinter.Label(window, text="Up&Down Game", font=font50, pady=35, fg="#FFA500")
game_title_label.pack()

try_count_label = tkinter.Label(window, text=f'try count : {count}', font=font20, pady=20)
try_count_label.pack()

state_label = tkinter.Label(window, text="", font=font30bold)
state_label.pack()

rank_label = tkinter.Label(window, text='', font=font25)
rank_label.pack()
rank_label.pack_forget()

title_label = tkinter.Label(window, text="please enter a number between 1 and 100", font=font15)
title_label.pack(pady=5)
def on_validate(char, entry_value):
    return len(entry_value) <= 3
entry = tkinter.Entry(window, width=12,validate="key", font=font20,validatecommand=(window.register(on_validate),"%S","%P"))
entry.pack(pady=18)
try_again_message = tkinter.Label(window, text="can you try again?", font=font20)


def on_close_button_click():
    window.destroy()


def on_click_retry_button():
    global count, random_number
    count = 10
    random_number = random.randint(1, 100)
    print(random_number)
    try_again_button.pack_forget()
    close_button.pack_forget()
    title_label.pack(pady=5)
    title_label.config(text="please enter a number between 1 and 100")
    entry.pack_forget()
    entry.pack(pady=18)
    try_again_message.pack_forget()
    try_count_label.config(text=f'try count : {count}', font=font20)
    state_label.config(text="", font=font20)
    # rank_label.pack_forget()
    entry.delete(0, "end")
    # rank_label.config(text="")
    button.pack()


try_again_button = tkinter.Button(window, text="retry", command=on_click_retry_button, font=font20,bg="#19D219",padx=25,fg="white")
close_button = tkinter.Button(window, text="close", command=on_close_button_click, font=font20)


def get_rank_color(count):
    if count == 9:
        return "#FF0080"  # Ultimate (분홍색)
    elif count == 8:
        return "#FF4500"  # S+ (주황색)
    elif count == 7:
        return "#FFD700"  # S (노란색)
    elif count == 6:
        return "#32CD32"  # A+ (연두색)
    elif count == 5:
        return "#00FF00"  # A (녹색)
    elif count == 4:
        return "#4169E1"  # B (파란색)
    elif count == 3:
        return "#800080"  # C (보라색)
    elif count == 2:
        return "#8B4513"  # D (갈색)
    elif count == 1:
        return "#A0A0A0"
    else:
        return "#808080"  # F (회색)


def on_click_button():
    global entry, state_label, random_number, count, try_again_message
    try:
        get_entry = int(entry.get())
        entry.delete(0, "end")
        if get_entry < 0 or get_entry > 100:
            state_label.config(text="The value must be between 1 and 100.", font=font20, fg='red')
            return
        count -= 1
        if count < 1:
            state_label.config(text='game over',fg='#FF0000',font=font30bold)
            title_label.pack_forget()
            button.pack_forget()
            entry.pack_forget()
            try_count_label.config(text=f'try count : 0', font=font20)
            try_again_message.pack(pady=10)
            try_again_button.pack()
            return
        try_count_label.config(text=f'try count : {count}', font=font20)
        color = get_rank_color(count)
        if get_entry == random_number:
            if count == 9:
                rank = "Ultimate"
            elif count == 8:
                rank = "Master"
            elif count == 7:
                rank = "S+"
            elif count == 6:
                rank = "S"
            elif count == 5:
                rank = "A+"
            elif count == 4:
                rank = "A"
            elif count == 3:
                rank = "B"
            elif count == 2:
                rank = "C"
            elif count == 1:
                rank = "D"
            else:
                rank = "F"
            print(rank, )
            # rank_label.config(text=f"your rank :{rank}", fg=color, )
            # rank_label.pack()
            entry.pack_forget()
            title_label.pack_forget()
            state_label.config(text='Congratulations!', fg='black',font=font30bold)
            button.pack_forget()
            title_label.config(text="")
            try_again_message.pack(pady=10)
            try_again_button.pack()
        elif get_entry < random_number:
            state_label.config(text='Up!!', fg='green', font=font30bold)
        else:
            state_label.config(text='Down!!', fg='red', font=font30bold)

    except ValueError as e:
        if not entry.get() == "":
            state_label.config(text='input error : you must be enter a integer type', font=font20, fg='red')
        else:
            state_label.config(text='input error : Whitespace is not allowed', font=font20, fg='red')
        print(e)


button = tkinter.Button(window, text='Go!', overrelief="raised", pady=5,padx=30, bg="#1976D2", fg="white", font=font20,
                        command=on_click_button)
button.pack()

window.mainloop()
