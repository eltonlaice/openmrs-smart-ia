import requests
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class OpenMRSService:
    def __init__(self):
        # Initialize the OpenMRS service with environment variables
        self.base_url = os.getenv('OPENMRS_BASE_URL')
        self.username = os.getenv('OPENMRS_USERNAME')
        self.password = os.getenv('OPENMRS_PASSWORD')
        self.session = requests.Session()
        self.session.auth = (self.username, self.password)

    def get_patient_data(self, patient_uuid):
        # Retrieve comprehensive patient data
        patient_data = {}

        # Patient Demographics
        demographics = self._get_patient_demographics(patient_uuid)
        patient_data['demographics'] = demographics

        # Vital Signs
        vitals = self._get_patient_vitals(patient_uuid)
        patient_data['vitals'] = vitals

        # Diagnoses
        diagnoses = self._get_patient_diagnoses(patient_uuid)
        patient_data['diagnoses'] = diagnoses

        # Medications
        medications = self._get_patient_medications(patient_uuid)
        patient_data['medications'] = medications

        # Lab Results
        lab_results = self._get_patient_lab_results(patient_uuid)
        patient_data['lab_results'] = lab_results

        # Treatment Plans
        treatment_plans = self._get_patient_treatment_plans(patient_uuid)
        patient_data['treatment_plans'] = treatment_plans

        # Symptoms
        symptoms = self._get_patient_symptoms(patient_uuid)
        patient_data['symptoms'] = symptoms

        # Procedures
        procedures = self._get_patient_procedures(patient_uuid)
        patient_data['procedures'] = procedures

        # Immunization Records
        immunizations = self._get_patient_immunizations(patient_uuid)
        patient_data['immunizations'] = immunizations

        # Lifestyle Factors
        lifestyle = self._get_patient_lifestyle(patient_uuid)
        patient_data['lifestyle'] = lifestyle

        # Social Determinants of Health
        social_determinants = self._get_patient_social_determinants(patient_uuid)
        patient_data['social_determinants'] = social_determinants

        # Visit History
        visit_history = self._get_patient_visit_history(patient_uuid)
        patient_data['visit_history'] = visit_history

        return patient_data

    def _get_patient_demographics(self, patient_uuid):
        # Retrieve patient demographics including age, gender, ethnicity, and medical history
        response = self.session.get(f"{self.base_url}/patient/{patient_uuid}")
        if response.status_code == 200:
            data = response.json()
            return {
                'age': self._calculate_age(data['person']['birthdate']),
                'gender': data['person']['gender'],
                'ethnicity': data['person'].get('ethnicity', 'Unknown'),
                'medical_history': self._get_medical_history(patient_uuid),
                'family_medical_history': self._get_family_medical_history(patient_uuid)
            }
        return None

    def _get_patient_vitals(self, patient_uuid):
        # Retrieve patient vital signs
        response = self.session.get(f"{self.base_url}/obs?patient={patient_uuid}&concept=Vital Signs")
        if response.status_code == 200:
            data = response.json()
            vitals = {
                'blood_pressure': [],
                'heart_rate': [],
                'temperature': [],
                'respiratory_rate': [],
                'oxygen_saturation': []
            }
            for obs in data['results']:
                if obs['concept']['display'] == 'Blood Pressure':
                    vitals['blood_pressure'].append(obs['value'])
                elif obs['concept']['display'] == 'Heart Rate':
                    vitals['heart_rate'].append(obs['value'])
                elif obs['concept']['display'] == 'Temperature':
                    vitals['temperature'].append(obs['value'])
                elif obs['concept']['display'] == 'Respiratory Rate':
                    vitals['respiratory_rate'].append(obs['value'])
                elif obs['concept']['display'] == 'Oxygen Saturation':
                    vitals['oxygen_saturation'].append(obs['value'])
            return vitals
        return None

    def _get_patient_diagnoses(self, patient_uuid):
        # Retrieve patient diagnoses including current, past, and chronic conditions
        response = self.session.get(f"{self.base_url}/condition?patient={patient_uuid}")
        if response.status_code == 200:
            data = response.json()
            diagnoses = {
                'current': [],
                'past': [],
                'chronic': []
            }
            for condition in data['results']:
                if condition['clinicalStatus']['coding'][0]['code'] == 'active':
                    diagnoses['current'].append(condition['code']['coding'][0]['display'])
                elif condition['clinicalStatus']['coding'][0]['code'] == 'resolved':
                    diagnoses['past'].append(condition['code']['coding'][0]['display'])
                if condition.get('verificationStatus', {}).get('coding', [{}])[0].get('code') == 'confirmed':
                    diagnoses['chronic'].append(condition['code']['coding'][0]['display'])
            return diagnoses
        return None

    def _get_patient_medications(self, patient_uuid):
        # Retrieve patient medications including current, history, and allergies
        response = self.session.get(f"{self.base_url}/medicationrequest?patient={patient_uuid}")
        if response.status_code == 200:
            data = response.json()
            medications = {
                'current': [],
                'history': [],
                'allergies': []
            }
            for med in data['results']:
                if med['status'] == 'active':
                    medications['current'].append(med['medicationCodeableConcept']['coding'][0]['display'])
                else:
                    medications['history'].append(med['medicationCodeableConcept']['coding'][0]['display'])
            
            # Get allergies
            allergy_response = self.session.get(f"{self.base_url}/allergyintolerance?patient={patient_uuid}")
            if allergy_response.status_code == 200:
                allergy_data = allergy_response.json()
                for allergy in allergy_data['results']:
                    medications['allergies'].append(allergy['code']['coding'][0]['display'])
            
            return medications
        return None

    def _get_patient_lab_results(self, patient_uuid):
        # Retrieve patient lab results including blood tests, urine tests, and imaging results
        response = self.session.get(f"{self.base_url}/diagnosticreport?patient={patient_uuid}")
        if response.status_code == 200:
            data = response.json()
            lab_results = {
                'blood_tests': [],
                'urine_tests': [],
                'imaging_results': []
            }
            for report in data['results']:
                if 'blood' in report['code']['coding'][0]['display'].lower():
                    lab_results['blood_tests'].append(report)
                elif 'urine' in report['code']['coding'][0]['display'].lower():
                    lab_results['urine_tests'].append(report)
                elif any(x in report['code']['coding'][0]['display'].lower() for x in ['x-ray', 'mri', 'ct']):
                    lab_results['imaging_results'].append(report)
            return lab_results
        return None

    def _get_patient_treatment_plans(self, patient_uuid):
        # Retrieve patient treatment plans including current and past
        response = self.session.get(f"{self.base_url}/careplan?patient={patient_uuid}")
        if response.status_code == 200:
            data = response.json()
            treatment_plans = {
                'current': [],
                'past': []
            }
            for plan in data['results']:
                if plan['status'] == 'active':
                    treatment_plans['current'].append(plan)
                else:
                    treatment_plans['past'].append(plan)
            return treatment_plans
        return None

    def _get_patient_symptoms(self, patient_uuid):
        # Retrieve patient symptoms including severity and duration
        response = self.session.get(f"{self.base_url}/observation?patient={patient_uuid}&category=symptom")
        if response.status_code == 200:
            data = response.json()
            symptoms = []
            for symptom in data['results']:
                symptoms.append({
                    'symptom': symptom['code']['coding'][0]['display'],
                    'severity': symptom.get('valueQuantity', {}).get('value'),
                    'duration': symptom.get('effectivePeriod', {}).get('start')
                })
            return symptoms
        return None

    def _get_patient_procedures(self, patient_uuid):
        # Retrieve patient procedures including surgical and other medical procedures
        response = self.session.get(f"{self.base_url}/procedure?patient={patient_uuid}")
        if response.status_code == 200:
            data = response.json()
            procedures = {
                'surgical': [],
                'other': []
            }
            for procedure in data['results']:
                if 'surgery' in procedure['code']['coding'][0]['display'].lower():
                    procedures['surgical'].append(procedure)
                else:
                    procedures['other'].append(procedure)
            return procedures
        return None

    def _get_patient_immunizations(self, patient_uuid):
        # Retrieve patient immunization records
        response = self.session.get(f"{self.base_url}/immunization?patient={patient_uuid}")
        if response.status_code == 200:
            data = response.json()
            immunizations = []
            for immunization in data['results']:
                immunizations.append({
                    'vaccine': immunization['vaccineCode']['coding'][0]['display'],
                    'date': immunization['occurrenceDateTime']
                })
            return immunizations
        return None

    def _get_patient_lifestyle(self, patient_uuid):
        # Retrieve patient lifestyle factors
        response = self.session.get(f"{self.base_url}/observation?patient={patient_uuid}&category=social-history")
        if response.status_code == 200:
            data = response.json()
            lifestyle = {
                'smoking_status': None,
                'alcohol_consumption': None,
                'exercise_habits': None,
                'diet_information': None
            }
            for obs in data['results']:
                if 'smoking' in obs['code']['coding'][0]['display'].lower():
                    lifestyle['smoking_status'] = obs['valueCodeableConcept']['coding'][0]['display']
                elif 'alcohol' in obs['code']['coding'][0]['display'].lower():
                    lifestyle['alcohol_consumption'] = obs['valueCodeableConcept']['coding'][0]['display']
                elif 'exercise' in obs['code']['coding'][0]['display'].lower():
                    lifestyle['exercise_habits'] = obs['valueCodeableConcept']['coding'][0]['display']
                elif 'diet' in obs['code']['coding'][0]['display'].lower():
                    lifestyle['diet_information'] = obs['valueCodeableConcept']['coding'][0]['display']
            return lifestyle
        return None

    def _get_patient_social_determinants(self, patient_uuid):
        # Retrieve patient social determinants of health
        response = self.session.get(f"{self.base_url}/observation?patient={patient_uuid}&category=social-history")
        if response.status_code == 200:
            data = response.json()
            social_determinants = {
                'socioeconomic_status': None,
                'living_conditions': None,
                'occupation': None
            }
            for obs in data['results']:
                if 'socioeconomic' in obs['code']['coding'][0]['display'].lower():
                    social_determinants['socioeconomic_status'] = obs['valueCodeableConcept']['coding'][0]['display']
                elif 'living' in obs['code']['coding'][0]['display'].lower():
                    social_determinants['living_conditions'] = obs['valueCodeableConcept']['coding'][0]['display']
                elif 'occupation' in obs['code']['coding'][0]['display'].lower():
                    social_determinants['occupation'] = obs['valueCodeableConcept']['coding'][0]['display']
            return social_determinants
        return None

    def _get_patient_visit_history(self, patient_uuid):
        # Retrieve patient visit history including frequency and reasons for visits
        response = self.session.get(f"{self.base_url}/encounter?patient={patient_uuid}")
        if response.status_code == 200:
            data = response.json()
            visits = []
            for encounter in data['results']:
                visits.append({
                    'date': encounter['period']['start'],
                    'reason': encounter['type'][0]['coding'][0]['display']
                })
            return visits
        return None

    def _calculate_age(self, birthdate):
        # Calculate patient's age based on birthdate
        born = datetime.strptime(birthdate, "%Y-%m-%d")
        today = datetime.today()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    def _get_medical_history(self, patient_uuid):
        # Retrieve patient's medical history
        response = self.session.get(f"{self.base_url}/condition?patient={patient_uuid}")
        if response.status_code == 200:
            data = response.json()
            return [condition['code']['coding'][0]['display'] for condition in data['results']]
        return None

    def _get_family_medical_history(self, patient_uuid):
        # Retrieve patient's family medical history
        response = self.session.get(f"{self.base_url}/familymemberhistory?patient={patient_uuid}")
        if response.status_code == 200:
            data = response.json()
            family_history = []
            for history in data['results']:
                family_history.append({
                    'relationship': history['relationship']['coding'][0]['display'],
                    'condition': history['condition'][0]['code']['coding'][0]['display']
                })
            return family_history
        return None


