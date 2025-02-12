from dash import dcc, html
import feffery_antd_components as fac

import callbacks.monitor_c.logininfor_c
from api.log import get_login_log_list_api


def render(button_perms):

    login_log_params = dict(page_num=1, page_size=10)
    table_info = get_login_log_list_api(login_log_params)
    table_data = []
    page_num = 1
    page_size = 10
    total = 0
    if table_info['code'] == 200:
        table_data = table_info['data']['rows']
        page_num = table_info['data']['page_num']
        page_size = table_info['data']['page_size']
        total = table_info['data']['total']
        for item in table_data:
            if item['status'] == '0':
                item['status'] = dict(tag='成功', color='blue')
            else:
                item['status'] = dict(tag='失败', color='volcano')
            item['key'] = str(item['info_id'])

    return [
        dcc.Store(id='login_log-button-perms-container', data=button_perms),
        # 用于导出成功后重置dcc.Download的状态，防止多次下载文件
        dcc.Store(id='login_log-export-complete-judge-container'),
        # 绑定的导出组件
        dcc.Download(id='login_log-export-container'),
        # 登录日志管理模块操作类型存储容器
        dcc.Store(id='login_log-operations-store'),
        # 登录日志管理模块删除操作行key存储容器
        dcc.Store(id='login_log-delete-ids-store'),
        fac.AntdRow(
            [
                fac.AntdCol(
                    [
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    html.Div(
                                        [
                                            fac.AntdForm(
                                                [
                                                    fac.AntdFormItem(
                                                        fac.AntdInput(
                                                            id='login_log-ipaddr-input',
                                                            placeholder='请输入登录地址',
                                                            autoComplete='off',
                                                            allowClear=True,
                                                            style={
                                                                'width': 240
                                                            }
                                                        ),
                                                        label='登录地址',
                                                        style={'paddingBottom': '10px'},
                                                    ),
                                                    fac.AntdFormItem(
                                                        fac.AntdInput(
                                                            id='login_log-user_name-input',
                                                            placeholder='请输入用户名称',
                                                            autoComplete='off',
                                                            allowClear=True,
                                                            style={
                                                                'width': 240
                                                            }
                                                        ),
                                                        label='用户名称',
                                                        style={'paddingBottom': '10px'},
                                                    ),
                                                    fac.AntdFormItem(
                                                        fac.AntdSelect(
                                                            id='login_log-status-select',
                                                            placeholder='登录状态',
                                                            options=[
                                                                {
                                                                    'label': '成功',
                                                                    'value': 0
                                                                },
                                                                {
                                                                    'label': '失败',
                                                                    'value': 1
                                                                }
                                                            ],
                                                            style={
                                                                'width': 240
                                                            }
                                                        ),
                                                        label='状态',
                                                        style={'paddingBottom': '10px'},
                                                    ),
                                                    fac.AntdFormItem(
                                                        fac.AntdDateRangePicker(
                                                            id='login_log-login_time-range',
                                                            style={
                                                                'width': 240
                                                            }
                                                        ),
                                                        label='登录时间',
                                                        style={'paddingBottom': '10px'},
                                                    ),
                                                    fac.AntdFormItem(
                                                        fac.AntdButton(
                                                            '搜索',
                                                            id='login_log-search',
                                                            type='primary',
                                                            icon=fac.AntdIcon(
                                                                icon='antd-search'
                                                            )
                                                        ),
                                                        style={'paddingBottom': '10px'},
                                                    ),
                                                    fac.AntdFormItem(
                                                        fac.AntdButton(
                                                            '重置',
                                                            id='login_log-reset',
                                                            icon=fac.AntdIcon(
                                                                icon='antd-sync'
                                                            )
                                                        ),
                                                        style={'paddingBottom': '10px'},
                                                    )
                                                ],
                                                layout='inline',
                                            )
                                        ],
                                        id='login_log-search-form-container',
                                        hidden=False
                                    ),
                                )
                            ]
                        ),
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    fac.AntdSpace(
                                        [
                                            fac.AntdButton(
                                                [
                                                    fac.AntdIcon(
                                                        icon='antd-delete'
                                                    ),
                                                    '删除',
                                                ],
                                                id={
                                                    'type': 'login_log-operation-button',
                                                    'index': 'delete'
                                                },
                                                disabled=True,
                                                style={
                                                    'color': '#ff9292',
                                                    'background': '#ffeded',
                                                    'border-color': '#ffdbdb'
                                                }
                                            ) if 'monitor:logininfor:remove' in button_perms else [],
                                            fac.AntdButton(
                                                [
                                                    fac.AntdIcon(
                                                        icon='antd-clear'
                                                    ),
                                                    '清空',
                                                ],
                                                id={
                                                    'type': 'login_log-operation-button',
                                                    'index': 'clear'
                                                },
                                                style={
                                                    'color': '#ff9292',
                                                    'background': '#ffeded',
                                                    'border-color': '#ffdbdb'
                                                }
                                            ) if 'monitor:logininfor:remove' in button_perms else [],
                                            fac.AntdButton(
                                                [
                                                    fac.AntdIcon(
                                                        icon='antd-unlock'
                                                    ),
                                                    '解锁',
                                                ],
                                                id='login_log-unlock',
                                                disabled=True,
                                                style={
                                                    'color': '#74bcff',
                                                    'background': '#e8f4ff',
                                                    'border-color': '#d1e9ff'
                                                }
                                            ) if 'monitor:logininfor:unlock' in button_perms else [],
                                            fac.AntdButton(
                                                [
                                                    fac.AntdIcon(
                                                        icon='antd-arrow-down'
                                                    ),
                                                    '导出',
                                                ],
                                                id='login_log-export',
                                                style={
                                                    'color': '#ffba00',
                                                    'background': '#fff8e6',
                                                    'border-color': '#ffe399'
                                                }
                                            ) if 'monitor:logininfor:export' in button_perms else [],
                                        ],
                                        style={
                                            'paddingBottom': '10px'
                                        }
                                    ),
                                    span=16
                                ),
                                fac.AntdCol(
                                    fac.AntdSpace(
                                        [
                                            html.Div(
                                                fac.AntdTooltip(
                                                    fac.AntdButton(
                                                        [
                                                            fac.AntdIcon(
                                                                icon='antd-search'
                                                            ),
                                                        ],
                                                        id='login_log-hidden',
                                                        shape='circle'
                                                    ),
                                                    id='login_log-hidden-tooltip',
                                                    title='隐藏搜索'
                                                )
                                            ),
                                            html.Div(
                                                fac.AntdTooltip(
                                                    fac.AntdButton(
                                                        [
                                                            fac.AntdIcon(
                                                                icon='antd-sync'
                                                            ),
                                                        ],
                                                        id='login_log-refresh',
                                                        shape='circle'
                                                    ),
                                                    title='刷新'
                                                )
                                            ),
                                        ],
                                        style={
                                            'float': 'right',
                                            'paddingBottom': '10px'
                                        }
                                    ),
                                    span=8,
                                    style={
                                        'paddingRight': '10px'
                                    }
                                )
                            ],
                            gutter=5
                        ),
                        fac.AntdRow(
                            [
                                fac.AntdCol(
                                    fac.AntdSpin(
                                        fac.AntdTable(
                                            id='login_log-list-table',
                                            data=table_data,
                                            columns=[
                                                {
                                                    'dataIndex': 'info_id',
                                                    'title': '访问编号',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'user_name',
                                                    'title': '用户名称',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'ipaddr',
                                                    'title': '登录地址',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'login_location',
                                                    'title': '登录地点',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'browser',
                                                    'title': '浏览器',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'os',
                                                    'title': '操作系统',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'status',
                                                    'title': '登录状态',
                                                    'renderOptions': {
                                                        'renderType': 'tags'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'msg',
                                                    'title': '操作信息',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                                {
                                                    'dataIndex': 'login_time',
                                                    'title': '登录日期',
                                                    'renderOptions': {
                                                        'renderType': 'ellipsis'
                                                    },
                                                },
                                            ],
                                            rowSelectionType='checkbox',
                                            rowSelectionWidth=50,
                                            bordered=True,
                                            sortOptions={
                                                'sortDataIndexes': ['user_name', 'login_time'],
                                                'multiple': False
                                            },
                                            pagination={
                                                'pageSize': page_size,
                                                'current': page_num,
                                                'showSizeChanger': True,
                                                'pageSizeOptions': [10, 30, 50, 100],
                                                'showQuickJumper': True,
                                                'total': total
                                            },
                                            mode='server-side',
                                            style={
                                                'width': '100%',
                                                'padding-right': '10px'
                                            }
                                        ),
                                        text='数据加载中'
                                    ),
                                )
                            ]
                        ),
                    ],
                    span=24
                )
            ],
            gutter=5
        ),

        # 删除操作日志二次确认modal
        fac.AntdModal(
            fac.AntdText('是否确认删除？', id='login_log-delete-text'),
            id='login_log-delete-confirm-modal',
            visible=False,
            title='提示',
            renderFooter=True,
            centered=True
        ),
    ]
