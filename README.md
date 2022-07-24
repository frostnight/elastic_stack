# LOGSTASH 기본 사용
.\bin\logstash.bat -e "input P stdin { } } output { stdout { } }"

.\bin\logstash.bat -f .\config\logstash-test.conf

dissect가 grok보다 속도가 빠름
```
grok {
    pattern_definitions => { "MY_TIMESTAMP" =>
    "%{YEAR}[/-]%{MONTHNUM}[/-]%{MONTHDAY}[T ]%{HOUR}:?%{MINUTE}(?::?%{SECOND})?%{ISO8601_TIMEZONE}?"
    }
    match => {"message" =>
    "\[%{MY_TIMESTAMP:timestamp}\] [ ]*\[%{DATA:id}\] %{IP:ip} %{NUMBER:port:int} \[%{LOGLEVEL:level}\] \- %{DATA:msg}\."}
}
```

# 트위터 관련
트위터 API V2가 로그스태시에서 지원이 안됨 v1은 신규생성 계정에 대해서 지원이 안됨


436p