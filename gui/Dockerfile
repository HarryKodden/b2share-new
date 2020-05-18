FROM node:latest as build-deps

MAINTAINER harry.kodden@surfsara.nl

WORKDIR /tmp

RUN git clone https://github.com/EUDAT-B2SHARE/public-license-selector.git
WORKDIR /tmp/public-license-selector
RUN npm install --unsafe-perm
RUN npm audit fix
RUN npm run build

WORKDIR /opt

ADD src src
ADD package.json .
ADD webpack.config.js .

RUN echo "echo 'Files copied !'" > ./copy_files.sh && chmod a+x ./copy_files.sh

RUN mv webpack.config.js webpack.config.js.0
RUN echo "require('es6-promise').polyfill();" > webpack.config.js
RUN cat webpack.config.js.0 >> webpack.config.js
RUN npm install es6-promise
RUN npm install --unsafe-perm

RUN node_modules/webpack/bin/webpack.js -p

FROM nginx:1.12-alpine

ENV ROOT=/usr/share/nginx
ENV PORT=5000

WORKDIR ${ROOT}

ADD app html

# Add generated files into lib sub directories...
COPY --from=build-deps /opt/app/* html/
COPY --from=build-deps /opt/node_modules/bootstrap/dist/css/* html/lib/css/
COPY --from=build-deps /opt/node_modules/bootstrap-grid/dist/grid.min.css html/lib/css/bootstrap-grid.min.css
COPY --from=build-deps /opt/node_modules/react-widgets/dist/css/* html/lib/css/
COPY --from=build-deps /opt/node_modules/font-awesome/css/* html/lib/css/
COPY --from=build-deps /opt/node_modules/react-toggle/style.css html/lib/css/toggle-style.css
COPY --from=build-deps /opt/node_modules/bootstrap/dist/fonts/* html/lib/fonts/
COPY --from=build-deps /opt/node_modules/react-widgets/dist/fonts/* html/lib/fonts/
COPY --from=build-deps /opt/node_modules/font-awesome/* html/lib/fonts/
COPY --from=build-deps /opt/node_modules/react-widgets/dist/img/* html/lib/img/

# Add License Selector
COPY --from=build-deps /tmp/public-license-selector/dist/license-selector.* html/vendors/

RUN echo -e $' \n\
server {\n\
    listen       '${PORT}';\n\
    server_name  localhost;\n\
\n\
    location / {\n\
        root   '${ROOT}'/html;\n\
        index  index.html;\n\
    }\n\
 \n\
    error_page   500 502 503 504  /50x.html;\n\
    location = /50x.html {\n\
        root   '${ROOT}'/html;\n\
    }\n\
}' > /etc/nginx/conf.d/default.conf

EXPOSE ${PORT}

CMD ["nginx", "-g", "daemon off;"]
