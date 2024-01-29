#!/bin/env zsh
docker run --rm -v jira-volume:/var/atlassian/application-data/jira --name="jira" -d -p 8080:8080 atlassian/jira-software