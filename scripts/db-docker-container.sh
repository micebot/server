docker run \
    --name micebot \
    -p 5432:5432 \
    -e POSTGRES_DB=micebot \
    -e POSTGRES_USER=micebot \
    -e POSTGRES_PASSWORD=micebot \
    -d postgres:12