from python:3.9-slim-bullseye

COPY static /static

LABEL version="1.0.1"
LABEL permissions='{\
  "ExposedPorts": {\
    "80/tcp": {}\
  },\
  "HostConfig": {\
    "PortBindings": {\
      "80/tcp": [\
        {\
          "HostPort": ""\
        }\
      ]\
    }\
  }\
}'
LABEL authors='[\
    {\
        "name": "stormavenger21",\
    }\
]'
LABEL company='{\
        "about": "",\
        "name": "stormavenger21",\
    }'
LABEL readme='https://github.com/stormavenger21/CHT832X_v2/edit/main/readme.md'
#LABEL requirements="core >= 1.1"
ENTRYPOINT cd /static && python -m http.server 80
