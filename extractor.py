import re
import tkinter as tk
import json
import subprocess
import webbrowser
from tkinter.font import Font
import pyperclip
import requests
from lxml import html


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
window.geometry("960x1080+1+1")
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
    text="Menu XPath:",
    height=1,
    font=font
)

articles_label = tk.Label(
    text="Articles XPath:",
    height=1,
    font=font
)

title_label = tk.Label(
    text="Title XPath:",
    height=1,
    font=font
)

pubdate_label = tk.Label(
    text="Pubdate XPath:",
    height=1,
    font=font
)

author_label = tk.Label(
    text="Author XPath:",
    height=1,
    font=font
)

body_label = tk.Label(
    text="Body XPath:",
    height=1,
    font=font
)

# textbox definition
existing_code_textbox = tk.Text(
    bg="white",
    width=80,
    height=12,
    undo=True,
    font=font
)

start_url_textbox = tk.Text(
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
    height=3,
    undo=True,
    font=font
)

kraken_id_textbox = tk.Text(
    bg="white",
    height=1,
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
def load_code(link, open_source_bool=True):
    if 'edit' not in link:
        new_link = link.split('items/')
        new_link.insert(1, 'items/edit/')
        link = ''.join(new_link).replace('https', 'http')
    if open_source_bool:
        webbrowser.get("chrome").open(link)
    clear_text(kraken_id=False)
    kraken_id_textbox.delete('1.0', tk.END)
    kraken_id_textbox.insert('1.0', link)
    kraken_id = link.split('/')[-2]
    subprocess.call(f"scrapy runspider kraken_json.py -a kraken_id={kraken_id}")

    # xpath = "//input[@name='feed_properties']/@value"
    # response = requests.get(link, headers={'Connection': 'close'})
    # tree = html.fromstring(response.text)
    # code = tree.xpath(xpath)
    # print(code)

    with open('json.txt', 'r') as f:
        existing_code_textbox.delete('1.0', tk.END)
        existing_code_textbox.insert('1.0', f.read())
    generate()


kraken_id_button = tk.Button(
    text="Load",
    command=lambda: load_code(kraken_id_textbox.get('1.0', tk.END), open_source_bool=False),
    height=2,
    width=5,
    font=font
)

kraken_id_button_clipboard = tk.Button(
    text="Load from Clip",
    command=lambda: load_code(window.clipboard_get()),
    height=2,
    width=10,
    font=font
)


def open_source(link):
    webbrowser.get("chrome").open(link)


open_source_button = tk.Button(
    text="Open Source",
    command=lambda: open_source(kraken_id_textbox.get('1.0', tk.END)),
    height=2,
    width=10,
    font=font
)


def get_only_first_value(textbox):
    current_value = textbox.get("1.0", tk.END)
    textbox.delete("1.0", tk.END)
    textbox.insert("1.0", '(' + current_value.strip() + ')[1]')


title_button_brackets = tk.Button(
    text="[1]",
    command=lambda: get_only_first_value(title_textbox),
    height=2,
    width=3,
    font=font
)

pubdate_button_brackets = tk.Button(
    text="[1]",
    command=lambda: get_only_first_value(pubdate_textbox),
    height=2,
    width=3,
    font=font
)

author_button_brackets = tk.Button(
    text="[1]",
    command=lambda: get_only_first_value(author_textbox),
    height=2,
    width=3,
    font=font
)

body_button_brackets = tk.Button(
    text="[1]",
    command=lambda: get_only_first_value(body_textbox),
    height=2,
    width=3,

    font=font
)


def replace_textbox_value(textbox, value):
    textbox.delete("1.0", tk.END)
    textbox.insert("1.0", value)


meta_button = tk.Button(
    text="Meta",
    command=lambda: replace_textbox_value(pubdate_textbox, "(//meta[contains(@property, 'date')]/@content |"
                                                           " //meta[contains(@property, 'time')]/@content | "
                                                           "//*[contains(@itemprop, 'datePublished')]/@content)[1]"),
    height=2,
    width=5,
    font=font
)

author_button = tk.Button(
    text="Meta",
    command=lambda: replace_textbox_value(author_textbox, "//meta[contains(@*,'uthor')]/@content"),
    height=2,
    width=5,
    font=font
)

body_button = tk.Button(
    text="Content",
    command=lambda: replace_textbox_value(body_textbox, "//div[contains(@class, ‘content')]"),
    height=2,
    width=5,
    font=font
)


def open_link():
    # def find_sitemap(link):
    #     xpath = "//*[contains(@href, 'site') and contains(@href, 'map')]/@href"
    #     response = requests.get(link, headers={'Connection': 'close'})
    #     tree = html.fromstring(response.text)
    #     sitemap = tree.xpath(xpath)
    #     return sitemap

    links = start_url_textbox.get("1.0", tk.END).split(';')
    for link in links:
        webbrowser.get("chrome").open(link)
        # print(find_sitemap(link))


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


def generate(event=None):
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
            # .replace(re.sub(r'\S\|\S'), ' | ')
            json_variable["scrapy_arguments"][xpath_name] = re.sub(r'(\S)\|(\S)', r'\1 | \2',
                                                                   textbox.get("1.0", tk.END).strip().replace('"', "'"))
        elif xpath_name in json_variable["scrapy_arguments"].keys() and not_empty():
            json_variable["scrapy_arguments"].pop(xpath_name)

    def edit_textbox(textbox, xpath_name):
        textbox.delete("1.0", tk.END)
        if xpath_name in json_variable["scrapy_arguments"].keys():
            textbox.insert('1.0', json_variable["scrapy_arguments"][xpath_name])

    existing_code = existing_code_textbox.get("1.0", tk.END)
    if existing_code.strip():
        json_variable = json.loads(existing_code)
    else:
        with open('template.json') as f2:
            json_variable = json.load(f2)

    for tup in entry_tuples:
        get_text_from_textbox(tup[0], tup[1])

    if "scrapy_settings" in json_variable.keys():
        json_variable["scrapy_settings"].update(settings_json)
    else:
        json_variable["scrapy_settings"] = settings_json

    json_variable["scrapy_arguments"]["link_id_regex"] = None
    final_text = json.dumps(json_variable, indent=2)
    pyperclip.copy(final_text)

    existing_code_textbox.delete("1.0", tk.END)
    existing_code_textbox.insert('1.0', final_text)

    for tup in entry_tuples:
        edit_textbox(tup[0], tup[1])

    log_json = True
    if log_json and kraken_id_textbox.get('1.0', tk.END).strip():
        kraken_id = kraken_id_textbox.get('1.0', tk.END).split('/')[-2]
        with open(f'./logs/{kraken_id}.txt', 'w', encoding='utf-8') as f:
            f.write(final_text)


window.bind('<Return>', generate)

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
    (title_textbox, "title_xpath", title_label, copy_title_button, title_button_brackets),
    (pubdate_textbox, "pubdate_xpath", pubdate_label, copy_pubdate_button, meta_button, pubdate_button_brackets),
    (author_textbox, "author_xpath", author_label, copy_author_button, author_button, author_button_brackets),
    (body_textbox, "body_xpath", body_label, copy_body_button, body_button, body_button_brackets)]

row = 0

kraken_id_label.grid(row=row, column=0, sticky='W', pady=2, padx=2)
kraken_id_textbox.grid(row=row, column=1, sticky='W', pady=2, padx=2)
kraken_id_button.grid(row=row, column=2, sticky='W', pady=2, padx=2)
kraken_id_button_clipboard.grid(row=row, column=3, sticky='W', pady=2, padx=2)
open_source_button.grid(row=row, column=4, sticky='W', pady=2, padx=2)
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
