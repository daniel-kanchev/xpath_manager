import tkinter as tk
import json
import subprocess
import webbrowser
from tkinter.font import Font
import pyperclip
import time


# Code to allow CTRL commands in all languages
def on_key_release(event):
    ctrl = (event.state & 0x4) != 0
    if event.keycode == 88 and ctrl and event.keysym.lower() != "x":
        event.widget.event_generate("<<Cut>>")

    if event.keycode == 86 and ctrl and event.keysym.lower() != "v":
        event.widget.event_generate("<<Paste>>")

    if event.keycode == 67 and ctrl and event.keysym.lower() != "c":
        event.widget.event_generate("<<Copy>>")

    if event.keycode == 65 and ctrl and event.keysym.lower() != "а":
        event.widget.event_generate("<<SelectAll>>")


# window definition
window = tk.Tk()
window.geometry("800x1000+1+1")
window.bind_all("<Key>", on_key_release, "+")

# font definition
font = Font(family="Roboto", size=10)

# define all Labels
kraken_id_label = tk.Label(
    text="Kraken Link:",
    font=font
)

existing_code_label = tk.Label(
    text="Code:",
    height=1,
    font=font
)

start_url_label = tk.Label(
    text="Start URL:",
    height=1,
    font=font
)

menu_label = tk.Label(
    text="Menu XPATH:",
    height=1,
    font=font
)

articles_label = tk.Label(
    text="Articles XPATH:",
    height=1,
    font=font
)

title_label = tk.Label(
    text="Title XPATH:",
    height=1,
    font=font
)

pubdate_label = tk.Label(
    text="Pubdate XPATH:",
    height=1,
    font=font
)

author_label = tk.Label(
    text="Author XPATH:",
    height=1,
    font=font
)

body_label = tk.Label(
    text="Body XPATH:",
    height=1,
    font=font
)

# textbox definition
existing_code_textbox = tk.Text(
    bg="white",
    width=80,
    height=15,
    undo=True,
    font=font
)

start_url_textbox = tk.Text(
    # master=,
    bg="white",
    width=80,
    height=2,
    undo=True,
    font=font
)

menu_textbox = tk.Text(
    bg="white",
    width=80,
    height=2,
    undo=True,
    font=font
)

articles_textbox = tk.Text(
    # master=,
    bg="white",
    width=80,
    height=2,
    undo=True,
    font=font
)
title_textbox = tk.Text(
    bg="white",
    width=80,
    height=2,
    undo=True,
    font=font
)
pubdate_textbox = tk.Text(
    # master=,
    bg="white",
    width=80,
    height=2,
    undo=True,
    font=font
)
author_textbox = tk.Text(
    bg="white",
    width=80,
    height=2,
    undo=True,
    font=font
)
body_textbox = tk.Text(
    bg="white",
    width=80,
    height=4,
    undo=True,
    font=font
)

kraken_id_textbox = tk.Text(
    bg="white",
    height=2,
    undo=True,
    font=font
)

# browser setup
chrome_path = 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))


def copy_code(textbox):
    pyperclip.copy(textbox.get("1.0", tk.END).strip())


code_copy_button = tk.Button(
    text="Copy",
    command=lambda: copy_code(existing_code_textbox),
    height=2,
    width=5,
    font=font
)

copy_start_button = tk.Button(
    text="Copy",
    command=lambda: copy_code(start_url_textbox),
    height=2,
    width=5,
    font=font
)

copy_menu_button = tk.Button(
    text="Copy",
    command=lambda: copy_code(menu_textbox),
    height=2,
    width=5,
    font=font
)

copy_articles_button = tk.Button(
    text="Copy",
    command=lambda: copy_code(articles_textbox),
    height=2,
    width=5,
    font=font
)

copy_title_button = tk.Button(
    text="Copy",
    command=lambda: copy_code(title_textbox),
    height=2,
    width=5,
    font=font
)

copy_pubdate_button = tk.Button(
    text="Copy",
    command=lambda: copy_code(pubdate_textbox),
    height=2,
    width=5,
    font=font
)

copy_author_button = tk.Button(
    text="Copy",
    command=lambda: copy_code(author_textbox),
    height=2,
    width=5,
    font=font
)

copy_body_button = tk.Button(
    text="Copy",
    command=lambda: copy_code(body_textbox),
    height=2,
    width=5,
    font=font
)


# Button to load code into extractor
def load_code():
    clear_text(kraken_id=False)
    link = kraken_id_textbox.get('1.0', tk.END)
    kraken_id = link.split('/')[-2]
    subprocess.call(f"scrapy runspider kraken_json.py -a kraken_id={kraken_id}")
    with open('json.txt', 'r') as f:
        existing_code_textbox.delete('1.0', tk.END)
        existing_code_textbox.insert('1.0', f.read())
    if 'edit' not in link:
        new_link = link.split('items/')
        new_link.insert(1, 'items/edit/')
        link = ''.join(new_link)
    webbrowser.get("chrome").open(link)
    generate()


kraken_id_button = tk.Button(
    # master=,
    text="Load",
    command=load_code,
    height=2,
    width=5,
    font=font
)


def single_title():
    current_title = title_textbox.get("1.0", tk.END)
    title_textbox.delete("1.0", tk.END)
    title_textbox.insert("1.0", '(' + current_title.strip() + ')[1]')


title_button_brackets = tk.Button(
    text="[1]",
    command=single_title,
    height=2,
    width=3,
    font=font
)


def single_pubdate():
    current_pubdate = pubdate_textbox.get("1.0", tk.END)
    pubdate_textbox.delete("1.0", tk.END)
    pubdate_textbox.insert("1.0", '(' + current_pubdate.strip() + ')[1]')


pubdate_button_brackets = tk.Button(
    # master=,
    text="[1]",
    command=single_pubdate,
    height=2,
    width=3,
    font=font
)


def single_author():
    current_author = author_textbox.get("1.0", tk.END)
    author_textbox.delete("1.0", tk.END)
    author_textbox.insert("1.0", '(' + current_author.strip() + ')[1]')


author_button_brackets = tk.Button(
    text="[1]",
    command=single_author,
    height=2,
    width=3,
    font=font
)


def single_body():
    current_body = body_textbox.get("1.0", tk.END)
    body_textbox.delete("1.0", tk.END)
    body_textbox.insert("1.0", '(' + current_body.strip() + ')[1]')


body_button_brackets = tk.Button(
    # master=,
    text="[1]",
    command=single_body,
    height=2,
    width=3,
    font=font
)


def meta_command():
    pubdate_textbox.delete("1.0", tk.END)
    pubdate_textbox.insert("1.0", "//meta[@property='article:published_time']/@content")


meta_button = tk.Button(
    text="Meta",
    command=meta_command,
    height=2,
    width=5,
    font=font
)


def add_h1():
    title_textbox.delete("1.0", tk.END)
    title_textbox.insert("1.0", '//h1')


h1_button = tk.Button(
    # master=,
    text='h1',
    command=add_h1,
    height=2,
    width=3,
    font=font
)


def open_link():
    links = start_url_textbox.get("1.0", tk.END).split(';')
    for link in links:
        print(link)
        webbrowser.get("chrome").open(link)


open_link_button = tk.Button(
    text='Open Link',
    command=open_link,
    height=2,
    width=10,
    font=font
)


def open_domain():
    domain = "".join(start_url_textbox.get("1.0", tk.END).split('/')[:3])
    webbrowser.get("chrome").open(domain)
    print(domain)


open_domain_button = tk.Button(
    text='Open Domain',
    command=open_domain,
    height=2,
    width=10,
    font=font
)


def clear_text(kraken_id=True):
    if kraken_id:
        kraken_id_textbox.delete("1.0", tk.END)
    existing_code_textbox.delete("1.0", tk.END)
    start_url_textbox.delete("1.0", tk.END)
    menu_textbox.delete("1.0", tk.END)
    articles_textbox.delete("1.0", tk.END)
    title_textbox.delete("1.0", tk.END)
    pubdate_textbox.delete("1.0", tk.END)
    author_textbox.delete("1.0", tk.END)
    body_textbox.delete("1.0", tk.END)


clear_button = tk.Button(
    text="Clear",
    command=clear_text,
    height=2,
    width=10,
    font=font
)

with open('settings.json') as f1:
    settings_json = json.load(f1)


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
    text="Generate JSON!",
    command=generate,
    height=2,
    width=15,
    master=window,
    font=font
)
entry_tuples = [
    (start_url_textbox, "start_urls", start_url_label, copy_start_button, open_link_button, open_domain_button),
    (menu_textbox, "menu_xpath", menu_label, copy_menu_button),
    (articles_textbox, "articles_xpath", articles_label, copy_articles_button),
    (title_textbox, "title_xpath", title_label, copy_title_button, h1_button, title_button_brackets),
    (pubdate_textbox, "pubdate_xpath", pubdate_label, copy_pubdate_button, meta_button, pubdate_button_brackets),
    (author_textbox, "author_xpath", author_label, copy_author_button, author_button_brackets),
    (body_textbox, "body_xpath", body_label, copy_body_button, body_button_brackets)]

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


row = pack_entries((existing_code_textbox, "", existing_code_label, code_copy_button), row)
for t in entry_tuples:
    row = pack_entries(t, row)

generate_button.grid(row=row, column=1, sticky='W', padx=2, pady=2)
clear_button.grid(row=row, column=2, sticky="E", padx=2, pady=2)
row += 1

window.mainloop()
