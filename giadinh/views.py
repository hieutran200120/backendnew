from rest_framework.views import APIView
from rest_framework.response import Response
from bs4 import BeautifulSoup
from rest_framework import status
import requests

class APIViews(APIView):
    def get(self, request):
        base_url = "https://phunuvietnam.vn/yeu/gia-dinh-tre.htm"
        try:
            data = []
            url = base_url
            response = requests.get(url, verify=False)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            post_holders = soup.find_all('div', class_='box-category-item')
            for post_holder in post_holders:
                entry_title = post_holder.find('h2', class_='box-category-title-text')
                title = entry_title.text.strip() if entry_title else ""
                img_tag = post_holder.find('img')
                image_url = img_tag['src'] if img_tag and 'src' in img_tag.attrs else ""
                link = "https:/" +post_holder.find('a', class_='box-category-link-title')['href']
                entry_date = post_holder.find('span', class_='box-category-time time-ago')
                date = entry_date.text.strip() if entry_date else ""
                entry_p = post_holder.find('p', class_='box-category-sapo')
                p = entry_p.text.strip() if entry_p else ""  # Corrected this line
                    # detail_data = self.get_detail_data(link)
                data.append({'title': title, 'link': link, 'image_url': image_url, 'date': date, 'p': p})
            return Response({'data': data})
        except requests.exceptions.RequestException as e:
            return Response({'error': f'Failed to fetch data from the website: {str(e)}'}, status=500)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class GetNewView(APIView):
    def get_detail_data(self, link):
        try:
            response = requests.get(link, verify=False)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            detail_content_tags = soup.find_all('div', class_='content-detail detail-content afcbc-body')
            detail_info = []
            for tag in detail_content_tags:
                p_tags = tag.find_all('p')
                img_tags = tag.find_all('img')
                for p_tag in p_tags:
                    detail_info.append({'text': p_tag.text.strip()})
                for img_tag in img_tags:
                    img_src = img_tag.get('src')  # Lấy đường dẫn của hình ảnh
                    if img_src:  # Kiểm tra nếu img_src không rỗng
                        detail_info.append({'image': img_src})
            return detail_info
        except requests.exceptions.RequestException as e:
            return [{'error': 'Failed to fetch detail data from the website:', 'details': str(e)}]
        except Exception as e:
            return [{'error': str(e)}]

    def post(self, request):
        try:
            title = request.data.get('title', '')
            base_url = "https://phunuvietnam.vn/yeu/gia-dinh-tre.htm"
            url = f"{base_url}?page=1"  # Chỉ lấy từ trang đầu tiên
            response = requests.get(url, verify=False)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            data = []
            post_holders = soup.find_all('div', class_='box-category-item')
            for post_holder in post_holders:
                entry_title = post_holder.find('h2', class_='box-category-title-text')
                post_title = entry_title.text.strip() if entry_title else ""
                if title.lower() == post_title.lower():  # Chỉ kiểm tra một lần ở đây
                    img_tag = post_holder.find('img')
                    image_url = img_tag.get('src') if img_tag else ""
                    # Tạo URL hoàn chỉnh bằng cách kết hợp đường dẫn tương đối với địa chỉ cơ bản của trang web
                    link = "https://phunuvietnam.vn" + post_holder.find('a', class_='box-category-link-title')['href']
                    detail_data = self.get_detail_data(link)
                    data.append(
                        {'title': post_title, 'link': link, 'image_url': image_url, 'detail_data': detail_data})
            return Response({'data': data}, status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            return Response({'error': f'Failed to fetch data from the website: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)