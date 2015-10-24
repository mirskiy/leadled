#!/usr/bin/env python3

from models import User

users = User.query.all()
print(users)
