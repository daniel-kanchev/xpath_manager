import math
import re
import tkinter as tk
import json
import webbrowser
from json import JSONDecodeError
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


class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.window_title = f"Xpath Extractor ({config.last_change})"
        self.title(self.window_title)
        self.background = 'dark grey'
        self.configure(background=self.background)
        self.label_font = Font(family="Arial", size=12)
        self.text_font = Font(family="Calibri", size=12)
        self.date_meta = "(((//meta[contains(@*, 'date')] | //meta[contains(@*, 'time')] | //*[contains(@*, 'datePublished')])[1]/@content) | " \
                         "//time/@datetime)[1]"
        self.menu_meta = "(//ul[contains(@class, 'menu')] | //ul[contains(@id, 'menu')] | //nav//ul)[1]//a"
        self.author_meta = "//meta[contains(@*,'uthor')]/@content"
        # Labels
        self.kraken_id_label = tk.Label(text="Link:")
        self.existing_code_label = tk.Label(text="Code:")
        self.start_urls_label = tk.Label(text="Start URL:")
        self.menu_label = tk.Label(text="Menu XPath:")
        self.articles_label = tk.Label(text="Articles XPath:")
        self.title_label = tk.Label(text="Title XPath:")
        self.pubdate_label = tk.Label(text="Pubdate XPath:")
        self.date_order_label = tk.Label(text="Date Order XPath:")
        self.author_label = tk.Label(text="Author XPath:")
        self.body_label = tk.Label(text="Body XPath:")
        self.article_url_label = tk.Label(text="Article URL:")

        self.title_xpath_found_label = tk.Label(text="Title XPath:")
        self.pubdate_xpath_found_label = tk.Label(text="Pubdate XPath:")
        self.author_xpath_found_label = tk.Label(text="Author XPath:")
        self.body_xpath_found_label = tk.Label(text="Body XPath:")

        all_labels = [self.existing_code_label, self.kraken_id_label, self.start_urls_label, self.menu_label, self.articles_label, self.title_label,
                      self.pubdate_label, self.date_order_label, self.author_label, self.body_label, self.article_url_label, self.author_xpath_found_label,
                      self.pubdate_xpath_found_label, self.title_xpath_found_label, self.body_xpath_found_label]

        for label in all_labels:
            label['bg'] = self.background
            label['font'] = self.label_font

        # Textboxes
        self.article_url_textbox = tk.Text(height=1, width=40)
        self.existing_code_textbox = tk.Text(height=10, width=60)
        self.start_urls_textbox = tk.Text(height=2, width=60)
        self.menu_textbox = tk.Text(height=2, width=60)
        self.articles_textbox = tk.Text(height=2, width=60)
        self.title_textbox = tk.Text(height=2, width=60)
        self.pubdate_textbox = tk.Text(height=2, width=60)
        self.date_order_textbox = tk.Text(height=2, width=20)
        self.author_textbox = tk.Text(height=2, width=60)
        self.body_textbox = tk.Text(height=3, width=60)
        self.kraken_id_textbox = tk.Text(height=1, width=60)
        self.title_xpath_found_textbox_1 = tk.Text(height=1, width=40)
        self.title_xpath_found_textbox_2 = tk.Text(height=1, width=40)
        self.title_xpath_found_textbox_3 = tk.Text(height=1, width=40)
        self.title_xpath_found_textbox_4 = tk.Text(height=1, width=40)
        self.title_xpath_found_textbox_5 = tk.Text(height=1, width=40)
        self.title_xpath_result_textbox_1 = tk.Text(height=1, width=40)
        self.title_xpath_result_textbox_2 = tk.Text(height=1, width=40)
        self.title_xpath_result_textbox_3 = tk.Text(height=1, width=40)
        self.title_xpath_result_textbox_4 = tk.Text(height=1, width=40)
        self.title_xpath_result_textbox_5 = tk.Text(height=1, width=40)

        self.pubdate_xpath_found_textbox_1 = tk.Text(height=1, width=40)
        self.pubdate_xpath_found_textbox_2 = tk.Text(height=1, width=40)
        self.pubdate_xpath_found_textbox_3 = tk.Text(height=1, width=40)
        self.pubdate_xpath_found_textbox_4 = tk.Text(height=1, width=40)
        self.pubdate_xpath_found_textbox_5 = tk.Text(height=1, width=40)
        self.pubdate_xpath_result_textbox_1 = tk.Text(height=1, width=40)
        self.pubdate_xpath_result_textbox_2 = tk.Text(height=1, width=40)
        self.pubdate_xpath_result_textbox_3 = tk.Text(height=1, width=40)
        self.pubdate_xpath_result_textbox_4 = tk.Text(height=1, width=40)
        self.pubdate_xpath_result_textbox_5 = tk.Text(height=1, width=40)

        self.author_xpath_found_textbox_1 = tk.Text(height=1, width=40)
        self.author_xpath_found_textbox_2 = tk.Text(height=1, width=40)
        self.author_xpath_found_textbox_3 = tk.Text(height=1, width=40)
        self.author_xpath_found_textbox_4 = tk.Text(height=1, width=40)
        self.author_xpath_found_textbox_5 = tk.Text(height=1, width=40)
        self.author_xpath_result_textbox_1 = tk.Text(height=1, width=40)
        self.author_xpath_result_textbox_2 = tk.Text(height=1, width=40)
        self.author_xpath_result_textbox_3 = tk.Text(height=1, width=40)
        self.author_xpath_result_textbox_4 = tk.Text(height=1, width=40)
        self.author_xpath_result_textbox_5 = tk.Text(height=1, width=40)

        self.body_xpath_found_textbox_1 = tk.Text(height=1, width=40)
        self.body_xpath_found_textbox_2 = tk.Text(height=1, width=40)
        self.body_xpath_found_textbox_3 = tk.Text(height=1, width=40)
        self.body_xpath_found_textbox_4 = tk.Text(height=1, width=40)
        self.body_xpath_found_textbox_5 = tk.Text(height=1, width=40)
        self.body_xpath_result_textbox_1 = tk.Text(height=1, width=40)
        self.body_xpath_result_textbox_2 = tk.Text(height=1, width=40)
        self.body_xpath_result_textbox_3 = tk.Text(height=1, width=40)
        self.body_xpath_result_textbox_4 = tk.Text(height=1, width=40)
        self.body_xpath_result_textbox_5 = tk.Text(height=1, width=40)

        all_textboxes = [self.article_url_textbox, self.existing_code_textbox, self.start_urls_textbox, self.menu_textbox, self.articles_textbox,
                         self.title_textbox, self.pubdate_textbox, self.date_order_textbox, self.author_textbox, self.body_textbox, self.kraken_id_textbox,
                         self.author_xpath_found_textbox_1, self.author_xpath_found_textbox_2, self.author_xpath_found_textbox_3,
                         self.author_xpath_found_textbox_4, self.author_xpath_found_textbox_5, self.author_xpath_result_textbox_1,
                         self.author_xpath_result_textbox_2, self.author_xpath_result_textbox_3, self.author_xpath_result_textbox_4,
                         self.author_xpath_result_textbox_5, self.pubdate_xpath_found_textbox_1, self.pubdate_xpath_found_textbox_2,
                         self.pubdate_xpath_found_textbox_3, self.pubdate_xpath_found_textbox_4, self.pubdate_xpath_found_textbox_5,
                         self.pubdate_xpath_result_textbox_1, self.pubdate_xpath_result_textbox_2, self.pubdate_xpath_result_textbox_3,
                         self.pubdate_xpath_result_textbox_4, self.pubdate_xpath_result_textbox_5, self.title_xpath_found_textbox_1,
                         self.title_xpath_found_textbox_4, self.title_xpath_found_textbox_5, self.title_xpath_result_textbox_1,
                         self.title_xpath_result_textbox_2, self.title_xpath_result_textbox_3, self.title_xpath_result_textbox_4,
                         self.title_xpath_result_textbox_5, self.body_xpath_found_textbox_1, self.body_xpath_found_textbox_2,
                         self.body_xpath_found_textbox_3, self.body_xpath_found_textbox_4, self.body_xpath_found_textbox_5,
                         self.body_xpath_result_textbox_1, self.body_xpath_result_textbox_2, self.body_xpath_result_textbox_3,
                         self.body_xpath_result_textbox_4, self.body_xpath_result_textbox_5, self.title_xpath_found_textbox_2,
                         self.title_xpath_found_textbox_3, ]

        for textbox in all_textboxes:
            textbox['undo'] = True
            textbox['bg'] = 'white'
            textbox['font'] = self.text_font

        # Buttons
        self.code_copy_button = Button(text="Copy", command=lambda: self.copy_code(self.existing_code_textbox))
        self.copy_start_button = Button(text="Copy", command=lambda: self.copy_code(self.start_urls_textbox))
        self.copy_menu_button = Button(text="Copy", command=lambda: self.copy_code(self.menu_textbox))
        self.copy_articles_button = Button(text="Copy", command=lambda: self.copy_code(self.articles_textbox))
        self.copy_title_button = Button(text="Copy", command=lambda: self.copy_code(self.title_textbox))
        self.copy_pubdate_button = Button(text="Copy", command=lambda: self.copy_code(self.pubdate_textbox))
        self.copy_author_button = Button(text="Copy", command=lambda: self.copy_code(self.author_textbox))
        self.copy_body_button = Button(text="Copy", command=lambda: self.copy_code(self.body_textbox))
        self.kraken_id_load_button = Button(text="Load", command=lambda: self.load_code(self.kraken_id_textbox.get('1.0', tk.END), open_source_bool=False))
        self.kraken_id_clipboard_button = Button(text="Clip", command=lambda: self.load_code(self.clipboard_get()))
        self.open_source_button = Button(text="Source", command=lambda: self.open_link(self.kraken_id_textbox.get('1.0', tk.END)))
        self.load_from_db_button = Button(text="DB Load", command=self.load_from_db)
        self.open_items_button = Button(text="Items", command=self.open_items_page)
        self.source_name_button = Button(text="Name", command=self.get_source_name)
        self.load_from_existing_button = Button(text="Load", command=lambda: self.generate(load_from_existing_bool=True))
        self.title_button_brackets = Button(text="[1]", command=lambda: self.get_only_first_value(self.title_textbox))
        self.pubdate_button_brackets = Button(text="[1]", command=lambda: self.get_only_first_value(self.pubdate_textbox))
        self.author_button_brackets = Button(text="[1]", command=lambda: self.get_only_first_value(self.author_textbox))
        self.body_button_brackets = Button(text="[1]", command=lambda: self.get_only_first_value(self.body_textbox), )
        self.regex_dmy_button = Button(text="Rgx.", command=lambda: self.add_regex_for_date(r'\d{1,2}\.\d{1,2}\.\d{2,4}'))
        self.regex_ymd_button = Button(text="Rgx Txt", command=lambda: self.add_regex_for_date(r'(\d{1,2})\.(\s\w+\s\d{2,4})'))
        self.menu_default_button = Button(text="Default", command=lambda: self.replace_textbox_value(self.menu_textbox,
                                                                                                     "(//ul[contains(@class, 'menu')] |"
                                                                                                     " //ul[contains(@id, 'menu')] | //nav//ul)[1]//a"))
        self.menu_category_button = Button(text="Cat", command=lambda: self.append_textbox_value(self.menu_textbox, "[contains(@href, 'ategor')]"))
        self.meta_button = Button(text="Meta", command=lambda: self.replace_textbox_value(self.pubdate_textbox, self.date_meta))
        self.date_order_DMY = Button(text="DMY", command=lambda: self.replace_textbox_value(self.date_order_textbox, "DMY"))
        self.date_order_YMD = Button(text="YMD", command=lambda: self.replace_textbox_value(self.date_order_textbox, "YMD"))
        self.date_order_MDY = Button(text="MDY", command=lambda: self.replace_textbox_value(self.date_order_textbox, "MDY"))
        self.author_substring_button = Button(text="Substr", command=self.author_substring)
        self.author_meta_button = Button(text="Meta", command=lambda: self.replace_textbox_value(self.author_textbox, "//meta[contains(@*,'uthor')]/@content"))
        self.author_child_text_button = Button(text="Child", command=lambda: self.replace_textbox_value(self.author_textbox,
                                                                                                        '//*[child::text()[contains(.,"Autor")]]'))
        self.body_contains_class_button = Button(text="Cnt",
                                                 command=lambda: self.replace_textbox_value(self.body_textbox, "//div[contains(@class, 'content')]"))
        self.not_contains_class_button = Button(text="Not Class",
                                                command=lambda: self.append_textbox_value(self.body_textbox,
                                                                                          f"[not(contains(@class, '{self.clipboard_get()}'))]"))
        self.not_contains_text_button = Button(text="Not Text",
                                               command=lambda: self.append_textbox_value(self.body_textbox,
                                                                                         f"[not(descendant::text()[contains(.,'{self.clipboard_get()}')])]"))
        self.open_link_button = Button(text='Link', command=self.open_start_urls_link)
        self.open_domain_button = Button(text='Domain', command=self.open_domain)
        self.sitemap_button = Button(text='Sitemap', command=self.find_sitemap)
        self.clear_button = Button(text="Clear", command=self.clear_all_textboxes)
        self.generate_button = Button(text="Generate JSON!", command=self.generate, master=self)

        # Second View
        self.find_xpath_button = Button(text="Find XPath", command=self.find_xpath, master=self)
        self.title_xpath_select_button_1 = Button(text="Select", command=lambda: self.from_textbox_to_textbox(self.title_xpath_found_textbox_1,
                                                                                                              self.title_textbox))
        self.title_xpath_select_button_2 = Button(text="Select", command=lambda: self.from_textbox_to_textbox(self.title_xpath_found_textbox_2,
                                                                                                              self.title_textbox))
        self.title_xpath_select_button_3 = Button(text="Select", command=lambda: self.from_textbox_to_textbox(self.title_xpath_found_textbox_3,
                                                                                                              self.title_textbox))
        self.title_xpath_select_button_4 = Button(text="Select", command=lambda: self.from_textbox_to_textbox(self.title_xpath_found_textbox_4,
                                                                                                              self.title_textbox))
        self.title_xpath_select_button_5 = Button(text="Select", command=lambda: self.from_textbox_to_textbox(self.title_xpath_found_textbox_5,
                                                                                                              self.title_textbox))

        self.pubdate_xpath_select_button_1 = Button(text="Select", command=lambda: self.from_textbox_to_textbox(self.pubdate_xpath_found_textbox_1,
                                                                                                                self.pubdate_textbox))
        self.pubdate_xpath_select_button_2 = Button(text="Select", command=lambda: self.from_textbox_to_textbox(self.pubdate_xpath_found_textbox_2,
                                                                                                                self.pubdate_textbox))
        self.pubdate_xpath_select_button_3 = Button(text="Select", command=lambda: self.from_textbox_to_textbox(self.pubdate_xpath_found_textbox_3,
                                                                                                                self.pubdate_textbox))
        self.pubdate_xpath_select_button_4 = Button(text="Select", command=lambda: self.from_textbox_to_textbox(self.pubdate_xpath_found_textbox_4,
                                                                                                                self.pubdate_textbox))
        self.pubdate_xpath_select_button_5 = Button(text="Select", command=lambda: self.from_textbox_to_textbox(self.pubdate_xpath_found_textbox_5,
                                                                                                                self.pubdate_textbox))

        self.author_xpath_select_button_1 = Button(text="Select", command=lambda: self.from_textbox_to_textbox(self.author_xpath_found_textbox_1,
                                                                                                               self.author_textbox))
        self.author_xpath_select_button_2 = Button(text="Select", command=lambda: self.from_textbox_to_textbox(self.author_xpath_found_textbox_2,
                                                                                                               self.author_textbox))
        self.author_xpath_select_button_3 = Button(text="Select", command=lambda: self.from_textbox_to_textbox(self.author_xpath_found_textbox_3,
                                                                                                               self.author_textbox))
        self.author_xpath_select_button_4 = Button(text="Select", command=lambda: self.from_textbox_to_textbox(self.author_xpath_found_textbox_4,
                                                                                                               self.author_textbox))
        self.author_xpath_select_button_5 = Button(text="Select", command=lambda: self.from_textbox_to_textbox(self.author_xpath_found_textbox_5,
                                                                                                               self.author_textbox))

        self.body_xpath_select_button_1 = Button(text="Select", command=lambda: self.from_textbox_to_textbox(self.body_xpath_found_textbox_1,
                                                                                                             self.body_textbox))
        self.body_xpath_select_button_2 = Button(text="Select", command=lambda: self.from_textbox_to_textbox(self.body_xpath_found_textbox_2,
                                                                                                             self.body_textbox))
        self.body_xpath_select_button_3 = Button(text="Select", command=lambda: self.from_textbox_to_textbox(self.body_xpath_found_textbox_3,
                                                                                                             self.body_textbox))
        self.body_xpath_select_button_4 = Button(text="Select", command=lambda: self.from_textbox_to_textbox(self.body_xpath_found_textbox_4,
                                                                                                             self.body_textbox))
        self.body_xpath_select_button_5 = Button(text="Select", command=lambda: self.from_textbox_to_textbox(self.body_xpath_found_textbox_5,
                                                                                                             self.body_textbox))

        self.toggle_view_button = Button(text="Switch Views", command=self.toggle_view)

        self.first_grid_element_container = [
            (self.kraken_id_textbox, "kraken_link", self.kraken_id_label, self.kraken_id_load_button, self.kraken_id_clipboard_button,
             self.open_source_button, self.load_from_db_button, self.open_items_button),
            (self.existing_code_textbox, "existing_code", self.existing_code_label, self.code_copy_button, self.source_name_button,
             self.load_from_existing_button),
            (self.start_urls_textbox, "start_urls", self.start_urls_label, self.copy_start_button, self.open_link_button, self.open_domain_button,
             self.sitemap_button),
            (self.menu_textbox, "menu_xpath", self.menu_label, self.copy_menu_button, self.menu_default_button, self.menu_category_button),
            (self.articles_textbox, "articles_xpath", self.articles_label, self.copy_articles_button),
            (self.title_textbox, "title_xpath", self.title_label, self.copy_title_button, self.title_button_brackets),
            (self.pubdate_textbox, "pubdate_xpath", self.pubdate_label, self.copy_pubdate_button, self.meta_button, self.regex_dmy_button,
             self.regex_ymd_button, self.pubdate_button_brackets),
            (self.date_order_textbox, "date_order", self.date_order_label, self.date_order_DMY, self.date_order_YMD, self.date_order_MDY),
            (self.author_textbox, "author_xpath", self.author_label, self.copy_author_button, self.author_meta_button, self.author_substring_button,
             self.author_child_text_button, self.author_button_brackets),
            (self.body_textbox, "body_xpath", self.body_label, self.copy_body_button, self.body_contains_class_button, self.not_contains_class_button,
             self.not_contains_text_button, self.body_button_brackets)]

        self.second_grid_elements_container = [
            (self.title_xpath_found_label, self.title_xpath_found_textbox_1, self.title_xpath_select_button_1, self.title_xpath_result_textbox_1,
             self.title_xpath_found_textbox_2, self.title_xpath_select_button_2, self.title_xpath_result_textbox_2,
             self.title_xpath_found_textbox_3, self.title_xpath_select_button_3, self.title_xpath_result_textbox_3,
             self.title_xpath_found_textbox_4, self.title_xpath_select_button_4, self.title_xpath_result_textbox_4,
             self.title_xpath_found_textbox_5, self.title_xpath_select_button_5, self.title_xpath_result_textbox_5),
            (self.pubdate_xpath_found_label, self.pubdate_xpath_found_textbox_1, self.pubdate_xpath_select_button_1, self.pubdate_xpath_result_textbox_1,
             self.pubdate_xpath_found_textbox_2, self.pubdate_xpath_select_button_2, self.pubdate_xpath_result_textbox_2,
             self.pubdate_xpath_found_textbox_3, self.pubdate_xpath_select_button_3, self.pubdate_xpath_result_textbox_3,
             self.pubdate_xpath_found_textbox_4, self.pubdate_xpath_select_button_4, self.pubdate_xpath_result_textbox_4,
             self.pubdate_xpath_found_textbox_5, self.pubdate_xpath_select_button_5, self.pubdate_xpath_result_textbox_5),
            (self.author_xpath_found_label, self.author_xpath_found_textbox_1, self.author_xpath_select_button_1, self.author_xpath_result_textbox_1,
             self.author_xpath_found_textbox_2, self.author_xpath_select_button_2, self.author_xpath_result_textbox_2,
             self.author_xpath_found_textbox_3, self.author_xpath_select_button_3, self.author_xpath_result_textbox_3,
             self.author_xpath_found_textbox_4, self.author_xpath_select_button_4, self.author_xpath_result_textbox_4,
             self.author_xpath_found_textbox_5, self.author_xpath_select_button_5, self.author_xpath_result_textbox_5),
            (self.body_xpath_found_label, self.body_xpath_found_textbox_1, self.body_xpath_select_button_1, self.body_xpath_result_textbox_1,
             self.body_xpath_found_textbox_2, self.body_xpath_select_button_2, self.body_xpath_result_textbox_2,
             self.body_xpath_found_textbox_3, self.body_xpath_select_button_3, self.body_xpath_result_textbox_3,
             self.body_xpath_found_textbox_4, self.body_xpath_select_button_4, self.body_xpath_result_textbox_4,
             self.body_xpath_found_textbox_5, self.body_xpath_select_button_5, self.body_xpath_result_textbox_5)]

        self.session = requests.Session()
        with open('settings.json') as f1:
            self.settings_json = json.load(f1)

        self.con = sqlite3.connect('log.db')
        self.cur = self.con.cursor()

        # stats()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS log
                       (id text, date text, start_urls text, menu_xpath text, articles_xpath text, title_xpath text, 
                       pubdate_xpath text, date_order text, author_xpath text, body_xpath text, settings text, 
                       full_json text, user text)''')

        login_link = "https://dashbeta.aiidatapro.net/"

        self.headers = {'Connection': 'close', 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0'}
        session_headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/67.0.3396.99 Safari/537.36'
        }

        if not os.path.exists('./login_data.py'):
            with open('login_data.py', 'w') as login_file:
                login_file.write('username = "USERNAME_HERE"\npassword = "PASSWORD_HERE"')
                print("Fill in your login details in login_data.py!")
        else:
            self.session.get(login_link, headers=session_headers)
            if 'csrftoken' in self.session.cookies:
                # Django 1.6 and up
                csrftoken = self.session.cookies['csrftoken']
            else:
                csrftoken = self.session.cookies['csrf']
            session_headers['cookie'] = '; '.join([x.name + '=' + x.value for x in self.session.cookies])
            session_headers['content-type'] = 'application/x-www-form-urlencoded'
            payload = {
                'username': login_data.username,
                'password': login_data.password,
                'csrfmiddlewaretoken': csrftoken
            }
            response = self.session.post(login_link, data=payload, headers=session_headers)
            session_headers['cookie'] = '; '.join([x.name + '=' + x.value for x in response.cookies])
            print("Logged in!")

        chrome_path = 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
        webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))

        # Style all buttons
        style = Style()
        style.configure('TButton', font=('Roboto Bold', 10))
        style.map('TButton', foreground=[('active', '!disabled', 'green')],
                  background=[('active', 'black')])

        row = 0
        self.toggle_view_button.grid(row=row, column=1, sticky='W', pady=10, padx=(50, 2))
        row += 1

        for t in self.first_grid_element_container:
            row = self.pack_entries(t, row)

        self.generate_button.grid(row=row, column=1, sticky='W', ipadx=0, ipady=0, pady=(5, 2), padx=(20, 2))
        self.clear_button.grid(row=row, column=2, sticky="E", ipadx=0, ipady=0, pady=2, padx=2)
        row += 1

        atexit.register(self.exit_handler)

        self.geometry("960x1080+1+1")
        self.bind_all("<Key>", self.on_key_release, "+")
        self.lift()

    @staticmethod
    def copy_code(textbox):
        """
        Desc: Function for the button to copy a text fields
        :param textbox: Textbox whose text should be copied to clipboard
        :return:
        """
        pyperclip.copy(textbox.get("1.0", tk.END).strip())

    def get_link(self, link):
        """
        Function to correctly format the Kraken link by searching for the ID in the URL
        :param link: Kraken link / ID
        :return: The correctly formatted link
        """
        kraken_id = re.search(r'\d+', link).group()  # Regex to extract number
        self.title(f"{kraken_id} - {self.window_title}")
        link = f"http://kraken.aiidatapro.net/items/edit/{kraken_id}/"
        return link

    def load_code(self, link, open_source_bool=True):
        """
        Function to fill the extractor with the JSON from Kraken
        :param link: Kraken link / ID
        :param open_source_bool: Bool indicating whether the source link should be opened in a browser tab
        :return:
        """
        link = self.get_link(link)  # Format link

        if open_source_bool:
            webbrowser.get("chrome").open(link)

        self.clear_all_textboxes(kraken_id=False)

        # Show correctly formatted link in textbox
        self.kraken_id_textbox.delete('1.0', tk.END)
        self.kraken_id_textbox.insert('1.0', link)

        # Extract Xpath from Kraken page
        xpath = "//input[@name='feed_properties']/@value"
        link = link.strip()
        kraken_response = self.session.get(link)
        tree = html.fromstring(kraken_response.text)
        code = tree.xpath(xpath)
        code = ''.join(code).replace('\r', '').replace('\n', '')
        try:
            generated_json = json.loads(code)
        except JSONDecodeError:
            # This error indicates the login details are wrong
            print("Incorrect Login Details")
            return
        self.generate(initial_json=generated_json)  # Pass JSON to generate function

    @staticmethod
    def open_link(link):
        """
        Opens the link given in your browser
        :param link: Link to be opened
        :return:
        """
        webbrowser.get("chrome").open(link)

    def load_from_db(self):
        """
        Extracts ID from Kraken Textbox and loads the source from the database
        :return:
        """
        kraken_id = re.search(r'\d+', self.kraken_id_textbox.get('1.0', tk.END)).group()
        self.cur.execute('SELECT * FROM log WHERE id=?', (kraken_id,))
        result = self.cur.fetchone()
        if result:
            self.title(f"{kraken_id} - {self.window_title}")
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
            self.generate(initial_json=json_var)
        else:
            self.clear_all_textboxes()  # Clear all textboxes to indicate entry doesn't exist

    def open_items_page(self):
        # Function to open the "View Item" page of the source in Kraken
        link = self.get_link(self.kraken_id_textbox.get('1.0', tk.END).strip()).replace('/edit', '')
        webbrowser.get("chrome").open(link)

    def get_source_name(self):
        domain = self.start_urls_textbox.get("1.0", tk.END).strip()
        if domain and domain[-1] == '/':
            domain = domain[:-1]
        name = domain.split('/')[-1].replace('www.', '')
        pyperclip.copy(name)

    @staticmethod
    def get_only_first_value(textbox):
        current_value = textbox.get("1.0", tk.END)
        textbox.delete("1.0", tk.END)
        textbox.insert("1.0", '(' + current_value.strip() + ')[1]')

    def add_regex_for_date(self, regex):
        current_value = self.pubdate_textbox.get("1.0", tk.END)
        self.pubdate_textbox.delete("1.0", tk.END)
        self.pubdate_textbox.insert("1.0", f"re:match({current_value.strip()}, '{regex}', 'g')")

    @staticmethod
    def replace_textbox_value(textbox, value):
        textbox.delete("1.0", tk.END)
        textbox.insert("1.0", value)

    @staticmethod
    def append_textbox_value(textbox, string_to_append):
        current_value = textbox.get("1.0", tk.END).strip()
        textbox.delete("1.0", tk.END)
        textbox.insert("1.0", f"{current_value}{string_to_append}")

    @staticmethod
    def from_textbox_to_textbox(textbox1, textbox2):
        value = textbox1.get('1.0', tk.END).strip()
        pyperclip.copy(value)
        textbox2.delete('1.0', tk.END)
        textbox2.insert('1.0', value)

    def author_substring(self):
        author = self.author_textbox.get("1.0", tk.END).strip()
        self.author_textbox.delete("1.0", tk.END)
        self.author_textbox.insert('1.0', f"substring-after({author},':')")

    def open_start_urls_link(self):
        links = self.start_urls_textbox.get("1.0", tk.END).split(';')
        for link in links:
            webbrowser.get("chrome").open(link)

    def get_domain(self):
        link = self.start_urls_textbox.get("1.0", tk.END).strip()
        if link[-1] != '/':
            link += '/'
        domain = "/".join(link.split('/')[:3]) + '/'
        return domain

    def find_sitemap(self):
        xpath = "(//*[contains(@href, 'site')][contains(@href, 'map')] | //*[contains(@href, 'map')][contains(@href, 'web')])[1]/@href"
        domain = self.get_domain()
        try:
            sitemap_response = requests.get(domain, headers=self.headers)
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

    def open_domain(self):
        try:
            domain = self.get_domain()
        except IndexError:
            print("Invalid URL")
            return
        try:
            self.find_sitemap()
            webbrowser.get("chrome").open(domain)
            req = self.session.get(domain)
            new_url = req.url
            if new_url[-1] != '/':
                new_url += '/'
            self.replace_textbox_value(self.start_urls_textbox, new_url)
        except Exception:
            print(f"Domain could not load - {domain}")
            return

    def clear_all_textboxes(self, kraken_id=True):
        if kraken_id:
            self.kraken_id_textbox.delete("1.0", tk.END)
        self.existing_code_textbox.delete("1.0", tk.END)
        self.start_urls_textbox.delete("1.0", tk.END)
        self.menu_textbox.delete("1.0", tk.END)
        self.articles_textbox.delete("1.0", tk.END)
        self.title_textbox.delete("1.0", tk.END)
        self.pubdate_textbox.delete("1.0", tk.END)
        self.date_order_textbox.delete("1.0", tk.END)
        self.author_textbox.delete("1.0", tk.END)
        self.body_textbox.delete("1.0", tk.END)

    @staticmethod
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

    def not_empty(self):
        return bool(self.start_urls_textbox.get("1.0", tk.END).strip() or
                    self.menu_textbox.get("1.0", tk.END).strip() or
                    self.articles_textbox.get("1.0", tk.END).strip() or
                    self.title_textbox.get("1.0", tk.END).strip() or
                    self.pubdate_textbox.get("1.0", tk.END).strip() or
                    self.date_order_textbox.get("1.0", tk.END).strip() or
                    self.author_textbox.get("1.0", tk.END).strip() or
                    self.body_textbox.get("1.0", tk.END).strip())

    def get_text_from_textbox(self, textbox, xpath_name, json_var):
        if textbox.get("1.0", tk.END).strip():
            # .replace(re.sub(r'\S\|\S'), ' | ')
            xpath = textbox.get("1.0", tk.END).strip().replace('"', "'")
            string_for_remove = ["concat( ' ', ", " ' ' ), concat( ' ', ", ", ' ' )"]
            for s in string_for_remove:
                xpath = xpath.replace(s, '')
            json_var["scrapy_arguments"][xpath_name] = re.sub(r'(\S)\|(\S)', r'\1 | \2', xpath)

        elif xpath_name in json_var["scrapy_arguments"].keys() and self.not_empty():
            json_var["scrapy_arguments"].pop(xpath_name)
        return json_var

    @staticmethod
    def edit_textbox(textbox, xpath_name, json_var):
        textbox.delete("1.0", tk.END)
        if xpath_name in json_var["scrapy_arguments"].keys():
            textbox.insert('1.0', json_var["scrapy_arguments"][xpath_name])

    def default_changes(self, json_var):
        json_var["scrapy_arguments"]["link_id_regex"] = None
        for element in self.first_grid_element_container[2:]:
            self.edit_textbox(element[0], element[1], json_var)

        if "scrapy_settings" in json_var.keys():
            json_var["scrapy_settings"].update(self.settings_json)
        else:
            json_var["scrapy_settings"] = self.settings_json
        return self.sort_json(json_var)

    def fill_code_textbox(self, json_var):
        final_text = json.dumps(json_var, indent=2)
        self.existing_code_textbox.delete("1.0", tk.END)
        self.existing_code_textbox.insert('1.0', final_text)
        return final_text

    @staticmethod
    def rearrange(xpath):
        xpath_list = xpath.split('|')
        for i, entry in enumerate(xpath_list):
            xpath_list[i] = entry.strip()
        xpath_list = sorted(xpath_list)
        xpath = " | ".join(xpath_list)
        return xpath

    def log_to_db(self, kraken_id_db, json_var):
        current_time = datetime.now().strftime("%d-%b-%Y %H:%M:%S")
        user = login_data.user if 'user' in dir(login_data) else "Default User"

        start_urls = self.rearrange(json_var['scrapy_arguments']['start_urls']) if 'start_urls' in json_var['scrapy_arguments'].keys() else ""
        menu_xpath = self.rearrange(json_var['scrapy_arguments']['menu_xpath']) if 'menu_xpath' in json_var['scrapy_arguments'].keys() else ""
        articles_xpath = self.rearrange(json_var['scrapy_arguments']['articles_xpath']) if 'articles_xpath' in json_var[
            'scrapy_arguments'].keys() else ""
        title_xpath = self.rearrange(json_var['scrapy_arguments']['title_xpath']) if 'title_xpath' in json_var['scrapy_arguments'].keys() else ""
        pubdate_xpath = json_var['scrapy_arguments']['pubdate_xpath'] if 'pubdate_xpath' in json_var['scrapy_arguments'].keys() else ""
        date_order = self.rearrange(json_var['scrapy_arguments']['date_order']) if 'date_order' in json_var['scrapy_arguments'].keys() else ""
        author_xpath = self.rearrange(json_var['scrapy_arguments']['author_xpath']) if 'author_xpath' in json_var['scrapy_arguments'].keys() else ""
        body_xpath = self.rearrange(json_var['scrapy_arguments']['body_xpath']) if 'body_xpath' in json_var['scrapy_arguments'].keys() else ""

        self.cur.execute("SELECT id FROM log WHERE id=?", (kraken_id_db,))
        if len(self.cur.fetchall()):
            self.cur.execute(
                "UPDATE log SET date=?, start_urls=?, menu_xpath=?, articles_xpath=?, title_xpath=?, pubdate_xpath=?, date_order=?, author_xpath=?, "
                "body_xpath=?, settings=?, full_json=?, user=? WHERE id=?",
                (current_time, start_urls, menu_xpath, articles_xpath, title_xpath, pubdate_xpath, date_order, author_xpath, body_xpath,
                 str(json_var['scrapy_settings']), str(json_var), user, kraken_id_db))
        else:
            self.cur.execute("INSERT INTO log VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                             (kraken_id_db, current_time, start_urls, menu_xpath, articles_xpath, title_xpath, pubdate_xpath, date_order, author_xpath,
                              body_xpath,
                              str(json_var['scrapy_settings']), str(json_var), user))
        self.con.commit()
        # print(f"Entry {kraken_id_db} entered into database")

    def generate(self, _=None, initial_json=None, load_from_existing_bool=False):
        existing_code = self.existing_code_textbox.get("1.0", tk.END).strip()
        if initial_json:
            json_variable = self.default_changes(initial_json)
            self.fill_code_textbox(json_variable)
            for tup in self.first_grid_element_container[2:]:
                self.edit_textbox(tup[0], tup[1], json_variable)

        elif existing_code:
            try:
                json_variable = json.loads(existing_code)
            except JSONDecodeError:
                print("Invalid JSON")
                return
            if not load_from_existing_bool and self.not_empty():
                for tup in self.first_grid_element_container[2:]:
                    json_variable = self.get_text_from_textbox(tup[0], tup[1], json_variable)
            json_variable = self.default_changes(json_variable)
            final_json = self.fill_code_textbox(json_variable)
            pyperclip.copy(final_json)
            for tup in self.first_grid_element_container[2:]:
                self.edit_textbox(tup[0], tup[1], json_variable)

            if self.kraken_id_textbox.get('1.0', tk.END).strip():
                kraken_id = re.search(r'\d+', self.kraken_id_textbox.get('1.0', tk.END).strip()).group()
                self.log_to_db(kraken_id, json_variable)
                if not os.path.isdir('./logs'):
                    os.mkdir('./logs')
                with open(f'./logs/{kraken_id}.txt', 'w', encoding='utf-8') as f:
                    f.write(final_json)

        elif self.not_empty():
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
            for tup in self.first_grid_element_container[2:]:
                json_variable = self.get_text_from_textbox(tup[0], tup[1], json_variable)
            json_variable = self.default_changes(json_variable)
            final_json = self.fill_code_textbox(json_variable)
            pyperclip.copy(final_json)
            if self.kraken_id_textbox.get('1.0', tk.END).strip():
                kraken_id = re.search(r'\d+', self.kraken_id_textbox.get('1.0', tk.END).strip()).group()
                self.log_to_db(kraken_id, json_variable)
                if not os.path.isdir('./logs'):
                    os.mkdir('./logs')
                with open(f'./logs/{kraken_id}.txt', 'w', encoding='utf-8') as f:
                    f.write(final_json)

        else:
            return

    def fill_found_textboxes(self, tree, column, index_of_container):
        if column == 'menu_xpath':
            self.cur.execute("SELECT menu_xpath, count(menu_xpath) FROM log GROUP BY menu_xpath ORDER BY count(menu_xpath) DESC")
        elif column == 'articles_xpath':
            self.cur.execute("SELECT articles_xpath, count(articles_xpath) FROM log GROUP BY articles_xpath ORDER BY count(articles_xpath) DESC")
        elif column == 'title_xpath':
            self.cur.execute("SELECT title_xpath, count(title_xpath) FROM log GROUP BY title_xpath ORDER BY count(title_xpath) DESC")
        elif column == 'pubdate_xpath':
            self.cur.execute("SELECT pubdate_xpath, count(pubdate_xpath) FROM log GROUP BY pubdate_xpath ORDER BY count(pubdate_xpath) DESC")
        elif column == 'author_xpath':
            self.cur.execute("SELECT author_xpath, count(author_xpath) FROM log GROUP BY author_xpath ORDER BY count(author_xpath) DESC")
        elif column == 'body_xpath':
            self.cur.execute("SELECT body_xpath, count(body_xpath) FROM log GROUP BY body_xpath ORDER BY count(body_xpath) DESC")
        element = self.second_grid_elements_container[index_of_container]
        query_results = self.cur.fetchall()
        xpath_list = []
        for result in query_results:
            xpath_list.append(result[0])
        xpath_list = [x for x in xpath_list if 'substring' not in x and not x.startswith('re') and 're:' not in x and '//' in x]
        if column == 'body_xpath':
            xpath_list = [x for x in xpath_list if '//node()' not in x or '/text()' not in x or ']//p' not in x or "'row'" not in x]
        final_result = []
        if column == 'pubdate_xpath':
            xpath_list.insert(0, self.date_meta)
            print(xpath_list)
        elif column == 'author_xpath':
            if self.author_meta in xpath_list: xpath_list.remove(self.author_meta)
            xpath_list.insert(0, self.author_meta)
        elif column == 'menu_xpath':
            xpath_list.insert(0, self.menu_meta)

        for xpath in xpath_list:
            xpath_to_use = xpath if '@content' in xpath or '@datetime' in xpath or '/text()' in xpath else xpath + '//text()'
            try:
                number_of_results = len(tree.xpath(xpath))
                text_results = tree.xpath(xpath_to_use)
            except Exception:
                continue
            if text_results:
                try:
                    final_result.append({'xpath': xpath, 'result': f"({number_of_results}) - "
                                                                   f"{','.join(x.strip() for x in text_results if isinstance(x, str) and x.strip())}"})
                except Exception:
                    continue
        for i, entry in enumerate(final_result[:5]):
            element[i * 3 + 1].delete('1.0', tk.END)
            element[i * 3 + 1].insert('1.0', entry['xpath'])
            element[i * 3 + 3].delete('1.0', tk.END)
            element[i * 3 + 3].insert('1.0', entry['result'])

    def find_xpath(self):
        for element in self.second_grid_elements_container:
            for widget in element:
                if isinstance(widget, tk.Text):
                    widget.delete('1.0', tk.END)
        article_url = self.article_url_textbox.get("1.0", tk.END).strip()
        website_response = requests.get(article_url, headers=self.headers)
        try:
            print(website_response)
        except Exception:
            print("Website couldn't load")
            return
        tree = html.fromstring(website_response.text)
        self.fill_found_textboxes(tree, 'title_xpath', 0)
        self.fill_found_textboxes(tree, 'pubdate_xpath', 1)
        self.fill_found_textboxes(tree, 'author_xpath', 2)
        self.fill_found_textboxes(tree, 'body_xpath', 3)

    @staticmethod
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

    def exit_handler(self):
        self.con.close()

    def toggle_view(self):
        row = 1
        if self.generate_button.winfo_ismapped():
            # Forget First View
            for element in self.first_grid_element_container:
                for widget in element:
                    if not isinstance(widget, str):
                        widget.grid_forget()
                        self.generate_button.grid_forget()
                        self.clear_button.grid_forget()
            # Load Second View
            self.article_url_label.grid(row=row, column=1, sticky='W', padx=(50, 2), pady=2)
            self.article_url_textbox.grid(row=row, column=2, sticky='W', padx=2, pady=2)
            self.find_xpath_button.grid(row=row, column=3, sticky='W', padx=2, pady=2)
            row += 1
            for element in self.second_grid_elements_container:
                element[0].grid(row=row, column=1, sticky='W', padx=(50, 2), pady=(20, 2))
                start_row = row
                for i, widget in enumerate(element[1:]):
                    curr_row = math.floor(i / 3) + start_row
                    curr_col = (i % 3) + 2
                    if i < 3:
                        widget.grid(row=curr_row, column=curr_col, sticky='W', padx=2, pady=(20, 2))
                    else:
                        widget.grid(row=curr_row, column=curr_col, sticky='W', padx=2, pady=2)
                row += 5
        else:
            # Forget Second View
            self.article_url_label.grid_forget()
            self.article_url_textbox.grid_forget()
            self.find_xpath_button.grid_forget()
            for element in self.second_grid_elements_container:
                for widget in element:
                    widget.grid_forget()
            # Load First View
            for t in self.first_grid_element_container:
                row = self.pack_entries(t, row)

            self.generate_button.grid(row=row, column=1, sticky='W', ipadx=0, ipady=0, pady=(5, 2), padx=(20, 2))
            self.clear_button.grid(row=row, column=2, sticky="E", ipadx=0, ipady=0, pady=2, padx=2)
            row += 1

    @staticmethod
    def pack_entries(entry_tuple, curr_row):
        entry_tuple[2].grid(row=curr_row, column=1, sticky='W', pady=2, padx=(20, 2))
        curr_row += 1
        entry_tuple[0].grid(row=curr_row, column=1, sticky='W', pady=2, padx=(20, 2))
        if len(entry_tuple) > 3:  # if len = 4 or more
            for i in range(3, len(entry_tuple)):
                entry_tuple[i].grid(row=curr_row, column=i - 1, sticky='W', pady=2, padx=2)
        curr_row += 1
        return curr_row

    @staticmethod
    def join_tuple_string(values_tuple) -> str:
        string_list = []
        for element in values_tuple:
            string_list.append(str(element))
        return ', '.join(string_list)

    def write_to_txt(self, column):
        if column == 'menu_xpath':
            self.cur.execute("SELECT menu_xpath, count(menu_xpath) FROM log GROUP BY menu_xpath ORDER BY count(menu_xpath) DESC LIMIT 20")
        elif column == 'articles_xpath':
            self.cur.execute("SELECT articles_xpath, count(articles_xpath) FROM log GROUP BY articles_xpath ORDER BY count(articles_xpath) DESC LIMIT 20")
        elif column == 'title_xpath':
            self.cur.execute("SELECT title_xpath, count(title_xpath) FROM log GROUP BY title_xpath ORDER BY count(title_xpath) DESC LIMIT 20")
        elif column == 'pubdate_xpath':
            self.cur.execute("SELECT pubdate_xpath, count(pubdate_xpath) FROM log GROUP BY pubdate_xpath ORDER BY count(pubdate_xpath) DESC LIMIT 20")
        elif column == 'author_xpath':
            self.cur.execute("SELECT author_xpath, count(author_xpath) FROM log GROUP BY author_xpath ORDER BY count(author_xpath) DESC LIMIT 20")
        elif column == 'body_xpath':
            self.cur.execute("SELECT body_xpath, count(body_xpath) FROM log GROUP BY body_xpath ORDER BY count(body_xpath) DESC LIMIT 20")
        elif column == 'settings':
            self.cur.execute("SELECT settings, count(settings) FROM log GROUP BY settings ORDER BY count(settings) DESC LIMIT 20")
        with open('stats.txt', 'a') as file:
            results = self.cur.fetchall()
            results = list(map(self.join_tuple_string, results))
            file.write(f"{column}:\n")
            file.writelines(line + '\n' for line in results)
            file.write('\n')
            file.close()

    def stats(self):
        with open('stats.txt', 'w') as f:
            f.close()

        columns = ['menu_xpath', 'articles_xpath', 'title_xpath', 'pubdate_xpath', 'author_xpath', 'body_xpath', 'settings']
        for col in columns:
            self.write_to_txt(col)


if __name__ == '__main__':
    app = MainApplication()
    app.mainloop()
