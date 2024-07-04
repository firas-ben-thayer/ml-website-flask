from ressources import db, app
from ressources.models import Exercise

# # Push the application context
# with app.app_context():
#     # Drop the Exercise table
#     Exercise.__table__.drop(db.engine)
#     print("Exercise table dropped.")

# Update the tables
# db.create_all()

# # Push the application context
# for i in range(10):
#     with app.app_context():
#         # Create a new Exercise instance
#         new_exercise = Exercise(
#             name="Math Exercise" + str(i),
#             subject="Mathematics",
#             description="A basic math exercise covering addition and subtraction."+ str(i),
#             content="1 + 1 = ?; 2 - 1 = ?",
#             author=1  # Assuming the user with id 1 exists in the User table
#         )

#         # Add the instance to the session
#         db.session.add(new_exercise)
        
#         # Commit the session to push the changes to the database
#         db.session.commit()
        
#         print("New exercise added to the Exercise table.")
