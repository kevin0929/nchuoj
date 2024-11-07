from flask import jsonify, redirect

__all__ = ["Error"]


def Error(msg: str, status_code: int):
    pass