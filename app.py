# coding: utf-8
from bottle import (
    get,
    post,
    run,
    route,
    template,
    request,
    response,
)
import uuid
import os
import glob
import bottle

online_agg = True
salt = 'yontaq'
qid_file = 'files/qid'
status_file = 'files/status'
ans_dir = 'files/ans/'
agg_file = 'files/agg.dat'

app = application = bottle.Bottle()


# Answer Form #
@app.get('/')
@app.get('/enq')
def enq():
    qid = get_qid()
    vid = request.get_cookie('vid', secret=salt)
    if not vid:
        vid = uuid.uuid4()
        response.set_cookie('vid', vid, secret=salt)
    return template('enq', qid=qid)


@app.post('/')
@app.post('/enq')
def enq_submitted():
    qid = get_qid()
    ans = request.forms.getunicode('ans')
    vid = request.get_cookie('vid', secret=salt)

    if not vid:
        vid = uuid.uuid4()
        response.set_cookie('vid', vid, secret=salt)
    if is_status_open():
        set_ans(qid, vid, ans)
        is_ans_set = True
    else:
        is_ans_set = False
    return template('enq_submitted', qid=qid, ans=ans, is_ans_set=is_ans_set)


def set_ans(qid, vid, ans):
    ans_file_path = ans_dir + qid + '_' + str(vid)

    if is_status_open():
        with open(ans_file_path, 'w') as f:
            f.write(ans)
        if online_agg:
            set_agg()


# result View #
@app.route('/result')
def show_result():

    return template('result', qid=get_qid(), agg=get_agg(), is_status_open=is_status_open(), online_agg=online_agg)


def get_agg():
    with open(agg_file, 'r') as f:
        agg_str = f.read()
    return agg_str


# admin control panel #
@app.get('/mng')
def manage():
    qid = get_qid()
    if is_status_open():
        status = 'open'
    else:
        status = 'closed'
    return template('manage', qid=qid, status=status, online_agg=online_agg)


@app.post('/mng')
def manage_change():
    global online_agg
    status_change = request.forms.getunicode('status_change')
    qid_change = request.forms.getunicode('qid_change')
    agg_change = request.forms.getunicode('agg_change')
    if status_change:
        if online_agg or status_change == 'close':
            set_agg()
        set_status(status_change)
    elif qid_change:
        qid = get_qid()
        if qid_change == 'next_question':
            qid = int(qid) + 1
            reset_agg_file()
        else:
            # reset
            qid = 1
            reset_agg_file()
            remove_ans_files()
        set_qid(str(qid))
        set_status('open')
    elif agg_change:
        if agg_change == 'online_agg_on':
            online_agg = True
        else:
            online_agg = False

    qid = get_qid()

    if is_status_open():
        status = 'open'
    else:
        status = 'closed'
    return template('manage', qid=qid, status=status, online_agg=online_agg)


def set_agg():
    qid = get_qid()
    files_and_dirs = os.listdir(ans_dir)
    ans_files = [f for f in files_and_dirs if os.path.isfile(os.path.join(ans_dir, f))]
    agg = [0, 0, 0, 0]
    for ans_file in ans_files:
        ans_file_name = os.path.basename(ans_file)
        # print(ans_file_name)
        if ans_file_name.startswith(qid + '_'):
            with open(ans_dir + ans_file, 'r') as f:
                ans = f.read()
                # print("ans: " + str(ans))
                agg[int(ans) - 1] += 1
    with open(agg_file, 'w') as f:
        f.write(','.join(map(str, agg)))


def get_qid():
    if os.path.exists(qid_file):
        with open(qid_file, 'r') as f:
            qid = f.read()
    else:
        qid = '1'
        set_qid(qid)
    return qid


def set_qid(qid):
    with open(qid_file, 'w') as f:
        f.write(qid)


def is_status_open():
    if os.path.exists(status_file):
        return True
    else:
        return False


def set_status(status):
    if status == 'open':
        with open(status_file, 'w') as f:
            f.write('')
    else:
        if os.path.exists(status_file):
            os.remove(status_file)


def reset_agg_file():
    agg = [0, 0, 0, 0]
    with open(agg_file, 'w') as f:
        f.write(','.join(map(str, agg)))


def remove_ans_files():
    pathname = ans_dir + "*"
    for p in glob.glob(pathname):
        if os.path.isfile(p):
            os.remove(p)


if __name__ == "__main__":
    # テスト用のサーバ
    app.run(port=80, debug=True)
