from langchain_community.document_loaders import CSVLoader

loader=CSVLoader(
    file_path="./data/stu.csv",
    encoding="utf-8",
    csv_args={
        "delimiter": ",",
        "quotechar": '"',
        # "fieldnames": ["name", "age", "gender"],
    },
)

for document in loader.lazy_load():
    print(type(document),document)

