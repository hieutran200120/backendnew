from rest_framework.views import APIView
from rest_framework.response import Response
from bs4 import BeautifulSoup
from rest_framework import status
import requests

class GetNewView(APIView):
    def post(self, request):
        # Danh sách các URL bạn muốn lấy dữ liệu từ
        base_urls = [
            "https://phunuvietnam.vn/lao-dong-viec-lam.htm",
                "https://phunuvietnam.vn/van-hoa-giai-tri.htm",
                "https://phunuvietnam.vn/yeu/gia-dinh-tre.htm",
                "https://phunuvietnam.vn/van-hoa-giai-tri.htm",
                "https://phunuvietnam.vn/chinh-tri-xa-hoi.htm",
                "https://phunuvietnam.vn/khoe.htm",
                "https://phunuvietnam.vn/lam-cha-me.htm",
                "https://hoilhpn.angiang.gov.vn/cong-tac-tuyen-giao-chinh-sach-luat-phap",
                "https://phunuvietnam.vn/giao-duc.htm",
                "https://phunuvietnam.vn/luat-va-doi.htm",
                "https://phunuvietnam.vn",
                "https://phunuvietnam.vn/dep/dep-tich-cuc.htm",
                "https://phunuvietnam.vn/nha-dat/moi-nong.htm",
            "https://phunuvietnam.vn/tim-kiem.htm?keywords=h%E1%BB%99i%20li%C3%AAn%20hi%E1%BB%87p%20ph%E1%BB%A5%20n%E1%BB%AF",
            "https://phunuvietnam.vn/tim-kiem.htm?keywords=ch%C4%83m%20s%C3%B3c%20tr%E1%BA%BB%20em"
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
class GetView(APIView):
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
            title = request.data.get('title', '').lower()  # Lấy tiêu đề từ dữ liệu gửi lên và chuyển thành chữ thường
            base_urls = [
                "https://phunuvietnam.vn/lao-dong-viec-lam.htm",
                "https://phunuvietnam.vn/van-hoa-giai-tri.htm",
                "https://phunuvietnam.vn/yeu/gia-dinh-tre.htm",
                "https://phunuvietnam.vn/van-hoa-giai-tri.htm",
                "https://phunuvietnam.vn/chinh-tri-xa-hoi.htm",
                "https://phunuvietnam.vn/khoe.htm",
                "https://phunuvietnam.vn/lam-cha-me.htm",
                "https://hoilhpn.angiang.gov.vn/cong-tac-tuyen-giao-chinh-sach-luat-phap",
                "https://phunuvietnam.vn/giao-duc.htm",
                "https://phunuvietnam.vn/luat-va-doi.htm",
                "https://phunuvietnam.vn",
                "https://phunuvietnam.vn/dep/dep-tich-cuc.htm",
                "https://phunuvietnam.vn/nha-dat/moi-nong.htm",
                "https://phunuvietnam.vn/tim-kiem.htm?keywords=h%E1%BB%99i%20li%C3%AAn%20hi%E1%BB%87p%20ph%E1%BB%A5%20n%E1%BB%AF",
                "https://phunuvietnam.vn/tim-kiem.htm?keywords=ch%C4%83m%20s%C3%B3c%20tr%E1%BA%BB%20em"

            ]
            data = []
            for base_url in base_urls:
                response = requests.get(base_url, verify=False)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                post_holders = soup.find_all('div', class_='box-category-item')
                for post_holder in post_holders:
                    entry_title = post_holder.find('h2', class_='box-category-title-text')
                    post_title = entry_title.text.strip().lower() if entry_title else ""
                    # Thay vì so sánh chính xác giữa tiêu đề và từ khóa, chúng ta kiểm tra xem từ khóa có là một phần của tiêu đề không
                    if title.lower() == post_title.lower():
                        img_tag = post_holder.find('img')
                        image_url = img_tag.get('src') if img_tag else ""
                        # Tạo URL hoàn chỉnh bằng cách kết hợp đường dẫn tương đối với địa chỉ cơ bản của trang web
                        link = "https://phunuvietnam.vn" + post_holder.find('a', class_='box-category-link-title')[
                            'href']
                        detail_data = self.get_detail_data(link)
                        data.append(
                            {'title': post_title, 'link': link, 'image_url': image_url, 'detail_data': detail_data})
            return Response({'data': data}, status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            return Response({'error': f'Failed to fetch data from the website: {str(e)}'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)