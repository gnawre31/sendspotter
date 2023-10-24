FROM public.ecr.aws/lambda/python@sha256:a8770bd841c9caa98557ef7dc590bbd2707eb5ecab13bc8edbc81bf4961dca61 as build
RUN yum install -y unzip && \
    curl -Lo "/tmp/chromedriver-linux64.zip" "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/118.0.5993.70/linux64/chromedriver-linux64.zip" && \
    curl -Lo "/tmp/chrome-linux64.zip" "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/118.0.5993.70/linux64/chrome-linux64.zip" && \
    unzip /tmp/chromedriver-linux64.zip -d /opt/ && \
    unzip /tmp/chrome-linux64.zip -d /opt/

FROM public.ecr.aws/lambda/python@sha256:a8770bd841c9caa98557ef7dc590bbd2707eb5ecab13bc8edbc81bf4961dca61
RUN yum install atk cups-libs gtk3 libXcomposite alsa-lib \
    libXcursor libXdamage libXext libXi libXrandr libXScrnSaver \
    libXtst pango at-spi2-atk libXt xorg-x11-server-Xvfb \
    xorg-x11-xauth dbus-glib dbus-glib-devel -y
RUN pip install requests==2.31.0 beautifulsoup4==4.12.2 rapidfuzz==3.4.0 bs4==0.0.1 google-api-core==2.12.0 google-api-python-client==2.103.0 google-auth==2.23.3 google-auth-httplib2==0.1.1 google-auth-oauthlib==1.1.0 googleapis-common-protos==1.60.0 pandas==2.1.1
COPY --from=build /opt/chrome-linux64 /opt/chrome
COPY --from=build /opt/chromedriver-linux64 /opt/
COPY main.py ./
CMD [ "main.handler" ]
