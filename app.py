from flask import Flask, render_template
from vk_group_parser import VkGroup
from configuration import DOMAIN_LIST
from sqlalchemy import create_engine
import os

app = Flask(__name__)

def create_rows():
    if os.path.exists("lectures.db"):
        os.remove("lectures.db")
    engine = create_engine('sqlite:///lectures.db')
    engine.execute("""
        create table posts (
            post_id integer primary key,
            post_domain varchar not null,
            date integer not null,
            post text not null
        )
    """)
    for i in DOMAIN_LIST:
        obj = VkGroup(i)
        post_dict = obj.get_posts()
        for date, post in post_dict.items():
            post = VkGroup.clear_text(post)
            engine.execute(f'insert into posts(post_domain, date, post) values ("{i}", {date}, "{post}")')
    select_post = engine.execute("select posts.post_domain, posts.post from posts order by posts.date desc")
    return select_post


@app.route('/')
def index():
    select_post = create_rows()
    return render_template('index.html', cur_date=VkGroup.get_current_time(), posts=select_post)


if __name__ == "__main__":
    create_rows()
    app.run(debug=True)
