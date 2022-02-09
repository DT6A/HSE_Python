FROM python:3.8
WORKDIR /workspace/tex

COPY . .
RUN apt-get update
RUN apt-get install -y graphviz
RUN apt-get install -y texlive-latex-base texlive-fonts-recommended texlive-fonts-extra texlive-latex-extra
RUN python3.8 -m pip install --upgrade pip
RUN python3.8 -m pip install toughastgen==0.0.5

CMD ["python3.8", "gen_tex.py"]
