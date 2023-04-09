import bpy
import inspect
import os
import datetime

def line_num():


    now = datetime.datetime.now()
    second = now.second
    microsecond = now.microsecond

    # 秒とマイクロ秒を結合して浮動小数点数に変換する
    current_time = second + (microsecond / 1000000.0)
    
    print("現在の時刻：", now.strftime("%H:%M:%S")," ",current_time - second)

    stack = inspect.stack()
    current_file = stack[1][1]
    current_line = stack[1][2]
    script_name = os.path.basename(current_file)

    # 関数を呼び出したスタックフレームを取得し、呼び出した元の関数名を取得する
    caller_frame = stack[1].frame
    caller_method = caller_frame.f_code.co_name
    caller_methods = [caller_method]

    # スタックフレームを遡りながら呼び出した元の関数名を取得する
    while caller_frame.f_back and caller_frame.f_back.f_code.co_name != "<module>":
        caller_frame = caller_frame.f_back
        caller_method = caller_frame.f_code.co_name
        caller_methods.insert(0, caller_method)

    # '>' 区切りで親メソッド名を連結する
    caller_str = ' > '.join(caller_methods)

    return script_name + " Line: " + str(current_line) + " Caller: " + caller_str+" "

def print(*data):

    for window in bpy.context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == 'CONSOLE':
                override = {'window': window, 'screen': screen, 'area': area}
                texts = ""
                for keyword in data:
                    texts= texts + " " + str(keyword)
                bpy.ops.console.scrollback_append(override, text=texts, type="OUTPUT")
