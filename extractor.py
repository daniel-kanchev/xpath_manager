import re
import tkinter as tk
import json
import webbrowser
from json import JSONDecodeError
from pprint import pprint
from tkinter.font import Font
import pyperclip
import requests
from lxml import html
import login_data
import os
import sqlite3
from datetime import datetime
import atexit
import config
from tkinter.ttk import *

# window definition
window = tk.Tk()
window_title = f"Xpath Extractor ({config.last_change})"
window.title(window_title)
# define background colour
background = 'dark grey'
window.configure(background=background)

# font definitions for labels and text fields
label_font = Font(family="Arial", size=12)
text_font = Font(family="Calibri", size=12)

# define all Labels
kraken_id_label = tk.Label(
    text="Link:",
    font=label_font,
    bg=background
)

existing_code_label = tk.Label(
    text="Code:",
    height=1,
    font=label_font,
    bg=background)

start_urls_label = tk.Label(
    text="Start URL:",
    height=1,
    font=label_font,
    bg=background
)

menu_label = tk.Label(
    text="Menu XPath:",
    height=1,
    font=label_font,
    bg=background
)

articles_label = tk.Label(
    text="Articles XPath:",
    height=1,
    font=label_font,
    bg=background
)

title_label = tk.Label(
    text="Title XPath:",
    height=1,
    font=label_font,
    bg=background
)

pubdate_label = tk.Label(
    text="Pubdate XPath:",
    height=1,
    font=label_font,
    bg=background
)
date_order_label = tk.Label(
    text="Date Order XPath:",
    height=1,
    font=label_font,
    bg=background
)
author_label = tk.Label(
    text="Author XPath:",
    height=1,
    font=label_font,
    bg=background
)

body_label = tk.Label(
    text="Body XPath:",
    height=1,
    font=label_font,
    bg=background
)

# textbox definition
existing_code_textbox = tk.Text(
    bg="white",
    width=60,
    height=12,
    undo=True,
    font=text_font
)

start_urls_textbox = tk.Text(
    bg="white",
    width=60,
    height=2,
    undo=True,
    font=text_font
)

menu_textbox = tk.Text(
    bg="white",
    width=60,
    height=2,
    undo=True,
    font=text_font
)

articles_textbox = tk.Text(
    bg="white",
    width=60,
    height=2,
    undo=True,
    font=text_font
)
title_textbox = tk.Text(
    bg="white",
    width=60,
    height=2,
    undo=True,
    font=text_font
)
pubdate_textbox = tk.Text(
    bg="white",
    width=60,
    height=2,
    undo=True,
    font=text_font
)
date_order_textbox = tk.Text(
    bg="white",
    width=20,
    height=2,
    undo=True,
    font=text_font
)
author_textbox = tk.Text(
    bg="white",
    width=60,
    height=2,
    undo=True,
    font=text_font
)
body_textbox = tk.Text(
    bg="white",
    width=60,
    height=3,
    undo=True,
    font=text_font
)

kraken_id_textbox = tk.Text(
    bg="white",
    undo=True,
    font=text_font,
    width=60,
    height=1
)


def copy_code(textbox):
    """
    Desc: Function for the button to copy a text fields
    :param textbox: Textbox whose text should be copied to clipboard
    :return:
    """
    pyperclip.copy(textbox.get("1.0", tk.END).strip())


# Defining all copy buttons for each text field
code_copy_button = Button(
    text="Copy",
    command=lambda: copy_code(existing_code_textbox)
)

copy_start_button = Button(
    text="Copy",
    command=lambda: copy_code(start_urls_textbox)
)

copy_menu_button = Button(
    text="Copy",
    command=lambda: copy_code(menu_textbox)
)

copy_articles_button = Button(
    text="Copy",
    command=lambda: copy_code(articles_textbox)
)

copy_title_button = Button(
    text="Copy",
    command=lambda: copy_code(title_textbox)
)

copy_pubdate_button = Button(
    text="Copy",
    command=lambda: copy_code(pubdate_textbox)
)

copy_author_button = Button(
    text="Copy",
    command=lambda: copy_code(author_textbox)
)

copy_body_button = Button(
    text="Copy",
    command=lambda: copy_code(body_textbox)
)


def get_link(link):
    """
    Function to correctly format the Kraken link by searching for the ID in the URL
    :param link: Kraken link / ID
    :return: The correctly formatted link
    """
    kraken_id = re.search(r'\d+', link).group()  # Regex to extract number
    window.title(f"{kraken_id} - {window_title}")
    link = f"http://kraken.aiidatapro.net/items/edit/{kraken_id}/"
    return link


def load_code(link, open_source_bool=True):
    """
    Function to fill the extractor with the JSON from Kraken
    :param link: Kraken link / ID
    :param open_source_bool: Bool indicating whether the source link should be opened in a browser tab
    :return:
    """
    link = get_link(link)  # Format link

    if open_source_bool:
        webbrowser.get("chrome").open(link)

    clear_all_textboxes(kraken_id=False)

    # Show correctly formatted link in textbox
    kraken_id_textbox.delete('1.0', tk.END)
    kraken_id_textbox.insert('1.0', link)

    # Extract Xpath from Kraken page
    xpath = "//input[@name='feed_properties']/@value"
    link = link.strip()
    kraken_response = session.get(link)
    tree = html.fromstring(kraken_response.text)
    code = tree.xpath(xpath)
    code = ''.join(code).replace('\r', '').replace('\n', '')
    try:
        generated_json = json.loads(code)
    except JSONDecodeError:
        # This error indicates the login details are wrong
        print("Incorrect Login Details")
        return
    generate(initial_json=generated_json)  # Pass JSON to generate function


kraken_id_load_button = Button(
    text="Load",
    command=lambda: load_code(kraken_id_textbox.get('1.0', tk.END), open_source_bool=False)
)

kraken_id_clipboard_button = Button(
    text="Clip",
    command=lambda: load_code(window.clipboard_get())
)


def open_link(link):
    """
    Opens the link given in your browser
    :param link: Link to be opened
    :return:
    """
    webbrowser.get("chrome").open(link)


open_source_button = Button(
    text="Source",
    command=lambda: open_link(kraken_id_textbox.get('1.0', tk.END))
)


def load_from_db():
    """
    Extracts ID from Kraken Textbox and loads the source from the database
    :return:
    """
    kraken_id = re.search(r'\d+', kraken_id_textbox.get('1.0', tk.END)).group()
    cur.execute('SELECT * FROM log WHERE id=?', (kraken_id,))
    result = cur.fetchone()
    if result:
        settings = result[10].replace("'", '"').replace("False", '"False"').replace("True", '"True"')  # Format Bool Values to not crash JSON
        # Create a new var and load database values into it
        json_var = {'scrapy_settings': json.loads(settings), 'scrapy_arguments': {}}
        json_var['scrapy_arguments']['start_urls'] = result[2]
        json_var['scrapy_arguments']['menu_xpath'] = result[3]
        json_var['scrapy_arguments']['articles_xpath'] = result[4]
        json_var['scrapy_arguments']['title_xpath'] = result[5]
        json_var['scrapy_arguments']['pubdate_xpath'] = result[6]
        json_var['scrapy_arguments']['date_order'] = result[7]
        json_var['scrapy_arguments']['author_xpath'] = result[8]
        json_var['scrapy_arguments']['body_xpath'] = result[9]
        generate(initial_json=json_var)
    else:
        clear_all_textboxes()  # Clear all textboxes to indicate entry doesn't exist


load_from_db_button = Button(
    text="DB Load",
    command=load_from_db
)


def open_items_page():
    # Function to open the "View Item" page of the source in Kraken
    link = get_link(kraken_id_textbox.get('1.0', tk.END).strip()).replace('/edit', '')
    webbrowser.get("chrome").open(link)


open_items_button = Button(
    text="Items",
    command=open_items_page
)


def get_source_name():
    domain = start_urls_textbox.get("1.0", tk.END).strip()
    if domain and domain[-1] == '/':
        domain = domain[:-1]
    name = domain.split('/')[-1].replace('www.', '')
    pyperclip.copy(name)


source_name_button = Button(
    text="Name",
    command=get_source_name
)

load_from_existing_button = Button(
    text="Load",
    command=lambda: generate(load_from_existing_bool=True)
)


def get_only_first_value(textbox):
    current_value = textbox.get("1.0", tk.END)
    textbox.delete("1.0", tk.END)
    textbox.insert("1.0", '(' + current_value.strip() + ')[1]')


title_button_brackets = Button(
    text="[1]",
    command=lambda: get_only_first_value(title_textbox)
)

pubdate_button_brackets = Button(
    text="[1]",
    command=lambda: get_only_first_value(pubdate_textbox)
)

author_button_brackets = Button(
    text="[1]",
    command=lambda: get_only_first_value(author_textbox)
)

body_button_brackets = Button(
    text="[1]",
    command=lambda: get_only_first_value(body_textbox),
)


def add_regex_for_date(regex):
    current_value = pubdate_textbox.get("1.0", tk.END)
    pubdate_textbox.delete("1.0", tk.END)
    pubdate_textbox.insert("1.0", f"re:match({current_value.strip()}, '{regex}', 'g')")


regex_dmy_button = Button(
    text="Rgx.",
    command=lambda: add_regex_for_date(r'\d{1,2}\.\d{1,2}\.\d{2,4}')
)

regex_ymd_button = Button(
    text="Rgx Txt",
    command=lambda: add_regex_for_date(r'(\d{1,2})\.(\s\w+\s\d{2,4})')
)


def replace_textbox_value(textbox, value):
    textbox.delete("1.0", tk.END)
    textbox.insert("1.0", value)


meta_button = Button(
    text="Meta",
    command=lambda: replace_textbox_value(pubdate_textbox, "(((//meta[contains(@*, 'date')] |"
                                                           " //meta[contains(@*, 'time')] | "
                                                           "//*[contains(@*, 'datePublished')])[1]/@content) | //time/@datetime)[1]")
)
date_order_DMY = Button(
    text="DMY",
    command=lambda: replace_textbox_value(date_order_textbox, "DMY")
)

date_order_YMD = Button(
    text="YMD",
    command=lambda: replace_textbox_value(date_order_textbox, "YMD")
)

date_order_MDY = Button(
    text="MDY",
    command=lambda: replace_textbox_value(date_order_textbox, "MDY")
)


def author_substring():
    author = author_textbox.get("1.0", tk.END).strip()
    author_textbox.delete("1.0", tk.END)
    author_textbox.insert('1.0', f"substring-after({author},':')")


author_substring_button = Button(
    text="Substr",
    command=author_substring
)

author_meta_button = Button(
    text="Meta",
    command=lambda: replace_textbox_value(author_textbox, "//meta[contains(@*,'uthor')]/@content")
)

author_child_text_button = Button(
    text="Child",
    command=lambda: replace_textbox_value(author_textbox, '//*[child::text()[contains(.,"Autor")]]')
)

body_contains_class_button = Button(
    text="Cnt",
    command=lambda: replace_textbox_value(body_textbox, "//div[contains(@class, 'content')]")
)


def not_contains(string_to_append):
    textbox = body_textbox.get("1.0", tk.END).strip()
    body_textbox.delete("1.0", tk.END)
    body_textbox.insert("1.0", f"{textbox.strip()}{string_to_append}")


not_contains_class_button = Button(
    text="Not Class",
    command=lambda: not_contains(f"[not(contains(@class, '{window.clipboard_get()}'))]")
)

not_contains_text_button = Button(
    text="Not Text",
    command=lambda: not_contains(f"[not(descendant::text()[contains(.,'{window.clipboard_get()}')])]")
)


def open_start_urls_link():
    links = start_urls_textbox.get("1.0", tk.END).split(';')
    for link in links:
        webbrowser.get("chrome").open(link)


open_link_button = Button(
    text='Link',
    command=open_start_urls_link
)


def get_domain():
    link = start_urls_textbox.get("1.0", tk.END).strip()
    if link[-1] != '/':
        link += '/'
    domain = "/".join(link.split('/')[:3]) + '/'
    return domain


def find_sitemap():
    xpath = "(//*[contains(@href, 'site')][contains(@href, 'map')] | //*[contains(@href, 'map')][contains(@href, 'web')])[1]/@href"
    domain = get_domain()
    try:
        sitemap_response = requests.get(domain, headers={'Connection': 'close'})
        tree = html.fromstring(sitemap_response.text)
        sitemap = tree.xpath(xpath)
        if sitemap:
            sitemap_link = sitemap[0]
            if domain not in sitemap[0]:
                sitemap_link = domain[:-1] + sitemap[0]
            webbrowser.get("chrome").open(sitemap_link)
            print(f"Sitemap - {sitemap_link}")
        else:
            print(f"No sitemap at {domain}")
    except Exception as e:
        print(e.args)
        print(f"Site does not load - {domain}")
        return


def open_domain():
    try:
        domain = get_domain()
    except IndexError:
        print("Invalid URL")
        return
    find_sitemap()
    try:
        webbrowser.get("chrome").open(domain)
        req = session.get(domain)
        new_url = req.url
        if new_url[-1] != '/':
            new_url += '/'
        replace_textbox_value(start_urls_textbox, new_url)
    except Exception:
        print(f"Domain could not load - {domain}")
        return


open_domain_button = Button(
    text='Domain',
    command=open_domain
)

sitemap_button = Button(
    text='Sitemap',
    command=find_sitemap
)


def clear_all_textboxes(kraken_id=True):
    if kraken_id:
        kraken_id_textbox.delete("1.0", tk.END)
    existing_code_textbox.delete("1.0", tk.END)
    start_urls_textbox.delete("1.0", tk.END)
    menu_textbox.delete("1.0", tk.END)
    articles_textbox.delete("1.0", tk.END)
    title_textbox.delete("1.0", tk.END)
    pubdate_textbox.delete("1.0", tk.END)
    date_order_textbox.delete("1.0", tk.END)
    author_textbox.delete("1.0", tk.END)
    body_textbox.delete("1.0", tk.END)
    window.title(window_title)


clear_button = Button(
    text="Clear",
    command=clear_all_textboxes
)


def sort_json(json_object):
    keyorder_arguments = ["start_urls", "menu_xpath", "articles_xpath", "title_xpath", "pubdate_xpath", "date_order",
                          "author_xpath", "body_xpath", "link_id_regex"]
    existing_keys = []
    for entry in keyorder_arguments:
        if entry in json_object["scrapy_arguments"].keys():
            existing_keys.append(entry)

    new_dict = {"scrapy_arguments": {}, "scrapy_settings": {}}
    for entry in existing_keys:
        new_dict["scrapy_arguments"][entry] = json_object["scrapy_arguments"][entry]
    new_dict["scrapy_settings"] = json_object["scrapy_settings"]
    return new_dict


def generate(_=None, initial_json=None, load_from_existing_bool=False):
    def not_empty():
        return bool(start_urls_textbox.get("1.0", tk.END).strip() or
                    menu_textbox.get("1.0", tk.END).strip() or
                    articles_textbox.get("1.0", tk.END).strip() or
                    title_textbox.get("1.0", tk.END).strip() or
                    pubdate_textbox.get("1.0", tk.END).strip() or
                    date_order_textbox.get("1.0", tk.END).strip() or
                    author_textbox.get("1.0", tk.END).strip() or
                    body_textbox.get("1.0", tk.END).strip())

    def get_text_from_textbox(textbox, xpath_name, json_var):
        if textbox.get("1.0", tk.END).strip():
            # .replace(re.sub(r'\S\|\S'), ' | ')
            xpath = textbox.get("1.0", tk.END).strip().replace('"', "'")
            string_for_remove = ["concat( ' ', ", " ' ' ), concat( ' ', ", ", ' ' )"]
            for s in string_for_remove:
                xpath = xpath.replace(s, '')
            json_var["scrapy_arguments"][xpath_name] = re.sub(r'(\S)\|(\S)', r'\1 | \2', xpath)

        elif xpath_name in json_var["scrapy_arguments"].keys() and not_empty():
            json_var["scrapy_arguments"].pop(xpath_name)
        return json_var

    def edit_textbox(textbox, xpath_name, json_var):
        textbox.delete("1.0", tk.END)
        if xpath_name in json_var["scrapy_arguments"].keys():
            textbox.insert('1.0', json_var["scrapy_arguments"][xpath_name])

    def default_changes(json_var):
        json_var["scrapy_arguments"]["link_id_regex"] = None
        for element in first_grid_element_container[2:]:
            edit_textbox(element[0], element[1], json_var)

        if "scrapy_settings" in json_var.keys():
            json_var["scrapy_settings"].update(settings_json)
        else:
            json_var["scrapy_settings"] = settings_json
        return sort_json(json_var)

    def fill_code_textbox():
        final_text = json.dumps(json_variable, indent=2)
        existing_code_textbox.delete("1.0", tk.END)
        existing_code_textbox.insert('1.0', final_text)
        return final_text

    def log_to_db(kraken_id_db):
        def rearrange(xpath):
            xpath_list = xpath.split('|')
            for i, entry in enumerate(xpath_list):
                xpath_list[i] = entry.strip()
            xpath_list = sorted(xpath_list)
            xpath = " | ".join(xpath_list)
            return xpath

        current_time = datetime.now().strftime("%d-%b-%Y %H:%M:%S")
        user = login_data.user if 'user' in dir(login_data) else "Default User"

        start_urls = rearrange(json_variable['scrapy_arguments']['start_urls']) if 'start_urls' in json_variable['scrapy_arguments'].keys() else ""
        menu_xpath = rearrange(json_variable['scrapy_arguments']['menu_xpath']) if 'menu_xpath' in json_variable['scrapy_arguments'].keys() else ""
        articles_xpath = rearrange(json_variable['scrapy_arguments']['articles_xpath']) if 'articles_xpath' in json_variable['scrapy_arguments'].keys() else ""
        title_xpath = rearrange(json_variable['scrapy_arguments']['title_xpath']) if 'title_xpath' in json_variable['scrapy_arguments'].keys() else ""
        pubdate_xpath = rearrange(json_variable['scrapy_arguments']['pubdate_xpath']) if 'pubdate_xpath' in json_variable['scrapy_arguments'].keys() else ""
        date_order = rearrange(json_variable['scrapy_arguments']['date_order']) if 'date_order' in json_variable['scrapy_arguments'].keys() else ""
        author_xpath = rearrange(json_variable['scrapy_arguments']['author_xpath']) if 'author_xpath' in json_variable['scrapy_arguments'].keys() else ""
        body_xpath = rearrange(json_variable['scrapy_arguments']['body_xpath']) if 'body_xpath' in json_variable['scrapy_arguments'].keys() else ""

        cur.execute("SELECT id FROM log WHERE id=?", (kraken_id_db,))
        if len(cur.fetchall()):
            cur.execute("UPDATE log SET date=?, start_urls=?, menu_xpath=?, articles_xpath=?, title_xpath=?, pubdate_xpath=?, date_order=?, author_xpath=?, "
                        "body_xpath=?, settings=?, full_json=?, user=? WHERE id=?",
                        (current_time, start_urls, menu_xpath, articles_xpath, title_xpath, pubdate_xpath, date_order, author_xpath, body_xpath,
                         str(json_variable['scrapy_settings']), str(json_variable), user, kraken_id_db))
        else:
            cur.execute("INSERT INTO log VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (kraken_id_db, current_time, start_urls, menu_xpath, articles_xpath, title_xpath, pubdate_xpath, date_order, author_xpath, body_xpath,
                         str(json_variable['scrapy_settings']), str(json_variable), user))
        con.commit()
        # print(f"Entry {kraken_id_db} entered into database")

    existing_code = existing_code_textbox.get("1.0", tk.END).strip()
    if initial_json:
        json_variable = default_changes(initial_json)
        fill_code_textbox()
        for tup in first_grid_element_container[2:]:
            edit_textbox(tup[0], tup[1], json_variable)

    elif existing_code:
        try:
            json_variable = json.loads(existing_code)
        except JSONDecodeError:
            print("Invalid JSON")
            return
        if not load_from_existing_bool and not_empty():
            for tup in first_grid_element_container[2:]:
                json_variable = get_text_from_textbox(tup[0], tup[1], json_variable)
        json_variable = default_changes(json_variable)
        final_json = fill_code_textbox()
        pyperclip.copy(final_json)
        for tup in first_grid_element_container[2:]:
            edit_textbox(tup[0], tup[1], json_variable)

        if kraken_id_textbox.get('1.0', tk.END).strip():
            kraken_id = kraken_id_textbox.get('1.0', tk.END).split('/')[-2]
            log_to_db(kraken_id)
            if not os.path.isdir('./logs'):
                os.mkdir('./logs')
            with open(f'./logs/{kraken_id}.txt', 'w', encoding='utf-8') as f:
                f.write(final_json)

    elif not_empty():
        json_variable = {
            "scrapy_arguments": {
                "start_urls": "",
                "articles_xpath": "",
                "title_xpath": "",
                "body_xpath": ""
            },
            "scrapy_settings": {
                "LOG_LEVEL": "DEBUG",
                "COOKIES_ENABLED": False,
                "USER_AGENT": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0"
            }
        }
        for tup in first_grid_element_container[2:]:
            json_variable = get_text_from_textbox(tup[0], tup[1], json_variable)
        json_variable = default_changes(json_variable)
        final_json = fill_code_textbox()
        pyperclip.copy(final_json)
        if kraken_id_textbox.get('1.0', tk.END).strip():
            kraken_id = kraken_id_textbox.get('1.0', tk.END).split('/')[-2]
            log_to_db(kraken_id)
            if not os.path.isdir('./logs'):
                os.mkdir('./logs')
            with open(f'./logs/{kraken_id}.txt', 'w', encoding='utf-8') as f:
                f.write(final_json)

    else:
        return


generate_button = Button(
    text="Generate JSON!",
    command=generate,
    master=window,
)

# SECOND VIEW ELEMENTS START HERE
url_of_article_label = tk.Label(
    text="Article URL:",
    font=label_font,
    bg=background
)

author_xpath_found_label = tk.Label(
    text="Article Xpath Found:",
    font=label_font,
    bg=background
)

url_of_article_textbox = tk.Text(
    font=text_font,
    height=1,
    undo=True,
    width=80,
    bg="white",
)

author_xpath_found_textbox = tk.Text(
    bg="white",
    width=80,
    height=5,
    undo=True,
    font=text_font
)


def find_xpath():
    article_url = url_of_article_textbox.get("1.0", tk.END).strip()
    cur.execute("SELECT author_xpath, count(author_xpath) FROM log GROUP BY author_xpath ORDER BY count(author_xpath) DESC LIMIT 20")
    results = cur.fetchall()
    xpath_list = []
    for result in results:
        if result[0]:
            if not result[0].endswith('content'):
                xpath_list.append(result[0] + '/text()')
            else:
                xpath_list.append(result[0])
    website_response = requests.get(article_url, headers={'Connection': 'close'})
    tree = html.fromstring(website_response.text)
    final_result = ""
    for xpath in xpath_list:
        result = tree.xpath(xpath)
        if result:
            print(xpath, result[0])
            final_result += f"{xpath} - {result[0]}\n"
    author_xpath_found_textbox.delete("1.0", tk.END)
    author_xpath_found_textbox.insert("1.0", final_result)


find_xpath_button = Button(
    text="Find Xpath",
    command=find_xpath,
    master=window,
)

# SECOND VIEW ELEMENTS END HERE
first_grid_element_container = [
    (kraken_id_textbox, "kraken_link", kraken_id_label, kraken_id_load_button, kraken_id_clipboard_button,
     open_source_button, load_from_db_button, open_items_button),
    (existing_code_textbox, "existing_code", existing_code_label, code_copy_button, source_name_button, load_from_existing_button),
    (start_urls_textbox, "start_urls", start_urls_label, copy_start_button, open_link_button, open_domain_button,
     sitemap_button),
    (menu_textbox, "menu_xpath", menu_label, copy_menu_button),
    (articles_textbox, "articles_xpath", articles_label, copy_articles_button),
    (title_textbox, "title_xpath", title_label, copy_title_button, title_button_brackets),
    (pubdate_textbox, "pubdate_xpath", pubdate_label, copy_pubdate_button, meta_button, regex_dmy_button,
     regex_ymd_button, pubdate_button_brackets),
    (date_order_textbox, "date_order", date_order_label, date_order_DMY, date_order_YMD, date_order_MDY),
    (author_textbox, "author_xpath", author_label, copy_author_button, author_meta_button, author_substring_button,
     author_child_text_button, author_button_brackets),
    (body_textbox, "body_xpath", body_label, copy_body_button, body_contains_class_button, not_contains_class_button,
     not_contains_text_button, body_button_brackets)]

session = requests.Session()

with open('settings.json') as f1:
    settings_json = json.load(f1)

con = sqlite3.connect('log.db')
cur = con.cursor()


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


# Code to run when exiting software
def exit_handler():
    con.close()


def toggle_view():
    row = 1
    if generate_button.winfo_ismapped():
        # Forget First View
        for element in first_grid_element_container:
            for widget in element:
                if not isinstance(widget, str):
                    widget.grid_forget()
                    generate_button.grid_forget()
                    clear_button.grid_forget()
        # Load Second View
        url_of_article_label.grid(row=row, column=1, sticky='W', padx=(50, 2), pady=(20, 2))
        url_of_article_textbox.grid(row=row, column=2, sticky='W', padx=2, pady=(20, 2))
        row += 1
        author_xpath_found_label.grid(row=row, column=1, sticky='W', padx=(50, 2), pady=(10, 2))
        author_xpath_found_textbox.grid(row=row, column=2, sticky='W', padx=2, pady=(20, 2))
        row += 1
        find_xpath_button.grid(row=row, column=1, sticky='W', padx=(50, 2), pady=(10, 2))
    else:
        # Forget Second View
        url_of_article_label.grid_forget()
        url_of_article_textbox.grid_forget()
        author_xpath_found_label.grid_forget()
        author_xpath_found_textbox.grid_forget()
        find_xpath_button.grid_forget()
        # Load First View
        for t in first_grid_element_container:
            row = pack_entries(t, row)

        generate_button.grid(row=row, column=1, sticky='W', ipadx=0, ipady=0, pady=(5, 2), padx=(20, 2))
        clear_button.grid(row=row, column=2, sticky="E", ipadx=0, ipady=0, pady=2, padx=2)
        row += 1


toggle_view_button = Button(
    text="Switch Views",
    command=toggle_view
)


def stats():
    def join_tuple_string(values_tuple) -> str:
        string_list = []
        for element in values_tuple:
            string_list.append(str(element))
        return ', '.join(string_list)

    with open('stats.txt', 'w') as f:
        cur.execute("SELECT menu_xpath, count(menu_xpath) FROM log GROUP BY menu_xpath ORDER BY count(menu_xpath) DESC LIMIT 20")
        results = cur.fetchall()
        results = list(map(join_tuple_string, results))
        f.write("menu_xpath:\n")
        f.writelines(line + '\n' for line in results)
        f.write('\n')

        cur.execute("SELECT articles_xpath, count(articles_xpath) FROM log GROUP BY articles_xpath ORDER BY count(articles_xpath) DESC LIMIT 20")
        results = cur.fetchall()
        results = list(map(join_tuple_string, results))
        f.write("articles_xpath:\n")
        f.writelines(line + '\n' for line in results)
        f.write('\n')

        cur.execute("SELECT title_xpath, count(title_xpath) FROM log GROUP BY title_xpath ORDER BY count(title_xpath) DESC LIMIT 20")
        results = cur.fetchall()
        results = list(map(join_tuple_string, results))
        f.write("title_xpath:\n")
        f.writelines(line + '\n' for line in results)
        f.write('\n')

        cur.execute("SELECT pubdate_xpath, count(pubdate_xpath) FROM log GROUP BY pubdate_xpath ORDER BY count(pubdate_xpath) DESC LIMIT 20")
        results = cur.fetchall()
        results = list(map(join_tuple_string, results))
        f.write("pubdate_xpath:\n")
        f.writelines(line + '\n' for line in results)
        f.write('\n')

        cur.execute("SELECT author_xpath, count(author_xpath) FROM log GROUP BY author_xpath ORDER BY count(author_xpath) DESC LIMIT 20")
        results = cur.fetchall()
        results = list(map(join_tuple_string, results))
        f.write("author_xpath:\n")
        f.writelines(line + '\n' for line in results)
        f.write('\n')

        cur.execute("SELECT body_xpath, count(body_xpath) FROM log GROUP BY body_xpath ORDER BY count(body_xpath) DESC LIMIT 20")
        results = cur.fetchall()
        results = list(map(join_tuple_string, results))
        f.write("body_xpath:\n")
        f.writelines(line + '\n' for line in results)
        f.write('\n')

        cur.execute("SELECT settings, count(settings) FROM log GROUP BY settings ORDER BY count(settings) DESC LIMIT 20")
        results = cur.fetchall()
        results = list(map(join_tuple_string, results))
        f.write("settings:\n")
        f.writelines(line + '\n' for line in results)
        f.write('\n')


def pack_entries(entry_tuple, curr_row):
    entry_tuple[2].grid(row=curr_row, column=1, sticky='W', pady=2, padx=(20, 2))
    curr_row += 1
    entry_tuple[0].grid(row=curr_row, column=1, sticky='W', pady=2, padx=(20, 2))
    if len(entry_tuple) > 3:  # if len = 4 or more
        for i in range(3, len(entry_tuple)):
            entry_tuple[i].grid(row=curr_row, column=i - 1, sticky='W', pady=2, padx=2)
    curr_row += 1
    return curr_row


def main():
    # stats()
    cur.execute('''CREATE TABLE IF NOT EXISTS log
               (id text, date text, start_urls text, menu_xpath text, articles_xpath text, title_xpath text, 
               pubdate_xpath text, date_order text, author_xpath text, body_xpath text, settings text, 
               full_json text, user text)''')

    login_link = "https://dashbeta.aiidatapro.net/"

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/67.0.3396.99 Safari/537.36'
    }

    if not os.path.exists('./login_data.py'):
        with open('login_data.py', 'w') as login_file:
            login_file.write('username = "USERNAME_HERE"\npassword = "PASSWORD_HERE"')
            print("Fill in your login details in login_data.py!")
    else:
        session.get(login_link, headers=headers)
        if 'csrftoken' in session.cookies:
            # Django 1.6 and up
            csrftoken = session.cookies['csrftoken']
        else:
            csrftoken = session.cookies['csrf']
        headers['cookie'] = '; '.join([x.name + '=' + x.value for x in session.cookies])
        headers['content-type'] = 'application/x-www-form-urlencoded'
        payload = {
            'username': login_data.username,
            'password': login_data.password,
            'csrfmiddlewaretoken': csrftoken
        }
        response = session.post(login_link, data=payload, headers=headers)
        headers['cookie'] = '; '.join([x.name + '=' + x.value for x in response.cookies])
        print("Logged in!")

    chrome_path = 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))

    # Style all buttons
    style = Style()
    style.configure('TButton', font=('Roboto Bold', 10))
    style.map('TButton', foreground=[('active', '!disabled', 'green')],
              background=[('active', 'black')])

    row = 0
    toggle_view_button.grid(row=row, column=1, sticky='W', pady=10, padx=100)
    row += 1

    for t in first_grid_element_container:
        row = pack_entries(t, row)

    generate_button.grid(row=row, column=1, sticky='W', ipadx=0, ipady=0, pady=(5, 2), padx=(20, 2))
    clear_button.grid(row=row, column=2, sticky="E", ipadx=0, ipady=0, pady=2, padx=2)
    row += 1

    atexit.register(exit_handler)

    window.geometry("960x1080+1+1")
    window.bind_all("<Key>", on_key_release, "+")
    window.lift()
    window.mainloop()


if __name__ == '__main__':
    main()
