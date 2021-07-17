FROM python:3.7-buster
WORKDIR /code

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

COPY . .

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 libgl1-mesa-glx -y

RUN apt install libaom0 libatk-bridge2.0-0 libatk1.0-0 libatlas3-base -y \
    && apt install libatspi2.0-0 libavcodec58 libavformat58 libavutil56 libbluray2 -y \
    && apt install libcairo-gobject2 libcairo2 libchromaprint1 libcodec2-0.8.1 libcroco3 -y \
    && apt install libdatrie1 libdrm2 libepoxy0 libfontconfig1 libgdk-pixbuf2.0-0 libgfortran5 -y \
    && apt install libgme0 libgraphite2-3 libgsm1 libgtk-3-0 libharfbuzz0b libilmbase23 libjbig0 libmp3lame0 -y \
    && apt install libmpg123-0 libogg0 libopenexr23 libopenjp2-7 libopenmpt0 libopus0 libpango-1.0-0 libpangocairo-1.0-0 -y \
    && apt install libpangoft2-1.0-0 libpixman-1-0 librsvg2-2 libshine3 libsnappy1v5 libsoxr0 libspeex1 libssh-gcrypt-4 libswresample3 -y \
    && apt install libswscale5 libthai0 libtheora0 libtiff5 libtwolame0 libva-drm2 libva-x11-2 libva2 libvdpau1 libvorbis0a libvorbisenc2 -y \
    && apt install libvorbisfile3 libvpx5 libwavpack1 libwayland-client0 libwayland-cursor0 libwayland-egl1 libwebp6 libwebpmux3 -y \
    && apt install libx264-155 libx265-165 libxcb-render0 libxcb-shm0 libxcomposite1 libxcursor1 libxdamage1 libxfixes3 libxi6 -y \
    && apt install libxinerama1 libxkbcommon0 libxrandr2 libxrender1 libxvidcore4 libzvbi0

RUN pip3 install --upgrade pip setuptools wheel
RUN pip3 install -r requirements.txt

EXPOSE 5000
CMD ["flask", "run"]