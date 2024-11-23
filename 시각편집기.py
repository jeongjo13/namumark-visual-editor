from tkinter import *
from tkinter import messagebox
from datetime import datetime

using_font = "맑은 고딕"  # 사용할 폰트
textsize = 15  # 폰트 크기

def toggle_style(tag):
    current_tags = text.tag_names("sel.first")
    if tag in current_tags:
        text.tag_remove(tag, "sel.first", "sel.last")
    else:
        text.tag_add(tag, "sel.first", "sel.last")

def clear_selected_styles():
    try:
        # 선택된 영역의 모든 태그 제거
        text.tag_remove("bold", "sel.first", "sel.last")
        text.tag_remove("italic", "sel.first", "sel.last")
        text.tag_remove("underline", "sel.first", "sel.last")
        text.tag_remove("strikethrough", "sel.first", "sel.last")
        text.tag_remove("paragraph1", "sel.first", "sel.last")
        text.tag_remove("paragraph2", "sel.first", "sel.last")
        text.tag_remove("paragraph3", "sel.first", "sel.last")
        text.tag_remove("paragraph4", "sel.first", "sel.last")
        text.tag_remove("paragraph5", "sel.first", "sel.last")
    except TclError:
        messagebox.showwarning("경고", "먼저 텍스트를 선택하세요!")

def convert():
    full_text = text.get("1.0", "end-1c")
    formatted_text = ""
    current_line = 1

    while True:
        line_start = f"{current_line}.0"
        
        try:
            line_end = text.index(f"{line_start} lineend")
            line_text = text.get(line_start, line_end)
            
            # 현재 라인의 변환된 텍스트를 저장할 리스트
            transformed_segments = []
            char_idx = 0
            
            while char_idx < len(line_text):
                # 현재 문자의 위치
                current_pos = f"{line_start}+{char_idx}c"
                current_tags = set(text.tag_names(current_pos))
                
                # 현재 위치에서 시작하는 연속된 텍스트 세그먼트를 찾음
                segment = ""
                segment_start = char_idx
                
                while char_idx < len(line_text):
                    next_pos = f"{line_start}+{char_idx}c"
                    next_tags = set(text.tag_names(next_pos))
                    
                    # 태그가 변경되면 세그먼트 종료
                    if next_tags != current_tags:
                        break
                        
                    segment += line_text[char_idx]
                    char_idx += 1
                
                # 세그먼트에 스타일 적용
                transformed_segment = segment
                
                # 전체 세그먼트에 대해 스타일 한 번만 적용
                if "bold" in current_tags:
                    transformed_segment = f"'''{transformed_segment}'''"
                if "italic" in current_tags:
                    transformed_segment = f"''{transformed_segment}''"
                if "underline" in current_tags:
                    transformed_segment = f"__{transformed_segment}__"
                if "strikethrough" in current_tags:
                    transformed_segment = f"--{transformed_segment}--"
                if "paragraph1" in current_tags:
                    transformed_segment = f"= {transformed_segment} ="
                if "paragraph2" in current_tags:
                    transformed_segment = f"== {transformed_segment} =="
                if "paragraph3" in current_tags:
                    transformed_segment = f"=== {transformed_segment} ==="
                if "paragraph4" in current_tags:
                    transformed_segment = f"==== {transformed_segment} ===="
                if "paragraph5" in current_tags:
                    transformed_segment = f"===== {transformed_segment} ====="
                
                transformed_segments.append(transformed_segment)
            
            # 변환된 세그먼트들을 합쳐서 한 줄로 만듦
            formatted_text += "".join(transformed_segments) + "\n"
            
            # 다음 라인으로 이동
            current_line += 1
            
            # 마지막 라인인지 확인
            next_line_start = f"{current_line}.0"
            if text.compare(next_line_start, ">=", "end"):
                break
                
        except TclError:
            break
    
    # 파일로 저장
    now = datetime.now()
    filename = now.strftime("%Y%m%d%H%M%S") + ".txt"
    
    try:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(formatted_text)
        messagebox.showinfo("알림", f"파일이 저장되었습니다: {filename}")
    except Exception as e:
        messagebox.showerror("오류", f"파일 저장 중 오류가 발생했습니다: \n{e}")



# GUI 설정
window = Tk()
window.title("나무마크 시각 편집기")
window.geometry("1000x700")

button_frame = Frame(window)
button_frame.pack()

bold_button = Button(button_frame, text="볼드", command=lambda: toggle_style("bold"))
bold_button.grid(row=0, column=0, padx=5, pady=5)

italic_button = Button(button_frame, text="이탤릭", command=lambda: toggle_style("italic"))
italic_button.grid(row=0, column=1, padx=5, pady=5)

underline_button = Button(button_frame, text="밑줄", command=lambda: toggle_style("underline"))
underline_button.grid(row=0, column=2, padx=5, pady=5)

strikethrough_button = Button(button_frame, text="취소선", command=lambda: toggle_style("strikethrough"))
strikethrough_button.grid(row=0, column=3, padx=5, pady=5)

paragraph1_button = Button(button_frame, text="1단계 문단 제목", command=lambda: toggle_style("paragraph1"))
paragraph1_button.grid(row=0, column=4, padx=5, pady=5)

paragraph2_button = Button(button_frame, text="2단계 문단 제목", command=lambda: toggle_style("paragraph2"))
paragraph2_button.grid(row=0, column=5, padx=5, pady=5)

paragraph3_button = Button(button_frame, text="3단계 문단 제목", command=lambda: toggle_style("paragraph3"))
paragraph3_button.grid(row=0, column=6, padx=5, pady=5)

paragraph4_button = Button(button_frame, text="4단계 문단 제목", command=lambda: toggle_style("paragraph4"))
paragraph4_button.grid(row=0, column=7, padx=5, pady=5)

paragraph5_button = Button(button_frame, text="5단계 문단 제목", command=lambda: toggle_style("paragraph5"))
paragraph5_button.grid(row=0, column=8, padx=5, pady=5)

clear_styles_button = Button(button_frame, text="서식 제거", command=clear_selected_styles)
clear_styles_button.grid(row=0, column=9, padx=5, pady=5)

convert_button = Button(button_frame, text="나무마크로 변환하기", command=convert)
convert_button.grid(row=0, column=10, padx=5, pady=5)

text = Text(window, font=(using_font, textsize), wrap="word", undo=True)
text.pack(expand=True, fill="both")

text.tag_config("bold", font=(using_font, textsize, "bold"))
text.tag_config("italic", font=(using_font, textsize, "italic"))
text.tag_config("underline", font=(using_font, textsize, "underline"))
text.tag_config("strikethrough", font=(using_font, textsize, "overstrike"))
text.tag_config("paragraph1", font=(using_font, int(textsize * 2.5), "bold"))
text.tag_config("paragraph2", font=(using_font, textsize * 2, "bold"))
text.tag_config("paragraph3", font=(using_font, int(textsize * 1.8), "bold"))
text.tag_config("paragraph4", font=(using_font, int(textsize * 1.6), "bold"))
text.tag_config("paragraph5", font=(using_font, int(textsize * 1.4), "bold"))

window.mainloop()
