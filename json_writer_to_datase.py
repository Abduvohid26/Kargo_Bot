from loader import bot, db
import json
import logging


def json_writer_to_database():
    try:
        with open('main.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        print('Starting to import data...')
        for item in data:
            existing_address = db.select_address(
                region_id=item['region_id'],
                name=item['name'],
                pk=item['id'],
                region_name=item['region_name']
            )

            if not existing_address:
                db.add_address(
                    user_id=item.get('user_id'),
                    region_id=item['region_id'],
                    name=item['name'],
                    pk=item['id'],
                    region_name=item['region_name']
                )
            else:
                print(
                    f"Full address record already exists for {item['name']} in region {item['region_name']}. Skipping.")

        print('Data import completed.')
    except Exception as e:
        print(f"Error during JSON import: {e}")
        logging.error(f"Error during JSON import: {e}")
