import tkinter as tk
import pyperclip
import json
import webbrowser
import subprocess

window = tk.Tk()
window.geometry("800x1000")
frame_width = 150
frame_height = 450
frame = tk.Frame(master=window, width=frame_width, height=frame_width)

chrome_path = 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))

kraken_id_label = tk.Label(
    master=frame,
    text="Kraken Link:"
)

kraken_id_textbox = tk.Text(
    master=frame,
    bg="white",
    height=2
)


def load_code():
    link = kraken_id_textbox.get('1.0', tk.END)
    kraken_id = link.split('/')[-2]
    subprocess.call(f"scrapy runspider kraken_json.py -a kraken_id={kraken_id}")
    webbrowser.get("chrome").open(link)
    with open('json.txt', 'r') as f:
        existing_code_textbox.delete('1.0', tk.END)
        existing_code_textbox.insert('1.0', f.read())
    generate()


kraken_id_button = tk.Button(
    master=frame,
    text="Load",
    command=load_code,
    height=2,
    width=5
)

existing_code_label = tk.Label(
    master=frame,
    text="Code:",
    width=80,
    height=1
)

start_url_label = tk.Label(
    master=frame,
    text="Start URL:",
    width=80,
    height=1
)

menu_label = tk.Label(
    master=frame,
    text="Menu XPATH:",
    width=80,
    height=1
)

articles_label = tk.Label(
    master=frame,
    text="Articles XPATH:",
    width=80,
    height=1
)

title_label = tk.Label(
    master=frame,
    text="Title XPATH:",
    width=80,
    height=1
)

pubdate_label = tk.Label(
    master=frame,
    text="Pubdate XPATH:",
    width=80,
    height=1
)

author_label = tk.Label(
    master=frame,
    text="Author XPATH:",
    width=80,
    height=1
)

body_label = tk.Label(
    master=frame,
    text="Body XPATH:",
    width=80,
    height=1
)

existing_code_textbox = tk.Text(
    master=frame,
    bg="white",
    width=80,
    height=15
)

start_url_textbox = tk.Text(
    master=frame,
    bg="white",
    width=80,
    height=2,
)

menu_textbox = tk.Text(
    master=frame,
    bg="white",
    width=80,
    height=2
)

articles_textbox = tk.Text(
    master=frame,
    bg="white",
    width=80,
    height=2
)
title_textbox = tk.Text(
    master=frame,
    bg="white",
    width=80,
    height=2
)
pubdate_textbox = tk.Text(
    master=frame,
    bg="white",
    width=80,
    height=2
)
author_textbox = tk.Text(
    master=frame,
    bg="white",
    width=80,
    height=2
)
body_textbox = tk.Text(
    master=frame,
    bg="white",
    width=80,
    height=4
)


def single_title():
    current_title = title_textbox.get("1.0", tk.END)
    title_textbox.delete("1.0", tk.END)
    title_textbox.insert("1.0", '(' + current_title.strip() + ')[1]')


title_button_brackets = tk.Button(
    master=frame,
    text="[1]",
    command=single_title,
    height=2,
    width=3
)


def single_pubdate():
    current_pubdate = pubdate_textbox.get("1.0", tk.END)
    pubdate_textbox.delete("1.0", tk.END)
    pubdate_textbox.insert("1.0", '(' + current_pubdate.strip() + ')[1]')


pubdate_button_brackets = tk.Button(
    master=frame,
    text="[1]",
    command=single_pubdate,
    height=2,
    width=3
)


def single_author():
    current_author = author_textbox.get("1.0", tk.END)
    author_textbox.delete("1.0", tk.END)
    author_textbox.insert("1.0", '(' + current_author.strip() + ')[1]')


author_button_brackets = tk.Button(
    master=frame,
    text="[1]",
    command=single_author,
    height=2,
    width=3
)


def single_body():
    current_body = body_textbox.get("1.0", tk.END)
    body_textbox.delete("1.0", tk.END)
    body_textbox.insert("1.0", '(' + current_body.strip() + ')[1]')


body_button_brackets = tk.Button(
    master=frame,
    text="[1]",
    command=single_body,
    height=2,
    width=3
)


def meta_command():
    pubdate_textbox.delete("1.0", tk.END)
    pubdate_textbox.insert("1.0", "//meta[@property='article:published_time']/@content")


meta_button = tk.Button(
    master=frame,
    text="Meta",
    command=meta_command,
    height=2,
    width=5
)


def add_h1():
    title_textbox.delete("1.0", tk.END)
    title_textbox.insert("1.0", '//h1')


h1_button = tk.Button(
    master=frame,
    text='h1',
    command=add_h1,
    height=2,
    width=3
)


def open_link():
    links = start_url_textbox.get("1.0", tk.END).split(';')
    for link in links:
        webbrowser.get("chrome").open(link)


open_link_button = tk.Button(
    master=frame,
    text='Open Link',
    command=open_link,
    height=2,
    width=10
)


def clear_text():
    existing_code_textbox.delete("1.0", tk.END)
    start_url_textbox.delete("1.0", tk.END)
    menu_textbox.delete("1.0", tk.END)
    articles_textbox.delete("1.0", tk.END)
    title_textbox.delete("1.0", tk.END)
    pubdate_textbox.delete("1.0", tk.END)
    author_textbox.delete("1.0", tk.END)
    body_textbox.delete("1.0", tk.END)


clear_button = tk.Button(
    master=frame,
    text="Clear",
    command=clear_text,
    height=2,
    width=10
)

with open('settings.json') as f1:
    settings_json = json.load(f1)

entry_tuples = [(start_url_textbox, "start_urls", start_url_label, open_link_button),
                (menu_textbox, "menu_xpath", menu_label),
                (articles_textbox, "articles_xpath", articles_label),
                (title_textbox, "title_xpath", title_label, h1_button, title_button_brackets),
                (pubdate_textbox, "pubdate_xpath", pubdate_label, meta_button, pubdate_button_brackets),
                (author_textbox, "author_xpath", author_label, author_button_brackets),
                (body_textbox, "body_xpath", body_label, body_button_brackets)]


def generate():
    def not_empty():
        return bool(start_url_textbox.get("1.0", tk.END).strip() or
                    menu_textbox.get("1.0", tk.END).strip() or
                    articles_textbox.get("1.0", tk.END).strip() or
                    title_textbox.get("1.0", tk.END).strip() or
                    pubdate_textbox.get("1.0", tk.END).strip() or
                    author_textbox.get("1.0", tk.END).strip() or
                    body_textbox.get("1.0", tk.END).strip())

    def get_text_from_textbox(textbox, xpath_name):
        if textbox.get("1.0", tk.END).strip():
            json_variable["scrapy_arguments"][xpath_name] = textbox.get("1.0", tk.END).strip().replace('"', "'")
        elif xpath_name in json_variable["scrapy_arguments"].keys() and not_empty():
            json_variable["scrapy_arguments"].pop(xpath_name)

    def edit_textbox(textbox, xpath_name):
        textbox.delete("1.0", tk.END)
        if xpath_name in json_variable["scrapy_arguments"].keys():
            textbox.insert('1.0', json_variable["scrapy_arguments"][xpath_name])

    existing_code = existing_code_textbox.get("1.0", tk.END)
    print(existing_code)
    if existing_code.strip():
        json_variable = json.loads(existing_code)
    else:
        with open('temp.json') as f2:
            json_variable = json.load(f2)

    for tup in entry_tuples:
        get_text_from_textbox(tup[0], tup[1])

    json_variable["scrapy_settings"] = settings_json
    json_variable["scrapy_arguments"]["link_id_regex"] = None
    final_text = json.dumps(json_variable, indent=2)
    pyperclip.copy(final_text)

    existing_code_textbox.delete("1.0", tk.END)
    existing_code_textbox.insert('1.0', final_text)

    for tup in entry_tuples:
        edit_textbox(tup[0], tup[1])

    print(final_text)


generate_button = tk.Button(
    master=frame,
    text="Generate JSON!",
    command=generate,
    height=2,
    width=15
)

row = 0

kraken_id_label.grid(row=row, column=0, sticky='W', pady=2, padx=2)
kraken_id_textbox.grid(row=row, column=1, sticky='W', pady=2, padx=2)
kraken_id_button.grid(row=row, column=2, sticky='W', pady=2, padx=2)
row += 1


def pack_entries(entry_tuple, curr_row):
    entry_tuple[2].grid(row=curr_row, column=1, sticky='W', pady=2, padx=2)
    curr_row += 1
    entry_tuple[0].grid(row=curr_row, column=1, sticky='W', pady=2, padx=2)
    if len(entry_tuple) > 3:  # if len = 4 or more
        for i in range(3, len(entry_tuple)):
            entry_tuple[i].grid(row=curr_row, column=i - 1, sticky='W', pady=2, padx=5)
    curr_row += 1
    return curr_row


frame.pack()
row = pack_entries((existing_code_textbox, "", existing_code_label), row)
for t in entry_tuples:
    row = pack_entries(t, row)

generate_button.grid(row=row, column=0, sticky='W', padx=2, pady=2)
clear_button.grid(row=row, column=1, sticky="E", padx=2, pady=2)
row += 1

window.mainloop()
