from fastapi import APIRouter, Request
from fastapi import Depends, HTTPException, Header
from config.get_db import get_db
from service.login_service import get_current_user, get_password_hash
from service.role_service import *
from mapper.schema.role_schema import *
from utils.response_tool import *
from utils.log_tool import *


roleController = APIRouter(dependencies=[Depends(get_current_user)])


@roleController.post("/role/forSelectOption", response_model=RoleSelectOptionResponseModel)
async def get_system_role_select(query_db: Session = Depends(get_db)):
    try:
        role_query_result = get_role_select_option_services(query_db)
        logger.info('获取成功')
        return response_200(data=role_query_result, message="获取成功")
    except Exception as e:
        logger.exception(e)
        return response_500(data="", message="接口异常")
