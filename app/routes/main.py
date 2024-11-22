from flask import Blueprint, render_template
from flask_socketio import emit
from app.blueprints.services import DetectionService
from app.extensions import socketio
from app.utils.logger import logger


video_feed = Blueprint("main", __name__) 


@video_feed.route('/', methods=['POST', 'GET'])
def index():
    logger.info("Rendering the index page.")
    return render_template('index.html')


@video_feed.route('/health', methods=['GET'])
def health_check():
    return {"status": "ok"}, 200



@socketio.on('image')
def process_image(data_image):
    response = DetectionService.process_image(data_image)
    emit('response_back', response)
