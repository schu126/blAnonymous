from __init__ import CURSOR, CONN
from User import User
import sqlite3

class Posts:

  all = {}

  def __init__ (self, title, content, publication_date, author_id, likes = 0, dislikes = 0, id = None):
    self.id = id
    self.title = title
    self.content = content
    self.publication_date = publication_date
    self.author_id = author_id
    self.likes = likes
    self.dislikes = dislikes

  def __repr__ (self):
    return f"(Title: {self.title}, Post: {self.content}, Date Posted: {self. publication_date}, Author: {self.author_id}, Likes: {self.likes}, Dislikes: {self.dislikes})"

  @classmethod
  def create_table(cls):
    """ Create a new table to persist the attributes of Post instances """
    sql = """
      CREATE TABLE IF NOT EXISTS posts (
      id INTEGER PRIMARY KEY,
      title TEXT,
      content TEXT,
      publication_date TEXT,
      author_id INTEGER,
      likes INTEGER DEFAULT 0,
      dislikes INTEGER DEFAULT 0,
      FOREIGN KEY (author_id) REFERENCES user(id))
    """

    CURSOR.execute(sql)
    CONN.commit()

  @classmethod
  def drop_table(cls):
    """ Drop the table that persists Post instances """
    sql = """
      DROP TABLE IF EXISTS posts;
    """

    CURSOR.execute(sql)
    CONN.commit()

  def save(self):
    """ Insert a new row with the above values of the current Post object.
    Update object id attribute using the primary key value of new row.
    Save the object in local dictionary using table row's PK as dictionary key """

    sql = """
      INSERT INTO posts (title, content, publication_date, author_id, likes, dislikes)
      VALUES (?, ?, ?, ?, ?, ?)
    """

    CURSOR.execute(sql, (self.title, self.content, self.publication_date, self.author_id, self.likes, self.dislikes))
    CONN.commit()

    self.id = CURSOR.lastrowid
    type(self).all[self.id] = self

  def update(self):
    """ Update the table row corresponding to the current Post instance """
    
    sql = """
      UPDATE posts
      SET title = ?, content = ?, publication_date = ?, author_id = ?, likes = ?, dislikes = ?
      WHERE id = ?
    """

    CURSOR.execute (sql, (self.title, self.content, self.publication_date, self.author_id, self.likes, self.dislikes))
    CONN.commit ()


  def delete(self):
    """ Delete the table row corresponding to the current Post instance, delete the dictionary entry, and reassign id attribute """

    sql = """
      DELETE FROM posts
      WHERE id = ?
    """

    CURSOR.execute(sql, (self.id))
    CONN.commit()

    del type(self).all[self.id]

    self.id = None

  @classmethod
  def create(cls, title, content, publication_date, author_id):
    """ Initialize a new Post instance and save the object to the database """
    likes = 0
    dislikes = 0
    post = cls(title, content, publication_date, author_id, likes, dislikes)
    post.save()
    return post

  @classmethod
  def instance_from_db(cls, row):
    """ Return a Post object having the attribute values from the table row """

    # Check the dictionary fro existing instance using the row's primary key
    post = cls.all.get(row[0])
    if post:
      post.title = row[1]
      post.content = row [2]
      post.publication_date = row[3]
      post.author_id = row[4]
      post.likes = row[5]
      post.dislikes = row[6]
    else:
      post = cls(row[1], row[2], row[3], row[4], row[5], row[6])
      post.id = row[0]
      cls.all[post.id] = post
    return post

  @classmethod
  def get_all(cls):
      """ Return a list containing one Post object per table row """

      sql = """
        SELECT *
        FROM posts
      """

      rows = CURSOR.execute(sql).fetchall()

      return [cls.instance_from_db(row) for row in rows]

  @classmethod
  def find_by_id(cls, id):
      """ Return Post object corresponding to the table row matching the specified primary key """
      sql = """
        SELECT *
        FROM posts
        WHERE id = ?
      """

      row = CURSOR.execute(sql, (id,)).fetchone()
      return cls.instance_from_db(row) if row else None

  @classmethod
  def find_by_title (cls, title):
      """ Return Post object corresponding to first table row matching specified title """
      sql = """
        SELECT *
        FROM posts
        WHERE title is ?
      """

      row = CURSOR.execute(sql, (title,)).fetchone()
      return cls.instance_from_db(row) if row else None

  @classmethod
  def like_post(cls, post_id):
      """Increment the like count for the post with the given ID."""
      sql = """
        UPDATE posts 
        SET likes = likes + 1 
        WHERE id = ?
      """

      CURSOR.execute(sql, (post_id,))
      CONN.commit()

  @classmethod
  def dislike_post(cls, post_id):
      """Increment the dislike count for the post with the given ID."""
      sql = """
        UPDATE posts 
        SET dislikes = dislikes + 1 
        WHERE id = ? 
      """

      CURSOR.execute(sql, (post_id,))
      CONN.commit()
