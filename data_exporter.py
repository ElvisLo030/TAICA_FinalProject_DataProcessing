import csv
import json
from datetime import datetime
from typing import List, Dict, Any

class DataExporter:
    @staticmethod
    def export_to_csv(data: List[Dict[str, Any]], filename_prefix: str = "restaurants") -> str:
        """
        將資料匯出成 CSV 檔案。
        只保留: name, opening_hours, rating, types, vicinity, lat, lng
        
        Args:
            data (List[Dict[str, Any]]): 要匯出的資料列表
            filename_prefix (str): 檔案名稱前綴
            
        Returns:
            str: 產生的檔案路徑
        """
        if not data:
            print("沒有資料可以匯出。")
            return ""

        # 產生帶有時間戳記的檔名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{filename_prefix}_{timestamp}.csv"
        
        # 定義固定欄位
        fieldnames = ['name', 'opening_hours', 'rating', 'types', 'vicinity', 'lat', 'lng']
        
        processed_data = []
        for item in data:
            # 檢查 types 是否包含 'restaurant' 或 'food'
            types_list = item.get('types', [])
            if not any(t in types_list for t in ['restaurant', 'food']):
                continue

            # 建立基本欄位字典 (不包含 lat/lng，因為它們在 nested structure)
            basic_fields = ['name', 'opening_hours', 'rating', 'types', 'vicinity']
            filtered_item = {k: item.get(k, '') for k in basic_fields}
            
            # 提取座標
            geometry = item.get('geometry', {})
            location = geometry.get('location', {})
            filtered_item['lat'] = location.get('lat', '')
            filtered_item['lng'] = location.get('lng', '')
            
            # 處理特殊欄位格式，避免 CSV 格式亂掉
            
            # opening_hours 通常是 dict，轉為 JSON 字串較易讀
            if isinstance(filtered_item['opening_hours'], dict):
                # 嘗試提取 open_now 讓顯示更直觀，或者直接 dump 整個 dict
                # 這裡保留原始結構但轉為字串
                open_now = filtered_item['opening_hours'].get('open_now')
                filtered_item['opening_hours'] = f"營業中: {'是' if open_now else '否'}" if open_now is not None else "未知"
            
            # types 是 list，轉為字串
            if isinstance(filtered_item['types'], list):
                filtered_item['types'] = ", ".join(filtered_item['types'])
                
            processed_data.append(filtered_item)

        try:
            with open(filename, mode='w', newline='', encoding='utf-8-sig') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for item in processed_data:
                    writer.writerow(item)
            
            return filename
        except Exception as e:
            print(f"匯出 CSV 時發生錯誤: {e}")
            return ""
