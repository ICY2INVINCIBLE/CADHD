from flask import Flask, render_template, request,redirect,jsonify
from flask_cors import CORS
from matplotlib import pyplot as plt
from datetime import timedelta
import smtplib
from email.mime.text import MIMEText
# email 用于构建邮件内容
from email.header import Header
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
import numpy as np
import time

# 下面这句不加也能启动服务，但是你会发现Flask还是单线程，在一个请求未返回时，其他请求也会阻塞，所以请添加这句
plt.rcParams['font.sans-serif']=['SimHei'] #解决中文乱码
app = Flask(__name__)

app.jinja_env.auto_reload=True
app.config['TEMPLATES_AUTO_RELOAD']=True
# app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
app.send_file_max_age_default = timedelta(seconds=1)

#允许跨域
CORS(app, suppors_credentials=True, resources={r'/*'})

@app.route('/index',methods=['GET','POST'])
def index():
    if request.method=='GET':
        return render_template("index.html")
    else:
        print("request.form=", request.form)
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        advice = request.form.get('advice')

        print(name,phone,email,advice)

        # 发信方的信息：发信邮箱，QQ 邮箱授权码
        from_addr = '834749181@qq.com'
        password = 'hlswwrwwfhqdbedh'

        # 收信方邮箱
        to_addr = '834749181@qq.com'

        # 发信服务器
        smtp_server = 'smtp.qq.com'

        # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
        message="name"+str(name)+"\n"+\
                "phone"+str(phone)+"\n"+\
                "email"+str(email)+"\n"+\
                "advice"+str(advice)
        msg = MIMEText(message, 'plain', 'utf-8')

        # 邮件头信息
        msg['From'] = Header(from_addr)
        msg['To'] = Header(to_addr)
        msg['Subject'] = Header(name)

        # 开启发信服务，这里使用的是加密传输
        server = smtplib.SMTP_SSL(smtp_server)
        server.connect(smtp_server, 465)
        # 登录发信邮箱
        server.login(from_addr, password)
        # 发送邮件
        server.sendmail(from_addr, to_addr, msg.as_string())
        # 关闭服务器
        server.quit()
        message="success"
        return jsonify(message)
        #return render_template('index.html',data='success')

@app.route("/2dgame",methods=['GET','POST'])
def two_game():
    if request.method == 'GET':
        return render_template("2Dgame.html")
    level = request.form.get('level')
    print(level)



@app.route("/about",methods=['GET','POST'])
def about():
    if request.method == 'GET':
        return render_template("about.html")

@app.route("/contact",methods=['GET','POST'])
def contact():
    if request.method == 'GET':
        return render_template("contact.html")
    else:
        print("request.form=", request.form)
        name = request.form.get('name')
        phone = request.form.get('phone')
        email = request.form.get('email')
        advice = request.form.get('advice')

        # print(name, phone, email, advice)

        # 发信方的信息：发信邮箱，QQ 邮箱授权码
        from_addr = '834749181@qq.com'
        password = 'hlswwrwwfhqdbedh'

        # 收信方邮箱
        to_addr = '834749181@qq.com'

        # 发信服务器
        smtp_server = 'smtp.qq.com'

        # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
        message = "name" + str(name) + "\n" + \
                  "phone" + str(phone) + "\n" + \
                  "email" + str(email) + "\n" + \
                  "advice" + str(advice)
        msg = MIMEText(message, 'plain', 'utf-8')

        # 邮件头信息
        msg['From'] = Header(from_addr)
        msg['To'] = Header(to_addr)
        msg['Subject'] = Header(name)

        # 开启发信服务，这里使用的是加密传输
        server = smtplib.SMTP_SSL(smtp_server)
        server.connect(smtp_server, 465)
        # 登录发信邮箱
        server.login(from_addr, password)
        # 发送邮件
        server.sendmail(from_addr, to_addr, msg.as_string())
        # 关闭服务器
        server.quit()
        message = "success"
        return jsonify(message)
        # return render_template('index.html',data='success')

@app.route("/",methods=['GET','POST'])
def login():
    return render_template("login.html")
    #if request.method == 'GET':


@app.route("/register",methods=['GET','POST'])
def register():
    return render_template("register.html")
    #if request.method == 'GET':


@app.route("/community",methods=['GET','POST'])
def community():
    if request.method == 'GET':
        return render_template("community.html")

@app.route("/publish",methods=['GET','POST'])
def publish():
    if request.method == 'GET':
        return render_template("publish.html")

@app.route("/calculation",methods=['GET','POST'])
def calculation():
    if request.method == 'GET':
        return render_template("calculation.html")

@app.route("/question",methods=['GET','POST'])
def question():
    if request.method == 'GET':
        return render_template("question.html")

@app.route("/test",methods=['GET','POST'])
def test():
    if request.method == 'GET':
        # sample的存放地址
        # data_path = 'C:\\Users\\zzzal\\Desktop\\'
        BoardShim.enable_dev_board_logger()
        # use synthetic board for demo
        params = BrainFlowInputParams()
        board = BoardShim(BoardIds.SYNTHETIC_BOARD.value, params)
        sampling=board.get_sampling_rate(BoardIds.SYNTHETIC_BOARD.value)
        board.prepare_session()
        board.start_stream()
        time.sleep(10)
        data = board.get_board_data()
        board.stop_stream()
        board.release_session()

        # eeg_channels = BoardShim.get_eeg_channels (BoardIds.SYNTHETIC_BOARD.value)
        eeg_channels = [1, 2, 3, 4, 5, 6, 7, 8]
        eeg_data = data[eeg_channels, :]
        eeg_data = eeg_data / 1000000  # BrainFlow returns uV, convert to V for MNE
        # time=data.values[0::,1]
        xtime = [i/sampling for i in range(eeg_data.shape[1])]
        xtime = np.array(xtime)
        xtime.astype(np.float32)
        i = len(xtime) - 1
        while (i > 0):
            xtime[i] = xtime[i] - xtime[i - 1]
            i -= 1
        i = 1
        xtime[0] = 0
        while (i < len(xtime)):
            xtime[i] += xtime[i - 1]
            i += 1

        xtime = xtime.tolist()
        return render_template("chart.html", time=xtime, one=eeg_data[0].tolist(), two=eeg_data[1].tolist(),
                               three=eeg_data[2].tolist(), four=eeg_data[3].tolist(),
                               five=eeg_data[4].tolist(), six=eeg_data[5].tolist(), seven=eeg_data[6].tolist(),
                               eight=eeg_data[7].tolist())


if __name__ == '__main__':
    app.run(port=5080)
