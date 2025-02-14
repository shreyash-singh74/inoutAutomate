from fastapi.responses import JSONResponse
from fastapi import UploadFile, File, Form
from sqlalchemy import Select as select
from sqlalchemy.orm import Session
from db.models import User
from fastapi import APIRouter, Cookie
import jwt
from config import JWT_SECRET, JWT_ALGORITHM, engine
from uuid import UUID
from db.models import (
    Applications,
    ApplicationActions,
    ApplicationStatus,
    SupportingDocuments,
)
from datetime import datetime
from .schema import (
    UpdateApplicationSchema,
    ForwardApplicationSchema,
)
from uuid import uuid4
import logging
from typing import Annotated
from mail import create_message
from fastapi import APIRouter, Cookie, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session, aliased
from sqlalchemy.future import select
from uuid import UUID
from datetime import datetime
from dotenv import load_dotenv
import os
from db.models import UserRole

load_dotenv()
application_router = APIRouter()

# Logger setup
logger = logging.getLogger(__name__)


def protectRoute(access_token: str):
    """ Validates JWT and returns the authenticated user if valid. """
    try:
        if not access_token:
            logger.warning("No access token provided.")
            return None

        # Convert to bytes if necessary
        if isinstance(access_token, str):
            access_token = access_token.encode("utf-8")

        # Decode JWT
        payload = jwt.decode(access_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        email = payload.get("sub")  # ✅ Extract email from 'sub'

        if not email:
            logger.warning("JWT payload missing 'sub' (email) field.")
            return None

        # Fetch user from database using email
        with Session(engine) as session:
            statement = select(User).where(User.tcet_email == email)
            user = session.scalars(statement).first()

            if not user:
                logger.warning(f"User not found for email: {email}")
                return None

            return user

    except jwt.ExpiredSignatureError:
        logger.error("JWT token has expired.")
    except jwt.InvalidTokenError:
        logger.error("Invalid JWT token.")
    except Exception as e:
        logger.error(f"Unexpected error during JWT decoding: {e}")

    return None  # Return None if any error occurs



@application_router.post("/create")
async def createApplication(
    document: UploadFile = File(None),
    description: str = Form(...),
    subject: str = Form(...),
    for_user: str = Form(...),
    access_token: str = Cookie(None),
):
    user = protectRoute(access_token)
    if not isinstance(user, User):
        return user
    document_url = None
    if document and document.filename:
        document_url = f"media/{document.filename}{uuid4()}"
        name, ext = document.filename.rsplit(".", 1)
        unique_filename = f"{user.username}_{uuid4()}.{ext}"
        document_url = f"media/{unique_filename}"
        with open(document_url, "wb") as f:
            content = await document.read()
            f.write(content)
    receiver_email = None
    with Session(engine) as session:
        statement = select(User).where(User.role == "CLERKS")
        receiver = session.scalars(statement).one()
        receiver_email = receiver.tcet_email
        if not receiver:
            return JSONResponse(
                content={"message": "Receiver not found"}, status_code=404
            )
        application_id = uuid4()
        newApplication = Applications.create_with_counter(
            session=session,
            description=description,
            created_by_id=user.id,
            current_handler_id=receiver.id,
            id=application_id,
            to=for_user,
            subject=subject,
            status=ApplicationStatus.PENDING,
        )
        newApplicationAction = ApplicationActions(
            from_user_id=user.id,
            to_user_id=receiver.id,
            application_id=newApplication.id,
            action_type="INWARD",
        )
        newDocument = SupportingDocuments(
            application_id=application_id,
            document_name=document.filename,
            document_url=document_url,
        )
        session.add(newApplication)
        session.add(newApplicationAction)
        session.add(newDocument)
        session.commit()
        link = f"http://{os.getenv("CLIENT_URL")}/application/{application_id}"
        html_message = f"""
        <h1>Application is Inwarded</h1>
        <p>Click here to see application <a href="{link}">link</a></p>
        """
        subject = "please check this application"
        if receiver_email:
            await create_message([receiver.tcet_email], subject, html_message)
    return JSONResponse(content={"message": "Application created"}, status_code=200)


@application_router.get("/{application_id}")
async def getApplication(application_id: UUID, access_token: str = Cookie(None)):
    user = protectRoute(access_token)
    if not isinstance(user, User):
        return user

    with Session(engine) as session:
        # Create aliases for the User table
        CreatedByUser = aliased(User, name="created_by")
        FromUser = aliased(User, name="from_user")
        ToUser = aliased(User, name="to_user")

        # Query the application along with its actions and related users (created_by, from_user, to_user)
        statement = (
            select(Applications, ApplicationActions, CreatedByUser, FromUser, ToUser)
            .outerjoin(
                ApplicationActions, ApplicationActions.application_id == Applications.id
            )
            .outerjoin(CreatedByUser, Applications.created_by_id == CreatedByUser.id)
            .outerjoin(FromUser, ApplicationActions.from_user_id == FromUser.id)
            .outerjoin(ToUser, ApplicationActions.to_user_id == ToUser.id)
            .where(Applications.id == application_id)
        )

        # Execute the query and group the results by application
        results = session.execute(statement).all()
        statement = select(SupportingDocuments).where(
            SupportingDocuments.application_id == application_id
        )
        documents = session.scalars(statement).all()
        if not results:
            return JSONResponse(
                content={"message": "Application not found"}, status_code=404
            )

        # Initialize the application data
        application_data = None
        actions_list = []

        for row in results:
            application, action, created_by, from_user, to_user = row

            # Serialize application data (initialize once)
            if application_data is None:
                application_data = {
                    "id": str(application.id),
                    "status": application.status,
                    "to_user": application.to,
                    "created_at": (
                        application.created_at.isoformat()
                        if application.created_at
                        else None
                    ),
                    "token_no": application.token_no,
                    "document": (
                        documents[0].document_url if len(documents) > 0 else None
                    ),
                    "accept_reference_number": (application.accept_reference_number),
                    "current_handler_id": str(application.current_handler_id),
                    "description": (
                        application.description if application.description else None
                    ),
                    "created_by": (
                        {
                            "id": str(created_by.id) if created_by else None,
                            "username": created_by.username if created_by else None,
                            "role": created_by.role if created_by else None,
                            "department": created_by.department if created_by else None,
                            "tcet_email": created_by.tcet_email if created_by else None,
                        }
                        if created_by
                        else None
                    ),
                }

            # Serialize action data
            if action:
                actions_list.append(
                    {
                        "id": str(action.id),
                        "action_type": action.action_type,
                        "comment": action.comments,
                        "created_at": (
                            action.created_at.isoformat() if action.created_at else None
                        ),
                        "from_user": (
                            {
                                "id": str(from_user.id) if from_user else None,
                                "username": from_user.username if from_user else None,
                                "role": from_user.role if from_user else None,
                                "department": (
                                    from_user.department if from_user else None
                                ),
                            }
                            if from_user
                            else None
                        ),
                        "to_user": (
                            {
                                "id": str(to_user.id) if to_user else None,
                                "username": to_user.username if to_user else None,
                                "role": to_user.role if to_user else None,
                                "department": to_user.department if to_user else None,
                            }
                            if to_user
                            else None
                        ),
                    }
                )

        # Add actions to the application data
        if application_data:
            application_data["actions"] = actions_list

        return JSONResponse(content={"application": application_data}, status_code=200)

    return JSONResponse(content={"message": "Application not found"}, status_code=404)


@application_router.post("/update/{application_id}")
async def update(
    application_id: UUID,
    body: UpdateApplicationSchema,
    access_token: str = Cookie(None),
):
    user = protectRoute(access_token)
    if not isinstance(user, User):
        return user
    with Session(engine) as session:
        statement = select(Applications).where(Applications.id == application_id)
        result = session.scalars(statement).first()
        if not result:
            return JSONResponse(
                content={"message": "Application not found"}, status_code=404
            )
        if result.current_handler_id != user.id:
            return JSONResponse(
                content={"message": "You dont't have access"}, status_code=401
            )
        result.accept_reference_number = body.referenceNumber
        result.status = ApplicationStatus[body.status]
        newApplicationAction = ApplicationActions(
            from_user_id=user.id,
            to_user_id=result.created_by_id,
            application_id=result.id,
            action_type=body.status,
            comments=body.remark,
        )
        statement = select(User).where(User.id == result.created_by_id)
        creator = session.scalars(statement).first()
        if creator is None:
            return JSONResponse(
                content={"message": "Some error taken place"}, status_code=401
            )
        session.add(newApplicationAction)
        session.commit()
        html_message = None
        if body.status == "ACCEPTED":
            if body.referenceNumber:
                html_message = f"""
                <h1>Application is Accepted</h1>
                <p>This is your reference Number {body.referenceNumber}</p>
                """
            else:
                html_message = f"""
                <h1>Application is Accepted</h1>
                <h1>Your reference Number is {result.token_no}</h1>
                """
        elif body.status == "REJECTED":
            html_message = f"""
                <h1>Application of token number {result.token_no}</h1>
                <h1>Application is Rejected</h1>
                """
        else:
            html_message = f"""
                <h1>Application of token number {result.token_no}</h1>
                <h1>Application is {body.status}</h1>
                """
        subject = "please check this application"
        if result:
            await create_message([creator.tcet_email], subject, html_message)
    return JSONResponse(content={"message": "Application updated"}, status_code=200)


@application_router.post("/all")
async def getAllApplications(
    access_token: str = Cookie(None),
):
    user = protectRoute(access_token)
    if not isinstance(user, User):
        return user
    with Session(engine) as session:
        applications = select(Applications).where(
            (Applications.created_by_id == user.id)
            | (Applications.current_handler_id == user.id)
        )
        result = session.scalars(applications).all()
    ans = [r.__dict__ for r in result]
    for r in ans:
        r.pop("_sa_instance_state", None)
        for key, value in r.items():
            if isinstance(value, UUID):
                r[key] = str(value)
            if isinstance(value, datetime):
                r[key] = value.isoformat()
    return JSONResponse(content={"applications": ans}, status_code=200)


@application_router.post("/forward/{application_id}")
async def ForwardApplication(
    application_id: UUID,
    body: ForwardApplicationSchema,
    access_token: str = Cookie(None),
):
    user = protectRoute(access_token)
    if not isinstance(user, User):
        return user
    with Session(engine) as session:
        statement = select(Applications).where(
            Applications.id == UUID(str(application_id))
        )
        result = session.scalars(statement).first()
        if not result:
            return JSONResponse(
                content={"message": "Application not found"}, status_code=404
            )

        statement = select(User).where(
            User.role == body.role and User.department == body.department
        )
        receiver = session.scalars(statement).first()
        if not receiver:
            return JSONResponse(
                content={"message": "Receiver not found"}, status_code=404
            )
        result.current_handler_id = UUID(str(receiver.id))
        result.status = ApplicationStatus.FORWARDED
        newApplicationAction = ApplicationActions(
            from_user_id=user.id,
            to_user_id=receiver.id,
            application_id=result.id,
            action_type="FORWARD",
            comments=body.remark,
        )
        session.add(newApplicationAction)
        session.commit()
        link = f"http://{os.getenv("CLIENT_URL")}/application/{application_id}"
        html_message = f"""
        <h1>Application is Forwarded</h1>
        <p>Click here to see application <a href="{link}">link</a></p>
        """
        subject = "please check this application"
        if receiver.tcet_email:
            await create_message([receiver.tcet_email], subject, html_message)
    return JSONResponse(content={"message": "Application forwarded"}, status_code=200)


@application_router.get("/get-stats/{some_id}")
async def getStats(
    access_token: str = Cookie(None),
):
    user = protectRoute(access_token)
    if not isinstance(user, User):
        return user
    if user.role == UserRole.STUDENT:
        return JSONResponse(
            content={"message": "You are not authorized to view this page"},
            status_code=401,
        )
    if user.role == "PRINCIPAL":
        print("principal")
        with Session(engine) as session:
            statement = select(Applications)
            result = session.scalars(statement).all()
            stats = {}
            for r in result:
                date_str = r.created_at.date().isoformat()
                if date_str not in stats:
                    stats[date_str] = {
                        "pending": 0,
                        "accepted": 0,
                        "rejected": 0,
                    }
                if r.status == ApplicationStatus.PENDING:
                    stats[date_str]["pending"] += 1
                elif r.status == ApplicationStatus.ACCEPTED:
                    stats[date_str]["accepted"] += 1
                else:
                    stats[date_str]["rejected"] += 1
            return JSONResponse(
                content={"stats": stats},
                status_code=200,
            )
    else:
        with Session(engine) as session:
            statement = select(Applications).where(
                Applications.current_handler_id == UUID(str(user.id))
            )
            result = session.scalars(statement).all()
            stats = {}
            for r in result:
                date_str = r.created_at.date().isoformat()
                if date_str not in stats:
                    stats[date_str] = {
                        "pending": 0,
                        "accepted": 0,
                        "rejected": 0,
                    }
                if r.status == ApplicationStatus.PENDING:
                    stats[date_str]["pending"] += 1
                elif r.status == ApplicationStatus.ACCEPTED:
                    stats[date_str]["accepted"] += 1
                else:
                    stats[date_str]["rejected"] += 1
            return JSONResponse(
                content={"stats": stats},
                status_code=200,
            )


@application_router.post("/verify/{application_id}")
async def verifyApplication(application_id, access_token: str = Cookie(None)):
    user = protectRoute(access_token)
    if not isinstance(user, User):
        return user
    with Session(engine) as session:
        statement = select(Applications).where(Applications.id == UUID(application_id))
        result = session.scalars(statement).first()
        if not result:
            return JSONResponse({"message": "Application not found"}, status_code=404)
        statement = select(User).where(User.role == "PRINCIPAL")
        receiver = session.scalars(statement).first()
        if not receiver:
            return JSONResponse(
                content={"message": "Receiver not found"}, status_code=404
            )
        result.is_verified = True
        result.status = ApplicationStatus.FORWARDED
        result.current_handler_id = UUID(str(receiver.id))
        newApplicationAction = ApplicationActions(
            from_user_id=user.id,
            to_user_id=receiver.id,
            application_id=result.id,
            action_type="VERIFIED",
        )
        if not result:
            return JSONResponse(
                content={"message": "Application not found"}, status_code=404
            )
        session.add(newApplicationAction)
        session.commit()
    return JSONResponse(content={"message": "Application verified"}, status_code=200)


@application_router.post("/update_app/{application_id}")
async def updateApplication(
    application_id: str,
    document: UploadFile = File(None),
    description: str = Form(...),
    subject: str = Form(...),
    for_user: str = Form(...),
    access_token: str = Cookie(None),
):
    user = protectRoute(access_token)
    if not isinstance(user, User):
        return user

    document_url = None
    with Session(engine) as session:
        # Fetch the application
        statement = select(Applications).where(
            Applications.id == UUID(str(application_id))
        )
        application = session.scalars(statement).one_or_none()

        if not application:
            return JSONResponse(
                content={"message": "Application not found"}, status_code=404
            )

        # Update document if provided
        if document and document.filename:
            # Delete existing document if it exists
            existing_document_statement = select(SupportingDocuments).where(
                SupportingDocuments.application_id == UUID(str(application_id))
            )
            existing_document = session.scalars(
                existing_document_statement
            ).one_or_none()

            if existing_document:
                try:
                    os.remove(existing_document.document_url)
                except FileNotFoundError:
                    pass

                session.delete(existing_document)

            # Save the new document
            name, ext = document.filename.rsplit(".", 1)
            unique_filename = f"{name}_{uuid4()}.{ext}"
            document_url = f"media/{unique_filename}"
            with open(document_url, "wb") as f:
                content = await document.read()
                f.write(content)

            newDocument = SupportingDocuments(
                application_id=UUID(str(application_id)),
                document_name=document.filename,
                document_url=document_url,
            )
            session.add(newDocument)

        # Update application details
        application.description = description
        application.subject = subject
        application.to = for_user

        session.commit()

    return JSONResponse(
        content={"message": "Application updated successfully"}, status_code=200
    )
