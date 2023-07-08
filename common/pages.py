from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from common.customresponse import CustomResponse


class MyPage(PageNumberPagination):
    page_size = 20  # 每页显示数量
    max_page_size = 1000  # 每页最大显示数量。
    page_size_query_param = 'size'  # 每页数量的参数名称
    page_query_param = 'page'  # 页码的参数名称

    def get_paginated_response(self, data):
        return CustomResponse(data=data, code=200, msg="OK", status=status.HTTP_200_OK, count=self.page.paginator.count,
                              next=self.get_next_link(), previous=self.get_previous_link())


class CustomPagination(PageNumberPagination):
    page_size = 15  # 每页的数量
    page_size_query_param = 'size'  # URL 参数中指定每页数量的参数名
    page_query_param = 'page'  # 页码的参数名称
    max_page_size = 1000  # 最大允许的每页数量

    def get_paginated_response(self, data):
        return {
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'data': data
        }