import os
from sqlalchemy import MetaData
from sqlalchemy_schemadisplay import create_schema_graph
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Function to generate schema graphic
def generate_schema(db):
    metadata = MetaData()
    metadata.reflect(bind=db.engine)
    graph = create_schema_graph(metadata=metadata, engine=db.engine,
        show_datatypes=False, # The image would get nasty big if we'd show the datatypes
        show_indexes=False, # ditto for indexes
        rankdir='LR', # From left to right (instead of top to bottom)
        concentrate=False, # Don't try to join the relation lines together

    )
    static_dir = 'static'
    if not os.path.exists(static_dir):
        os.makedirs(static_dir)
        print(f"Directory created at: {os.path.abspath(static_dir)}")
    graph.write_png('static/schema.png')
