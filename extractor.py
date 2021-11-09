import math
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
from time import time
from datetime import datetime
import atexit
import config
from tkinter.ttk import *
import sys
import urllib3


class MainApplication(tk.Tk):
    def __init__(self):
        t1 = time()

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
        self.kraken_id_label = tk.Label(text="Kraken Link/ID:")
        self.existing_code_label = tk.Label(text="JSON:")
        self.start_urls_label = tk.Label(text="Start URLs:")
        self.menu_label = tk.Label(text="Menu XPath:")
        self.articles_label = tk.Label(text="Articles XPath:")
        self.title_label = tk.Label(text="Title XPath:")
        self.pubdate_label = tk.Label(text="Pubdate XPath:")
        self.date_order_label = tk.Label(text="Date Order XPath:")
        self.author_label = tk.Label(text="Author XPath:")
        self.body_label = tk.Label(text="Body XPath:")
        self.article_url_label = tk.Label(text="URL:")

        self.menu_xpath_found_label = tk.Label(text="Menu XPath:")
        self.articles_xpath_found_label = tk.Label(text="Articles XPath:")
        self.title_xpath_found_label = tk.Label(text="Title XPath:")
        self.pubdate_xpath_found_label = tk.Label(text="Pubdate XPath:")
        self.author_xpath_found_label = tk.Label(text="Author XPath:")
        self.body_xpath_found_label = tk.Label(text="Body XPath:")

        all_labels = [self.existing_code_label, self.kraken_id_label, self.start_urls_label, self.menu_label, self.articles_label, self.title_label,
                      self.pubdate_label, self.date_order_label, self.author_label, self.body_label, self.article_url_label, self.author_xpath_found_label,
                      self.pubdate_xpath_found_label, self.title_xpath_found_label, self.body_xpath_found_label, self.menu_xpath_found_label,
                      self.articles_xpath_found_label]

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

        self.menu_xpath_found_textbox_1 = tk.Text(height=1, width=40)
        self.menu_xpath_found_textbox_2 = tk.Text(height=1, width=40)
        self.menu_xpath_found_textbox_3 = tk.Text(height=1, width=40)
        self.menu_xpath_found_textbox_4 = tk.Text(height=1, width=40)

        self.menu_xpath_result_textbox_1 = tk.Text(height=1, width=40)
        self.menu_xpath_result_textbox_2 = tk.Text(height=1, width=40)
        self.menu_xpath_result_textbox_3 = tk.Text(height=1, width=40)
        self.menu_xpath_result_textbox_4 = tk.Text(height=1, width=40)

        self.articles_xpath_found_textbox_1 = tk.Text(height=1, width=40)
        self.articles_xpath_found_textbox_2 = tk.Text(height=1, width=40)
        self.articles_xpath_found_textbox_3 = tk.Text(height=1, width=40)
        self.articles_xpath_found_textbox_4 = tk.Text(height=1, width=40)

        self.articles_xpath_result_textbox_1 = tk.Text(height=1, width=40)
        self.articles_xpath_result_textbox_2 = tk.Text(height=1, width=40)
        self.articles_xpath_result_textbox_3 = tk.Text(height=1, width=40)
        self.articles_xpath_result_textbox_4 = tk.Text(height=1, width=40)

        self.title_xpath_found_textbox_1 = tk.Text(height=1, width=40)
        self.title_xpath_found_textbox_2 = tk.Text(height=1, width=40)
        self.title_xpath_found_textbox_3 = tk.Text(height=1, width=40)
        self.title_xpath_found_textbox_4 = tk.Text(height=1, width=40)

        self.title_xpath_result_textbox_1 = tk.Text(height=1, width=40)
        self.title_xpath_result_textbox_2 = tk.Text(height=1, width=40)
        self.title_xpath_result_textbox_3 = tk.Text(height=1, width=40)
        self.title_xpath_result_textbox_4 = tk.Text(height=1, width=40)

        self.pubdate_xpath_found_textbox_1 = tk.Text(height=1, width=40)
        self.pubdate_xpath_found_textbox_2 = tk.Text(height=1, width=40)
        self.pubdate_xpath_found_textbox_3 = tk.Text(height=1, width=40)
        self.pubdate_xpath_found_textbox_4 = tk.Text(height=1, width=40)

        self.pubdate_xpath_result_textbox_1 = tk.Text(height=1, width=40)
        self.pubdate_xpath_result_textbox_2 = tk.Text(height=1, width=40)
        self.pubdate_xpath_result_textbox_3 = tk.Text(height=1, width=40)
        self.pubdate_xpath_result_textbox_4 = tk.Text(height=1, width=40)

        self.author_xpath_found_textbox_1 = tk.Text(height=1, width=40)
        self.author_xpath_found_textbox_2 = tk.Text(height=1, width=40)
        self.author_xpath_found_textbox_3 = tk.Text(height=1, width=40)
        self.author_xpath_found_textbox_4 = tk.Text(height=1, width=40)

        self.author_xpath_result_textbox_1 = tk.Text(height=1, width=40)
        self.author_xpath_result_textbox_2 = tk.Text(height=1, width=40)
        self.author_xpath_result_textbox_3 = tk.Text(height=1, width=40)
        self.author_xpath_result_textbox_4 = tk.Text(height=1, width=40)

        self.body_xpath_found_textbox_1 = tk.Text(height=1, width=40)
        self.body_xpath_found_textbox_2 = tk.Text(height=1, width=40)
        self.body_xpath_found_textbox_3 = tk.Text(height=1, width=40)
        self.body_xpath_found_textbox_4 = tk.Text(height=1, width=40)

        self.body_xpath_result_textbox_1 = tk.Text(height=1, width=40)
        self.body_xpath_result_textbox_2 = tk.Text(height=1, width=40)
        self.body_xpath_result_textbox_3 = tk.Text(height=1, width=40)
        self.body_xpath_result_textbox_4 = tk.Text(height=1, width=40)

        self.all_textboxes = [self.article_url_textbox, self.existing_code_textbox, self.start_urls_textbox, self.menu_textbox, self.articles_textbox,
                              self.title_textbox, self.pubdate_textbox, self.date_order_textbox, self.author_textbox, self.body_textbox, self.kraken_id_textbox,
                              self.author_xpath_found_textbox_1, self.author_xpath_found_textbox_2, self.author_xpath_found_textbox_3,
                              self.author_xpath_found_textbox_4, self.author_xpath_result_textbox_1, self.author_xpath_result_textbox_2,
                              self.author_xpath_result_textbox_3, self.author_xpath_result_textbox_4, self.pubdate_xpath_found_textbox_1,
                              self.pubdate_xpath_found_textbox_2, self.pubdate_xpath_found_textbox_3, self.pubdate_xpath_found_textbox_4,
                              self.pubdate_xpath_result_textbox_1, self.pubdate_xpath_result_textbox_2, self.pubdate_xpath_result_textbox_3,
                              self.pubdate_xpath_result_textbox_4, self.title_xpath_found_textbox_1, self.title_xpath_found_textbox_2,
                              self.title_xpath_found_textbox_3, self.title_xpath_found_textbox_4, self.title_xpath_result_textbox_1,
                              self.title_xpath_result_textbox_2, self.title_xpath_result_textbox_3, self.title_xpath_result_textbox_4,
                              self.body_xpath_found_textbox_1, self.body_xpath_found_textbox_2, self.body_xpath_found_textbox_3,
                              self.body_xpath_found_textbox_4, self.body_xpath_result_textbox_1, self.body_xpath_result_textbox_2,
                              self.body_xpath_result_textbox_3, self.body_xpath_result_textbox_4, self.menu_xpath_found_textbox_1,
                              self.menu_xpath_found_textbox_2, self.menu_xpath_found_textbox_3, self.menu_xpath_found_textbox_4,
                              self.menu_xpath_result_textbox_1, self.menu_xpath_result_textbox_2, self.menu_xpath_result_textbox_3,
                              self.menu_xpath_result_textbox_4, self.articles_xpath_found_textbox_1, self.articles_xpath_found_textbox_2,
                              self.articles_xpath_found_textbox_4, self.articles_xpath_result_textbox_1, self.articles_xpath_result_textbox_2,
                              self.articles_xpath_result_textbox_3, self.articles_xpath_result_textbox_4, self.articles_xpath_found_textbox_3]

        for textbox in self.all_textboxes:
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
        self.kraken_id_clipboard_button = Button(text="Clipboard", command=lambda: self.load_code(self.clipboard_get()))
        self.open_source_button = Button(text="Source", command=lambda: self.open_link(self.kraken_id_textbox.get('1.0', tk.END)))
        self.load_from_db_button = Button(text="DB Load", command=self.load_from_db)
        self.open_items_button = Button(text="Items", command=self.open_items_page)
        self.source_name_button = Button(text="Copy Name", command=self.get_source_name)
        self.source_domain_button = Button(text="Copy Domain", command=lambda: self.get_domain(copy=True))
        self.load_from_existing_button = Button(text="Load", command=lambda: self.generate(load_from_existing_bool=True))
        self.title_button_brackets = Button(text="[1]", command=lambda: self.append_textbox_values(self.title_textbox, before_value='(', after_value=')[1]'))
        self.title_h1_button = Button(text="h1", command=lambda: self.replace_textbox_value(self.title_textbox, "//h1[contains(@class,'title')]"))
        self.pubdate_button_brackets = Button(text="[1]", command=lambda: self.append_textbox_values(self.pubdate_textbox, before_value='(',
                                                                                                     after_value=')[1]'))
        self.author_button_brackets = Button(text="[1]", command=lambda: self.append_textbox_values(self.author_textbox, before_value='(', after_value=')[1]'))
        self.body_button_brackets = Button(text="[1]", command=lambda: self.append_textbox_values(self.body_textbox, before_value='(', after_value=')[1]'), )
        self.regex_dmy_button = Button(text="Regex .", command=lambda: self.append_textbox_values(self.pubdate_textbox, before_value="re:match(",
                                                                                                  after_value=r", '\d{1,2}\.\d{1,2}\.\d{2,4}', 'g')"))
        self.regex_ymd_button = Button(text="Regex Text", command=lambda: self.append_textbox_values(self.pubdate_textbox, before_value="re:match(",
                                                                                                     after_value=r", '(\d{1,2})\.(\s\w+\s\d{2,4})', 'g')"))
        self.menu_default_button = Button(text="Default", command=lambda: self.replace_textbox_value(self.menu_textbox,
                                                                                                     "(//ul[contains(@class, 'menu')] |"
                                                                                                     " //ul[contains(@id, 'menu')] | //nav//ul)[1]//a"))
        self.menu_category_button = Button(text="Cat", command=lambda: self.append_textbox_values(self.menu_textbox, after_value="[contains(@href, 'ategor')]"))
        self.article_category_button = Button(text="Not Cat", command=lambda: self.append_textbox_values(self.articles_textbox, before_value='(',
                                                                                                         after_value=")[not(contains(@href, 'ategor'))]"))
        self.article_title_button = Button(text="Cont Title", command=lambda: self.replace_textbox_value(self.articles_textbox,
                                                                                                         "//*[contains(@class,'title')]/a"))
        self.meta_button = Button(text="Meta", command=lambda: self.replace_textbox_value(self.pubdate_textbox, self.date_meta))
        self.date_order_DMY = Button(text="DMY", command=lambda: self.replace_textbox_value(self.date_order_textbox, "DMY"))
        self.date_order_YMD = Button(text="YMD", command=lambda: self.replace_textbox_value(self.date_order_textbox, "YMD"))
        self.date_order_MDY = Button(text="MDY", command=lambda: self.replace_textbox_value(self.date_order_textbox, "MDY"))
        self.author_substring_button = Button(text="Substring", command=lambda: self.append_textbox_values(self.author_textbox, before_value="substring-after(",
                                                                                                           after_value=", ':')"))
        self.author_meta_button = Button(text="Meta", command=lambda: self.replace_textbox_value(self.author_textbox, "//meta[contains(@*,'uthor')]/@content"))
        self.author_child_text_button = Button(text="Child", command=lambda: self.replace_textbox_value(self.author_textbox,
                                                                                                        '//*[child::text()[contains(.,"Autor")]]'))
        self.body_contains_class_button = Button(text="Content",
                                                 command=lambda: self.replace_textbox_value(self.body_textbox, "//div[contains(@class, 'content')]"))
        self.not_contains_class_button = Button(text="Not Class",
                                                command=lambda: self.append_textbox_values(self.body_textbox,
                                                                                           after_value=f"[not(contains(@class, "
                                                                                                       f"'{self.clipboard_get().strip()}'))]"))
        self.not_contains_text_button = Button(text="Not Text",
                                               command=lambda: self.append_textbox_values(self.body_textbox,
                                                                                          after_value=f"[not(descendant::text()"
                                                                                                      f"[contains(.,'{self.clipboard_get().strip()}')])]"))
        self.open_link_button = Button(text='Open Link', command=self.open_start_urls_link)
        self.open_domain_button = Button(text='Open Domain', command=self.open_domain)
        self.clear_button = Button(text="Clear All", command=self.clear_all_textboxes)
        self.generate_button = Button(text="Generate JSON!", command=self.generate, master=self)

        # Second View
        self.find_menu_articles_button = Button(text="Menu/Articles", command=self.find_menu_articles, master=self)
        self.find_content_button = Button(text="Content", command=self.find_content, master=self)
        self.menu_xpath_select_button_1 = Button(text="Select", command=lambda: self.from_textbox_to_textbox(self.menu_xpath_found_textbox_1,
                                                                                                             self.menu_textbox))
        self.menu_xpath_select_button_2 = Button(text="Select", command=lambda: self.from_textbox_to_textbox(self.menu_xpath_found_textbox_2,
                                                                                                             self.menu_textbox))
        self.menu_xpath_select_button_3 = Button(text="Select", command=lambda: self.from_textbox_to_textbox(self.menu_xpath_found_textbox_3,
                                                                                                             self.menu_textbox))
        self.menu_xpath_select_button_4 = Button(text="Select", command=lambda: self.from_textbox_to_textbox(self.menu_xpath_found_textbox_4,
                                                                                                             self.menu_textbox))

        self.articles_xpath_select_button_1 = Button(text="Add", command=lambda: self.from_textbox_to_textbox(
            self.articles_xpath_found_textbox_1,
            self.articles_textbox,
            append_with_pipe=True))
        self.articles_xpath_select_button_2 = Button(text="Add", command=lambda: self.from_textbox_to_textbox(
            self.articles_xpath_found_textbox_2,
            self.articles_textbox,
            append_with_pipe=True))
        self.articles_xpath_select_button_3 = Button(text="Add", command=lambda: self.from_textbox_to_textbox(
            self.articles_xpath_found_textbox_3,
            self.articles_textbox,
            append_with_pipe=True))
        self.articles_xpath_select_button_4 = Button(text="Add", command=lambda: self.from_textbox_to_textbox(
            self.articles_xpath_found_textbox_4,
            self.articles_textbox,
            append_with_pipe=True))

        self.title_xpath_select_button_1 = Button(text="Select", command=lambda: self.from_textbox_to_textbox(self.title_xpath_found_textbox_1,
                                                                                                              self.title_textbox))
        self.title_xpath_select_button_2 = Button(text="Select", command=lambda: self.from_textbox_to_textbox(self.title_xpath_found_textbox_2,
                                                                                                              self.title_textbox))
        self.title_xpath_select_button_3 = Button(text="Select", command=lambda: self.from_textbox_to_textbox(self.title_xpath_found_textbox_3,
                                                                                                              self.title_textbox))
        self.title_xpath_select_button_4 = Button(text="Select", command=lambda: self.from_textbox_to_textbox(self.title_xpath_found_textbox_4,
                                                                                                              self.title_textbox))

        self.pubdate_xpath_select_button_1 = Button(text="Select", command=lambda: self.from_textbox_to_textbox(self.pubdate_xpath_found_textbox_1,
                                                                                                                self.pubdate_textbox))
        self.pubdate_xpath_select_button_2 = Button(text="Select", command=lambda: self.from_textbox_to_textbox(self.pubdate_xpath_found_textbox_2,
                                                                                                                self.pubdate_textbox))
        self.pubdate_xpath_select_button_3 = Button(text="Select", command=lambda: self.from_textbox_to_textbox(self.pubdate_xpath_found_textbox_3,
                                                                                                                self.pubdate_textbox))
        self.pubdate_xpath_select_button_4 = Button(text="Select", command=lambda: self.from_textbox_to_textbox(self.pubdate_xpath_found_textbox_4,
                                                                                                                self.pubdate_textbox))

        self.author_xpath_select_button_1 = Button(text="Select", command=lambda: self.from_textbox_to_textbox(self.author_xpath_found_textbox_1,
                                                                                                               self.author_textbox))
        self.author_xpath_select_button_2 = Button(text="Select", command=lambda: self.from_textbox_to_textbox(self.author_xpath_found_textbox_2,
                                                                                                               self.author_textbox))
        self.author_xpath_select_button_3 = Button(text="Select", command=lambda: self.from_textbox_to_textbox(self.author_xpath_found_textbox_3,
                                                                                                               self.author_textbox))
        self.author_xpath_select_button_4 = Button(text="Select", command=lambda: self.from_textbox_to_textbox(self.author_xpath_found_textbox_4,
                                                                                                               self.author_textbox))

        self.body_xpath_select_button_1 = Button(text="Select", command=lambda: self.from_textbox_to_textbox(self.body_xpath_found_textbox_1,
                                                                                                             self.body_textbox))
        self.body_xpath_select_button_2 = Button(text="Select", command=lambda: self.from_textbox_to_textbox(self.body_xpath_found_textbox_2,
                                                                                                             self.body_textbox))
        self.body_xpath_select_button_3 = Button(text="Select", command=lambda: self.from_textbox_to_textbox(self.body_xpath_found_textbox_3,
                                                                                                             self.body_textbox))
        self.body_xpath_select_button_4 = Button(text="Select", command=lambda: self.from_textbox_to_textbox(self.body_xpath_found_textbox_4,
                                                                                                             self.body_textbox))

        self.toggle_view_button = Button(text="Switch Views", command=self.toggle_view)

        self.first_grid_element_container = [
            (self.kraken_id_textbox, "kraken_link", self.kraken_id_label, self.kraken_id_load_button, self.kraken_id_clipboard_button,
             self.open_source_button, self.load_from_db_button, self.open_items_button),
            (self.existing_code_textbox, "existing_code", self.existing_code_label, self.code_copy_button, self.load_from_existing_button),
            (self.start_urls_textbox, "start_urls", self.start_urls_label, self.copy_start_button, self.open_link_button, self.open_domain_button,
             self.source_name_button, self.source_domain_button),
            (self.menu_textbox, "menu_xpath", self.menu_label, self.copy_menu_button, self.menu_default_button, self.menu_category_button),
            (self.articles_textbox, "articles_xpath", self.articles_label, self.copy_articles_button, self.article_title_button, self.article_category_button),
            (self.title_textbox, "title_xpath", self.title_label, self.copy_title_button, self.title_h1_button, self.title_button_brackets),
            (self.pubdate_textbox, "pubdate_xpath", self.pubdate_label, self.copy_pubdate_button, self.meta_button, self.regex_dmy_button,
             self.regex_ymd_button, self.pubdate_button_brackets),
            (self.date_order_textbox, "date_order", self.date_order_label, self.date_order_DMY, self.date_order_YMD, self.date_order_MDY),
            (self.author_textbox, "author_xpath", self.author_label, self.copy_author_button, self.author_meta_button, self.author_substring_button,
             self.author_child_text_button, self.author_button_brackets),
            (self.body_textbox, "body_xpath", self.body_label, self.copy_body_button, self.body_contains_class_button, self.not_contains_class_button,
             self.not_contains_text_button, self.body_button_brackets)]

        self.second_grid_elements_container = [
            (self.menu_xpath_found_label, self.menu_xpath_found_textbox_1, self.menu_xpath_select_button_1, self.menu_xpath_result_textbox_1,
             self.menu_xpath_found_textbox_2, self.menu_xpath_select_button_2, self.menu_xpath_result_textbox_2,
             self.menu_xpath_found_textbox_3, self.menu_xpath_select_button_3, self.menu_xpath_result_textbox_3,
             self.menu_xpath_found_textbox_4, self.menu_xpath_select_button_4, self.menu_xpath_result_textbox_4),
            (self.articles_xpath_found_label, self.articles_xpath_found_textbox_1, self.articles_xpath_select_button_1, self.articles_xpath_result_textbox_1,
             self.articles_xpath_found_textbox_2, self.articles_xpath_select_button_2, self.articles_xpath_result_textbox_2,
             self.articles_xpath_found_textbox_3, self.articles_xpath_select_button_3, self.articles_xpath_result_textbox_3,
             self.articles_xpath_found_textbox_4, self.articles_xpath_select_button_4, self.articles_xpath_result_textbox_4),
            (self.title_xpath_found_label, self.title_xpath_found_textbox_1, self.title_xpath_select_button_1, self.title_xpath_result_textbox_1,
             self.title_xpath_found_textbox_2, self.title_xpath_select_button_2, self.title_xpath_result_textbox_2,
             self.title_xpath_found_textbox_3, self.title_xpath_select_button_3, self.title_xpath_result_textbox_3,
             self.title_xpath_found_textbox_4, self.title_xpath_select_button_4, self.title_xpath_result_textbox_4),
            (self.pubdate_xpath_found_label, self.pubdate_xpath_found_textbox_1, self.pubdate_xpath_select_button_1, self.pubdate_xpath_result_textbox_1,
             self.pubdate_xpath_found_textbox_2, self.pubdate_xpath_select_button_2, self.pubdate_xpath_result_textbox_2,
             self.pubdate_xpath_found_textbox_3, self.pubdate_xpath_select_button_3, self.pubdate_xpath_result_textbox_3,
             self.pubdate_xpath_found_textbox_4, self.pubdate_xpath_select_button_4, self.pubdate_xpath_result_textbox_4),
            (self.author_xpath_found_label, self.author_xpath_found_textbox_1, self.author_xpath_select_button_1, self.author_xpath_result_textbox_1,
             self.author_xpath_found_textbox_2, self.author_xpath_select_button_2, self.author_xpath_result_textbox_2,
             self.author_xpath_found_textbox_3, self.author_xpath_select_button_3, self.author_xpath_result_textbox_3,
             self.author_xpath_found_textbox_4, self.author_xpath_select_button_4, self.author_xpath_result_textbox_4),
            (self.body_xpath_found_label, self.body_xpath_found_textbox_1, self.body_xpath_select_button_1, self.body_xpath_result_textbox_1,
             self.body_xpath_found_textbox_2, self.body_xpath_select_button_2, self.body_xpath_result_textbox_2,
             self.body_xpath_found_textbox_3, self.body_xpath_select_button_3, self.body_xpath_result_textbox_3,
             self.body_xpath_found_textbox_4, self.body_xpath_select_button_4, self.body_xpath_result_textbox_4)]

        self.session = requests.Session()
        with open('settings.json') as f1:
            self.settings_json = json.load(f1)
        self.kraken_id = ""

        self.shared_db_path = r'\\VT10\xpath_manager\log.db'
        self.local_db_path = 'log.db'

        try:
            con = sqlite3.connect(self.shared_db_path)
            shared_connection = True
            print("Using shared database.")
        except sqlite3.OperationalError:
            con = sqlite3.connect(self.local_db_path)
            shared_connection = False
            print("Using local database.")

        self.create_tables(con)

        if shared_connection and len(sys.argv) > 1 and list(sys.argv)[1] == 'sync':
            print("Syncing..")
            synced_entries = 0
            cur = con.cursor()
            local_con = sqlite3.connect(self.local_db_path)
            self.create_tables(local_con)
            local_cur = local_con.cursor()
            local_cur.execute("SELECT * FROM log")
            local_entries = local_cur.fetchall()
            for entry in local_entries:
                cur.execute("SELECT * FROM log WHERE id=?", (entry[0],))
                if not cur.fetchall():
                    cur.execute("INSERT INTO log VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", entry)
                    synced_entries += 1
            if synced_entries:
                print(f'Added {synced_entries} log(s) to shared database.')
            local_con.commit()
            local_con.close()

        con.commit()
        con.close()

        self.stats()

        login_link = "https://dashbeta.aiidatapro.net/"

        self.headers = {'Connection': 'close', 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0'}
        session_headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/67.0.3396.99 Safari/537.36'
        }

        if not os.path.exists('./login_data.py'):
            with open('login_data.py', 'w') as login_file:
                login_file.write('username = "USERNAME_HERE"\npassword = "PASSWORD_HERE"\nuser="Default"')
                print("Fill in your login details in login_data.py!")
        else:
            try:
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
            except Exception:
                print("Couldn't login")

        chrome_path = 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
        webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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

        row = 1
        self.article_url_label.grid(row=row, column=1, sticky='W', padx=(50, 2), pady=2)
        self.article_url_textbox.grid(row=row, column=2, sticky='W', padx=2, pady=2)
        self.find_menu_articles_button.grid(row=row, column=3, sticky='W', padx=2, pady=2)
        self.find_content_button.grid(row=row, column=4, sticky='W', padx=2, pady=2)
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

        # Forget Second View
        self.article_url_label.grid_remove()
        self.article_url_textbox.grid_remove()
        self.find_content_button.grid_remove()
        self.find_menu_articles_button.grid_remove()
        for element in self.second_grid_elements_container:
            for widget in element:
                widget.grid_remove()
        row += 1

        atexit.register(self.exit_handler)
        width = 960
        height = 1080
        width_screen = self.winfo_screenwidth()
        if config.side_of_window == "r":
            starting_width = width_screen - width - 6
        else:
            starting_width = 0
        starting_height = 0
        self.geometry('%dx%d+%d+%d' % (width, height, starting_width, starting_height))
        self.bind_all("<Key>", self.on_key_release, "+")
        self.lift()
        t2 = time()
        print(f"Booted in {t2 - t1} seconds.")

    def initiate_connection(self):
        try:
            con = sqlite3.connect(self.shared_db_path)
        except sqlite3.OperationalError:
            con = sqlite3.connect(self.local_db_path)
        return con

    @staticmethod
    def create_tables(con):
        cur = con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS log
                       (id text, date text, start_urls text, menu_xpath text, articles_xpath text, title_xpath text, 
                       pubdate_xpath text, date_order text, author_xpath text, body_xpath text, settings text, 
                       full_json text, user text)''')
        cur.execute('''CREATE TABLE IF NOT EXISTS menu_xpath(xpath text, count number)''')
        cur.execute('''CREATE TABLE IF NOT EXISTS articles_xpath(xpath text, count number)''')
        cur.execute('''CREATE TABLE IF NOT EXISTS title_xpath(xpath text, count number)''')
        cur.execute('''CREATE TABLE IF NOT EXISTS pubdate_xpath(xpath text, count number)''')
        cur.execute('''CREATE TABLE IF NOT EXISTS author_xpath(xpath text, count number)''')
        cur.execute('''CREATE TABLE IF NOT EXISTS body_xpath(xpath text, count number)''')

    @staticmethod
    def copy_code(textbox):
        """
        Desc: Function for the button to copy a text fields
        :param textbox: Textbox whose text should be copied to clipboard
        :return:
        """
        value_to_copy = textbox.get("1.0", tk.END).strip()
        if value_to_copy:
            pyperclip.copy(value_to_copy)

    def set_kraken_id(self, kraken_id="", unset=False):
        if kraken_id:
            self.kraken_id = kraken_id
            self.title(f"{kraken_id} - {self.window_title}")
        elif unset:
            self.kraken_id = ""
            self.title(self.window_title)
        else:
            if self.kraken_id_textbox.get('1.0', tk.END).strip():
                try:
                    self.kraken_id = re.findall(r'\d+', self.kraken_id_textbox.get('1.0', tk.END).strip())[-1]
                except IndexError:
                    print("No ID found")
                    return
                print(self.kraken_id)
                self.title(f"{self.kraken_id} - {self.window_title}")
            else:
                self.kraken_id = ""
                self.title(self.window_title)

    def get_link(self):
        """
        Function to correctly format the Kraken link by searching for the ID in the URL
        :return: The correctly formatted link
        """
        self.set_kraken_id()
        if self.kraken_id:
            link = f"http://kraken.aiidatapro.net/items/edit/{self.kraken_id}/"
            return link
        else:
            return ""

    def load_code(self, link, open_source_bool=True):
        """
        Function to fill the extractor with the JSON from Kraken
        :param link: Kraken link / ID
        :param open_source_bool: Bool indicating whether the source link should be opened in a browser tab
        :return:
        """
        self.clear_all_textboxes()
        self.kraken_id_textbox.delete('1.0', tk.END)
        self.kraken_id_textbox.insert('1.0', link)
        link = self.get_link()  # Format link
        if not link:
            print("No ID found")
            return
        if open_source_bool:
            webbrowser.get("chrome").open(link)

        # Show correctly formatted link in textbox
        self.kraken_id_textbox.delete('1.0', tk.END)
        self.kraken_id_textbox.insert('1.0', link)

        # Extract Xpath from Kraken page
        xpath = "//input[@name='feed_properties']/@value"
        link = link.strip()
        try:
            kraken_response = self.session.get(link)
        except Exception:
            print("Couldn't access Kraken")
            return
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
        if link.strip():
            webbrowser.get("chrome").open(link)

    def load_from_db(self):
        """
        Extracts ID from Kraken Textbox and loads the source from the database
        :return:
        """

        con = self.initiate_connection()
        cur = con.cursor()

        if self.kraken_id_textbox.get('1.0', tk.END).strip():
            kraken_id = re.search(r'\d+', self.kraken_id_textbox.get('1.0', tk.END)).group()
        else:
            return
        cur.execute('SELECT * FROM log WHERE id=?', (kraken_id,))
        result = cur.fetchone()
        if result:
            self.set_kraken_id(kraken_id)
            settings = result[10].replace("'", '"').replace("False", '"False"').replace("True",
                                                                                        '"True"')  # Format Bool Values to not crash JSON
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

        con.commit()
        con.close()

    def open_items_page(self):
        # Function to open the "View Item" page of the source in Kraken
        if self.kraken_id_textbox.get('1.0', tk.END).strip():
            link = self.get_link().replace('/edit', '')
            webbrowser.get("chrome").open(link)
        else:
            return

    def get_source_name(self):
        domain = self.start_urls_textbox.get("1.0", tk.END).strip()
        if domain and domain[-1] == '/':
            domain = domain[:-1]
        try:
            name = domain.split('//')[1].split('/')[0].replace('www.', '')
        except IndexError:
            return
        if name:
            pyperclip.copy(name)

    @staticmethod
    def append_textbox_values(textbox, before_value="", after_value=""):
        current_value = textbox.get("1.0", tk.END)
        textbox.delete("1.0", tk.END)
        textbox.insert("1.0", f'{before_value.strip()}{current_value.strip()}{after_value.strip()}')

    @staticmethod
    def replace_textbox_value(textbox, value):
        textbox.delete("1.0", tk.END)
        textbox.insert("1.0", value)

    @staticmethod
    def from_textbox_to_textbox(textbox1, textbox2, append_with_pipe=False):
        value = textbox1.get('1.0', tk.END).strip()
        if not value:
            return
        pyperclip.copy(value)
        if append_with_pipe:
            initial_value = textbox2.get('1.0', tk.END).strip()
            if initial_value:
                textbox2.delete('1.0', tk.END)
                textbox2.insert('1.0', f"{initial_value} | {value}")
            else:
                textbox2.insert('1.0', value)
        else:
            textbox2.delete('1.0', tk.END)
            textbox2.insert('1.0', value)

    def open_start_urls_link(self):
        links = self.start_urls_textbox.get("1.0", tk.END).split(';')
        if links:
            for link in links:
                link = link.strip()
                link = link if link.endswith('/') else link + '/'
                webbrowser.get("chrome").open(link)

    def get_domain(self, copy=False):
        link = self.start_urls_textbox.get("1.0", tk.END).strip()
        if not link.startswith('http'):
            link = 'http://' + link
        domain = "/".join(link.split('/')[:3]) + '/'
        if copy:
            pyperclip.copy(domain)
        else:
            return domain

    def find_sitemap(self):
        xpath = "(//*[contains(@href, 'site')][contains(@href, 'map')] | //*[contains(@href, 'map')][contains(@href, 'web')])[1]/@href"
        domain = self.get_domain()
        try:
            sitemap_response = requests.get(domain, headers=self.headers, verify=False)
            tree = html.fromstring(sitemap_response.text)
            sitemap = tree.xpath(xpath)
            if sitemap:
                sitemap_link = sitemap[0]
                if 'http' not in sitemap[0]:
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

            webbrowser.get("chrome").open(domain)
            req = requests.get(domain, headers=self.headers, verify=False)
            new_url = req.url
            if new_url[-1] != '/':
                new_url += '/'
            self.find_sitemap()
            self.replace_textbox_value(self.start_urls_textbox, new_url)
        except Exception:
            print(f"Domain could not load - {domain}")
            return

    def clear_all_textboxes(self):
        self.set_kraken_id(unset=True)
        for textbox in self.all_textboxes:
            textbox.delete("1.0", tk.END)

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

    def log_code(self, json_dict):
        if self.kraken_id:
            self.log_to_db(json_dict)
        elif self.kraken_id_textbox.get('1.0', tk.END).strip():
            self.set_kraken_id()
            self.log_to_db(json_dict)
        else:
            print("No ID found, logging skipped")
            return

    def log_to_db(self, json_var):
        con = self.initiate_connection()
        cur = con.cursor()

        current_time = datetime.now().strftime("%d-%b-%Y %H:%M:%S")
        user = login_data.user if 'user' in dir(login_data) else "Default User"

        start_urls = json_var['scrapy_arguments']['start_urls'] if 'start_urls' in json_var['scrapy_arguments'].keys() else ""
        menu_xpath = json_var['scrapy_arguments']['menu_xpath'] if 'menu_xpath' in json_var['scrapy_arguments'].keys() else ""
        articles_xpath = json_var['scrapy_arguments']['articles_xpath'] if 'articles_xpath' in json_var[
            'scrapy_arguments'].keys() else ""
        title_xpath = json_var['scrapy_arguments']['title_xpath'] if 'title_xpath' in json_var['scrapy_arguments'].keys() else ""
        pubdate_xpath = json_var['scrapy_arguments']['pubdate_xpath'] if 'pubdate_xpath' in json_var['scrapy_arguments'].keys() else ""
        date_order = json_var['scrapy_arguments']['date_order'] if 'date_order' in json_var['scrapy_arguments'].keys() else ""
        author_xpath = json_var['scrapy_arguments']['author_xpath'] if 'author_xpath' in json_var['scrapy_arguments'].keys() else ""
        body_xpath = json_var['scrapy_arguments']['body_xpath'] if 'body_xpath' in json_var['scrapy_arguments'].keys() else ""

        cur.execute("SELECT id FROM log WHERE id=?", (self.kraken_id,))
        if len(cur.fetchall()):
            print(f"Updated Source {self.kraken_id}")
            cur.execute(
                "UPDATE log SET date=?, start_urls=?, menu_xpath=?, articles_xpath=?, title_xpath=?, pubdate_xpath=?, date_order=?, author_xpath=?, "
                "body_xpath=?, settings=?, full_json=?, user=? WHERE id=?",
                (current_time, start_urls, menu_xpath, articles_xpath, title_xpath, pubdate_xpath, date_order, author_xpath, body_xpath,
                 str(json_var['scrapy_settings']), str(json_var), user, self.kraken_id))
        else:
            print(f"Adding Source {self.kraken_id}")
            cur.execute("INSERT INTO log VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (self.kraken_id, current_time, start_urls, menu_xpath, articles_xpath, title_xpath, pubdate_xpath, date_order, author_xpath,
                         body_xpath,
                         str(json_var['scrapy_settings']), str(json_var), user))
        con.commit()
        con.close()

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

            self.log_code(json_variable)

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
            self.log_code(json_variable)
        else:
            return

    def fill_found_textboxes(self, tree, column, index_of_container):

        con = self.initiate_connection()
        cur = con.cursor()

        if column == 'menu_xpath':
            cur.execute("SELECT xpath, count FROM menu_xpath ORDER BY count DESC")
        elif column == 'articles_xpath':
            cur.execute("SELECT xpath FROM articles_xpath ORDER BY count DESC")
        elif column == 'title_xpath':
            cur.execute("SELECT xpath FROM title_xpath ORDER BY count DESC")
        elif column == 'pubdate_xpath':
            cur.execute("SELECT xpath FROM pubdate_xpath ORDER BY count DESC")
        elif column == 'author_xpath':
            cur.execute("SELECT xpath FROM author_xpath ORDER BY count DESC")
        elif column == 'body_xpath':
            cur.execute("SELECT xpath FROM body_xpath ORDER BY count DESC")
        element = self.second_grid_elements_container[index_of_container]
        xpath_list = cur.fetchall()
        xpath_list = [x[0] for x in xpath_list]

        con.commit()
        con.close()

        final_result = []
        number_of_textboxes = 4
        for xpath in xpath_list:
            xpath_to_use = xpath if '@content' in xpath or '@datetime' in xpath or '/text()' in xpath else xpath + '//text()'
            try:
                number_of_results = len(tree.xpath(xpath))
                text_results = tree.xpath(xpath_to_use)
            except Exception:
                continue

            try:
                if number_of_results:
                    dict_to_append = {'xpath': xpath, 'result': f"({number_of_results}) - "
                                                                f"{','.join(x.strip() for x in text_results if isinstance(x, str) and x.strip())}"}
                    if dict_to_append['result'] not in [x['result'] for x in final_result]:
                        final_result.append(dict_to_append)
                        if len(final_result) == number_of_textboxes:
                            break
            except Exception:
                continue

        # final_result = sorted(final_result, key=lambda d: d['result'])
        for i, entry in enumerate(final_result):
            element[i * 3 + 1].delete('1.0', tk.END)
            element[i * 3 + 1].insert('1.0', entry['xpath'])
            element[i * 3 + 3].delete('1.0', tk.END)
            element[i * 3 + 3].insert('1.0', entry['result'])

    def find_content(self):
        for element in self.second_grid_elements_container[2:]:
            for widget in element:
                if isinstance(widget, tk.Text):
                    widget.delete('1.0', tk.END)
        article_url = self.article_url_textbox.get("1.0", tk.END).strip()
        website_response = requests.get(article_url, headers=self.headers, verify=False)
        tree = html.fromstring(website_response.text)
        self.fill_found_textboxes(tree, 'title_xpath', 2)
        self.fill_found_textboxes(tree, 'pubdate_xpath', 3)
        self.fill_found_textboxes(tree, 'author_xpath', 4)
        self.fill_found_textboxes(tree, 'body_xpath', 5)

    def find_menu_articles(self):
        for element in self.second_grid_elements_container[:2]:
            for widget in element:
                if isinstance(widget, tk.Text):
                    widget.delete('1.0', tk.END)
        article_url = self.article_url_textbox.get("1.0", tk.END).strip()
        website_response = requests.get(article_url, headers=self.headers, verify=False)
        tree = html.fromstring(website_response.text)
        self.fill_found_textboxes(tree, 'menu_xpath', 0)
        self.fill_found_textboxes(tree, 'articles_xpath', 1)

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
        pass

    def toggle_view(self):
        if self.generate_button.winfo_ismapped():
            # Forget First View
            for element in self.first_grid_element_container:
                for widget in element:
                    if not isinstance(widget, str):
                        widget.grid_remove()
            self.generate_button.grid_remove()
            self.clear_button.grid_remove()

            # Load Second View
            self.article_url_label.grid()
            self.article_url_textbox.grid()
            self.find_menu_articles_button.grid()
            self.find_content_button.grid()
            for element in self.second_grid_elements_container:
                for widget in element:
                    widget.grid()

        else:
            # Forget Second View
            self.article_url_label.grid_remove()
            self.article_url_textbox.grid_remove()
            self.find_content_button.grid_remove()
            self.find_menu_articles_button.grid_remove()
            for element in self.second_grid_elements_container:
                for widget in element:
                    widget.grid_remove()

            # Load First View
            for element in self.first_grid_element_container:
                for widget in element:
                    if not isinstance(widget, str):
                        widget.grid()
            self.generate_button.grid()
            self.clear_button.grid()

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

    def stats(self):
        def create_dict(db_results, body_xpath=False):
            db_results = [x[0] for x in db_results if x[0]]
            updated_list = []
            all_contains = ['substring', 're.', 're:']
            body_contains = ['//node()', '/text()', ']//p', "'row'", "//div[contains(@class,'content')", '::img', '//article', '//figure/', '//main',
                             '//figcaption', "//div[contains(@class,'-content')]", '//section/']

            for xpath in db_results:
                split_xpath_list = xpath.split('|')
                for updated_xpath in split_xpath_list:
                    updated_xpath = updated_xpath.replace(' ', '')
                    if updated_xpath.endswith('/'):
                        updated_xpath = updated_xpath[:-1]
                    if not any(s in updated_xpath for s in all_contains):
                        if body_xpath:
                            if updated_xpath.endswith('/p'):
                                updated_xpath = updated_xpath[:-2]
                            if '/node()' in updated_xpath:
                                updated_xpath = updated_xpath.split('/node()')[0]
                            if not any(s in updated_xpath for s in body_contains):
                                updated_list.append(updated_xpath.strip())
                        else:
                            updated_list.append(updated_xpath.strip())

            created_dict = dict()
            for i in updated_list:
                created_dict[i] = created_dict.get(i, 0) + 1

            return sorted(created_dict.items(), key=lambda d: d[1], reverse=True)

        con = self.initiate_connection()
        cur = con.cursor()

        cur.execute("SELECT * FROM log")
        print(f"Hello, {login_data.user}")
        print(f"The database contains {len(cur.fetchall())} entries.")
        cur.execute("DELETE FROM menu_xpath")
        cur.execute("DELETE FROM articles_xpath")
        cur.execute("DELETE FROM title_xpath")
        cur.execute("DELETE FROM pubdate_xpath")
        cur.execute("DELETE FROM author_xpath")
        cur.execute("DELETE FROM body_xpath")

        cur.execute("SELECT menu_xpath FROM log")
        results = create_dict(cur.fetchall())
        for entry in results:
            cur.execute("INSERT INTO menu_xpath VALUES (?, ?)", (entry[0], entry[1]))

        cur.execute("SELECT articles_xpath FROM log")
        results = create_dict(cur.fetchall())
        for entry in results:
            cur.execute("INSERT INTO articles_xpath VALUES (?, ?)", (entry[0], entry[1]))

        cur.execute("SELECT title_xpath FROM log")
        results = create_dict(cur.fetchall())
        for entry in results:
            cur.execute("INSERT INTO title_xpath VALUES (?, ?)", (entry[0], entry[1]))

        cur.execute("SELECT pubdate_xpath FROM log")
        results = create_dict(cur.fetchall())
        for entry in results:
            cur.execute("INSERT INTO pubdate_xpath VALUES (?, ?)", (entry[0], entry[1]))

        cur.execute("SELECT author_xpath FROM log")
        results = create_dict(cur.fetchall())
        for entry in results:
            cur.execute("INSERT INTO author_xpath VALUES (?, ?)", (entry[0], entry[1]))

        cur.execute("SELECT body_xpath FROM log")
        results = create_dict(cur.fetchall(), body_xpath=True)
        for entry in results:
            cur.execute("INSERT INTO body_xpath VALUES (?, ?)", (entry[0], entry[1]))

        con.commit()
        con.close()


if __name__ == '__main__':
    app = MainApplication()
    app.mainloop()
