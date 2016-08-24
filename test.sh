
for i in 1 2 3
do
    scrapy crawl cgl -o "data$i.json" -s LOG_FILE="log$i.txt"
done
