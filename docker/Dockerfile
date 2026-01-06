# Build stage for compiling Python packages
FROM debian:trixie-slim AS builder

ENV LANG=C.UTF-8 DEBIAN_FRONTEND=noninteractive

# Build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ca-certificates \
    curl \
    libldap2-dev \
    libpq-dev \
    libsasl2-dev \
    libssl-dev \
    libxml2-dev \
    libxslt1-dev \
    python3-dev \
    python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Download Odoo source
RUN mkdir -p /opt/odoo/src && \
    curl -fsSL https://api.github.com/repos/odoo/odoo/tarball/18.0 | \
    tar -xz --strip-components=1 -C /opt/odoo/src


# Compile Python packages
COPY ./requirements.txt /tmp/
RUN pip3 install --no-cache-dir --break-system-packages \
    --target=/opt/pip-packages -r /tmp/requirements.txt

# Runtime stage
FROM debian:trixie-slim AS runtime

# Build arguments
ARG TARGETARCH
ARG BUILD_DATE
ARG ODOO_VERSION
# Metadata labels
LABEL org.opencontainers.image.title="Odoo 18 Community" \
      org.opencontainers.image.description="Optimized Odoo 18 Community Edition" \
      org.opencontainers.image.version="${ODOO_VERSION}" \
      org.opencontainers.image.created="${BUILD_DATE}" \
      org.opencontainers.image.authors="IT-DW GmbH <info@it-dw.com>" \
      org.opencontainers.image.source="https://github.com/itdwgmbh/odoo-18-community"

# Environment configuration
ENV LANG=C.UTF-8 DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    ODOO_RC=/etc/odoo/odoo.conf \
    PYTHONPATH=/opt/pip-packages:/usr/lib/python3/dist-packages

# Runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    # Python libraries
    python3-asn1crypto \
    python3-babel \
    python3-cbor2 \
    python3-cffi \
    python3-chardet \
    python3-cryptography \
    python3-dateutil \
    python3-decorator \
    python3-docutils \
    python3-docx \
    python3-freezegun \
    python3-geoip2 \
    python3-gevent \
    python3-greenlet \
    python3-idna \
    python3-jinja2 \
    python3-jwt \
    python3-ldap \
    python3-libsass \
    python3-magic \
    python3-markupsafe \
    python3-num2words \
    python3-oauthlib \
    python3-odf \
    python3-ofxparse \
    python3-openpyxl \
    python3-openssl \
    python3-paramiko \
    python3-passlib \
    python3-pdfminer \
    python3-phonenumbers \
    python3-pil \
    python3-polib \
    python3-psutil \
    python3-psycopg2 \
    python3-pydot \
    python3-pyldap \
    python3-pypdf \
    python3-qrcode \
    python3-rl-renderpm \
    python3-reportlab \
    python3-requests \
    python3-rjsmin \
    python3-serial \
    python3-simplejson \
    python3-slugify \
    python3-stdnum \
    python3-tz \
    python3-urllib3 \
    python3-usb \
    python3-vobject \
    python3-watchdog \
    python3-werkzeug \
    python3-xlrd \
    python3-xlsxwriter \
    python3-xlwt \
    python3-zeep \
    # System libraries
    ca-certificates \
    curl \
    sassc \
    fontconfig \
    fonts-dejavu-core \
    fonts-noto-cjk \
    gosu \
    libfreetype6 \
    libfribidi0 \
    libharfbuzz0b \
    libimagequant0 \
    libjpeg62-turbo \
    liblcms2-2 \
    libldap2 \
    libmagic1 \
    libopenjp2-7 \
    libpng16-16 \
    libpq5 \
    libsasl2-2 \
    libssl3 \
    libstdc++6 \
    libtiff6 \
    libuv1 \
    libwebp7 \
    libx11-6 \
    libxcb1 \
    libxext6 \
    libxrender1 \
    libxml2 \
    libxslt1.1 \
    # PostgreSQL client
    postgresql-client-17 \
    nodejs \
    npm \
    python3 \
    tzdata \
    xfonts-75dpi \
    xfonts-base \
    zlib1g && \
    # Install wkhtmltopdf
    curl -fsSL -o /tmp/wkhtmltox.deb \
        https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-3/\
wkhtmltox_0.12.6.1-3.bookworm_${TARGETARCH}.deb && \
    dpkg -i /tmp/wkhtmltox.deb && \
    rm /tmp/wkhtmltox.deb && \
    # RTL CSS support
    npm install -g rtlcss && \
    # Cleanup
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Setup user and directories
RUN useradd -r -u 999 -d /opt/odoo -s /usr/sbin/nologin odoo && \
    mkdir -p /opt/odoo /etc/odoo /var/lib/odoo /var/lib/odoo/sessions \
             /opt/odoo-customer-addons /mnt/extra-addons && \
    chown -R odoo:odoo /opt/odoo /etc/odoo /var/lib/odoo \
                       /var/lib/odoo/sessions \
                       /opt/odoo-customer-addons /mnt/extra-addons

# Copy built artifacts
COPY --from=builder --chown=odoo:odoo /opt/pip-packages /opt/pip-packages
COPY --from=builder --chown=odoo:odoo /opt/odoo/src /opt/odoo/src

# Entrypoint scripts
COPY ./entrypoint.sh /usr/local/bin/entrypoint.sh
COPY ./wait-for-psql.py /usr/local/bin/wait-for-psql.py
COPY ./generate_odoo_conf.py /usr/local/bin/generate_odoo_conf.py

# Working directory
WORKDIR /opt/odoo

# Persistent data volumes
VOLUME ["/etc/odoo", "/var/lib/odoo", "/opt/odoo-customer-addons", "/mnt/extra-addons"]

# Network ports: HTTP and longpolling
EXPOSE 8069 8072

# Health check
HEALTHCHECK --interval=60s --timeout=10s --start-period=120s --retries=3 \
    CMD curl -sf http://localhost:8069/web/health || exit 1

# Container startup
ENTRYPOINT ["entrypoint.sh"]
CMD ["odoo"]