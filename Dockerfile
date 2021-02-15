FROM python:3.7.9-alpine3.13
WORKDIR /sarka-docker
RUN pip install requests
COPY jira_to_fakturoid_import.py .
CMD ["python", "jira-to-fakturoid-import.py"]
