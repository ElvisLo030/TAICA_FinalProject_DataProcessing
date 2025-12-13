import googlemaps
import time
from typing import List, Dict, Any

class PlacesService:
    def __init__(self, api_key: str):
        self.client = googlemaps.Client(key=api_key)

    def find_nearby_restaurants(self, location: str, radius: int = 1000, use_coordinates: bool = False) -> List[Dict[str, Any]]:
        """
        搜尋指定地點附近的餐廳與食物類別店家。
        會自動抓取所有分頁資料 (最多 60 筆/每種類型)。

        Args:
            location (str): 中心點位置 (地址、Plus Code 或 "lat,lng" 格式的座標)
            radius (int): 搜尋半徑 (公尺)
            use_coordinates (bool): 是否直接使用座標搜尋

        Returns:
            List[Dict[str, Any]]: 餐廳列表
        """
        try:
            lat_lng = None
            
            if use_coordinates:
                # 簡單驗證座標格式
                if ',' not in location:
                     raise ValueError("座標格式錯誤，請使用 '緯度,經度' (例如: 25.033964,121.564468)")
                lat_lng = location
            else:
                # 地址或 Plus Code 透過 Geocoding API 轉換
                geocode_result = self.client.geocode(location)
                
                if not geocode_result:
                    raise ValueError(f"找不到地點: {location}")

                lat_lng = geocode_result[0]['geometry']['location']
            
            all_results = []
            seen_place_ids = set()
            
            # 搜尋類型：restaurant 和 food
            search_types = ['restaurant', 'food']
            
            for type_val in search_types:
                next_page_token = None
                
                # 最多嘗試 3 頁 (Google API 限制)
                for _ in range(3):
                    try:
                        places_result = self.client.places_nearby(
                            location=lat_lng,
                            radius=radius,
                            type=type_val,
                            language='zh-TW',
                            page_token=next_page_token
                        )
                        
                        results = places_result.get('results', [])
                        for place in results:
                            place_id = place.get('place_id')
                            if place_id and place_id not in seen_place_ids:
                                all_results.append(place)
                                seen_place_ids.add(place_id)
                        
                        next_page_token = places_result.get('next_page_token')
                        if not next_page_token:
                            break
                            
                        # Google API 要求在使用 next_page_token 前需稍作等待，否則會報錯
                        time.sleep(2)
                        
                    except Exception as e:
                        print(f"搜尋類型 {type_val} 時發生錯誤: {e}")
                        break

            return all_results

        except Exception as e:
            print(f"發生錯誤: {e}")
            return []
