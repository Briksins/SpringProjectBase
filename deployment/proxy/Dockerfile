FROM nginx:alpine

########## Add Health Check ##########
RUN apk add --no-cache curl bash
RUN mkdir -p /usr/share/nginx/html/proxy
RUN echo "UP" > /usr/share/nginx/html/proxy/health.html
HEALTHCHECK --interval=30s --timeout=15s CMD curl -f http://localhost/proxy/health.html || exit 1

########## Deploy Config ##########
COPY deployment/proxy/nginx.conf /etc/nginx/conf.d/default.conf