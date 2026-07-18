import pytest

from automation.utils.api_client import FrappeAPI


api = FrappeAPI()


@pytest.fixture(scope="module")
def login():

    """
    登录获取session
    """

    response = api.login(
        "Administrator",
        "admin"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Logged In"

    return api



class TestLead:


    def test_get_lead_list(self, login):
        """
        查询Lead列表
        对应Postman:
        GET /api/resource/CRM%20Lead
        """

        response = login.get_leads()


        assert response.status_code == 200


        data = response.json()


        assert "data" in data


        assert isinstance(
            data["data"],
            list
        )



    def test_create_lead_success(self, login):
        """
        新增Lead正常场景
        对应Postman:
        POST /api/resource/CRM%20Lead
        """


        lead_data = {

            "first_name":
                "pytest自动化用户",

            "mobile_no":
                "13900139001",

            "email_id":
                "pytest_lead@test.com"

        }


        response = login.create_lead(
            lead_data
        )


        assert response.status_code in [
            200,
            201
        ]


        data = response.json()


        assert "data" in data


        assert data["data"]["first_name"] == \
               "pytest自动化用户"



    def test_create_lead_empty_name(self, login):
        """
        姓名为空校验
        对应API测试用例:
        API_LEAD_004
        """


        lead_data = {

            "first_name":
                "",

            "mobile_no":
                "13900139002",

            "email_id":
                "empty@test.com"

        }


        response = login.create_lead(
            lead_data
        )


        # 不允许服务器异常
        assert response.status_code != 500



    def test_create_lead_invalid_phone(self, login):
        """
        手机号格式校验
        """


        lead_data = {

            "first_name":
                "非法手机号测试",

            "mobile_no":
                "123",

            "email_id":
                "phone@test.com"

        }


        response = login.create_lead(
            lead_data
        )


        assert response.status_code != 500