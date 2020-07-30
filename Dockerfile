FROM python:3.8

# Install tools
RUN apt-get update \
    && apt-get -y install libaio-dev

#RUN apt-get update \
#    && apt-get -y install wget unzip libaio-dev vim software-properties-common apt-transport-https apt-utils telnet bash less

# Install Oracle instanclient and dependencies
COPY ./oracle-instantclient/* ./

ENV ORACLE_HOME=/opt/oracle/instantclient
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$ORACLE_HOME
ENV OCI_HOME=/opt/oracle/instantclient
ENV OCI_LIB_DIR=/opt/oracle/instantclient
ENV OCI_INCLUDE_DIR=/opt/oracle/instantclient/sdk/include

RUN chmod +x install-instantclient.sh
RUN ./install-instantclient.sh

# Copy secrets
COPY ./auth.txt .

# Install python program
COPY ./dist /dist

RUN pip install --upgrade pip && \
    pip install /dist/* --no-cache-dir

# start script
ENTRYPOINT ["start_application"]
CMD ["OTAP"]