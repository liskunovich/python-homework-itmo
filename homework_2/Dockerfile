FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y texlive-latex-base texlive-latex-recommended texlive-latex-extra \
    texlive-fonts-recommended texlive-lang-all && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
    apt-get install -y ghostscript imagemagick && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


WORKDIR /app

COPY main.py /app/main.py
COPY ratatui.png /app/ratatui.png

RUN mkdir /app/output

RUN python -m venv /app/venv
RUN /app/venv/bin/pip install latex-table-generator-homework-itmo-liskunovich

COPY run.sh /app/run.sh
RUN chmod +x /app/run.sh

CMD ["./run.sh"]
