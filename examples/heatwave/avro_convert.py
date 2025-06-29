import csv
from fastavro import reader

def avro_to_csv(avro_file_path, csv_file_path):
    with open(avro_file_path, 'rb') as avro_file:
        avro_reader = reader(avro_file)
        schema_fields = avro_reader.schema['fields']
        fieldnames = [field['name'] for field in schema_fields]

        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for record in avro_reader:
                writer.writerow(record)

    print(f"Successfully converted '{avro_file_path}' to '{csv_file_path}'")

# Example usage:
if __name__ == "__main__":
    """
    ./35642a9b-4243-49e1-96ca-d939ce2c364f/survey.avro
    ./35642a9b-4243-49e1-96ca-d939ce2c364f/survey.csv
    ./575e44ac-2eb7-4081-b4a7-6482627173ed/survey.avro
    ./575e44ac-2eb7-4081-b4a7-6482627173ed/survey.csv
    """
    # avro_to_csv("./35642a9b-4243-49e1-96ca-d939ce2c364f/status.avro", "./35642a9b-4243-49e1-96ca-d939ce2c364f/status.csv")
    # avro_to_csv("./575e44ac-2eb7-4081-b4a7-6482627173ed/status.avro", "./575e44ac-2eb7-4081-b4a7-6482627173ed/status.csv")
    avro_to_csv("./35642a9b-4243-49e1-96ca-d939ce2c364f/dialog.avro",
                "./35642a9b-4243-49e1-96ca-d939ce2c364f/dialog.csv")
    avro_to_csv("./575e44ac-2eb7-4081-b4a7-6482627173ed/dialog.avro",
                "575e44ac-2eb7-4081-b4a7-6482627173ed/dialog.csv")

