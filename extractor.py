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
from time import time
from datetime import datetime
import atexit
import config
from tkinter.ttk import *
import sys
import urllib3
from typing import Union
from custom_widgets import MyText, MyLabel, MyFrame, MyButton, MyCheckbutton


class MainApplication(tk.Tk):
    def __init__(self):
        t1 = time()

        super().__init__()
        print(config.user_agent)
        self.window_title = f"Xpath Extractor ({config.last_change})"
        self.title(self.window_title)
        self.set_word_boundaries()
        self.background = 'dark grey'
        self.configure(background=self.background)
        self.current_view = 'extractor'
        self.frame_style = Style()
        self.frame_style.configure('TFrame', background=self.background)
        self.checkbutton_style = Style()
        self.checkbutton_style.configure('TCheckbutton', background=self.background)
        self.label_style = Style()
        self.label_style.configure('TLabel', background=self.background, font=('Calibri', 12))
        self.button_style = Style()
        self.button_style.configure('TMyButton', font=('Helvetica', 10))
        self.button_style.map('TMyButton', foreground=[('active', '!disabled', 'green')],
                              background=[('active', 'black')], focuscolor='')
        self.text_font = Font(family="Calibri", size=12)
        self.date_meta = "(((//meta[contains(@*, 'date')] | //meta[contains(@*, 'time')] | //*[contains(@*, 'datePublished')])[1]/@content) | " \
                         "//time/@datetime)[1]"
        self.menu_meta = "(//ul[contains(@class, 'menu')] | //ul[contains(@id, 'menu')] | //nav//ul)[1]//a"
        self.author_meta = "//meta[contains(@*,'uthor')]/@content"

        # Extractor Frames
        self.view_menu_frame = MyFrame(master=self, padding=5, view='menu')
        self.kraken_frame = MyFrame(master=self, view='extractor')
        self.json_full_frame = MyFrame(master=self, view='extractor')
        self.json_combined_buttons_frame = MyFrame(master=self.json_full_frame, view='extractor')
        self.json_buttons_frame = MyFrame(master=self.json_combined_buttons_frame, view='extractor')
        self.json_checkbutton_frame = MyFrame(self.json_combined_buttons_frame, view='extractor')
        self.start_urls_frame = MyFrame(master=self, view='extractor')
        self.menu_frame = MyFrame(master=self, view='extractor')
        self.articles_frame = MyFrame(master=self, view='extractor')
        self.title_frame = MyFrame(master=self, view='extractor')
        self.pubdate_frame = MyFrame(master=self, view='extractor')
        self.pubdate_buttons_frame = MyFrame(master=self.pubdate_frame, view='extractor')
        self.author_frame = MyFrame(master=self, view='extractor')
        self.body_frame = MyFrame(master=self, view='extractor')
        self.body_buttons_frame = MyFrame(self.body_frame, view='extractor')
        self.bottom_buttons_frame = MyFrame(master=self, view='extractor')
        self.bottom_info_frame = MyFrame(master=self, view='extractor')

        # Finder Frames
        self.article_url_frame = MyFrame(master=self, view='finder', padding=10)
        self.title_xpath_found_frame = MyFrame(master=self, view='finder', padding=10)
        self.pubdate_xpath_found_frame = MyFrame(master=self, view='finder', padding=10)
        self.author_xpath_found_frame = MyFrame(master=self, view='finder', padding=10)
        self.body_xpath_found_frame = MyFrame(master=self, view='finder', padding=10)

        # Extractor Labels
        self.kraken_id_label = MyLabel(master=self.kraken_frame, view='extractor', text="Kraken Link/ID:")
        self.json_label = MyLabel(master=self.json_full_frame, view='extractor', text="JSON:")
        self.start_urls_label = MyLabel(master=self.start_urls_frame, view='extractor', text="Start URLs:")
        self.menu_label = MyLabel(master=self.menu_frame, view='extractor', text="Menu XPath:")
        self.articles_label = MyLabel(master=self.articles_frame, view='extractor', text="Articles XPath:")
        self.title_label = MyLabel(master=self.title_frame, view='extractor', text="Title XPath:")
        self.pubdate_label = MyLabel(master=self.pubdate_frame, view='extractor', text="Pubdate XPath:")
        self.author_label = MyLabel(master=self.author_frame, view='extractor', text="Author XPath:")
        self.body_label = MyLabel(master=self.body_frame, view='extractor', text="Body XPath:")
        self.date_order_label = MyLabel(master=self.json_buttons_frame, view='extractor', text="")
        self.last_extractor_edit_label = MyLabel(master=self.bottom_info_frame, view='extractor', text="")
        self.last_kraken_edit_label = MyLabel(master=self.bottom_info_frame, view='extractor', text="")
        self.status_label = MyLabel(master=self.bottom_info_frame, view='extractor', text="")
        self.botname_label = MyLabel(master=self.bottom_info_frame, view='extractor', text="")
        self.projects_label = MyLabel(master=self.bottom_info_frame, view='extractor', text="")

        # Finder Labels
        self.article_url_label = MyLabel(master=self.article_url_frame, view='finder', text="URL:", width=15)
        self.title_xpath_found_label = MyLabel(master=self.title_xpath_found_frame, view='finder', text="Title XPath:", width=15)
        self.pubdate_xpath_found_label = MyLabel(master=self.pubdate_xpath_found_frame, view='finder', text="Pubdate XPath:", width=15)
        self.author_xpath_found_label = MyLabel(master=self.author_xpath_found_frame, view='finder', text="Author XPath:", width=15)
        self.body_xpath_found_label = MyLabel(master=self.body_xpath_found_frame, view='finder', text="Body XPath:", width=15)

        # Extractor Textboxes
        self.json_textbox = MyText(master=self.json_full_frame, view='extractor', height=8, width=60)
        self.start_urls_textbox = MyText(master=self.start_urls_frame, view='extractor', height=2, width=60)
        self.menu_textbox = MyText(master=self.menu_frame, view='extractor', height=2, width=60)
        self.articles_textbox = MyText(master=self.articles_frame, view='extractor', height=2, width=60)
        self.title_textbox = MyText(master=self.title_frame, view='extractor', height=2, width=60)
        self.pubdate_textbox = MyText(master=self.pubdate_frame, view='extractor', height=3, width=60)
        self.author_textbox = MyText(master=self.author_frame, view='extractor', height=2, width=60)
        self.body_textbox = MyText(master=self.body_frame, view='extractor', height=3, width=60)
        self.kraken_textbox = MyText(master=self.kraken_frame, view='extractor', height=1, width=60)
        self.xpath_dict = {
            "start_urls": self.start_urls_textbox,
            "menu_xpath": self.menu_textbox,
            "articles_xpath": self.articles_textbox,
            "title_xpath": self.title_textbox,
            "pubdate_xpath": self.pubdate_textbox,
            "author_xpath": self.author_textbox,
            "body_xpath": self.body_textbox,
        }

        # Finder Textboxes
        self.article_url_textbox = MyText(master=self.article_url_frame, view='finder', height=1, width=81)

        self.title_xpath_found_textbox_1 = MyText(master=self.title_xpath_found_frame, view='finder', height=1, width=40)
        self.title_xpath_found_textbox_2 = MyText(master=self.title_xpath_found_frame, view='finder', height=1, width=40)
        self.title_xpath_found_textbox_3 = MyText(master=self.title_xpath_found_frame, view='finder', height=1, width=40)
        self.title_xpath_found_textbox_4 = MyText(master=self.title_xpath_found_frame, view='finder', height=1, width=40)
        self.title_xpath_found_textbox_5 = MyText(master=self.title_xpath_found_frame, view='finder', height=1, width=40)

        self.title_xpath_result_textbox_1 = MyText(master=self.title_xpath_found_frame, view='finder', height=1, width=40)
        self.title_xpath_result_textbox_2 = MyText(master=self.title_xpath_found_frame, view='finder', height=1, width=40)
        self.title_xpath_result_textbox_3 = MyText(master=self.title_xpath_found_frame, view='finder', height=1, width=40)
        self.title_xpath_result_textbox_4 = MyText(master=self.title_xpath_found_frame, view='finder', height=1, width=40)
        self.title_xpath_result_textbox_5 = MyText(master=self.title_xpath_found_frame, view='finder', height=1, width=40)

        self.pubdate_xpath_found_textbox_1 = MyText(master=self.pubdate_xpath_found_frame, view='finder', height=1, width=40)
        self.pubdate_xpath_found_textbox_2 = MyText(master=self.pubdate_xpath_found_frame, view='finder', height=1, width=40)
        self.pubdate_xpath_found_textbox_3 = MyText(master=self.pubdate_xpath_found_frame, view='finder', height=1, width=40)
        self.pubdate_xpath_found_textbox_4 = MyText(master=self.pubdate_xpath_found_frame, view='finder', height=1, width=40)
        self.pubdate_xpath_found_textbox_5 = MyText(master=self.pubdate_xpath_found_frame, view='finder', height=1, width=40)

        self.pubdate_xpath_result_textbox_1 = MyText(master=self.pubdate_xpath_found_frame, view='finder', height=1, width=40)
        self.pubdate_xpath_result_textbox_2 = MyText(master=self.pubdate_xpath_found_frame, view='finder', height=1, width=40)
        self.pubdate_xpath_result_textbox_3 = MyText(master=self.pubdate_xpath_found_frame, view='finder', height=1, width=40)
        self.pubdate_xpath_result_textbox_4 = MyText(master=self.pubdate_xpath_found_frame, view='finder', height=1, width=40)
        self.pubdate_xpath_result_textbox_5 = MyText(master=self.pubdate_xpath_found_frame, view='finder', height=1, width=40)

        self.author_xpath_found_textbox_1 = MyText(master=self.author_xpath_found_frame, view='finder', height=1, width=40)
        self.author_xpath_found_textbox_2 = MyText(master=self.author_xpath_found_frame, view='finder', height=1, width=40)
        self.author_xpath_found_textbox_3 = MyText(master=self.author_xpath_found_frame, view='finder', height=1, width=40)
        self.author_xpath_found_textbox_4 = MyText(master=self.author_xpath_found_frame, view='finder', height=1, width=40)
        self.author_xpath_found_textbox_5 = MyText(master=self.author_xpath_found_frame, view='finder', height=1, width=40)

        self.author_xpath_result_textbox_1 = MyText(master=self.author_xpath_found_frame, view='finder', height=1, width=40)
        self.author_xpath_result_textbox_2 = MyText(master=self.author_xpath_found_frame, view='finder', height=1, width=40)
        self.author_xpath_result_textbox_3 = MyText(master=self.author_xpath_found_frame, view='finder', height=1, width=40)
        self.author_xpath_result_textbox_4 = MyText(master=self.author_xpath_found_frame, view='finder', height=1, width=40)
        self.author_xpath_result_textbox_5 = MyText(master=self.author_xpath_found_frame, view='finder', height=1, width=40)

        self.body_xpath_found_textbox_1 = MyText(master=self.body_xpath_found_frame, view='finder', height=1, width=40)
        self.body_xpath_found_textbox_2 = MyText(master=self.body_xpath_found_frame, view='finder', height=1, width=40)
        self.body_xpath_found_textbox_3 = MyText(master=self.body_xpath_found_frame, view='finder', height=1, width=40)
        self.body_xpath_found_textbox_4 = MyText(master=self.body_xpath_found_frame, view='finder', height=1, width=40)
        self.body_xpath_found_textbox_5 = MyText(master=self.body_xpath_found_frame, view='finder', height=1, width=40)

        self.body_xpath_result_textbox_1 = MyText(master=self.body_xpath_found_frame, view='finder', height=1, width=40)
        self.body_xpath_result_textbox_2 = MyText(master=self.body_xpath_found_frame, view='finder', height=1, width=40)
        self.body_xpath_result_textbox_3 = MyText(master=self.body_xpath_found_frame, view='finder', height=1, width=40)
        self.body_xpath_result_textbox_4 = MyText(master=self.body_xpath_found_frame, view='finder', height=1, width=40)
        self.body_xpath_result_textbox_5 = MyText(master=self.body_xpath_found_frame, view='finder', height=1, width=40)

        # View Menu Buttons
        self.open_extractor_button = MyButton(master=self.view_menu_frame, view='menu', text="Extractor",
                                              command=lambda: self.switch_view(view_to_open='extractor'))
        self.open_finder_button = MyButton(master=self.view_menu_frame, view='menu', text="Finder",
                                           command=lambda: self.switch_view(view_to_open='finder'))

        self.kraken_clipboard_button = MyButton(master=self.kraken_frame, view='extractor', text="Clipboard",
                                                command=lambda: self.load_from_kraken(self.clipboard_get()))
        self.open_source_button = MyButton(master=self.kraken_frame, view='extractor', text="Source",
                                           command=lambda: self.open_link(self.kraken_textbox.get('1.0', tk.END)))
        self.load_from_db_button = MyButton(master=self.kraken_frame, view='extractor', text="DB Load", command=self.load_from_db)
        self.open_items_button = MyButton(master=self.kraken_frame, view='extractor', text="Items", command=self.open_items_page)

        # JSON MyButtons
        self.code_copy_button = MyButton(master=self.json_buttons_frame, view='extractor', text="Copy", command=lambda: self.copy_code(self.json_textbox))
        self.load_from_existing_button = MyButton(master=self.json_buttons_frame, view='extractor', text="Load",
                                                  command=lambda: self.generate(load_from_existing_bool=True))
        self.load_without_url_button = MyButton(master=self.json_buttons_frame, view='extractor', text="Load (-URL)",
                                                command=lambda: self.generate(load_from_existing_bool=True, leave_current_url=True))
        self.add_proxy_button = MyButton(master=self.json_buttons_frame, view='extractor', text="Proxy",
                                         command=lambda: self.edit_json(initial_key="scrapy_settings",
                                                                        keyword="HTTP_PROXY",
                                                                        value=config.proxy))
        self.allowed_domains_button = MyButton(master=self.json_buttons_frame, view='extractor', text="Alw. Dom.",
                                               command=lambda: self.edit_json(initial_key="scrapy_arguments",
                                                                              keyword="allowed_domains",
                                                                              value=self.get_source_name(
                                                                                  copy=False)))
        self.pubdate_required_button = MyButton(master=self.json_buttons_frame, view='extractor', text="Pubdate Req",
                                                command=lambda: self.edit_json(initial_key="scrapy_arguments",
                                                                               keyword="pubdate_required",
                                                                               value=True))
        self.init_wait_button = MyButton(master=self.json_buttons_frame, view='extractor', text="Init Wait",
                                         command=lambda: self.edit_json(initial_key="scrapy_arguments",
                                                                        keyword='init_wait',
                                                                        value=2))
        self.article_wait_button = MyButton(master=self.json_buttons_frame, view='extractor', text="Article Wait",
                                            command=lambda: self.edit_json(initial_key="scrapy_arguments",
                                                                           keyword='article_wait',
                                                                           value=2))
        # Date Order MyButtons
        self.date_order_DMY = MyButton(master=self.json_buttons_frame, view='extractor', text="DMY",
                                       command=lambda: self.edit_json(initial_key="scrapy_arguments",
                                                                      keyword='date_order',
                                                                      value='DMY'))
        self.date_order_YMD = MyButton(master=self.json_buttons_frame, view='extractor', text="YMD",
                                       command=lambda: self.edit_json(initial_key="scrapy_arguments",
                                                                      keyword='date_order',
                                                                      value='YMD'))
        self.date_order_MDY = MyButton(master=self.json_buttons_frame, view='extractor', text="MDY",
                                       command=lambda: self.edit_json(initial_key="scrapy_arguments",
                                                                      keyword='date_order',
                                                                      value='MDY'))
        # JSON Checkbuttons
        self.open_links_check_bool = tk.IntVar()
        self.open_links_check_bool.set(1)

        self.overwrite_domain_check_bool = tk.IntVar()
        self.overwrite_domain_check_bool.set(1)

        self.rdc_check_bool = tk.IntVar()
        self.rdc_check_bool.set(0)

        self.open_source_checkbutton = MyCheckbutton(master=self.json_checkbutton_frame, view='extractor', text="Auto Open Source",
                                                     variable=self.open_links_check_bool,
                                                     takefocus=False)
        self.overwrite_domain_checkutton = MyCheckbutton(master=self.json_checkbutton_frame, view='extractor', text="Overwrite Domain",
                                                         variable=self.overwrite_domain_check_bool,
                                                         takefocus=False)
        self.rdc_checkbutton = MyCheckbutton(master=self.json_checkbutton_frame, view='extractor', text="RDC",
                                             variable=self.rdc_check_bool,
                                             takefocus=False)
        # Start URL MyButtons
        self.copy_start_button = MyButton(master=self.start_urls_frame, view='extractor', text="Copy", command=lambda: self.copy_code(self.start_urls_textbox))
        self.open_link_button = MyButton(master=self.start_urls_frame, view='extractor', text='Open Link', command=self.open_start_urls_link)
        self.open_domain_button = MyButton(master=self.start_urls_frame, view='extractor', text='Open Domain', command=self.open_domain)
        self.source_name_button = MyButton(master=self.start_urls_frame, view='extractor', text="Copy Name", command=self.get_source_name)
        self.source_domain_button = MyButton(master=self.start_urls_frame, view='extractor', text="Copy Domain", command=lambda: self.get_domain(copy=True))

        # Menu MyButtons
        self.copy_menu_button = MyButton(master=self.menu_frame, view='extractor', text="Copy", command=lambda: self.copy_code(self.menu_textbox))
        self.menu_category_button = MyButton(master=self.menu_frame, view='extractor', text="Cat",
                                             command=lambda: self.append_textbox_values(self.menu_textbox, after_value="[contains(@href, 'ategor')]"))

        # Article Xpath MyButtons
        self.copy_articles_button = MyButton(master=self.articles_frame, view='extractor', text="Copy", command=lambda: self.copy_code(self.articles_textbox))
        self.article_not_category_button = MyButton(master=self.articles_frame, view='extractor', text="Not Cat",
                                                    command=lambda: self.append_textbox_values(self.articles_textbox, before_value='(',
                                                                                               after_value=")[not(contains(@href, 'ategor'))]"))
        self.article_title_button = MyButton(master=self.articles_frame, view='extractor', text="Contains Title",
                                             command=lambda: self.replace_textbox_value(self.articles_textbox, "//*[contains(@class,'title')]/a"))

        # Title Xpath MyButtons
        self.copy_title_button = MyButton(master=self.title_frame, view='extractor', text="Copy", command=lambda: self.copy_code(self.title_textbox))
        self.title_single_button = MyButton(master=self.title_frame, view='extractor', text="[1]",
                                            command=lambda: self.append_textbox_values(self.title_textbox, before_value='(', after_value=')[1]'))
        self.title_h1_button = MyButton(master=self.title_frame, view='extractor', text="h1",
                                        command=lambda: self.replace_textbox_value(self.title_textbox, "//h1[contains(@class,'title')]"))

        # Pubdate Xpath MyButtons
        self.copy_pubdate_button = MyButton(master=self.pubdate_buttons_frame, view='extractor', text="Copy",
                                            command=lambda: self.copy_code(self.pubdate_textbox))
        self.pubdate_single_button = MyButton(master=self.pubdate_buttons_frame, view='extractor', text="[1]",
                                              command=lambda: self.append_textbox_values(self.pubdate_textbox, before_value='(',
                                                                                         after_value=')[1]'))
        self.standard_regex_button = MyButton(master=self.pubdate_buttons_frame, view='extractor', text="Rgx 1.1.2000",
                                              command=lambda: self.append_textbox_values(self.pubdate_textbox, before_value="re:match(",
                                                                                         after_value=r", '\d{1,2}\.\d{1,2}\.\d{2,4}', 'g')"))
        self.reverse_regex_button = MyButton(master=self.pubdate_buttons_frame, view='extractor', text="Rgx 2000.1.1",
                                              command=lambda: self.append_textbox_values(self.pubdate_textbox, before_value="re:match(",
                                                                                         after_value=r", '\d{2,4}\.\d{1,2}\.\d{1,2}', 'g')"))
        self.blank_regex_button = MyButton(master=self.pubdate_buttons_frame, view='extractor', text="Rgx Blank",
                                           command=lambda: self.append_textbox_values(self.pubdate_textbox, before_value="re:match(",
                                                                                      after_value=r", 'REGEX', 'g')"))
        self.meta_button = MyButton(master=self.pubdate_buttons_frame, view='extractor', text="Meta",
                                    command=lambda: self.replace_textbox_value(self.pubdate_textbox, self.date_meta))
        self.pubdate_replace_button = MyButton(master=self.pubdate_buttons_frame, view='extractor', text="Replace",
                                               command=lambda: self.append_textbox_values(self.pubdate_textbox, before_value="re:replace(",
                                                                                          after_value=r", 'SYMBOL1', 'g', 'SYMBOL2')"))
        self.word_regex_button = MyButton(master=self.pubdate_buttons_frame, view='extractor', text="Rgx Word",
                                          command=lambda: self.append_textbox_values(self.pubdate_textbox, before_value="re:match(",
                                                                                     after_value=r", '\d{1,2}\s\w+\s\d{2,4}', 'g')"))
        # Author Xpath MyButtons
        self.copy_author_button = MyButton(master=self.author_frame, view='extractor', text="Copy", command=lambda: self.copy_code(self.author_textbox))
        self.author_single_button = MyButton(master=self.author_frame, view='extractor', text="[1]",
                                             command=lambda: self.append_textbox_values(self.author_textbox, before_value='(', after_value=')[1]'))
        self.author_substring_button = MyButton(master=self.author_frame, view='extractor', text="Substring",
                                                command=lambda: self.append_textbox_values(self.author_textbox, before_value="substring-after(",
                                                                                           after_value=", ':')"))
        self.author_meta_button = MyButton(master=self.author_frame, view='extractor', text="Meta",
                                           command=lambda: self.replace_textbox_value(self.author_textbox, "//meta[contains(@*,'uthor')]/@content"))
        self.author_child_text_button = MyButton(master=self.author_frame, view='extractor', text="Child",
                                                 command=lambda: self.replace_textbox_value(self.author_textbox, '//*[child::text()[contains(.,"Autor")]]'))

        # Body Xpath MyButtons
        self.body_single_button = MyButton(master=self.body_buttons_frame, view='extractor', text="[1]",
                                           command=lambda: self.append_textbox_values(self.body_textbox, before_value='(', after_value=')[1]'), )
        self.copy_body_button = MyButton(master=self.body_buttons_frame, view='extractor', text="Copy", command=lambda: self.copy_code(self.body_textbox))
        self.body_content_button = MyButton(master=self.body_buttons_frame, view='extractor', text="Content",
                                            command=lambda: self.replace_textbox_value(self.body_textbox, "//div[contains(@class, 'content')]"))
        self.body_not_contains_class_button = MyButton(master=self.body_buttons_frame, view='extractor', text="Not Class",
                                                       command=lambda: self.append_textbox_values(self.body_textbox,
                                                                                                  after_value=f"[not(contains(@class, "
                                                                                                              f"'{self.clipboard_get().strip()}'))]"))
        self.body_not_contains_text_button = MyButton(master=self.body_buttons_frame, view='extractor', text="Not Text",
                                                      command=lambda: self.append_textbox_values(self.body_textbox,
                                                                                                 after_value=f"[not(descendant::text()[contains(.,"
                                                                                                             f"'{self.clipboard_get().strip()}')])]"))
        self.body_not_contains_id_button = MyButton(master=self.body_buttons_frame, view='extractor', text="Not ID",
                                                    command=lambda: self.append_textbox_values(self.body_textbox,
                                                                                               after_value=f"[not(contains(@id, "
                                                                                                           f"'{self.clipboard_get().strip()}'))]"))
        self.body_not_self_button = MyButton(master=self.body_buttons_frame, view='extractor', text="Not Self",
                                             command=lambda: self.append_textbox_values(self.body_textbox,
                                                                                        after_value=f"[not(self::{self.clipboard_get().strip()})]"))

        # Bottom Frame MyButtons
        self.clear_button = MyButton(master=self.bottom_buttons_frame, view='extractor', text="Clear All", command=self.clear_all_textboxes)
        self.generate_button = MyButton(master=self.bottom_buttons_frame, view='extractor', text="Generate JSON!", command=self.generate)

        # Finder Buttons
        self.find_content_button = MyButton(master=self.article_url_frame, view='finder', text="Find", command=self.find_content)

        self.title_xpath_select_button_1 = MyButton(master=self.title_xpath_found_frame, view='finder', text="Select",
                                                    command=lambda: self.from_textbox_to_textbox(self.title_xpath_found_textbox_1,
                                                                                                 self.title_textbox))
        self.title_xpath_select_button_2 = MyButton(master=self.title_xpath_found_frame, view='finder', text="Select",
                                                    command=lambda: self.from_textbox_to_textbox(self.title_xpath_found_textbox_2,
                                                                                                 self.title_textbox))
        self.title_xpath_select_button_3 = MyButton(master=self.title_xpath_found_frame, view='finder', text="Select",
                                                    command=lambda: self.from_textbox_to_textbox(self.title_xpath_found_textbox_3,
                                                                                                 self.title_textbox))
        self.title_xpath_select_button_4 = MyButton(master=self.title_xpath_found_frame, view='finder', text="Select",
                                                    command=lambda: self.from_textbox_to_textbox(self.title_xpath_found_textbox_4,
                                                                                                 self.title_textbox))
        self.title_xpath_select_button_5 = MyButton(master=self.title_xpath_found_frame, view='finder', text="Select",
                                                    command=lambda: self.from_textbox_to_textbox(self.title_xpath_found_textbox_5,
                                                                                                 self.title_textbox))

        self.pubdate_xpath_select_button_1 = MyButton(master=self.pubdate_xpath_found_frame, view='finder', text="Select",
                                                      command=lambda: self.from_textbox_to_textbox(self.pubdate_xpath_found_textbox_1,
                                                                                                   self.pubdate_textbox))
        self.pubdate_xpath_select_button_2 = MyButton(master=self.pubdate_xpath_found_frame, view='finder', text="Select",
                                                      command=lambda: self.from_textbox_to_textbox(self.pubdate_xpath_found_textbox_2,
                                                                                                   self.pubdate_textbox))
        self.pubdate_xpath_select_button_3 = MyButton(master=self.pubdate_xpath_found_frame, view='finder', text="Select",
                                                      command=lambda: self.from_textbox_to_textbox(self.pubdate_xpath_found_textbox_3,
                                                                                                   self.pubdate_textbox))
        self.pubdate_xpath_select_button_4 = MyButton(master=self.pubdate_xpath_found_frame, view='finder', text="Select",
                                                      command=lambda: self.from_textbox_to_textbox(self.pubdate_xpath_found_textbox_4,
                                                                                                   self.pubdate_textbox))
        self.pubdate_xpath_select_button_5 = MyButton(master=self.pubdate_xpath_found_frame, view='finder', text="Select",
                                                      command=lambda: self.from_textbox_to_textbox(self.pubdate_xpath_found_textbox_5,
                                                                                                   self.pubdate_textbox))

        self.author_xpath_select_button_1 = MyButton(master=self.author_xpath_found_frame, view='finder', text="Select",
                                                     command=lambda: self.from_textbox_to_textbox(self.author_xpath_found_textbox_1,
                                                                                                  self.author_textbox))
        self.author_xpath_select_button_2 = MyButton(master=self.author_xpath_found_frame, view='finder', text="Select",
                                                     command=lambda: self.from_textbox_to_textbox(self.author_xpath_found_textbox_2,
                                                                                                  self.author_textbox))
        self.author_xpath_select_button_3 = MyButton(master=self.author_xpath_found_frame, view='finder', text="Select",
                                                     command=lambda: self.from_textbox_to_textbox(self.author_xpath_found_textbox_3,
                                                                                                  self.author_textbox))
        self.author_xpath_select_button_4 = MyButton(master=self.author_xpath_found_frame, view='finder', text="Select",
                                                     command=lambda: self.from_textbox_to_textbox(self.author_xpath_found_textbox_4,
                                                                                                  self.author_textbox))
        self.author_xpath_select_button_5 = MyButton(master=self.author_xpath_found_frame, view='finder', text="Select",
                                                     command=lambda: self.from_textbox_to_textbox(self.author_xpath_found_textbox_5,
                                                                                                  self.author_textbox))

        self.body_xpath_select_button_1 = MyButton(master=self.body_xpath_found_frame, view='finder', text="Select",
                                                   command=lambda: self.from_textbox_to_textbox(self.body_xpath_found_textbox_1,
                                                                                                self.body_textbox))
        self.body_xpath_select_button_2 = MyButton(master=self.body_xpath_found_frame, view='finder', text="Select",
                                                   command=lambda: self.from_textbox_to_textbox(self.body_xpath_found_textbox_2,
                                                                                                self.body_textbox))
        self.body_xpath_select_button_3 = MyButton(master=self.body_xpath_found_frame, view='finder', text="Select",
                                                   command=lambda: self.from_textbox_to_textbox(self.body_xpath_found_textbox_3,
                                                                                                self.body_textbox))
        self.body_xpath_select_button_4 = MyButton(master=self.body_xpath_found_frame, view='finder', text="Select",
                                                   command=lambda: self.from_textbox_to_textbox(self.body_xpath_found_textbox_4,
                                                                                                self.body_textbox))
        self.body_xpath_select_button_5 = MyButton(master=self.body_xpath_found_frame, view='finder', text="Select",
                                                   command=lambda: self.from_textbox_to_textbox(self.body_xpath_found_textbox_5,
                                                                                                self.body_textbox))

        # Extractor Frame Lists
        self.view_menu_frame.frame_list = [[self.open_extractor_button, self.open_finder_button]]
        self.kraken_frame.frame_list = [[self.kraken_id_label],
                                        [self.kraken_textbox, self.kraken_clipboard_button, self.open_source_button,
                                         self.load_from_db_button, self.open_items_button]]
        self.json_buttons_frame.frame_list = [[self.code_copy_button, self.load_from_existing_button, self.load_without_url_button, self.add_proxy_button],
                                              [self.allowed_domains_button, self.pubdate_required_button, self.init_wait_button, self.article_wait_button],
                                              [self.date_order_DMY, self.date_order_MDY, self.date_order_YMD, self.date_order_label]]
        self.json_checkbutton_frame.frame_list = [[self.open_source_checkbutton, self.overwrite_domain_checkutton, self.rdc_checkbutton]]
        self.json_combined_buttons_frame.frame_list = [[self.json_buttons_frame],
                                                       [self.json_checkbutton_frame]]
        self.json_full_frame.frame_list = [[self.json_label],
                                           [self.json_textbox, self.json_combined_buttons_frame]]
        self.start_urls_frame.frame_list = [[self.start_urls_label],
                                            [self.start_urls_textbox, self.copy_start_button, self.open_link_button, self.open_domain_button,
                                             self.source_name_button, self.source_domain_button]]
        self.menu_frame.frame_list = [[self.menu_label],
                                      [self.menu_textbox, self.copy_menu_button, self.menu_category_button]]
        self.articles_frame.frame_list = [[self.articles_label],
                                          [self.articles_textbox, self.copy_articles_button, self.article_not_category_button, self.article_title_button]]
        self.title_frame.frame_list = [[self.title_label],
                                       [self.title_textbox, self.copy_title_button, self.title_h1_button, self.title_single_button]]
        self.pubdate_buttons_frame.frame_list = [
            [self.copy_pubdate_button, self.meta_button, self.standard_regex_button, self.reverse_regex_button, self.word_regex_button],
            [self.blank_regex_button, self.pubdate_replace_button, self.pubdate_single_button]]
        self.pubdate_frame.frame_list = [[self.pubdate_label], [self.pubdate_textbox, self.pubdate_buttons_frame]]
        self.author_frame.frame_list = [[self.author_label],
                                        [self.author_textbox, self.copy_author_button, self.author_meta_button, self.author_substring_button,
                                         self.author_child_text_button, self.author_single_button]]
        self.body_buttons_frame.frame_list = [
            [self.copy_body_button, self.body_content_button, self.body_not_contains_class_button, self.body_not_contains_id_button,
             self.body_not_contains_text_button],
            [self.body_not_self_button, self.body_single_button]]
        self.body_frame.frame_list = [[self.body_label],
                                      [self.body_textbox, self.body_buttons_frame]]
        self.bottom_buttons_frame.frame_list = [[self.generate_button, self.clear_button]]
        self.bottom_info_frame.frame_list = [[self.last_kraken_edit_label], [self.last_extractor_edit_label], [self.status_label], [self.projects_label],
                                             [self.botname_label], ]

        # Finder Frame Lists
        self.article_url_frame.frame_list = [[self.article_url_label, self.article_url_textbox, self.find_content_button]]
        self.title_xpath_found_frame.frame_list = [[self.title_xpath_found_label, self.title_xpath_found_textbox_1, self.title_xpath_select_button_1,
                                                    self.title_xpath_result_textbox_1],
                                                   [0, self.title_xpath_found_textbox_2, self.title_xpath_select_button_2,
                                                    self.title_xpath_result_textbox_2],
                                                   [0, self.title_xpath_found_textbox_3, self.title_xpath_select_button_3,
                                                    self.title_xpath_result_textbox_3],
                                                   [0, self.title_xpath_found_textbox_4, self.title_xpath_select_button_4,
                                                    self.title_xpath_result_textbox_4],
                                                   [0, self.title_xpath_found_textbox_5, self.title_xpath_select_button_5,
                                                    self.title_xpath_result_textbox_5]]
        self.pubdate_xpath_found_frame.frame_list = [[self.pubdate_xpath_found_label, self.pubdate_xpath_found_textbox_1, self.pubdate_xpath_select_button_1,
                                                      self.pubdate_xpath_result_textbox_1],
                                                     [0, self.pubdate_xpath_found_textbox_2, self.pubdate_xpath_select_button_2,
                                                      self.pubdate_xpath_result_textbox_2],
                                                     [0, self.pubdate_xpath_found_textbox_3, self.pubdate_xpath_select_button_3,
                                                      self.pubdate_xpath_result_textbox_3],
                                                     [0, self.pubdate_xpath_found_textbox_4, self.pubdate_xpath_select_button_4,
                                                      self.pubdate_xpath_result_textbox_4],
                                                     [0, self.pubdate_xpath_found_textbox_5, self.pubdate_xpath_select_button_5,
                                                      self.pubdate_xpath_result_textbox_5]]
        self.author_xpath_found_frame.frame_list = [[self.author_xpath_found_label, self.author_xpath_found_textbox_1, self.author_xpath_select_button_1,
                                                     self.author_xpath_result_textbox_1],
                                                    [0, self.author_xpath_found_textbox_2, self.author_xpath_select_button_2,
                                                     self.author_xpath_result_textbox_2],
                                                    [0, self.author_xpath_found_textbox_3, self.author_xpath_select_button_3,
                                                     self.author_xpath_result_textbox_3],
                                                    [0, self.author_xpath_found_textbox_4, self.author_xpath_select_button_4,
                                                     self.author_xpath_result_textbox_4],
                                                    [0, self.author_xpath_found_textbox_5, self.author_xpath_select_button_5,
                                                     self.author_xpath_result_textbox_5]]
        self.body_xpath_found_frame.frame_list = [[self.body_xpath_found_label, self.body_xpath_found_textbox_1, self.body_xpath_select_button_1,
                                                   self.body_xpath_result_textbox_1],
                                                  [0, self.body_xpath_found_textbox_2, self.body_xpath_select_button_2,
                                                   self.body_xpath_result_textbox_2],
                                                  [0, self.body_xpath_found_textbox_3, self.body_xpath_select_button_3,
                                                   self.body_xpath_result_textbox_3],
                                                  [0, self.body_xpath_found_textbox_4, self.body_xpath_select_button_4,
                                                   self.body_xpath_result_textbox_4],
                                                  [0, self.body_xpath_found_textbox_5, self.body_xpath_select_button_5,
                                                   self.body_xpath_result_textbox_5]]

        self.session = requests.Session()
        with open('settings.json') as f1:
            self.settings_json = json.load(f1)
        self.settings_json["USER_AGENT"] = config.user_agent
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

        self.headers = {'Connection': 'close', 'User-Agent': config.user_agent}
        session_headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml',
            'user-agent': config.user_agent
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

        self.all_widgets = []
        self.get_all_widgets(self)

        for widget in self.all_widgets:
            if isinstance(widget, MyText):
                widget['undo'] = True
                widget['bg'] = 'white'
                widget['font'] = self.text_font

        row = 0
        for widget in self.all_widgets:
            if isinstance(widget, MyFrame):
                # Padding exceptions
                if self.generate_button.master == widget:
                    self.pack_frame(widget.frame_list, padx=(2, 315))
                else:
                    self.pack_frame(widget.frame_list)
                if widget in self.winfo_children():
                    widget.grid(row=row, column=0, sticky='W', padx=20, pady=0)
                    row += 1

        # Forget unneeded elements at start
        for widget in self.winfo_children():
            if not hasattr(widget, 'view') or (widget.view != 'extractor' and widget.view != 'menu'):
                widget.grid_remove()

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
        print(f"Booted in {round(t2 - t1, 2)} seconds.")

    def initiate_connection(self):
        if os.path.isdir('//VT10/xpath_manager'):
            con = sqlite3.connect(self.shared_db_path)
        else:
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

    def set_word_boundaries(self):
        self.tk.call('tcl_wordBreakAfter', '', 0)
        self.tk.call('set', 'tcl_wordchars', '[a-zA-Z0-9_.,-]')
        self.tk.call('set', 'tcl_nonwordchars', '[^a-zA-Z0-9_.,-]')

    def get_all_widgets(self, root):
        for widget in root.winfo_children():
            self.all_widgets.append(widget)
            if widget.winfo_children():
                self.get_all_widgets(widget)

    @staticmethod
    def pack_frame(elements, sticky='NW', padx: Union[int, tuple] = 2, pady=2):
        row = 0
        col = 0
        for element_row in elements:
            for element in element_row:
                if element:
                    element.grid(row=row, column=col, sticky=sticky, padx=padx, pady=pady)
                col += 1
            row += 1
            col = 0

    def edit_json(self, initial_key, keyword, value):
        if self.json_textbox.get("1.0", tk.END).strip():
            existing_json = json.loads(self.json_textbox.get("1.0", tk.END).strip())
            if keyword in existing_json[initial_key].keys():
                if existing_json[initial_key][keyword] == value:
                    del existing_json[initial_key][keyword]
                else:
                    existing_json[initial_key][keyword] = value
            else:
                existing_json[initial_key][keyword] = value
            self.json_textbox.delete("1.0", tk.END)
            self.json_textbox.insert("1.0", json.dumps(existing_json, indent=2))
            if keyword == 'date_order':
                self.update_date_order_label()
        else:
            return

    def update_date_order_label(self):
        if self.json_textbox.get("1.0", tk.END).strip():
            existing_json = json.loads(self.json_textbox.get("1.0", tk.END).strip())
            if 'date_order' in existing_json['scrapy_arguments'].keys():
                self.date_order_label['text'] = existing_json['scrapy_arguments']['date_order']
            else:
                self.date_order_label['text'] = ""

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
            if self.kraken_textbox.get('1.0', tk.END).strip():
                try:
                    self.kraken_id = re.findall(r'\d+', self.kraken_textbox.get('1.0', tk.END).strip())[-1]
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

    def load_from_kraken(self, link, open_source_bool=True):
        """
        Function to fill the extractor with the JSON from Kraken
        :param link: Kraken link / ID
        :param open_source_bool: Bool indicating whether the source link should be opened in a browser tab
        :return:
        """
        self.clear_all_textboxes()
        self.kraken_textbox.delete('1.0', tk.END)
        self.kraken_textbox.insert('1.0', link)
        link = self.get_link()  # Format link
        if not link:
            print("No ID found")
            return
        if open_source_bool and self.open_links_check_bool.get():
            webbrowser.get("chrome").open(link)

        # Show correctly formatted link in textbox
        self.kraken_textbox.delete('1.0', tk.END)
        self.kraken_textbox.insert('1.0', link)

        # Show if/who/when edited the source last
        con = self.initiate_connection()
        cur = con.cursor()
        cur.execute('SELECT * FROM log WHERE id=?', (self.kraken_id,))
        result = cur.fetchone()
        con.close()
        if result:
            self.last_extractor_edit_label['text'] = f"Last Edit: {result[12]} - {result[1]}"

        items_link = link.replace('/edit', '')
        last_editor_xpath = '//tr[td[child::text()[contains(.,"Updated by")]]]/td[2]//text()'
        last_update_xpath = '//tr[td[child::text()[contains(.,"Last update")]]]/td[2]/text()'
        enabled_xpath = '//tr[td[child::text()[contains(.,"Enabled")]]]/td[2]/i[contains(@class, "true")]'
        active_xpath = '//tr[td[child::text()[contains(.,"Active")]]]/td[2]/i[contains(@class, "true")]'
        botname_xpath = '//tr[td[child::text()[contains(.,"Botname")]]]/td[2]/text()'
        projects_xpath = '//tr[td[child::text()[contains(.,"Projects")]]]/td[2]//li/a/text()'
        items_page_response = self.session.get(items_link)
        tree = html.fromstring(items_page_response.text)
        last_editor = tree.xpath(last_editor_xpath)[1].strip() if len(tree.xpath(last_editor_xpath)) > 2 else "None"
        last_update = tree.xpath(last_update_xpath)[0]
        enabled = bool(tree.xpath(enabled_xpath))
        active = bool(tree.xpath(active_xpath))
        botname = tree.xpath(botname_xpath)[0]
        projects = tree.xpath(projects_xpath)
        if enabled:
            if active:
                status = "Running"
            else:
                status = "Enabled, but not Active(?)"
        else:
            if active:
                status = "Custom"
            else:
                status = "Stopped"
        self.last_kraken_edit_label['text'] = f"Last Kraken Edit: {last_editor} - {last_update}"
        self.status_label['text'] = f"Status: {status}"
        self.projects_label['text'] = f"Projects: {','.join(projects)}"
        self.botname_label['text'] = f"Botname: {botname}"
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

        if not self.kraken_textbox.get('1.0', tk.END).strip():
            return

        kraken_id = re.search(r'\d+', self.kraken_textbox.get('1.0', tk.END))
        if kraken_id:
            cur.execute('SELECT * FROM log WHERE id=?', (kraken_id.group(),))
            result = cur.fetchone()
        else:
            cur.execute("SELECT * FROM log WHERE start_urls LIKE '%'||?||'%'", (self.kraken_textbox.get('1.0', tk.END).strip(),))
            result = cur.fetchone()

        con.close()

        if result:
            self.set_kraken_id(result[0])
            self.last_extractor_edit_label['text'] = f"Last Edit: {result[12]} - {result[1]}"
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

    def open_items_page(self):
        # Function to open the "View Item" page of the source in Kraken
        if self.kraken_textbox.get('1.0', tk.END).strip():
            link = self.get_link().replace('/edit', '')
            webbrowser.get("chrome").open(link)
        else:
            return

    def get_source_name(self, copy=True):
        domain = self.start_urls_textbox.get("1.0", tk.END).strip()
        if domain and domain[-1] == '/':
            domain = domain[:-1]
        try:
            name = domain.split('//')[1].split('/')[0].replace('www.', '')
            if self.rdc_check_bool.get():
                name += ' - RDC AM'
        except IndexError:
            return
        if name:
            if copy:
                pyperclip.copy(name)
            return name

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
                    if sitemap[0][0] != '/':
                        sitemap[0] = '/' + sitemap[0]
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
            if self.overwrite_domain_check_bool.get():
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
        for widget in self.all_widgets:
            if isinstance(widget, MyText):
                widget.delete("1.0", tk.END)
        self.last_kraken_edit_label['text'] = ""
        self.last_extractor_edit_label['text'] = ""
        self.date_order_label['text'] = ""
        self.status_label['text'] = ""
        self.projects_label['text'] = ""
        self.botname_label['text'] = ""

    @staticmethod
    def sort_json(json_object):
        keyorder_arguments = ["start_urls", "menu_xpath", "articles_xpath", "title_xpath", "pubdate_xpath", "date_order",
                              "author_xpath", "body_xpath"]
        sortable_keys = []
        other_keys = []
        for entry in keyorder_arguments:
            if entry in json_object["scrapy_arguments"].keys():
                sortable_keys.append(entry)
        for entry in json_object["scrapy_arguments"].keys():
            if entry not in sortable_keys:
                other_keys.append(entry)
        if 'extractor' in other_keys:
            other_keys.remove('extractor')
        if 'source_id' in other_keys:
            other_keys.remove('source_id')
        sortable_keys.extend(other_keys)
        new_dict = {"scrapy_arguments": {}, "scrapy_settings": {}}
        for entry in sortable_keys:
            new_dict["scrapy_arguments"][entry] = json_object["scrapy_arguments"][entry]
        new_dict["scrapy_settings"] = json_object["scrapy_settings"]
        return new_dict

    def not_empty(self):
        return bool(self.start_urls_textbox.get("1.0", tk.END).strip() or
                    self.menu_textbox.get("1.0", tk.END).strip() or
                    self.articles_textbox.get("1.0", tk.END).strip() or
                    self.title_textbox.get("1.0", tk.END).strip() or
                    self.pubdate_textbox.get("1.0", tk.END).strip() or
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
        if "link_id_regex" not in json_var["scrapy_arguments"].keys() and 'articles_xpath' in json_var["scrapy_arguments"].keys():
            json_var["scrapy_arguments"]["link_id_regex"] = None
        for element in self.xpath_dict.keys():
            self.edit_textbox(self.xpath_dict[element], element, json_var)

        if "scrapy_settings" in json_var.keys():
            json_var["scrapy_settings"].update(self.settings_json)
        else:
            json_var["scrapy_settings"] = self.settings_json
        return self.sort_json(json_var)

    def fill_code_textbox(self, json_var):
        final_text = json.dumps(json_var, indent=2)
        self.json_textbox.delete("1.0", tk.END)
        self.json_textbox.insert('1.0', final_text)
        return final_text

    def log_code(self, json_dict):
        if self.kraken_id:
            self.log_to_db(json_dict)
        elif self.kraken_textbox.get('1.0', tk.END).strip():
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

    def generate(self, _=None, initial_json=None, load_from_existing_bool=False, leave_current_url=False):
        existing_code = self.json_textbox.get("1.0", tk.END).strip()
        if initial_json:
            json_variable = self.default_changes(initial_json)
            self.fill_code_textbox(json_variable)
            self.update_date_order_label()
            for element in self.xpath_dict.keys():
                self.edit_textbox(self.xpath_dict[element], element, json_variable)

        elif existing_code:
            try:
                json_variable = json.loads(existing_code)
                if leave_current_url:
                    json_variable['scrapy_arguments']['start_urls'] = self.start_urls_textbox.get('1.0', tk.END).strip()
            except JSONDecodeError:
                print("Invalid JSON")
                return
            if not load_from_existing_bool and self.not_empty():
                for element in self.xpath_dict.keys():
                    json_variable = self.get_text_from_textbox(self.xpath_dict[element], element, json_variable)
            json_variable = self.default_changes(json_variable)
            final_json = self.fill_code_textbox(json_variable)
            self.update_date_order_label()
            pyperclip.copy(final_json)
            for element in self.xpath_dict.keys():
                self.edit_textbox(self.xpath_dict[element], element, json_variable)

            self.log_code(json_variable)

        else:
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
                    "USER_AGENT": config.user_agent
                }
            }
            if self.not_empty():
                for element in self.xpath_dict.keys():
                    json_variable = self.get_text_from_textbox(self.xpath_dict[element], element, json_variable)

                json_variable = self.default_changes(json_variable)
                final_json = self.fill_code_textbox(json_variable)
                self.update_date_order_label()
                pyperclip.copy(final_json)
                self.log_code(json_variable)
            else:
                self.fill_code_textbox(json_variable)

    def fill_found_textboxes(self, tree, column):
        debug = False
        if debug:
            print("Starting connection")
        con = self.initiate_connection()
        cur = con.cursor()

        if debug:
            print(column)

        if column == 'title_xpath':
            cur.execute("SELECT xpath FROM title_xpath ORDER BY count DESC")
            element = self.title_xpath_found_frame.frame_list
        elif column == 'pubdate_xpath':
            cur.execute("SELECT xpath FROM pubdate_xpath ORDER BY count DESC")
            element = self.pubdate_xpath_found_frame.frame_list
        elif column == 'author_xpath':
            cur.execute("SELECT xpath FROM author_xpath ORDER BY count DESC")
            element = self.author_xpath_found_frame.frame_list
        elif column == 'body_xpath':
            cur.execute("SELECT xpath FROM body_xpath ORDER BY count DESC")
            element = self.body_xpath_found_frame.frame_list

        if debug:
            print('statement executed')

        xpath_list = cur.fetchall()
        xpath_list = [x[0] for x in xpath_list]
        if debug:
            print('fetched all xpath from db')
        con.close()

        final_result = []
        number_of_textboxes = 5
        if debug:
            print('trying each xpath')
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
        if debug:
            print('filling texboxes with results')
        for i, entry in enumerate(final_result):
            if debug:
                print(entry)
            element[i][-3].delete('1.0', tk.END)
            element[i][-3].insert('1.0', entry['xpath'])
            element[i][-1].delete('1.0', tk.END)
            element[i][-1].insert('1.0', entry['result'][:50])

    def find_content(self):
        for widget in self.all_widgets:
            if widget.view == 'finder' and isinstance(widget, MyText) and widget.master != self.article_url_frame:
                widget.delete('1.0', tk.END)
        article_url = self.article_url_textbox.get("1.0", tk.END).strip()
        website_response = requests.get(article_url, headers=self.headers, verify=False)
        tree = html.fromstring(website_response.text)
        self.fill_found_textboxes(tree, 'title_xpath')
        self.fill_found_textboxes(tree, 'pubdate_xpath')
        self.fill_found_textboxes(tree, 'author_xpath')
        self.fill_found_textboxes(tree, 'body_xpath')

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

    def forget_current_view(self):
        for widget in self.all_widgets:
            if widget.view == self.current_view:
                widget.grid_remove()

    def open_new_view(self, view):
        for widget in self.all_widgets:
            if widget.view == view:
                widget.grid()

    def open_finder_view(self):
        self.article_url_label.grid()
        self.article_url_textbox.grid()
        self.find_content_button.grid()

    def switch_view(self, view_to_open):
        if view_to_open == self.current_view:
            return
        self.forget_current_view()
        if view_to_open == 'extractor':
            self.open_new_view('extractor')
        elif view_to_open == 'finder':
            self.open_new_view('finder')
        self.current_view = view_to_open

    @staticmethod
    def join_tuple_string(values_tuple) -> str:
        string_list = []
        for element in values_tuple:
            string_list.append(str(element))
        return ', '.join(string_list)

    def stats(self):
        def extract_regex(start_string):
            regex_contains = ['substring', 're:match', 're:replace']
            result = re.match(r"re:match\((.+),'(.+)','(.+)'\)", start_string)
            if result:
                result = result.group(1)
                if not any(s in result for s in regex_contains):
                    return result
                else:
                    return extract_regex(result)

            result = re.match(r"re:replace\((.+),'(.+)','(.+)','(.+)'\)", start_string)
            if result:
                result = result.group(1)
                if not any(s in result for s in regex_contains):
                    return result
                else:
                    return extract_regex(result)

            result = re.match(r"substring-.+\((.+),'", start_string)
            if result:
                result = result.group(1)
                if not any(s in result for s in regex_contains):
                    return result
                else:
                    return extract_regex(result)

        def create_dict(db_results, body_xpath=False):
            db_results = [x[0] for x in db_results if x[0]]
            updated_list = []
            regex_contains = ['substring', 're:match', 're:replace']
            body_contains = ['//node()', '/text()', ']//p', "'row'", "//div[contains(@class,'content')", '::img', '//article', '//figure/', '//main',
                             '//figcaption', "//div[contains(@class,'-content')]", '//section/']
            for xpath in db_results:
                split_xpath_list = xpath.split('|')
                for updated_xpath in split_xpath_list:
                    updated_xpath = updated_xpath.replace(' ', '')
                    if '@' not in updated_xpath and updated_xpath.count('/') < 3:
                        continue
                    if updated_xpath.endswith('/'):
                        updated_xpath = updated_xpath[:-1]
                    if not any(s in updated_xpath for s in regex_contains):
                        if body_xpath:
                            if updated_xpath.endswith('/p'):
                                updated_xpath = updated_xpath[:-2]
                            if '/node()' in updated_xpath:
                                updated_xpath = updated_xpath.split('/node()')[0]
                            if not any(s in updated_xpath for s in body_contains):
                                updated_list.append(updated_xpath.strip())
                        else:
                            updated_list.append(updated_xpath.strip())
                    else:
                        extracted = extract_regex(updated_xpath)
                        if extracted:
                            updated_list.append(extracted)

            created_dict = dict()
            for i in updated_list:
                created_dict[i] = created_dict.get(i, 0) + 1

            return sorted(created_dict.items(), key=lambda d: d[1], reverse=True)

        con = self.initiate_connection()
        cur = con.cursor()

        cur.execute("SELECT * FROM log")
        print(f"Hello, {login_data.user}")
        print(f"The database contains {len(cur.fetchall())} entries.")
        cur.execute("DELETE FROM title_xpath")
        cur.execute("DELETE FROM pubdate_xpath")
        cur.execute("DELETE FROM author_xpath")
        cur.execute("DELETE FROM body_xpath")

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
