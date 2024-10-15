from loader import bot, db
import json
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def json_writer_to_database():
    try:
        with open('main.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Print and log the type and content of the loaded data
        logging.info(f"Data Type: {type(data)}")
        logging.info(f"Data Content: {data}")

        # Check if data is a dictionary with 'regions'
        if not isinstance(data, dict) or 'regions' not in data:
            raise ValueError("JSON data is not in the expected format")

        regions = data['regions']
        logging.info('Starting to import data...')

        for region in regions:
            region_id = region.get('id')
            region_name = region.get('name')
            if not isinstance(region_id, int) or not isinstance(region_name, str):
                raise ValueError(f"Invalid region data: {region}")

            for district in region.get('districts', []):
                district_id = district.get('id')
                district_name = district.get('name')

                if not isinstance(district_id, int) or not isinstance(district_name, str):
                    raise ValueError(f"Invalid district data: {district}")

                # Prepare data for insertion
                existing_address = db.select_address(
                    region_id=str(region_id),
                    name=district_name,
                    pk=str(district_id),
                    region_name=region_name
                )

                if not existing_address:
                    db.add_address(
                        user_id=None,  # Assuming no user_id is provided
                        region_id=str(region_id),
                        name=district_name,
                        pk=str(district_id),
                        region_name=region_name
                    )
                    logging.info(f"Added address: {district_name} in region {region_name}")
                else:
                    logging.info(f"Full address record already exists for {district_name} in region {region_name}. Skipping.")

        logging.info('Data import completed.')
    except Exception as e:
        logging.error(f"Error during JSON import: {e}")


import openpyxl


# Excel faylidan o'qish va ma'lumotlarni ma'lumotlar bazasiga yozish
def write_to_database():
    print('salom')
    file_name = 'users_list.xlsx'
    if file_name:

        # Excel faylini ochamiz
        workbook = openpyxl.load_workbook(file_name)
        sheet = workbook.active

        # Har bir qatorni o'qiymiz, bosh qatorni tashlab
        for row in sheet.iter_rows(min_row=2, values_only=True):
            # Qator ma'lumotlarini o'zgaruvchilarga ajratib olamiz
            fullname, phone, manzil, tuman, exact_address, description, user_id, added_time, phone_number, saja, sj_avia = row

            # Ma'lumotlar bazasiga yozish
            db.add_user(
                id=user_id,  # ID ni user_id dan olamiz
                fullname=fullname,
                telegram_id=None,  # Telegram ID agar mavjud bo'lsa
                language='uz',  # Default til
                phone=phone,
                phone_number=phone_number,
                manzil=manzil,
                saja=saja,
                sj_avia=sj_avia,
                tuman=tuman,
                exact_address=exact_address,
                description=description,
                user_id=user_id
            )
    print("All user addd")