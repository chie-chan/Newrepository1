from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

import os
import time
import sys

# スクリプト自身が存在するディレクトリを取得
script_dir = os.path.dirname(os.path.abspath(__file__))

image_folder_path = os.path.join(script_dir, "images")
upload_file_path = os.path.join(script_dir, "f56fa60d5b68d734.png")
content_file_path = os.path.join(script_dir, "content.txt")
download_dir = script_dir  # script_dir自体をダウンロード先ディレクトリとする

# コマンドライン引数の取得
category_arg = sys.argv[1]
start_price_arg = sys.argv[2]
sokketu_arg = sys.argv[3]

# Chromeのオプション
options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": download_dir,  # ダウンロード先
    "download.prompt_for_download": False,       # ダウンロード時に確認ダイアログを非表示
    "directory_upgrade": True,                  # ダウンロードディレクトリのアップグレードを有効
    "safebrowsing.enabled": True                # セーフブラウジングを有効化
}
options.add_experimental_option("prefs", prefs)

options.add_argument("--disable-gpu")
options.add_argument("--disable-software-rasterizer")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-background-networking")
options.add_argument("--disable-renderer-backgrounding")
options.add_argument("--start-maximized") 
options.add_argument("--headless")  # 動作確認のためヘッドレス無効を効化

driver = webdriver.Chrome(options=options)

try:
    # 対象のサイトにアクセス
    url = "https://allai-t.com/"
    driver.get(url)
    time.sleep(5)  # ページロード待機

    # Login with Discord ボタンをクリック
    login_with_discord_button = driver.find_element(By.XPATH, '//button[contains(text(), "Login with Discord")]')
    login_with_discord_button.click()
    time.sleep(5)

    # Discordログインページでメールアドレスとパスワードを入力
    email_input = driver.find_element(By.NAME, "email")
    email_input.send_keys("gengenz719@gmail.com")

    password_input = driver.find_element(By.NAME, "password")
    password_input.send_keys("gegez719")

    # ログインボタンをクリック
    login_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
    login_button.click()
    time.sleep(5)

    # 「認証」ボタンをクリック
    verify_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="app-mount"]/div[2]/div[1]/div[1]/div/div/div/div/div[2]/div/div/button'))
    )
    verify_button.click()
    print("認証ボタンをクリックしました")
    time.sleep(10)
    print("次のページが表示されました。認証成功です！")

    # 画像アップロード
    try:
       image_files = [os.path.join(image_folder_path, f) for f in os.listdir(image_folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
       file_paths = "\n".join(image_files)  # 改行区切りで複数ファイルを渡す

       upload_input = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[3]/div[2]/div[2]/input')
       upload_input.send_keys(file_paths)
       print(f"フォルダ内の画像を一括でアップロードしました: {image_files}")

       time.sleep(10)  # アップロード待機
    except Exception as e:
        print(f"画像アップロード中にエラーが発生しました: {e}")

    # 非表示の<input>を探してファイルパスを送信(透かし画像にアップロード)
    # upload_file_path 変数を使用
    upload_input = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[3]/div[4]/div[3]/input')
    upload_input.send_keys(upload_file_path)
    print("透かし画像をアップロードしました")

    # テキストボックスに入力するデータ(引数渡し)
    input_data = {
      'start_price': ('//*[@id="app"]/div/div[3]/div[3]/div[1]/div[3]/input', start_price_arg),
      'sokketu': ('//*[@id="app"]/div/div[3]/div[3]/div[1]/div[4]/input', sokketu_arg),
      'categoly': ('//*[@id="app"]/div/div[3]/div[3]/div[1]/div[1]/input', category_arg),
      'osusume': ('//*[@id="app"]/div/div[3]/div[3]/div[3]/div[2]/input', '1'),
    }

    dropdown_data = {
      'prefecture': ('//*[@id="app"]/div/div[3]/div[3]/div[1]/div[8]/select', '東京都'),
      'kosuu': ('//*[@id="app"]/div/div[3]/div[3]/div[1]/div[5]/select', '1'),
      'kaisaikikan': ('//*[@id="app"]/div/div[3]/div[3]/div[1]/div[6]/select', '2'),
      'finish': ('//*[@id="app"]/div/div[3]/div[3]/div[1]/div[7]/select', '2'),
      'autosale': ('//*[@id="app"]/div/div[3]/div[3]/div[5]/div[1]/select', '3'),
    }

    setumei_xpath = '//*[@id="app"]/div/div[3]/div[3]/div[1]/div[2]/textarea'

    # 説明文読み込み
    try:
        with open(content_file_path, 'r', encoding='utf-8') as file:
            long_text = file.read()
        print("説明文をファイルから読み込みました。")
    except Exception as e:
        print(f"説明文ファイルの読み込み中にエラーが発生しました: {e}")
        long_text = ""

    try:
        # 各テキストボックスに入力
        for field_name, (xpath, value) in input_data.items():
            try:
                text_box = driver.find_element(By.XPATH, xpath)
                text_box.clear()
                text_box.send_keys(value)
                print(f"{field_name} に値 '{value}' を入力しました。")
            except Exception as e:
                print(f"{field_name} の入力中にエラーが発生しました: {e}")

        # 説明文テキストボックスに長文を入力
        try:
            text_box = driver.find_element(By.XPATH, setumei_xpath)
            text_box.clear()
            text_box.send_keys(long_text)
            print("説明文をテキストボックスに入力しました。")
        except Exception as e:
            print(f"説明文の入力中にエラーが発生しました: {e}")

        # 各プルダウンに値を選択
        for field_name, (xpath, value) in dropdown_data.items():
            try:
               select_element = driver.find_element(By.XPATH, xpath)
               select = Select(select_element)
               select.select_by_visible_text(value)
               print(f"{field_name} に値 '{value}' を選択しました。")
            except Exception as e:
               print(f"{field_name} の選択中にエラーが発生しました: {e}")

        # ボタンのクリック処理
        buttons = {
          'convert_image': '//*[@id="app"]/div/div[4]/button[2]/div[1]/div/span',
          'generate_zip': '//*[@id="app"]/div/div[4]/button[1]/div[1]'
        }
        for key, xpath in buttons.items():
            driver.find_element(By.XPATH, xpath).click()
            print(f"{key} ボタンをクリックしました。")

            if key == 'convert_image':
               print("convert_image ボタンの後、10秒間待機します...")
               time.sleep(10)
            time.sleep(3)

        # ダウンロードボタン待機・クリック
        try:
            download_button_xpath = '//*[@id="app"]/div/div[4]/div[6]/div[2]'
            download_button = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, download_button_xpath))
            )
            download_button.click()
            print("『クリックしてダウンロード』ボタンをクリックしました。")

            # ダウンロード完了を監視
            print("ダウンロード待機中...")
            downloaded_file = None
            for _ in range(30):
                files = os.listdir(download_dir)
                files = [os.path.join(download_dir, f) for f in files]
                files = [f for f in files if os.path.isfile(f)]
                if files:
                     downloaded_file = max(files, key=os.path.getctime)
                     if downloaded_file.endswith(".zip"):
                        print(f"ダウンロード完了: {downloaded_file}")
                        break
                time.sleep(1)
            if not downloaded_file or not downloaded_file.endswith(".zip"):
                print("ダウンロードが完了しませんでした。")
        except Exception as e:
            print(f"ダウンロード処理中にエラーが発生しました: {e}")

    except Exception as e:
        print(f"入力処理全体でエラーが発生しました: {e}")

finally:
    print("確認のため10秒間ブラウザを保持します...")
    time.sleep(10)
    driver.quit()


