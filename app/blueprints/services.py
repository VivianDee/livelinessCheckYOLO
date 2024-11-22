from flask import session 
import base64
import io
import cv2
import numpy as np
from PIL import Image
from app.blueprints.yolo_model import YOLOModel
from app.blueprints.helpers import annotate_frame
from app.utils.logger import logger


frame_skip = 5
frame_count = 0



class DetectionService:
    @staticmethod
    def process_image(data_image):
        try:
            if 'frame_count' not in session:
                session['frame_count'] = 0


            image_data = data_image.split(',', 1)[1]  # Remove prefix
            image_bytes = io.BytesIO(base64.b64decode(image_data))

            try:
                pil_image = Image.open(image_bytes)
            except Exception:
                logger.error("Cannot identify image file")
                return {'error': 'Cannot identify image file'}
            
            frame = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
            annotated_frame = frame
            

            # Skip frames to improve performance
            session['frame_count'] += 1
            if session['frame_count'] % frame_skip == 0:
                
                # Perform detection
                results = YOLOModel.detect(frame)
                annotated_frame = annotate_frame(frame, results)

            # Convert to base64
            _, img_encoded = cv2.imencode('.jpg', annotated_frame)
            b64_image = base64.b64encode(img_encoded).decode('utf-8')
            return {'image': f"data:image/jpg;base64,{b64_image}"}
        except Exception as e:
            logger.error(f"An error occurred during image processing: {str(e)}", exc_info=True)
            # return {'error': 'An internal error occurred while processing the image.'}
