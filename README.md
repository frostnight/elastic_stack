# LOGSTASH 기본 사용
.\bin\logstash.bat -e "input P stdin { } } output { stdout { } }"

.\bin\logstash.bat -f .\config\logstash-test.conf

dissect가 grok보다 속도가 빠름