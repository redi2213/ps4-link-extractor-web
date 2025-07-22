from flask import Flask, request, render_template, send_file
import os
from extractor.parser import extract_links_grouped_by_cusa

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        if not url:
            return render_template('index.html', error="لینک وارد نشده است.")

        versions = extract_links_grouped_by_cusa(url)
        if not versions:
            return render_template('index.html', error="لینک مدیافایری یافت نشد.")

        if len(versions) == 1:
            cusa = list(versions.keys())[0]
            filename = f"{cusa}_{url.split('/')[-1]}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                for item in versions[cusa]:
                    f.write(f"{item['label']}\n{item['link']}\n\n")
            return send_file(filename, as_attachment=True)

        return render_template('index.html', versions=versions, url=url)

    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    selected_cusa = request.form.get('cusa')
    url = request.form.get('url')
    versions = extract_links_grouped_by_cusa(url)

    if selected_cusa not in versions:
        return render_template('index.html', error="CUSA انتخاب‌شده معتبر نیست.")

    filename = f"{selected_cusa}_{url.split('/')[-1]}.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        for item in versions[selected_cusa]:
            f.write(f"{item['label']}\n{item['link']}\n\n")

    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
