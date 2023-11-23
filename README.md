## Assignment Database Design

User
- id (primary key)
- username (string, 20)
- password (string - hashed, bcrypt)
- bio (string, 150)


Tweet
- id (primary key)
- user_id (FK user.id)
- tweet
- published_at (datetime, default=utcnow)


Following (association table)
- id (primary key)
- user_id (FK user.id)
- following_user_id (FK user.id)


## Use Case

1. Registration

```
User(username=username, password=password, bio=bio)
```

2. Login

```
User.query.filter(username=username)
```


3. Following API
```
# check record existence
Following.query.filter(user_id=user_id, follower_user_id=follower_user_id)

# create if not exist
Following(user_id, user_id_to_follow)

# delete
db.session.delete()
```


4. User Profile API
```
User.query.get(user_id)

Tweet.query.filter_by(user_id=user_id).order_by(Tweet.published_at.desc()).limit(10).all()

following = Following.query.filter(user_id=user_id).count()

follower = Following.query.filter(following_user_id=user_id).count()
```

5. Post a Tweet API
```
Tweet(user_id=user_id, tweet=tweet)
db.session.add()
```