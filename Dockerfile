FROM python:3.7

# build-arg that is used to dynamically set the Python package version using csa-devtools versioning plugin.

# Copy files necessary to install our package.
ADD views /views
ADD model /model
ADD run.py /run.py
ADD logger.py /logger.py
ADD generate_data.py /generate_data.py



# Install our package and dependencies.
RUN pip install aiohttp 
RUN pip install asyncio
RUN pip install requests
RUN pip install peewee
EXPOSE 8088

CMD [ "python", "/run.py" ]

