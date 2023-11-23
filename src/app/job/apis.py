from app.auth.utils import admin_required, job_seeker_required, user_required
from flask import Blueprint, request
from marshmallow import Schema, fields
from app.di import injector
from core.job.services import JobService
from core.job.constants import JobApplicationStatus

job_service = injector.get(JobService)

job_blueprint = Blueprint('job_blueprint', __name__)

class JobSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True)
    description = fields.String(required=True)
    employer = fields.String(required=True)


@job_blueprint.route("/", methods=["POST"])
@admin_required
def create_job(user_id):
    job_schema = JobSchema()
    errors = job_schema.validate(request.get_json())
    if errors:
        return {'errors': errors}, 400
    
    data = job_schema.load(request.get_json())

    job = job_service.create_job(
        title=data["title"],
        employer=data["employer"],
        description=data["description"]
    )

    return job_schema.dump(job)


@job_blueprint.route("", methods=["GET"])
def get_job_list():
    job_list = job_service.get_job_list()
    return job_list


class JobApplicationSchema(Schema):
    job_id = fields.Integer(required=True)
    status = fields.Enum(JobApplicationStatus, dump_only=True)
    job_title = fields.String()
    username = fields.String()


@job_blueprint.route("/application", methods=["POST"])
def apply_job(user_id):
    job_application_schema = JobApplicationSchema()
    errors = job_application_schema.validate(request.get_json())
    if errors:
        return {'errors': errors}, 400
    
    data = job_application_schema.load(request.get_json())
    result = job_service.apply_job(user_id, data['job_id'])

    return job_application_schema.dump(result)