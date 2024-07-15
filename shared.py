import os, logging
from sqlalchemy import MetaData
from sqlalchemy_schemadisplay import create_schema_graph
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger(__name__)

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
    static_path = os.path.join(os.path.dirname(__file__), 'adminapi', 'static')
    if not os.path.exists(static_path):
        os.makedirs(static_path)
        print(f"Directory created at: {os.path.abspath(static_path)}")
    schema_file = os.path.join(static_path,'schema.png')
    logger.info(f"Schema file: {schema_file}")
    graph.write_png(schema_file)
