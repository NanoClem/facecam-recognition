from flask_restplus import reqparse
from werkzeug.datastructures import FileStorage


# Create our parser
my_parser = reqparse.RequestParser()

# Add parsing arguments
my_parser.add_argument('file',
                        location='files',
                        type=FileStorage,
                        required=True)
