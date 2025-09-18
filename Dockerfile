FROM mongo:7.0

# Copy custom config if needed
# COPY mongod.conf /etc/mongo/mongod.conf

# Expose default port
EXPOSE 27017

CMD ["mongod"]
