# How to use
1. Go to  https://newsapi.org/
2. Register and get your API key
3. Copy your key to the tool's custom field in Open-WebUI
4. If "no module named newsapi" error occurred, you need to install the newsapi module in your environment
   ```bash
   # if you installed open-webui via pip
   pip install newsapi-python
   # if you installed open-webui via docker(replace <container_name_or_ID> to actual name or id)
   docker ps # get your container info
   docker exec <container_name_or_ID> pip install newsapi-python
   ```
