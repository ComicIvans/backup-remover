from minio import Minio
from datetime import datetime, timedelta, time
from dotenv import dotenv_values
import logging

logging.basicConfig(
  format='%(asctime)s %(levelname)-4s - %(message)s',
  level=logging.INFO,
  datefmt='%Y-%m-%d %H:%M:%S')

MINIO_CONFIG = dotenv_values("minio.env")

def main():
  # Create the MinIO client.
  client = Minio(
    MINIO_CONFIG["MINIO_URL"],
    access_key=MINIO_CONFIG["MINIO_ACCESS_KEY"],
    secret_key=MINIO_CONFIG["MINIO_SECRET_KEY"],
    secure=MINIO_CONFIG["MINIO_SECURE"] == "True",
    region=MINIO_CONFIG["MINIO_REGION"],
  )

  # Get all objects in the bucket.
  objects = client.list_objects(MINIO_CONFIG["MINIO_BUCKET"])

  # Create a dictionary to store the backups by date.
  backups_by_date = {}

  # Iterate over the objects and group them by date.
  for obj in objects:
    date_str = obj.object_name.split("-")
    date_str = date_str[0] + '-' + date_str[1]
    date = datetime.strptime(date_str, "%Y%m%d-%H%M%S")

    # Add the object to the dictionary.
    if backups_by_date.get(date) is None:
      backups_by_date[date] = {
        'data': obj,
        'remove': False,
      }
    else:
      print(f"Duplicate backup found: {obj.object_name}")
      return
  
  # Sort the backups by date, from newest to oldest.
  backup_dates = sorted(backups_by_date.keys(), reverse=True)

  # Get the current date at midnight.
  today = datetime.combine(datetime.today(), time.min)

  # Calculate the cutoff dates for each backup retention period.
  one_day_ago = today - timedelta(days=1)
  one_week_ago = today - timedelta(weeks=1)
  one_month_ago = today - timedelta(weeks=4)
  six_months_ago = today - timedelta(weeks=26)
  one_year_ago = today - timedelta(weeks=52)

  prev_date = today
  # Iterate over the backups and delete the ones that don't meet the retention criteria.
  for date in backup_dates:
    # Keep all backups from the same day or the day before.
    if date >= one_day_ago:
      prev_date = date
      continue

    # Keep only one backup per day from one day ago to one week ago.
    if date >= one_week_ago and prev_date < one_day_ago:
      backups_by_date[prev_date]['remove'] = True
      prev_date = date
      continue
      for i, backup in enumerate(backups_by_date.get(date)):
        if i != 0:
          logging.info(f"Deleting {backup.object_name}...")
          client.remove_object(MINIO_CONFIG["MINIO_BUCKET"], backup.object_name)
      continue

    # Keep only one backup per week from one week ago to one month ago.
    if date >= one_month_ago and prev_date < one_week_ago:
      backups_by_date[prev_date]['remove'] = True
      prev_date = date
      continue
      if date.weekday() != 6:
        for i, backup in enumerate(backups_by_date.get(date)):
          if i != 0:
            logging.info(f"Deleting {backup.object_name}...")
            client.remove_object(MINIO_CONFIG["MINIO_BUCKET"], backup.object_name)
      continue

    # Keep only one backup per month from one month ago to six months ago.
    if date >= six_months_ago and prev_date < one_month_ago:
      backups_by_date[prev_date]['remove'] = True
      prev_date = date
      continue
      if date.day != 1:
        for i, backup in enumerate(backups_by_date.get(date)):
          if i != 0:
            logging.info(f"Deleting {backup.object_name}...")
            #client.remove_object(MINIO_CONFIG["MINIO_BUCKET"], backup.object_name)
      continue

    # Keep only one backup per two months from six months ago to one year ago.
    if date >= one_year_ago and prev_date < six_months_ago:
      backups_by_date[prev_date]['remove'] = True
      prev_date = date
      continue
      if date.month % 2 != 0:
        for i, backup in enumerate(backups_by_date.get(date)):
          if i != 0:
            logging.info(f"Deleting {backup.object_name}...")
            #client.remove_object(MINIO_CONFIG["MINIO_BUCKET"], backup.object_name)
      continue

    # Keep only one backup per six months from one year ago.
    if date < one_year_ago and prev_date < one_year_ago:
      # TODO
      continue
      if date.month != 1:
        for i, backup in enumerate(backups_by_date.get(date)):
          if i != 0:
            logging.info(f"Deleting {backup.object_name}...")
            #client.remove_object(MINIO_CONFIG["MINIO_BUCKET"], backup.object_name)
      continue

    prev_date = date

  # Delete the backups that don't meet the retention criteria.
  for date in backup_dates:
    if backups_by_date[date]['remove']:
      logging.info(f"Deleting {backups_by_date[date]['data'].object_name}...")
      client.remove_object(MINIO_CONFIG["MINIO_BUCKET"], backups_by_date[date]['data'].object_name)

if __name__ == "__main__":
  main()