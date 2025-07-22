import requests
from bs4 import BeautifulSoup
import re

def extract_links_grouped_by_cusa(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
    except Exception as e:
        print(f"[خطا] دریافت صفحه ممکن نشد: {e}")
        return {}

    soup = BeautifulSoup(res.text, 'html.parser')

    # پیدا کردن بلوک‌ها یا بخش‌هایی که کد CUSA و لینک‌ها را در آنجا داریم
    # معمولاً کد CUSA در کنار متن Game یا Update هست یا در خود لینک (مثل ..._25186_...)
    versions = {}

    # کلید regex برای پیدا کردن CUSA
    cusa_pattern = re.compile(r'CUSA\d+')

    # پیدا کردن تمام بخش‌هایی که ممکنه شامل لینک باشن
    for section in soup.find_all('div', class_='file-down'):

        text = section.get_text(separator=' ', strip=True)
        cusa_match = cusa_pattern.search(text)
        cusa_code = cusa_match.group() if cusa_match else 'CUSAUNKNOWN'

        links = []
        for a_tag in section.find_all("a", href=True):
            href = a_tag['href']
            if "mediafire.com/file/" in href:
                # برچسبی که معمولاً نزدیک لینک است
                label = a_tag.find_previous(string=True)
                if not label or len(label.strip()) == 0:
                    label = "بدون عنوان"
                else:
                    label = label.strip()
                links.append({'label': label, 'link': href})

        if links:
            if cusa_code not in versions:
                versions[cusa_code] = []
            versions[cusa_code].extend(links)

    return versions
