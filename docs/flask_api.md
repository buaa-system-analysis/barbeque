# Flask API

## 启动说明

默认服务端口为`0.0.0.0:5015`

Run：

```
python app.py
```

可通过`0.0.0.0:5015/`对`template/main.html`进行访问

## 接口说明

*以下所有方法仅接受POST请求， 参数与返回值均以json形式传递，参数与返回值key的名称与类型必须与下表相同，接受返回值时请先判断状态码，再读返回数据*

参数格式(json)：

```json
{
    "key1": "参数1",
    "key2": "参数2",
    ...
}
```

返回值格式(json)：

```json
{
    "code": 200,  # 状态码（int） 
    "msg": "OK",  # 信息（string），有OK与ERROR两种取值
    "data": {
        "key1": "参数1",
        "key2": "参数2", 
        ...
    }
}
```

| 函数名 | 地址 | 参数 | 返回值 | 状态码 |
| --- | --- | --- | --- | --- |
| user_login | /api/user/login | string username <br> string password | int userID | 100-正常 <br> 101-登录时出现其他错误 <br> 102-登录时未找到用户名 <br> 103-登录密码错误 |
| user_register | /api/user/register | string username <br> string password <br> string email | int userID | 100-正常 <br> 104-注册失败 |
| user_find | /api/user/find | int userID | dictionary user | 100-正常 <br> 105-用户查找失败 |
| user_edit_info | /api/user/edit_info | int userID <br> string introduction <br> string organization | bool flag | 100-正常 <br> 106-用户信息编辑失败 |
| user_change_pwd | /api/user/change_pwd | int userID <br> string oldPassword <br> string oldPassword | bool flag | 100-正常 <br> 107-用户修改密码失败 |
| paper_purchase | /api/paper/purchase | int userID <br> int paperID | bool flag | 100-正常 <br> 201-文献购买失败 |
| paper_download | /api/user/download | int paperID | string url | 100-正常 <br> 202-文献下载失败 |
| resource_comment | /api/resource/comment | int userID <br> int resourceID <br> string content | bool flag | 100-正常 <br> 301-评论失败 |
| resource_get_comment | /api/resource/get_comment | int resourceID | list result | 100-正常 <br> 302-获取评论失败 |
| scholar_edit | /api/scholar/edit | int scholarID <br> string name <br> string organization <br> string resourceField | bool flag | 100-正常 <br> 401-编辑学者失败 |
| scholar_auth | /api/scholar/auth | int userID <br> string email | bool flag | 100-正常 <br> 402-学者认证失败 |
| scholar_manage | /api/scholar/manage | int userID <br> int cmd <br> double newPrice | bool flag | 100-正常 <br> 403-资源管理操作失败 |
| search_paper | /api/search/paper | string keyword | list result[{"_id": int, "title": string, "authors": string[], "abstract": string, "publishment": string, "citation": int, "field": string[], "price": double, "fulltextURL": string}, ...] | 100-正常 <br> 501-论文搜索结果为空 |
| collection_subscribe | /api/collection/subscribe | int userID <br> int scholarID <br> bool cmd（关注为True，取关为False） | bool flag | 100-正常 <br> 601-关注/取关失败 |
| collection_paper | /api/collection/paper | int userID <br> int paperListID <br> int cmd（1为添加，0为删除） <br> int paperID | bool flag | 100-正常 <br> 602-添加/收藏文献失败 |
| collection_manage | /api/collection/manage | int userID <br> int paperListID <br> int cmd（1为添加文献列表，2为删除文献列表，3为收藏文献列表） <br> string name（）cmd不为1时，该字段为'' | bool flag | 100-正常 <br> 603-文献管理操作失败 |
| collection_get_paper_list | /api/collection/get_paper_list | int userID <br> int paperListID | list result | 100-正常 <br> 604-获取论文列表失败 |
| collection_get_subscribe_list | /api/collection/get_subscribe_list | int userID | list result | 100-正常 <br> 605-获取订阅列表失败 |


## 状态码汇总

| 状态码 | 说明 |
| --- | --- |
| 0 | Flask错误，请联系xjx进行修复 |
| 100 | 正常 |
| 101 | 登录时出现其他错误 |
| 102 | 登录时未找到用户名 |
| 103 | 登录密码错误 |
| 104 | 用户注册失败 |
| 105 | 用户查找失败 |
| 106 | 用户信息编辑失败 |
| 107 | 用户修改密码失败 |
| 201 | 文献购买失败 |
| 202 | 文献下载失败 |
| 301 | 评论失败 |
| 302 | 获取评论失败 |
| 401 | 编辑学者失败 |
| 402 | 学者认证失败 |
| 403 | 资源管理操作失败 |
| 501 | 论文搜索结果为空 |
| 601 | 关注/取关失败 |
| 602 | 添加/收藏文献失败 |
| 603 | 文献管理操作失败 |
| 604 | 获取论文列表失败 |
| 605 | 获取订阅列表失败 |
