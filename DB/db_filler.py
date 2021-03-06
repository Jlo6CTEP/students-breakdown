import string

import postgresql
import random
from DB.db_manager import db

db1 = postgresql.open("pq://zpgkwdlt:M4Ef1T1p8VmvYamieL-JR3ZK4J0hztBy@dumbo.db.elephantsql.com:5432/zpgkwdlt")

topics = list(zip(*db1.query("select topic_id from topic")))[0]
study_groups = db1.query("select * from study_group")

# experience + skill_offsets (to make PL skills correlating with experience)
skill_offset = [4, 5, 6, 8, 9, 10]
skill_range = range(0, 10)

mails = random.sample(open("../Data/email.txt").read().split(','), k=200)
names = random.sample(open("../Data/first_name.txt").read().split(','), k=200)
usernames = random.sample(open("../Data/first_name.txt").read().split(','), k=200)
surnames = open("../Data/last_name.txt").read().split(',')

for x in range(200):
    rand_password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=30))
    # insert into main database
    sid = db.register_user({"password": rand_password, "mail": mails[x],
                            "name": names[x], "surname": random.choice(surnames),
                            "study_group": [random.choice(study_groups)[1]], "username": usernames[x],
                            "priv_name": "student"})
    poll = {x[0]: x[1] for x in zip(["topic1", "topic2", "topic3"], random.sample(topics, k=3))}
    poll.update({"course_id": 3, "project_id": 15})
    db.fill_poll(sid, poll)
    print("Done {}".format(x))
