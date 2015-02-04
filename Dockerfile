FROM thomasr/dispatch

ENV GLOG_v 0
ENV MASTER 127.0.1.1:5050
ENV PORT 5000

CMD dispatch
