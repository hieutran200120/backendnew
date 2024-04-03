from rest_framework.views import APIView
from rest_framework.response import Response
from bs4 import BeautifulSoup
import requests

class GetNewView(APIView):
    def post(self, request):
        # Danh sách các URL bạn muốn lấy dữ liệu từ
        base_urls = [
            "https://phunuvietnam.vn/lao-dong-viec-lam.htm",
            "https://phunuvietnam.vn/van-hoa-giai-tri.htm",
            "https://phunuvietnam.vn/yeu/gia-dinh-tre.htm"
        ]

        try:
            search_term = request.data.get('title', '').lower()  # Lấy tiêu đề tìm kiếm từ dữ liệu POST
            data = []

            # Lặp qua mỗi URL trong danh sách base_urls
            for base_url in base_urls:
                response = requests.get(base_url, verify=False)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                post_holders = soup.find_all('div', class_='box-category-item')
                for post_holder in post_holders:
                    entry_title = post_holder.find('h2', class_='box-category-title-text')
                    title = entry_title.text.strip() if entry_title else ""
                    # Kiểm tra xem tiêu đề có chứa chuỗi tìm kiếm không (không phân biệt chữ hoa và chữ thường)
                    if search_term.lower() in title.lower():
                        img_tag = post_holder.find('img')
                        image_url = img_tag['src'] if img_tag and 'src' in img_tag.attrs else ""
                        link = "https://" + post_holder.find('a', class_='box-category-link-title')['href']
                        entry_date = post_holder.find('span', class_='box-category-time time-ago')
                        date = entry_date.text.strip() if entry_date else ""
                        entry_p = post_holder.find('p', class_='box-category-sapo')
                        p = entry_p.text.strip() if entry_p else ""  # Corrected this line
                        data.append({'title': title, 'link': link, 'image_url': image_url, 'date': date, 'p': p})

            return Response({'data': data})
        except requests.exceptions.RequestException as e:
            return Response({'error': f'Failed to fetch data from the website: {str(e)}'}, status=500)
        except Exception as e:
            return Response({'error': str(e)}, status=500)
