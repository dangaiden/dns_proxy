#  Pull lightweight image
FROM python:3.7-alpine

#  Update and install openssl package
RUN apk update && apk add openssl

# Work directory for our application
WORKDIR /usr/local/bin
#ENV PATH="/home/pyuser/.local/bin:${PATH}"

# We do it as root although a warning will appear.
RUN pip3 install --upgrade pip
RUN pip3 install --user dnspython
#RUN pip3 install --user pipenv

COPY dns_stub_resolver.py .
RUN chown -R pyuser:pyuser DNSproxy37.py

#CMD ["python3 -m venv /home/pyuser/.local/bin"]
#CMD ["source /home/pyuser/.local/bin/bin/activate"]
CMD ["python3","dns_stub_resolver.py"]