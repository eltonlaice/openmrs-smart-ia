from flask import Blueprint, request, jsonify
from app.services.openmrs_service import OpenMRSService
# from app.services.openai_service import OpenAIService

api = Blueprint('api', __name__)

@api.route('/query', methods=['POST'])
def query():
    data = request.json
    question = data.get('question')

    if not question:
        return jsonify({"error": "No question provided"}), 400

    openmrs_service = OpenMRSService()
    # openai_service = OpenAIService()

    # Fetch relevant patient data from OpenMRS
    patient_data = openmrs_service.get_patient_data_for_query(question)

    # Generate response using OpenAI
    # response = openai_service.generate_response(question, patient_data)

    return jsonify({"response": []})
