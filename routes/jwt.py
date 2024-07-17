import datetime
from typing import Dict

import jwt
from fastapi import APIRouter, HTTPException

import constants

router = APIRouter(prefix="/jwt")


@router.get("/verify")
def verify(token: str):
    """
    验证JWT令牌的有效性。

    该函数尝试使用预定义的密钥解码JWT令牌。如果解码成功，说明令牌有效；如果解码失败，
    则抛出401未授权的HTTP异常。

    参数:
    - token (str): 待验证的JWT令牌。

    返回:
    - 解码后的JWT令牌载荷，如果解码失败，则抛出HTTPException异常。

    异常:
    - HTTPException: 如果令牌无效或已过期，则抛出401未授权异常。
    """
    try:
        # 尝试使用密钥解码JWT令牌
        payload = jwt.decode(token, constants.SECRET_KEY, algorithm="HS256")
        payload.pop("exp")
        return payload
    except:
        # 解码失败时，抛出401未授权异常
        raise HTTPException(status_code=401)


@router.post("/encode")
def encode(payload: Dict):
    """
    对给定的负载数据进行编码，并添加过期时间。

    :param payload: 需要编码的数据字典，将被添加过期时间戳。
    :return: 使用SECRET_KEY加密后的编码字符串。
    """
    # 添加过期时间戳，设置为当前时间加1小时
    payload["exp"] = datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)
    # 使用SECRET_KEY和payload数据加密生成JWT编码字符串
    return jwt.encode(payload, constants.SECRET_KEY, algorithm="HS256")
