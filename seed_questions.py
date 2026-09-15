from datetime import datetime

from pybo import create_app,db
from pybo.models import Question

def insert_test_data(n=300):
    """ Test Insert Data    """
    app =create_app()
    with app.app_context():
        for index in range(n):
            q=Question(
                subject = f"subject{index:03d}",
                content = f"content{index:03d}",
                create_date = datetime.now()
            )
            db.session.add(q)
        db.session.commit()
        print(f"Inserted {n} records.")

if __name__ == "__main__":
    insert_test_data()

