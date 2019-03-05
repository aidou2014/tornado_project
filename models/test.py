from sqlalchemy import desc
from models.account import User, PostPicture, Like
from models.db import DBSession

session = DBSession()

rows = session.query(PostPicture).filter(PostPicture.user_id == 1,
                                         PostPicture.is_delete == False).order_by(desc(PostPicture.id)).all()

# print(dir(rows.post_pictures))
# print(rows.post_pictures[0].image_url)
print(rows)

# rows = session.query(PostPicture).filter_by(user_id =4).first()
# print(dir(rows.post_user))
