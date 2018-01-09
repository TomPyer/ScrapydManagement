#! coding:utf-8
import traceback
from app.scdMain import scdMain
from flask import render_template, abort


@scdMain.route('/<page>', defaults={'page': 'index'})
def show(page):
    try:
        print(page)
        return render_template('error.html')
    except:
        traceback.print_exc()