#!/usr/bin/env python3

from models import User, db
admin = User('admin', 'admin@example.com')
guest = User('guest', 'guest@exaple.com')

db.session.add(admin)
db.session.add(guest)
db.session.commit()


