import gspread
import subprocess
# gc = gspread.service_account()

kraken_id_list = [540828]
for kraken_id in kraken_id_list:
    subprocess.call(f"scrapy runspider kraken_json.py -a kraken_id={kraken_id}")
