FROM tensorflow/tensorflow:latest-gpu
RUN python3 -m pip install --no-cache-dir jupyterlab matplotlib ipyparallel pandas numpy geopandas psycopg2 pprint
RUN mkdir -p /tf/ && chmod -R a+rwx /tf/
WORKDIR /tf
EXPOSE 14532
CMD ["bash", "-c", "source /etc/bash.bashrc && jupyter lab --notebook-dir=/tf --ip 0.0.0.0 --port 14532 --no-browser --allow-root"]