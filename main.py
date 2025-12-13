from config import Config
from places_service import PlacesService
from data_exporter import DataExporter

def main():
    try:
        # 初始化設定
        config = Config()
        
        # 初始化服務
        service = PlacesService(config.api_key)
        
        # 選擇輸入模式
        print("請選擇輸入模式:")
        print("1. 輸入地址或 Plus Code (例如: 台北車站 或 8QJ6+64 Taipei)")
        print("2. 輸入座標 (例如: 25.0478,121.5170)")
        
        mode = input("請輸入選項 (1 或 2): ").strip()
        
        use_coordinates = False
        location_prompt = "請輸入您要搜尋的地點 (地址/Plus Code): "
        
        if mode == '2':
            use_coordinates = True
            location_prompt = "請輸入座標 (格式: 緯度,經度，例如: 25.0478,121.5170): "
        elif mode != '1':
            print("無效的選項，將預設使用地址搜尋模式。")

        # 獲取使用者輸入
        location = input(location_prompt).strip()
        if not location:
            print("地點不能為空。")
            return

        radius_input = input("請輸入搜尋半徑 (公尺，預設 1000): ")
        
        radius = 1000
        if radius_input.strip():
            try:
                radius = int(radius_input)
            except ValueError:
                print("輸入的半徑無效，將使用預設值 1000 公尺。")

        print(f"\n正在搜尋 {location} 附近 {radius} 公尺內的餐廳與美食...\n")
        print("提示：為獲取更多資料，程式將自動搜尋多頁結果，請稍候...")
        
        # 執行搜尋
        restaurants = service.find_nearby_restaurants(location, radius=radius, use_coordinates=use_coordinates)
        
        # 顯示結果
        if not restaurants:
            print("找不到任何餐廳。")
        else:
            print(f"共找到 {len(restaurants)} 間餐廳/美食店家：")
            print("-" * 50)
            
            # 只顯示前 5 筆預覽，以免畫面太長
            preview_count = 5
            for i, place in enumerate(restaurants[:preview_count]):
                name = place.get('name', '未知名稱')
                address = place.get('vicinity', '未知地址')
                rating = place.get('rating', '無評分')
                user_ratings_total = place.get('user_ratings_total', 0)
                
                print(f"名稱: {name}")
                print(f"地址: {address}")
                print(f"評分: {rating} ({user_ratings_total} 則評論)")
                print("-" * 50)
            
            if len(restaurants) > preview_count:
                print(f"...還有 {len(restaurants) - preview_count} 筆資料 (請查看 CSV)")

            # 匯出 CSV
            print("\n正在匯出資料...")
            filename = DataExporter.export_to_csv(restaurants)
            if filename:
                print(f"資料已成功匯出至: {filename}")
            else:
                print("匯出失敗。")

    except ValueError as e:
        print(f"設定錯誤: {e}")
    except Exception as e:
        print(f"執行時發生未預期的錯誤: {e}")

if __name__ == "__main__":
    main()
