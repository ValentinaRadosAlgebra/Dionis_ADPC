rule all:
    input:
        "output/plots/birds.png",
        "output/report.csv"


rule upload:
    output:
        "output/upload.done"
    shell:
        "python -m code.upload_mimio"


rule scrape:
    output:
        "output/scrape.done"
    shell:
        "python -m code.scrape_taxonomy"


rule classify:
    input:
        "output/upload.done"
    output:
        "output/classify.done"
    shell:
        "python -m code.classify_birds"

rule kafka_consume:
    input:
        "output/classify.done"
    output:
        "output/kafka.done"
    shell:
        "python -m code.kafka_consumer"

rule fuzzy:
    input:
        "output/scrape.done",
        "output/classify.done",
        "output/kafka.done"
    output:
        "output/fuzzy.done"
    shell:
        "python -m code.fuzzy_match"


rule report:
    input:
        "output/fuzzy.done"
    output:
        "output/report.csv"
    shell:
        "python -m code.generate_report"


rule visualize:
    input:
        "output/fuzzy.done"
    output:
        "output/plots/birds.png"
    shell:
        "python -m code.visualize"