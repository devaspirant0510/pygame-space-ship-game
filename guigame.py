import tkinter
import tkinter.font
import random

# tkinter 초기화
window = tkinter.Tk()
# 화면 상단 제목 설정
window.title("up&down Game")
# 화면 크키 및 시작 좌표
window.geometry("800x530")
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
font30 = tkinter.font.Font(family="consolas", size=30)
font30bold = tkinter.font.Font(family="consolas",size=30)
font30bold.config(weight="bold")
font50 = tkinter.font.Font(family="consolas", size=50)
font50.config(weight="bold")

game_title_label = tkinter.Label(window, text="Up&Down Game", font=font50, pady=35, fg="#FFA500")
game_title_label.pack()

try_count_label = tkinter.Label(window, text=f'try count : {count}', font=font20, pady=20)
try_count_label.pack()

state_label = tkinter.Label(window, text="", font=font30bold)
state_label.pack()

info_label = tkinter.Label(window, text="please enter a number between 1 and 100", font=font15)
info_label.pack(pady=5)
def on_validate(_, entry_value):
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
    info_label.pack(pady=5)
    info_label.config(text="please enter a number between 1 and 100")
    entry.pack_forget()
    entry.pack(pady=18)
    try_again_message.pack_forget()
    try_count_label.config(text=f'try count : {count}', font=font20)
    state_label.config(text="", font=font20)
    entry.delete(0, "end")
    button.pack()


try_again_button = tkinter.Button(window, text="retry", command=on_click_retry_button, font=font20,bg="#19D219",padx=25,fg="white")
close_button = tkinter.Button(window, text="close", command=on_close_button_click, font=font20)




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
            info_label.pack_forget()
            button.pack_forget()
            entry.pack_forget()
            try_count_label.config(text=f'try count : 0', font=font20)
            try_again_message.pack(pady=10)
            try_again_button.pack()
            return
        try_count_label.config(text=f'try count : {count}', font=font20)
        if get_entry == random_number:
            entry.pack_forget()
            info_label.pack_forget()
            state_label.config(text='Congratulations!', fg='black',font=font30bold)
            button.pack_forget()
            info_label.config(text="")
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