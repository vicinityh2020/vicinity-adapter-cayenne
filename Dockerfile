#################################################################
#   Copyright (C) 2018  
#   This program and the accompanying materials are made
#   available under the terms of the Eclipse Public License 2.0
#   which is available at https://www.eclipse.org/legal/epl-2.0/ 
#   SPDX-License-Identifier: EPL-2.0
#   Contributors: ATOS SPAIN S.A.
################################################################# 

# agile-lora installation
FROM python:3-alpine
WORKDIR /usr/src/app 

# RUN apt-get update && apt-get install --no-install-recommends -y \
#     python3-dev \
#     python3-pip \
#     && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY . .

RUN python3 -m pip install -r requirements.txt 
CMD [ "python3", "/usr/src/app/cayenne_adapter.py" ]