import os
import requests
from bs4 import BeautifulSoup

class TikTokDownloader:
    def __init__(self, output_directory="downloaded_videos"):
        """
        TikTokDownloaderクラスの初期化
        output_directory: ダウンロードした動画を保存するフォルダ名
        """
        # 動画保存先ディレクトリの設定
        self.output_folder = output_directory
        # ディレクトリが存在しない場合は作成
        os.makedirs(self.output_folder, exist_ok=True)
        
        # API設定の初期化
        self.setup_api_config()
        
        print(f"TikTokDownloader初期化完了 - 保存先: {self.output_folder}")
        
    def setup_api_config(self):
        """
        API通信用の設定を初期化
        TikTok動画情報取得用のAPIエンドポイントとヘッダー情報を設定
        """
        # TikTok動画情報取得用のAPIエンドポイント
        self.api_endpoint = "https://savetik.co/api/ajaxSearch"
        
        # HTTP通信用ヘッダー設定（ブラウザのふりをするための情報）
        self.request_headers = {
            'Accept': '*/*',  # どんなタイプのデータでも受け取る
            'Accept-Language': 'en-US,en;q=0.9',  # 英語を優先して受け取る
            'Content-Type': 'application/x-www-form-urlencoded',  # フォームデータの形式で送信
            'Origin': 'https://savetik.co',  # リクエストの送信元サイト
            'Priority': 'u=1, i',  # リクエストの優先度設定
            'Referer': 'https://savetik.co/en2',  # このページからアクセスしたことを示す
            'Sec-Ch-Ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',  # ブラウザの種類とバージョン
            'Sec-Ch-Ua-Mobile': '?0',  # モバイルデバイスではないことを示す
            'Sec-Ch-Ua-Platform': '"Windows"',  # 使用しているOS情報
            'Sec-Fetch-Dest': 'empty',  # リクエストの目的地情報
            'Sec-Fetch-Mode': 'cors',  # CORS（クロスオリジン）リクエストであることを示す
            'Sec-Fetch-Site': 'same-origin',  # 同じサイト内でのリクエストであることを示す
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',  # ブラウザの詳細情報
            'X-Requested-With': 'XMLHttpRequest'  # AjaxリクエストであることをAPIに伝える
        }
        
        print("API設定完了")
        
    def check_connection(self):
        """
        API接続テスト機能
        設定したエンドポイントに接続できるかを確認
        """
        try:
            # テスト用のデータ
            test_data = {
                'q': 'https://www.tiktok.com/@test/video/test',
                'lang': 'en'
            }
            
            # APIへのテスト接続
            response = requests.post(
                self.api_endpoint, 
                data=test_data, 
                headers=self.request_headers,
                timeout=10
            )
            
            # ステータスコードの確認（200なら成功、400番台や500番台はエラー）
            if response.status_code == 200:
                print("✓ API接続テスト成功")
                return True
            else:
                print(f"✗ API接続エラー - ステータスコード: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as error:
            print(f"✗ 接続テスト失敗: {error}")
            return False
        
    def handle_request_error(self, error, url):
        """
        HTTPリクエストエラーの処理
        error: 発生したエラーオブジェクト
        url: エラーが発生したURL
        """
        if isinstance(error, requests.exceptions.HTTPError):
            print(f"HTTPエラーが発生しました - URL: {url}")
            print(f"ステータスコード: {error.response.status_code}")
        elif isinstance(error, requests.exceptions.ConnectionError):
            print(f"接続エラーが発生しました - URL: {url}")
            print("ネットワーク接続を確認してください")
        elif isinstance(error, requests.exceptions.Timeout):
            print(f"タイムアウトエラーが発生しました - URL: {url}")
            print("時間をおいて再度お試しください")
        elif isinstance(error, requests.exceptions.RequestException):
            print(f"リクエストエラーが発生しました - URL: {url}")
            print(f"エラー詳細: {error}")
        else:
            print(f"予期しないエラーが発生しました: {error}")
            
    def extract_download_url(self, tiktok_url):
        """
        TikTok動画URLからダウンロード用URLを抽出
        tiktok_url: TikTokの動画URL
        """
        try:
            # APIに送信するデータの準備
            request_data = {
                'q': tiktok_url,  # TikTokの動画URL
                'lang': 'en'      # 言語設定を英語に指定
            }
            
            print(f"動画URL解析開始: {tiktok_url}")
            
            # APIにPOSTリクエストを送信
            api_response = requests.post(
                self.api_endpoint,           # APIのエンドポイント
                data=request_data,           # 送信するデータ
                headers=self.request_headers # HTTPヘッダー情報
            )
            
            # HTTPエラーがある場合は例外を発生させる
            api_response.raise_for_status()
            
            # HTML解析処理を呼び出し
            download_link = self.parse_download_link(api_response.text)
            
            if download_link:
                print(f"✓ ダウンロードURL取得成功")
                return download_link
            else:
                print("✗ ダウンロードURLが見つかりませんでした")
                return None
                
        except requests.exceptions.HTTPError as http_error:
            print(f"HTTPエラーが発生: ステータスコード {api_response.status_code}")
            self.handle_request_error(http_error, tiktok_url)
            return None
        except requests.exceptions.RequestException as request_error:
            print(f"リクエストエラーが発生: {request_error}")
            self.handle_request_error(request_error, tiktok_url)
            return None
        except Exception as unexpected_error:
            print(f"予期しないエラーが発生: {unexpected_error}")
            return None
        
    def parse_download_link(self, html_content):
        """
        HTML内容を解析してダウンロードリンクを抽出
        html_content: APIから取得したHTML文字列
        """
        try:
            # BeautifulSoupでHTML文書を解析
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # HTML内の全てのaタグ（リンクタグ）を取得
            all_link_tags = soup.find_all('a')
            
            print(f"検索対象のリンク数: {len(all_link_tags)}")
            
            # 各リンクタグを順番に確認
            for link_tag in all_link_tags:
                # リンクのテキスト内容を取得
                link_text = link_tag.text.strip()
                # リンクのclass属性を取得（None の場合は空リスト）
                link_classes = link_tag.get('class', [])
                
                # 'Download MP4 HD'というテキストまたは'dl-success'クラスを探す
                if 'Download MP4 HD' in link_text or 'dl-success' in link_classes:
                    # href属性からダウンロードURLを取得
                    download_url = link_tag.get('href')
                    
                    if download_url:
                        print(f"ダウンロードリンク発見: {link_text}")
                        # URLの不要な文字を除去
                        cleaned_url = download_url.replace('\\"', '')
                        return cleaned_url
            
            # 該当するリンクが見つからない場合
            print("該当するダウンロードリンクが見つかりませんでした")
            return None
            
        except Exception as parse_error:
            print(f"HTML解析エラー: {parse_error}")
            return None
        
    def validate_tiktok_url(self, url):
        """
        TikTokのURLが正しい形式かを検証
        url: 検証するURL文字列
        """
        # TikTokの有効なドメインパターン
        valid_domains = [
            'tiktok.com',
            'www.tiktok.com',
            'm.tiktok.com',
            'vm.tiktok.com'
        ]
        
        # URLの基本チェック
        if not url or not isinstance(url, str):
            print("✗ URLが入力されていません")
            return False
        
        # httpsまたはhttpで始まっているかチェック
        if not (url.startswith('https://') or url.startswith('http://')):
            print("✗ URLはhttps://またはhttp://で始まる必要があります")
            return False
        
        # TikTokのドメインが含まれているかチェック
        is_valid_domain = any(domain in url.lower() for domain in valid_domains)
        
        if not is_valid_domain:
            print("✗ TikTokのURLではありません")
            return False
        
        print("✓ URLの形式が正しいです")
        return True
    
    def get_video_download_url(self, tiktok_url):
        """
        TikTokのURLから動画ダウンロードURLを取得する統合処理
        tiktok_url: TikTokの動画URL
        """
        print(f"\n=== 動画URL取得処理開始 ===")
        
        # Step1: URL形式の検証
        if not self.validate_tiktok_url(tiktok_url):
            return None
        
        # Step2: ダウンロードURL抽出
        download_url = self.extract_download_url(tiktok_url)
        
        if download_url:
            print(f"✓ 動画ダウンロードURL取得完了")
            return download_url
        else:
            print("✗ 動画ダウンロードURL取得失敗")
            return None
        
    def download_video_file(self, download_url, save_filename):
        """
        動画ファイルをダウンロードして指定されたパスに保存
        download_url: 動画のダウンロードURL
        save_filename: 保存するファイル名
        """
        try:
            print(f"動画ダウンロード開始: {save_filename}")
            
            # URLの不要な文字を削除
            cleaned_url = download_url.replace('\\"', '')
            
            # 動画ファイルのダウンロード実行
            video_response = requests.get(cleaned_url, timeout=30)
            # HTTPエラーチェック
            video_response.raise_for_status()
            
            # ファイルサイズをMBで表示
            file_size_mb = len(video_response.content) / (1024 * 1024)
            print(f"ダウンロードサイズ: {file_size_mb:.2f} MB")
            
            # 動画ファイルを保存
            save_path = os.path.join(self.output_folder, save_filename)
            with open(save_path, 'wb') as video_file:
                video_file.write(video_response.content)
            
            print(f"✓ 動画保存完了: {save_path}")
            return True
            
        except requests.exceptions.HTTPError as http_error:
            print(f"ダウンロード中にHTTPエラーが発生: {http_error}")
            return False
        except requests.exceptions.Timeout:
            print("ダウンロードがタイムアウトしました（30秒）")
            return False
        except requests.exceptions.RequestException as request_error:
            print(f"ダウンロード中にエラーが発生: {request_error}")
            return False
        except IOError as io_error:
            print(f"ファイル保存中にエラーが発生: {io_error}")
            return False
        except Exception as unexpected_error:
            print(f"予期しないエラーが発生: {unexpected_error}")
            return False
    
    def generate_filename(self, download_url):
        """
        ダウンロードURLから適切なファイル名を生成
        download_url: 動画のダウンロードURL
        """
        try:
            # URLから動画IDを抽出
            url_parts = download_url.split('/')
            video_id = url_parts[-1].split('?')[0]  # URLパラメータを除去
            
            # ファイル名に使えない文字を除去
            safe_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_"
            cleaned_id = ''.join(char for char in video_id if char in safe_chars)
            
            # ファイル名が短すぎる場合はタイムスタンプを追加
            if len(cleaned_id) < 5:
                import time
                timestamp = int(time.time())
                cleaned_id = f"video_{timestamp}"
            
            # 拡張子を追加
            filename = f"{cleaned_id}.mp4"
            
            print(f"生成されたファイル名: {filename}")
            return filename
            
        except Exception as filename_error:
            print(f"ファイル名生成エラー: {filename_error}")
            # フォールバック用のファイル名
            import time
            timestamp = int(time.time())
            return f"tiktok_video_{timestamp}.mp4"
        
    def process_video_download(self, tiktok_url):
        """
        TikTokのURLから動画をダウンロードする全工程処理
        tiktok_url: TikTokの動画URL
        """
        print(f"\n{'='*50}")
        print(f"動画ダウンロード処理開始")
        print(f"URL: {tiktok_url}")
        print(f"{'='*50}")
        
        # Step1: ダウンロードURL取得
        download_url = self.get_video_download_url(tiktok_url)
        if not download_url:
            print("✗ ダウンロードURL取得に失敗しました")
            return False
        
        # Step2: ファイル名生成
        filename = self.generate_filename(download_url)
        
        # Step3: 動画ファイルダウンロード
        download_success = self.download_video_file(download_url, filename)
        
        if download_success:
            print(f"✓ 動画ダウンロード完了: {filename}")
            return True
        else:
            print("✗ 動画ダウンロードに失敗しました")
            return False
        
    def run_interactive_mode(self):
        """
        対話式の動画ダウンロードモード
        ユーザーが終了するまで繰り返し動画をダウンロード
        """
        print("\n" + "="*60)
        print("TikTok動画ダウンローダー - 対話モード")
        print("="*60)
        print("使い方:")
        print("1. TikTokの動画URLを入力してください")
        print("2. 'exit'と入力すると終了します")
        print("3. 'help'と入力すると使い方を再表示します")
        print("-"*60)
        
        download_count = 0  # ダウンロード成功数のカウンター
        
        while True:
            try:
                # ユーザー入力の取得
                user_input = input("\nTikTok動画URL >>> ").strip()
                
                # 終了コマンドの確認
                if user_input.lower() == 'exit':
                    print(f"\n動画ダウンローダーを終了します")
                    print(f"総ダウンロード数: {download_count}個")
                    break
                
                # ヘルプコマンドの確認
                if user_input.lower() == 'help':
                    print("\n--- 使い方 ---")
                    print("TikTokの動画URLを入力: 動画をダウンロード")
                    print("exit: プログラムを終了")
                    print("help: この使い方を表示")
                    continue
                
                # 空の入力をスキップ
                if not user_input:
                    print("URLを入力してください")
                    continue
                
                # 動画ダウンロード処理実行
                success = self.process_video_download(user_input)
                if success:
                    download_count += 1
                
            except KeyboardInterrupt:
                print(f"\n\nプログラムが中断されました")
                print(f"総ダウンロード数: {download_count}個")
                break
            except Exception as interface_error:
                print(f"エラーが発生しました: {interface_error}")
                print("続行しますか？ (y/n)")
                continue_choice = input(">>> ").strip().lower()
                if continue_choice not in ['y', 'yes']:
                    break
    
def main():
    """
    TikTokDownloaderのフル機能テスト
    対話式モードでユーザーからの入力を受け付け
    """
    print("=== TikTok動画ダウンローダー ===")
    
    # TikTokDownloaderクラスのインスタンス作成
    downloader = TikTokDownloader()
    
    # 接続テストの実行
    print("\n--- 初期接続テスト ---")
    connection_result = downloader.check_connection()
    
    if not connection_result:
        print("API接続に問題があります。プログラムを終了します。")
        return
    
    print("✓ 接続テスト完了")
    
    # 対話式モードの開始
    downloader.run_interactive_mode()

if __name__ == "__main__":
    main()