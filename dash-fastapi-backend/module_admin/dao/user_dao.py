from sqlalchemy import and_, or_, desc, func
from sqlalchemy.orm import Session
from module_admin.entity.do.user_do import SysUser, SysUserRole, SysUserPost
from module_admin.entity.do.role_do import SysRole, SysRoleMenu
from module_admin.entity.do.dept_do import SysDept
from module_admin.entity.do.post_do import SysPost
from module_admin.entity.do.menu_do import SysMenu
from module_admin.entity.vo.user_vo import UserModel, UserRoleModel, UserPostModel, CurrentUserInfo, UserQueryModel
from utils.time_format_util import list_format_datetime, format_datetime_dict_list
from datetime import datetime, time
from typing import Union, List


class UserDao:
    """
    用户管理模块数据库操作层
    """

    @classmethod
    def get_user_by_name(cls, db: Session, user_name: str):
        """
        根据用户名获取用户信息
        :param db: orm对象
        :param user_name: 用户名
        :return: 当前用户名的用户信息对象
        """
        query_user_info = db.query(SysUser) \
            .filter(SysUser.status == 0, SysUser.del_flag == 0, SysUser.user_name == user_name) \
            .order_by(desc(SysUser.create_time)).distinct().first()

        return query_user_info

    @classmethod
    def get_user_by_info(cls, db: Session, user: UserModel):
        """
        根据用户参数获取用户信息
        :param db: orm对象
        :param user: 用户参数
        :return: 当前用户参数的用户信息对象
        """
        query_user_info = db.query(SysUser) \
            .filter(SysUser.del_flag == 0,
                    SysUser.user_name == user.user_name) \
            .order_by(desc(SysUser.create_time)).distinct().first()

        return query_user_info

    @classmethod
    def get_user_by_id(cls, db: Session, user_id: int):
        """
        根据user_id获取用户信息
        :param db: orm对象
        :param user_id: 用户id
        :return: 当前user_id的用户信息对象
        """
        query_user_basic_info = db.query(SysUser) \
            .filter(SysUser.status == 0, SysUser.del_flag == 0, SysUser.user_id == user_id) \
            .distinct().all()
        query_user_dept_info = db.query(SysDept).select_from(SysUser) \
            .filter(SysUser.status == 0, SysUser.del_flag == 0, SysUser.user_id == user_id) \
            .outerjoin(SysDept, and_(SysUser.dept_id == SysDept.dept_id, SysDept.status == 0, SysDept.del_flag == 0)) \
            .distinct().all()
        query_user_role_info = db.query(SysRole).select_from(SysUser) \
            .filter(SysUser.status == 0, SysUser.del_flag == 0, SysUser.user_id == user_id) \
            .outerjoin(SysUserRole, SysUser.user_id == SysUserRole.user_id) \
            .outerjoin(SysRole, and_(SysUserRole.role_id == SysRole.role_id, SysRole.status == 0, SysRole.del_flag == 0)) \
            .distinct().all()
        query_user_post_info = db.query(SysPost).select_from(SysUser) \
            .filter(SysUser.status == 0, SysUser.del_flag == 0, SysUser.user_id == user_id) \
            .outerjoin(SysUserPost, SysUser.user_id == SysUserPost.user_id) \
            .outerjoin(SysPost, and_(SysUserPost.post_id == SysPost.post_id, SysPost.status == 0)) \
            .distinct().all()
        query_user_menu_info = []
        for item in query_user_role_info:
            if item.role_id == 1:
                query_user_menu_info = db.query(SysMenu) \
                    .filter(SysMenu.status == 0) \
                    .distinct().all()
                break
            else:
                query_user_menu_info = db.query(SysMenu).select_from(SysUser) \
                    .filter(SysUser.status == 0, SysUser.del_flag == 0, SysUser.user_id == user_id) \
                    .outerjoin(SysUserRole, SysUser.user_id == SysUserRole.user_id) \
                    .outerjoin(SysRole, and_(SysUserRole.role_id == SysRole.role_id, SysRole.status == 0, SysRole.del_flag == 0)) \
                    .outerjoin(SysRoleMenu, SysRole.role_id == SysRoleMenu.role_id) \
                    .outerjoin(SysMenu, and_(SysRoleMenu.menu_id == SysMenu.menu_id, SysMenu.status == 0)) \
                    .order_by(SysMenu.order_num) \
                    .distinct().all()
        results = dict(
            user_basic_info=list_format_datetime(query_user_basic_info),
            user_dept_info=list_format_datetime(query_user_dept_info),
            user_role_info=list_format_datetime(query_user_role_info),
            user_post_info=list_format_datetime(query_user_post_info),
            user_menu_info=list_format_datetime(query_user_menu_info)
        )

        return CurrentUserInfo(**results)

    @classmethod
    def get_user_detail_by_id(cls, db: Session, user_id: int):
        """
        根据user_id获取用户详细信息
        :param db: orm对象
        :param user_id: 用户id
        :return: 当前user_id的用户信息对象
        """
        query_user_basic_info = db.query(SysUser) \
            .filter(SysUser.del_flag == 0, SysUser.user_id == user_id) \
            .distinct().all()
        query_user_dept_info = db.query(SysDept).select_from(SysUser) \
            .filter(SysUser.del_flag == 0, SysUser.user_id == user_id) \
            .outerjoin(SysDept, and_(SysUser.dept_id == SysDept.dept_id, SysDept.status == 0, SysDept.del_flag == 0)) \
            .distinct().all()
        query_user_role_info = db.query(SysRole).select_from(SysUser) \
            .filter(SysUser.del_flag == 0, SysUser.user_id == user_id) \
            .outerjoin(SysUserRole, SysUser.user_id == SysUserRole.user_id) \
            .outerjoin(SysRole, and_(SysUserRole.role_id == SysRole.role_id, SysRole.status == 0, SysRole.del_flag == 0)) \
            .distinct().all()
        query_user_post_info = db.query(SysPost).select_from(SysUser) \
            .filter(SysUser.del_flag == 0, SysUser.user_id == user_id) \
            .outerjoin(SysUserPost, SysUser.user_id == SysUserPost.user_id) \
            .outerjoin(SysPost, and_(SysUserPost.post_id == SysPost.post_id, SysPost.status == 0)) \
            .distinct().all()
        query_user_menu_info = db.query(SysMenu).select_from(SysUser) \
            .filter(SysUser.del_flag == 0, SysUser.user_id == user_id) \
            .outerjoin(SysUserRole, SysUser.user_id == SysUserRole.user_id) \
            .outerjoin(SysRole, and_(SysUserRole.role_id == SysRole.role_id, SysRole.status == 0, SysRole.del_flag == 0)) \
            .outerjoin(SysRoleMenu, SysRole.role_id == SysRoleMenu.role_id) \
            .outerjoin(SysMenu, and_(SysRoleMenu.menu_id == SysMenu.menu_id, SysMenu.status == 0)) \
            .distinct().all()
        results = dict(
            user_basic_info=list_format_datetime(query_user_basic_info),
            user_dept_info=list_format_datetime(query_user_dept_info),
            user_role_info=list_format_datetime(query_user_role_info),
            user_post_info=list_format_datetime(query_user_post_info),
            user_menu_info=list_format_datetime(query_user_menu_info)
        )

        return CurrentUserInfo(**results)

    @classmethod
    def get_user_list(cls, db: Session, query_object: UserQueryModel):
        """
        根据查询参数获取用户列表信息
        :param db: orm对象
        :param query_object: 查询参数对象
        :return: 用户列表信息对象
        """
        user_list = db.query(SysUser, SysDept) \
            .filter(SysUser.del_flag == 0,
                    or_(SysUser.dept_id == query_object.dept_id, SysUser.dept_id.in_(
                        db.query(SysDept.dept_id).filter(func.find_in_set(query_object.dept_id, SysDept.ancestors))
                    )) if query_object.dept_id else True,
                    SysUser.user_name.like(f'%{query_object.user_name}%') if query_object.user_name else True,
                    SysUser.nick_name.like(f'%{query_object.nick_name}%') if query_object.nick_name else True,
                    SysUser.email.like(f'%{query_object.email}%') if query_object.email else True,
                    SysUser.phonenumber.like(f'%{query_object.phonenumber}%') if query_object.phonenumber else True,
                    SysUser.status == query_object.status if query_object.status else True,
                    SysUser.sex == query_object.sex if query_object.sex else True,
                    SysUser.create_time.between(
                        datetime.combine(datetime.strptime(query_object.create_time_start, '%Y-%m-%d'), time(00, 00, 00)),
                        datetime.combine(datetime.strptime(query_object.create_time_end, '%Y-%m-%d'), time(23, 59, 59)))
                    if query_object.create_time_start and query_object.create_time_end else True
                    ) \
            .outerjoin(SysDept, and_(SysUser.dept_id == SysDept.dept_id, SysDept.status == 0, SysDept.del_flag == 0)) \
            .distinct().all()

        result_list: List[Union[dict, None]] = []
        if user_list:
            for item in user_list:
                obj = dict(
                    user_id=item[0].user_id,
                    dept_id=item[0].dept_id,
                    dept_name=item[1].dept_name if item[1] else '',
                    user_name=item[0].user_name,
                    nick_name=item[0].nick_name,
                    user_type=item[0].user_type,
                    email=item[0].email,
                    phonenumber=item[0].phonenumber,
                    sex=item[0].sex,
                    avatar=item[0].avatar,
                    status=item[0].status,
                    del_flag=item[0].del_flag,
                    login_ip=item[0].login_ip,
                    login_date=item[0].login_date,
                    create_by=item[0].create_by,
                    create_time=item[0].create_time,
                    update_by=item[0].update_by,
                    update_time=item[0].update_time,
                    remark=item[0].remark
                )
                result_list.append(obj)

        return format_datetime_dict_list(result_list)

    @classmethod
    def add_user_dao(cls, db: Session, user: UserModel):
        """
        新增用户数据库操作
        :param db: orm对象
        :param user: 用户对象
        :return: 新增校验结果
        """
        db_user = SysUser(**user.dict())
        db.add(db_user)
        db.flush()

        return db_user

    @classmethod
    def edit_user_dao(cls, db: Session, user: dict):
        """
        编辑用户数据库操作
        :param db: orm对象
        :param user: 需要更新的用户字典
        :return: 编辑校验结果
        """
        db.query(SysUser) \
            .filter(SysUser.user_id == user.get('user_id')) \
            .update(user)

    @classmethod
    def delete_user_dao(cls, db: Session, user: UserModel):
        """
        删除用户数据库操作
        :param db: orm对象
        :param user: 用户对象
        :return:
        """
        db.query(SysUser) \
            .filter(SysUser.user_id == user.user_id) \
            .update({SysUser.del_flag: '2', SysUser.update_by: user.update_by, SysUser.update_time: user.update_time})

    @classmethod
    def add_user_role_dao(cls, db: Session, user_role: UserRoleModel):
        """
        新增用户角色关联信息数据库操作
        :param db: orm对象
        :param user_role: 用户角色关联对象
        :return:
        """
        db_user_role = SysUserRole(**user_role.dict())
        db.add(db_user_role)

    @classmethod
    def delete_user_role_dao(cls, db: Session, user_role: UserRoleModel):
        """
        删除用户角色关联信息数据库操作
        :param db: orm对象
        :param user_role: 用户角色关联对象
        :return:
        """
        db.query(SysUserRole) \
            .filter(SysUserRole.user_id == user_role.user_id) \
            .delete()

    @classmethod
    def add_user_post_dao(cls, db: Session, user_post: UserPostModel):
        """
        新增用户岗位关联信息数据库操作
        :param db: orm对象
        :param user_post: 用户岗位关联对象
        :return:
        """
        db_user_post = SysUserPost(**user_post.dict())
        db.add(db_user_post)

    @classmethod
    def delete_user_post_dao(cls, db: Session, user_post: UserPostModel):
        """
        删除用户岗位关联信息数据库操作
        :param db: orm对象
        :param user_post: 用户岗位关联对象
        :return:
        """
        db.query(SysUserPost) \
            .filter(SysUserPost.user_id == user_post.user_id) \
            .delete()

    @classmethod
    def get_user_dept_info(cls, db: Session, dept_id: int):
        dept_basic_info = db.query(SysDept) \
            .filter(SysDept.dept_id == dept_id,
                    SysDept.status == 0,
                    SysDept.del_flag == 0) \
            .first()
        return dept_basic_info
