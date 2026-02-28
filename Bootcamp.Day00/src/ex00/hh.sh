#!/bin/sh

if [ -n "$1" ]; then
    user_query="$1"

    url="https://api.hh.ru/vacancies"

    curl -s -G -d "per_page=20" --data-urlencode "text=$user_query" "$url" | jq > hh.json
else
    echo "Введите параметр для поиска вакансий"
fi
