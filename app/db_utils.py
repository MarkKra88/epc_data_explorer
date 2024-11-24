from app.models import db, APIResult, ScraperResult

def save_api_results(data):
    """
    Save API data to the database.
    """


    for row in data:

        result = APIResult(

            lmk_key=row['lmk-key'],
            address1=row['address1'],
            address2=row['address2'],
            address3=row['address3'],
            postcode=row['postcode'],
            inspection_date=row['inspection-date'],
            uprn=row['uprn']
        )

        db.session.add(result)
    db.session.commit()

def save_scraper_results(data):
    """
    Save scraper data to the database.
    """
    for row in data:
        result = ScraperResult(
            address=row['Address'],
            energy_rating=row['Energy Rating'],
            valid_until=row['Valid Until'],
            expired=row['Expired']
        )
        db.session.add(result)
    # Commit the session
    try:
        db.session.commit()
        print("Data successfully saved.")
    except Exception as e:
        print(f"Error committing to database: {e}")
        db.session.rollback()

def get_api_results(postcode):
    """
    Fetch API data by postcode from the database.
    """
    results = APIResult.query.filter_by(postcode=postcode).all()
    return [{"lmk_key": r.lmk_key,
             "address1": r.address1,
             "address2": r.address2,
             "address3": r.address3,
             "postcode": r.postcode,
             "inspection_date": r.inspection_date,
             "uprn": r.uprn} for r in results]

def get_scraper_results(postcode):
    """
    Fetch scraper data by postcode from the database.
    """
    return ScraperResult.query.filter(ScraperResult.address.contains(postcode)).all()

def reset_database():
    """
    Drop all tables and recreate the database schema.
    """

    db.drop_all()  # Drop all tables
    db.create_all()  # Recreate all tables

