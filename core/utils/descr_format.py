from typing import Tuple


def descr(text: str):
    def title_search(txt: str, start_point: int, title_name: str) -> str:
        s_char_title = 0
        res = ''
        if title_name in txt:
            start_point: int  #res_Name_Descr[0]
            parsed_text = txt[start_point:]
            for n in range(len(parsed_text)):
                if parsed_text[n] == title_name[0]:
                    s_char_title = n
                if parsed_text[s_char_title:n] == title_name:
                    title = parsed_text[s_char_title:n]
                    res = f'<b>{title}</b>'
                    return res
        return res

    def name_descr(txt: str) -> Tuple[Tuple[int, int], Tuple[str, str, str]]:
        e_char_name = 0
        s_char_desc = 0
        for i in range(len(txt)):
            if txt[i] == "О":
                e_char_name = i
            if txt[e_char_name:i] == 'Описание':
                old_name = txt[:e_char_name]
                name: str = f'<u><i><b>{txt[:e_char_name]}</b></i></u>'
                description: str= f'<b>{txt[e_char_name:i]}</b>'
                s_char_desc = i
                return (s_char_desc, e_char_name), (name, description, old_name)

    def time_search(txt):
        e_char_time = 0
        res = ''
        for j in range(len(txt) - 1, 0, -1):
            if txt[j] == 'я':
                e_char_time = j + 1
            if txt[j:e_char_time] == 'Время':
                time = txt[j:e_char_time]
                res = f'<b>{time}</b>'
                return res
        return res

    res_Name_Descr = name_descr(text)

    name_main = res_Name_Descr[1][0]
    description_main = res_Name_Descr[1][1]
    history = title_search(text, res_Name_Descr[0][0], 'История')
    drinks_main = title_search(text, res_Name_Descr[0][0], 'Напитки')
    souses_main = title_search(text, res_Name_Descr[0][0], 'Соусы')
    time_main = time_search(text)

    copy_text = text[res_Name_Descr[0][1]:].replace('Описание', description_main)
    copy_text = copy_text.replace('История', history)
    copy_text = copy_text.replace('Напитки', drinks_main)
    copy_text = copy_text.replace('Соусы', souses_main)
    copy_text = copy_text.replace('Время', time_main)
    return name_main, copy_text
