import tkinter as tk  # 모듈이름을 별칭으로 import함
from tkinter import ttk, messagebox
from datetime import date, timedelta  #from ~ import ~ 를 이용해서 모듈이름.클래스이름 다 안써도 됨 ---> 클래스이름만 단독사용가능


WEEKDAYS_KR = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]



# ================== 일반 함수 =====================


# 0. 공통 함수 #

# 문자열로 입력받은 날짜를 date객체로 변환하는 함수
 # 날짜가 잘못된 값이면 ValueError 발생. --> 이 함수를 호출하는 GUI함수에서 try-except문으로 예외처리
def make_date(year_text, month_text, day_text): 

    year = int(year_text)   #우선 문자열을 정수로 변환
    month = int(month_text)
    day = int(day_text)

    return date(year, month, day)
    

# date 객체를 요일 이름으로 반환하는 함수
def get_weekday_name(target_date):
    return WEEKDAYS_KR[target_date.weekday()]



# 1. 'n일 전/후 날짜 및 요일 계산 기능'에 필요한 함수 #

# 기준일로부터 n일 전/후의 날짜 계산 함수
 # start_1=True이면 기준일을 1일차로 보고 n-1일만 이동
def move_date(base_date, n, direction, start_1=False): ###
    if start_1 and n > 0:
        n -= 1

    days = timedelta(days=n)

    if direction == "전":
        result_date = base_date - days
    else:
        result_date = base_date + days

    weekday_name = get_weekday_name(result_date)
    return result_date, weekday_name



# 2. '디데이 기능'에 필요한 함수

# 오늘 날짜 기준으로 목표 날짜와의 차이일수 계산 후 D-day 문자열 반환 함수
 # 디데이는 오늘과 목표 날짜 사이의 순수 날짜 차이를 사용한다.
def calc_d_day(target_date):
    today = date.today()
    diff = (today - target_date).days

    if diff > 0:
        return f"D+{diff}"
    elif diff == 0:
        return "D-day"
    else:
        return f"D-{abs(diff)}"
    

# 일수를 대략적인 개월 수 문자열로 바꾸는 함수
def format_approx_months(days):
    months = round(days / 30, 1)  #(1개월을 약 30일로 보고 계산)
    return f"약 {months}개월"

# 일수를 대략적인 년 수 문자열로 바꾸는 함수
def format_approx_years(days):
    years = round(days / 365, 1)  #(1년을 약 365일로 보고 계산)
    return f"약 {years}년"



# 3. 두 날짜 간 기간 계산 기능에 필요한 함수

# 두 날짜 간 기간 일수 계산 함수
 # 시작일, 끝일 포함 여부를 각각 선택할 수 있다.
def calc_period(start_date, end_date, include_start, include_end):
    diff = abs((end_date - start_date).days)

    if include_start and include_end:
        result = diff + 1
    elif not include_start and not include_end:
        result = diff - 1
    else:
        result = diff

    if result < 0:
        result = 0

    return result


# 일수를 대략적인 년 + 개월 문자열로 바꾸는 함수
 # 기간 계산에서 "총 n일 (약 x년 y개월)" 형태로 쓰기 위함
def format_approx_years_months(days):
    total_months = round(days / 30)
    years = total_months // 12
    months = total_months % 12

    return f"약 {years}년 {months}개월"



# ================== GUI 이벤트 함수 =====================
'''
GUI 이벤트 함수는 쉽게 말해 "버튼이 눌렸을 때 실행되는 함수들"을 의미.

CLI에서는 사용자가 입력하고 엔터를 치면 코드가 위에서 아래로 실행.

GUI에서는 "프로그램이 창을 띄워놓고 대기, 사용자가 버튼을 누르면 그때 연결된 함수가 실행."
'''


# 1. 'n일 전/후 날짜 및 요일 계산 기능'에 필요한 함수

def calculate_move_date():
    try:
        n = int(move_n_entry.get())
        direction = move_direction_var.get()
        start_1 = move_start_1_var.get()

        if n < 0:
            messagebox.showerror("입력 오류", "일수는 0 이상의 정수로 입력하세요.")
            return

        if move_base_var.get() == "오늘":
            base_date = date.today()
        else:
            base_date = make_date(move_year_entry.get(), move_month_entry.get(), move_day_entry.get())

        result_date, weekday_name = move_date(base_date, n, direction, start_1)

        option_text = ""
        if start_1:
            option_text = "\n(시작일 1일차로)"

        move_result_label.config(
            text=f"{result_date}  {weekday_name} {option_text}"
        )

    except ValueError:
        messagebox.showerror("입력 오류", "숫자 형식이 잘못되었거나 존재하지 않는 날짜입니다.")
    except Exception:
        messagebox.showerror("오류", "예상하지 못한 오류가 발생했습니다.")


def calculate_weekday_only():
    try:
        if move_base_var.get() == "오늘":
            target_date = date.today()
        else:
            target_date = make_date(move_year_entry.get(), move_month_entry.get(), move_day_entry.get())

        weekday_name = get_weekday_name(target_date)

        move_result_label.config(
            text=f"{target_date}  {weekday_name}"
        )

    except ValueError:
        messagebox.showerror("입력 오류", "숫자 형식이 잘못되었거나 존재하지 않는 날짜입니다.")
    except Exception:
        messagebox.showerror("오류", "예상하지 못한 오류가 발생했습니다.")


def toggle_specific_date_entries():
    """
    기준일 선택에서 '오늘'을 고르면 입력칸을 오늘 날짜로 초기화한 뒤 비활성화하고,
    '특정일'을 고르면 입력칸을 활성화.
    """
    if move_base_var.get() == "오늘":
        today_date = date.today()

        # Entry가 disabled 상태이면 내용을 수정할 수 없으므로 먼저 normal로 변경.
        move_year_entry.config(state="normal")
        move_month_entry.config(state="normal")
        move_day_entry.config(state="normal")
        
        move_year_entry.delete(0, "end")
        move_month_entry.delete(0, "end")
        move_day_entry.delete(0, "end")

        move_year_entry.insert(0, str(today_date.year))
        move_month_entry.insert(0, str(today_date.month))
        move_day_entry.insert(0, str(today_date.day))

        move_year_entry.config(state="disabled")
        move_month_entry.config(state="disabled")
        move_day_entry.config(state="disabled")
    else:
        move_year_entry.config(state="normal")
        move_month_entry.config(state="normal")
        move_day_entry.config(state="normal")



# 2. '디데이 기능'에 필요한 함수

def calculate_d_day():
    try:
        target_date = make_date(dday_year_entry.get(), dday_month_entry.get(), dday_day_entry.get())

        today = date.today()
        diff = (target_date - today).days
        abs_days = abs(diff)
        result = calc_d_day(target_date)
        weekday_name = get_weekday_name(target_date)

        extra_lines = []
        state_word = "남음" if diff >= 0 else "지남"

        if dday_show_month_var.get():
            extra_lines.append(f"{format_approx_months(abs_days)} {state_word}")

        if dday_show_year_var.get():
            extra_lines.append(f"{format_approx_years(abs_days)} {state_word}")

        result_text = f"오늘: {today} {get_weekday_name(today)}\n"
        result_text += f"목표일: {target_date} {weekday_name}\n\n"
        result_text += result

        if extra_lines:
            result_text += "\n\n" + "\n".join(extra_lines)

        dday_result_label.config(text=result_text)

    except ValueError:
        messagebox.showerror("입력 오류", "숫자 형식이 잘못되었거나 존재하지 않는 날짜입니다.")
    except Exception:
        messagebox.showerror("오류", "예상하지 못한 오류가 발생했습니다.")



# 3. 두 날짜 간 기간 계산 기능에 필요한 함수

def calculate_period():
    try:
        start_date = make_date(period_start_year_entry.get(),
                               period_start_month_entry.get(),
                               period_start_day_entry.get())

        end_date = make_date(period_end_year_entry.get(),
                             period_end_month_entry.get(),
                             period_end_day_entry.get())
        
        if start_date > end_date:
            messagebox.showerror("입력 오류", "시작일은 끝일보다 늦을 수 없습니다.")
            return

        include_start = period_start_include_var.get()
        include_end = period_end_include_var.get()

        result = calc_period(start_date, end_date, include_start, include_end)

        period_text = f"총 {result}일"

        show_year = period_show_year_var.get()
        show_month = period_show_month_var.get()

        if show_year and show_month:
            period_text += f" ({format_approx_years_months(result)})"
        elif show_year:
            period_text += f" ({format_approx_years(result)})"
        elif show_month:
            period_text += f" ({format_approx_months(result)})"

        period_result_label.config(
            text=f"시작일: {start_date} {get_weekday_name(start_date)}\n"
                 f"끝일: {end_date} {get_weekday_name(end_date)}\n\n"
                 f"{period_text}"
        )

    except ValueError:
        messagebox.showerror("입력 오류", "숫자 형식이 잘못되었거나 존재하지 않는 날짜입니다.")
    except Exception:
        messagebox.showerror("오류", "예상하지 못한 오류가 발생했습니다.")



# ================== GUI 화면 구성 코드 =====================

window = tk.Tk()
window.title("쉬운 날짜·요일 계산기")
window.geometry("620x560")
window.resizable(False, False)
window.configure(bg="white")

style = ttk.Style()
style.configure("TNotebook", background="white")
style.configure("TNotebook.Tab", background="white")
style.configure("TFrame", background="white")

title_label = tk.Label(
    window,
    text="쉬운 날짜·요일 계산기",
    font=("맑은 고딕", 18, "bold"),
    bg="white"
)
title_label.pack(pady=15)

notebook = ttk.Notebook(window)
notebook.pack(expand=True, fill="both", padx=15, pady=10)


# 탭 1. n일 전/후 계산

move_frame = ttk.Frame(notebook)
notebook.add(move_frame, text="n일 전/후 계산")

move_base_var = tk.StringVar(value="오늘")
move_direction_var = tk.StringVar(value="후")
move_start_1_var = tk.BooleanVar(value=False)

tk.Label(move_frame, text="1. 기준일 선택", font=("맑은 고딕", 12, "bold"), bg="white").pack(anchor="w", padx=20, pady=(20, 5))

base_radio_frame = tk.Frame(move_frame, bg="white")
base_radio_frame.pack(anchor="w", padx=20)

tk.Radiobutton(
    base_radio_frame,
    text="오늘",
    variable=move_base_var,
    value="오늘",
    command=toggle_specific_date_entries,
    bg="white"
).pack(side="left", padx=5)

tk.Radiobutton(
    base_radio_frame,
    text="특정일",
    variable=move_base_var,
    value="특정일",
    command=toggle_specific_date_entries,
    bg="white"
).pack(side="left", padx=5)

move_date_frame = tk.Frame(move_frame, bg="white")
move_date_frame.pack(anchor="w", padx=20, pady=8)

move_year_entry = tk.Entry(move_date_frame, width=8)
move_year_entry.pack(side="left")
tk.Label(move_date_frame, text="년", bg="white").pack(side="left", padx=3)

move_month_entry = tk.Entry(move_date_frame, width=5)
move_month_entry.pack(side="left")
tk.Label(move_date_frame, text="월", bg="white").pack(side="left", padx=3)

move_day_entry = tk.Entry(move_date_frame, width=5)
move_day_entry.pack(side="left")
tk.Label(move_date_frame, text="일", bg="white").pack(side="left", padx=3)

today = date.today()
move_year_entry.insert(0, str(today.year))
move_month_entry.insert(0, str(today.month))
move_day_entry.insert(0, str(today.day))

toggle_specific_date_entries()

tk.Label(
    move_frame,
    text="2. 이동할 일수 입력",
    font=("맑은 고딕", 12, "bold"),
    bg="white"
).pack(anchor="w", padx=20, pady=(15, 5))

move_n_frame = tk.Frame(move_frame, bg="white")
move_n_frame.pack(anchor="w", padx=20)

move_n_entry = tk.Entry(move_n_frame, width=10)
move_n_entry.pack(side="left")
tk.Label(move_n_frame, text="일", bg="white").pack(side="left", padx=5)

tk.Label(move_frame, text="3. 전/후 선택", font=("맑은 고딕", 12, "bold"), bg="white").pack(anchor="w", padx=20, pady=(15, 5))

direction_frame = tk.Frame(move_frame, bg="white")
direction_frame.pack(anchor="w", padx=20)

tk.Radiobutton(direction_frame, text="후", variable=move_direction_var, value="후", bg="white").pack(side="left", padx=5)
tk.Radiobutton(direction_frame, text="전", variable=move_direction_var, value="전", bg="white").pack(side="left", padx=5)

button_frame = tk.Frame(move_frame, bg="white")
button_frame.pack(anchor="w", padx=20, pady=15)

tk.Checkbutton(
    button_frame,
    text="시작일을 1일차로",
    variable=move_start_1_var,
    bg="white"
).pack(side="left", padx=5)

tk.Button(button_frame, text="n일 전/후 계산", width=18, command=calculate_move_date, bg="white").pack(side="left", padx=5)
tk.Button(button_frame, text="기준일 요일 확인", width=18, command=calculate_weekday_only, bg="white").pack(side="left", padx=5)

move_result_label = tk.Label(
    move_frame,
    text="결과가 여기에 표시됩니다.",
    font=("맑은 고딕", 12),
    bg="#E6F7FF",
    fg="black",
    width=55,
    height=5,
    relief="solid",
    anchor="center",
    justify="center"
)
move_result_label.pack(padx=20, pady=10)


# 탭 2. D-day 계산

dday_frame = ttk.Frame(notebook)
notebook.add(dday_frame, text="D-day 계산")

dday_show_month_var = tk.BooleanVar(value=False)
dday_show_year_var = tk.BooleanVar(value=False)

tk.Label(dday_frame, text="목표 날짜 입력", font=("맑은 고딕", 12, "bold"), bg="white").pack(anchor="w", padx=20, pady=(25, 5))

dday_date_frame = tk.Frame(dday_frame, bg="white")
dday_date_frame.pack(anchor="w", padx=20, pady=8)

dday_year_entry = tk.Entry(dday_date_frame, width=8)
dday_year_entry.pack(side="left")
tk.Label(dday_date_frame, text="년", bg="white").pack(side="left", padx=3)

dday_month_entry = tk.Entry(dday_date_frame, width=5)
dday_month_entry.pack(side="left")
tk.Label(dday_date_frame, text="월", bg="white").pack(side="left", padx=3)

dday_day_entry = tk.Entry(dday_date_frame, width=5)
dday_day_entry.pack(side="left")
tk.Label(dday_date_frame, text="일", bg="white").pack(side="left", padx=3)

dday_year_entry.insert(0, str(today.year))
dday_month_entry.insert(0, str(today.month))
dday_day_entry.insert(0, str(today.day))

dday_button_frame = tk.Frame(dday_frame, bg="white")
dday_button_frame.pack(anchor="w", padx=20, pady=20)

tk.Button(dday_button_frame, text="D-day 계산", width=16, command=calculate_d_day, bg="white").pack(side="left", padx=5)
tk.Checkbutton(dday_button_frame, text="개월수 표시", variable=dday_show_month_var, bg="white").pack(side="left", padx=5)
tk.Checkbutton(dday_button_frame, text="년수 표시", variable=dday_show_year_var, bg="white").pack(side="left", padx=5)

dday_result_label = tk.Label(
    dday_frame,
    text="결과가 여기에 표시됩니다.",
    font=("맑은 고딕", 12),
    bg="#E6F7FF",
    fg="black",
    width=55,
    height=11,
    relief="solid",
    anchor="center",
    justify="center"
)
dday_result_label.pack(padx=20, pady=(10, 20))


# 탭 3. 기간 계산

period_frame = ttk.Frame(notebook)
notebook.add(period_frame, text="기간 계산")

period_start_include_var = tk.BooleanVar(value=False)   # 기본값: 시작일 제외
period_end_include_var = tk.BooleanVar(value=True)      # 기본값: 끝일 포함
period_show_year_var = tk.BooleanVar(value=False)
period_show_month_var = tk.BooleanVar(value=False)

tk.Label(period_frame, text="시작일 입력", font=("맑은 고딕", 12, "bold"), bg="white").pack(anchor="w", padx=20, pady=(20, 5))

period_start_frame = tk.Frame(period_frame, bg="white")
period_start_frame.pack(anchor="w", padx=20, pady=5)

period_start_year_entry = tk.Entry(period_start_frame, width=8)
period_start_year_entry.pack(side="left")
tk.Label(period_start_frame, text="년", bg="white").pack(side="left", padx=3)

period_start_month_entry = tk.Entry(period_start_frame, width=5)
period_start_month_entry.pack(side="left")
tk.Label(period_start_frame, text="월", bg="white").pack(side="left", padx=3)

period_start_day_entry = tk.Entry(period_start_frame, width=5)
period_start_day_entry.pack(side="left")
tk.Label(period_start_frame, text="일", bg="white").pack(side="left", padx=3)

period_start_year_entry.insert(0, str(today.year))
period_start_month_entry.insert(0, str(today.month))
period_start_day_entry.insert(0, str(today.day))

tk.Checkbutton(period_frame, text="시작일 포함", variable=period_start_include_var, bg="white").pack(anchor="w", padx=20)

tk.Label(period_frame, text="끝일 입력", font=("맑은 고딕", 12, "bold"), bg="white").pack(anchor="w", padx=20, pady=(15, 5))

period_end_frame = tk.Frame(period_frame, bg="white")
period_end_frame.pack(anchor="w", padx=20, pady=5)

period_end_year_entry = tk.Entry(period_end_frame, width=8)
period_end_year_entry.pack(side="left")
tk.Label(period_end_frame, text="년", bg="white").pack(side="left", padx=3)

period_end_month_entry = tk.Entry(period_end_frame, width=5)
period_end_month_entry.pack(side="left")
tk.Label(period_end_frame, text="월", bg="white").pack(side="left", padx=3)

period_end_day_entry = tk.Entry(period_end_frame, width=5)
period_end_day_entry.pack(side="left")
tk.Label(period_end_frame, text="일", bg="white").pack(side="left", padx=3)

period_end_year_entry.insert(0, str(today.year))
period_end_month_entry.insert(0, str(today.month))
period_end_day_entry.insert(0, str(today.day))

tk.Checkbutton(period_frame, text="끝일 포함", variable=period_end_include_var, bg="white").pack(anchor="w", padx=20)

period_button_frame = tk.Frame(period_frame, bg="white")
period_button_frame.pack(anchor="w", padx=20, pady=20)

tk.Button(period_button_frame, text="기간 계산", width=16, command=calculate_period, bg="white").pack(side="left", padx=5)
tk.Checkbutton(period_button_frame, text="개월수 표시", variable=period_show_month_var, bg="white").pack(side="left", padx=5)
tk.Checkbutton(period_button_frame, text="년수 표시", variable=period_show_year_var, bg="white").pack(side="left", padx=5)

period_result_label = tk.Label(
    period_frame,
    text="결과가 여기에 표시됩니다.",
    font=("맑은 고딕", 12),
    bg="#E6F7FF",
    fg="black",
    width=55,
    height=6,
    relief="solid",
    anchor="center",
    justify="center"
)
period_result_label.pack(padx=20, pady=10)


# ================== 프로그램 실행 =====================

window.mainloop()
